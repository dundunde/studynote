# 克隆自聚宽文章：https://www.joinquant.com/post/68316
# 标题：小盘股进阶版：RSRS+MACD+ATR
# 作者：吖桂

# ============================================================================
# A股小盘股量化交易策略 - 重构版
# 策略逻辑：小市值选股 + MACD背离择时 + ATR移动止损
# ============================================================================

from jqdata import *
from jqfactor import *
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, time
import MyTT


# ============================================================================
# 第一部分：策略配置与初始化
# ============================================================================

class StrategyConfig:
    """策略参数配置类（便于统一管理和调参）"""
    # 持仓参数
    STOCK_NUM = 6                      # 目标持仓数量

    # 止损参数
    ATR_MULTIPLIER = 2.5               # ATR止损倍数
    ATR_PERIOD = 14                    # ATR计算周期
    FALLBACK_STOPLOSS = 0.88           # 备用固定止损比例（仅当ATR数据不足时使用）

    # 止盈参数
    PROFIT_TARGET = 2.0                # 翻倍止盈倍数
    TIME_STOPLOSS_DAYS = 30            # 时间止损天数阈值
    TIME_STOPLOSS_PROFIT = 0.05        # 时间止损最低收益率要求

    # 选股参数
    LIQUIDITY_THRESHOLD = 20000000     # 5日均成交额门槛（2000万）
    NEW_STOCK_DAYS = 375               # 次新股过滤天数

    # 大盘择时参数
    MARKET_INDEX = '399101.XSHE'       # 深证综指
    MARKET_MA_PERIOD = 20              # 大盘均线周期
    MARKET_RISK_LOOKBACK = 20          # 大盘风险信号回溯天数
    DEFENSIVE_CASH_RATIO = 0.5         # 防御模式仓位比例

    # MACD参数
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    MACD_WINDOW = 10                   # 背离检测窗口
    MACD_HISTORY = 60                  # MACD计算历史长度

    # RSRS参数
    RSRS_N = 18                        # RSRS回归周期（计算斜率的窗口）
    RSRS_M = 600                       # RSRS标准化周期（用于计算均值和标准差）
    RSRS_BUY_THRESHOLD = 0.7           # RSRS买入阈值（标准分）
    RSRS_SELL_THRESHOLD = -0.7         # RSRS卖出/降仓阈值（标准分）
    RSRS_POSITION_ADJUST = True        # 是否启用RSRS动态仓位调整

    # 特殊交易日
    EMPTY_MONTHS = False                # 是否启用空仓月（1月、4月）
    
def initialize(context):
    """策略初始化函数"""
    # -------- 平台设置 --------
    set_option('avoid_future_data', True)
    set_benchmark('000001.XSHG')
    set_option('use_real_price', True)
    set_slippage(FixedSlippage(0.0003))
    set_order_cost(OrderCost(
        open_tax=0,
        close_tax=0.0005,
        open_commission=0.0000841,
        close_commission=0.0000841,
        close_today_commission=0,
        min_commission=5
    ), type='stock')

    # -------- 日志配置 --------
    log.set_level('order', 'error')
    log.set_level('system', 'error')
    log.set_level('strategy', 'debug')

    # -------- 全局变量初始化 --------
    _init_global_vars()

    # -------- 定时任务调度 --------
    run_daily(prepare_stock_list, '9:05')      # 盘前准备
    run_daily(update_market_signal, '9:30')    # 大盘信号更新
    run_weekly(weekly_adjustment, 3, '10:00')  # 周二调仓
    run_daily(execute_stop_logic, '10:00')     # 止盈止损检查
    run_daily(trade_afternoon, '14:50')        # 尾盘涨停检查
    run_daily(close_account, '14:55')          # 空仓月清仓
    run_weekly(print_position_info, 5, '15:10') # 周五持仓报告


def _init_global_vars():
    """初始化全局变量（集中管理，避免散落各处）"""
    # 持仓相关
    g.hold_list = []                   # 当前持仓列表
    g.yesterday_limit_up_list = []     # 昨日涨停列表
    g.target_list = []                 # 本周目标股票池
    g.bought_this_week = []            # 本周已买入列表（防重复）

    # 止损相关
    g.stop_loss_prices = {}            # ATR止损价字典 {stock: price}

    # 择时相关
    g.market_risk_signals = []         # 大盘风险信号历史（MACD顶背离）
    g.rsrs_score = 0.0                 # 当前RSRS标准分
    g.rsrs_history = []                # RSRS历史记录（用于趋势判断）
    g.is_empty_month = False           # 是否处于空仓月

    # 交易原因标记
    g.sell_reason = ''                 # 上次卖出原因（'limitup'/'stoploss'/''）


# ============================================================================
# 第二部分：大盘择时模块
# ============================================================================

def calculate_rsrs(stock, context):
    """
    计算RSRS指标（阻力支撑相对强度）
    原理：
    1. 对过去N天的最高价和最低价做线性回归，得到斜率β
    2. 用R²对斜率加权，得到修正斜率 = β * R²
    3. 对过去M天的修正斜率做标准化，得到RSRS标准分

    返回: float (标准分，越大越强势)
    """
    config = StrategyConfig

    try:
        # 获取足够的历史数据（多取1天以防包含当日）
        df = attribute_history(
            stock,
            config.RSRS_M + config.RSRS_N + 1,
            '1d',
            fields=['high', 'low']
        ).dropna()

        # 关键修复：剔除当日不完整数据
        # 如果最后一行是今天，必须删除（9:30时的数据High=Low=Open=Close，会导致失真）
        current_date = context.current_dt.date()
        if len(df) > 0 and df.index[-1].date() == current_date:
            log.debug(f"RSRS计算: 检测到当日不完整数据，剔除最后一行 {df.index[-1].date()}")
            df = df[:-1]

        if len(df) < config.RSRS_M:
            log.debug(f"RSRS数据不足: {stock} 仅有 {len(df)} 天")
            return 0.0

        # 计算滚动窗口的斜率序列
        slopes = []
        for i in range(len(df) - config.RSRS_N + 1):
            high_window = df['high'].values[i:i + config.RSRS_N]
            low_window = df['low'].values[i:i + config.RSRS_N]

            # 线性回归：high = β * low + α
            # 斜率β反映了价格的上行阻力强度
            try:
                beta = np.polyfit(low_window, high_window, 1)[0]

                # 计算R²（决定系数）
                correlation = np.corrcoef(high_window, low_window)[0, 1]
                r_squared = correlation ** 2

                # R²加权修正（R²越高，线性关系越强，斜率越可信）
                weighted_slope = beta * r_squared
                slopes.append(weighted_slope)

            except Exception as e:
                log.debug(f"RSRS回归计算失败: {e}")
                continue

        if len(slopes) < config.RSRS_M:
            return 0.0

        # 标准化：计算最近M天斜率的标准分
        recent_slopes = slopes[-config.RSRS_M:]
        latest_slope = slopes[-1]

        mean_slope = np.mean(recent_slopes)
        std_slope = np.std(recent_slopes)

        if std_slope < 1e-6:  # 避免除零
            return 0.0

        # RSRS标准分 = (当前斜率 - 均值) / 标准差
        rsrs_score = (latest_slope - mean_slope) / std_slope

        return rsrs_score

    except Exception as e:
        log.error(f"RSRS计算异常 {stock}: {e}")
        return 0.0


def calculate_macd_divergence(stock, context):
    """
    计算MACD背离信号
    返回: {'dead': bool, 'gold': bool}
    """
    config = StrategyConfig
    result = {'dead': False, 'gold': False}

    try:
        # 获取历史数据（多取1天以防包含当日）
        df = attribute_history(
            stock,
            config.MACD_HISTORY + 1,
            '1d',
            fields=['close', 'volume']
        ).dropna()

        # 关键修复：剔除当日不完整数据
        current_date = context.current_dt.date()
        if len(df) > 0 and df.index[-1].date() == current_date:
            log.debug(f"MACD计算: 检测到当日不完整数据，剔除最后一行")
            df = df[:-1]

        if len(df) < config.MACD_WINDOW:
            return result

        # 计算MACD指标
        df['dif'], df['dea'], df['macd'] = MyTT.MACD(
            df.close,
            SHORT=config.MACD_FAST,
            LONG=config.MACD_SLOW,
            M=config.MACD_SIGNAL
        )

        # 提取最近窗口期数据
        recent_price = df['close'].values[-config.MACD_WINDOW:]
        recent_dif = df['dif'].values[-config.MACD_WINDOW:]
        x = np.arange(config.MACD_WINDOW)

        # 计算线性回归斜率
        slope_price = np.polyfit(x, recent_price, 1)[0]
        slope_dif = np.polyfit(x, recent_dif, 1)[0]

        # 顶背离检测（价格上涨 + 指标下跌）
        if slope_price > 0.01 and slope_dif < -0.001:
            if df['macd'].values[-1] < df['macd'].values[-2]:
                result['dead'] = True
                log.info(f"【顶背离】{stock} 价格斜率:{slope_price:.4f} DIF斜率:{slope_dif:.4f}")

        # 底背离检测（价格下跌 + 指标回升 + 量能放大）
        if slope_price < -0.01 and slope_dif > 0.001:
            recent_vol = df['volume'].values[-3:].mean()
            avg_vol = df['volume'].values[-20:].mean()
            if df['macd'].values[-1] > df['macd'].values[-2] and recent_vol > avg_vol * 1.05:
                result['gold'] = True
                log.info(f"【底背离】{stock} 价格减速 + 量能确认")

    except Exception as e:
        log.error(f"MACD计算异常: {e}")

    return result


def update_market_signal(context):
    """
    更新大盘信号（每日9:30执行）
    包括：
    1. MACD顶背离信号（风险信号）
    2. RSRS标准分（强弱信号）
    """
    config = StrategyConfig

    # 更新MACD背离信号
    macd_signal = calculate_macd_divergence(config.MARKET_INDEX, context)
    g.market_risk_signals.append(macd_signal['dead'])

    # 保持MACD信号列表长度在100以内
    if len(g.market_risk_signals) > 100:
        g.market_risk_signals = g.market_risk_signals[-100:]

    # 更新RSRS指标
    rsrs_score = calculate_rsrs(config.MARKET_INDEX, context)
    g.rsrs_score = rsrs_score
    g.rsrs_history.append(rsrs_score)

    # 保持RSRS历史长度在100以内
    if len(g.rsrs_history) > 100:
        g.rsrs_history = g.rsrs_history[-100:]

    # 日志输出
    log.info(f"【市场信号】MACD顶背离: {macd_signal['dead']}, RSRS标准分: {rsrs_score:.2f}")


def is_market_safe():
    """判断大盘是否安全（最近N天无风险信号）"""
    lookback = StrategyConfig.MARKET_RISK_LOOKBACK
    recent_signals = g.market_risk_signals[-lookback:] if len(g.market_risk_signals) >= lookback else g.market_risk_signals
    return True not in recent_signals


def get_rsrs_position_ratio():
    """
    根据RSRS指标动态调整仓位比例
    返回: float (0.0 - 1.0)

    策略逻辑：
    - RSRS > 0.7：强势市场，满仓（1.0）
    - 0.7 > RSRS > -0.7：中性市场，满仓（1.0）
    - RSRS < -0.7：弱势市场，半仓（0.5）
    - RSRS < -1.5：极弱市场，空仓（0.0）
    """
    config = StrategyConfig

    if not config.RSRS_POSITION_ADJUST:
        return 1.0  # 未启用RSRS仓位调整，默认满仓

    rsrs = g.rsrs_score

    # 极弱市场：空仓
    if rsrs < -1.5:
        log.info(f"【RSRS极弱】{rsrs:.2f} < -1.5，建议空仓")
        return 0.0

    # 弱势市场：半仓
    elif rsrs < config.RSRS_SELL_THRESHOLD:
        log.info(f"【RSRS弱势】{rsrs:.2f} < {config.RSRS_SELL_THRESHOLD}，降低至半仓")
        return 0.5

    # 中性/强势市场：满仓
    else:
        if rsrs > config.RSRS_BUY_THRESHOLD:
            log.info(f"【RSRS强势】{rsrs:.2f} > {config.RSRS_BUY_THRESHOLD}，满仓")
        else:
            log.debug(f"【RSRS中性】{rsrs:.2f}，满仓")
        return 1.0


# ============================================================================
# 第三部分：选股模块
# ============================================================================

def get_stock_list(context):
    """
    主选股逻辑：
    1. 基础过滤（ST、停牌、涨跌停、次新股等）
    2. 流动性过滤（5日均成交额）
    3. 财务过滤（PE>0, PB>0）
    4. 市值排序（从小到大）
    """
    config = StrategyConfig

    # 第一步：获取基础股票池
    initial_list = get_index_stocks(config.MARKET_INDEX)

    # 第二步：基础过滤
    initial_list = _apply_basic_filters(context, initial_list)

    # 第三步：流动性过滤
    liquidity_list = _apply_liquidity_filter(initial_list, config.LIQUIDITY_THRESHOLD)

    if not liquidity_list:
        log.warn("警告：流动性过滤后无可选股票")
        return []

    # 第四步：财务+市值筛选
    q = query(
        valuation.code,
        valuation.market_cap
    ).filter(
        valuation.code.in_(liquidity_list),
        valuation.pe_ratio > 0,
        valuation.pb_ratio > 0,
        indicator.adjusted_profit > 0
    ).order_by(
        valuation.market_cap.asc()
    )

    df = get_fundamentals(q)

    if df is None or df.empty:
        log.warn("警告：财务筛选后无可选股票")
        return []

    # 返回前 2*stock_num 只股票作为候选池
    stock_list = list(df.code)[:2 * config.STOCK_NUM]
    log.info(f"选股完成，候选池前10: {stock_list[:10]}")

    return stock_list


def _apply_basic_filters(context, stock_list):
    """应用基础过滤器"""
    stock_list = filter_new_stock(context, stock_list)
    stock_list = filter_kcbj_stock(stock_list)
    stock_list = filter_st_stock(stock_list)
    stock_list = filter_paused_stock(stock_list)
    # 注意：涨跌停过滤已移至交易下单前（buy_stocks函数），此处无需过滤
    # 原因：9:05 执行时还未开盘，调用这些过滤器只能获取昨日数据，无意义
    return stock_list


def _apply_liquidity_filter(stock_list, threshold):
    """流动性过滤：5日平均成交额"""
    if not stock_list:
        return []

    money_df = history(5, unit='1d', field='money', security_list=stock_list)
    avg_money = money_df.mean()
    liquidity_list = avg_money[avg_money > threshold].index.tolist()

    return liquidity_list


# ----------- 过滤器函数集合 -----------

def filter_paused_stock(stock_list):
    """过滤停牌股票"""
    current_data = get_current_data()
    return [s for s in stock_list if not current_data[s].paused]


def filter_st_stock(stock_list):
    """过滤ST及退市风险股票"""
    current_data = get_current_data()
    return [s for s in stock_list
            if not current_data[s].is_st
            and 'ST' not in current_data[s].name
            and '*' not in current_data[s].name
            and '退' not in current_data[s].name]


def filter_kcbj_stock(stock_list):
    """过滤科创板和北交所股票"""
    return [s for s in stock_list
            if s[0] not in ('4', '8') and s[:2] != '68']


def filter_limitup_stock(context, stock_list):
    """过滤涨停股票（持仓股除外）"""
    last_prices = history(1, unit='1m', field='close', security_list=stock_list)
    current_data = get_current_data()
    return [s for s in stock_list
            if s in context.portfolio.positions.keys()
            or last_prices[s][-1] < current_data[s].high_limit]


def filter_limitdown_stock(context, stock_list):
    """过滤跌停股票（持仓股除外）"""
    last_prices = history(1, unit='1m', field='close', security_list=stock_list)
    current_data = get_current_data()
    return [s for s in stock_list
            if s in context.portfolio.positions.keys()
            or last_prices[s][-1] > current_data[s].low_limit]


def filter_new_stock(context, stock_list):
    """过滤次新股（上市时间小于375天）"""
    yesterday = context.previous_date
    return [s for s in stock_list
            if (yesterday - get_security_info(s).start_date).days >= StrategyConfig.NEW_STOCK_DAYS]


# ============================================================================
# 第四部分：交易执行模块
# ============================================================================

def weekly_adjustment(context):
    """
    周一调仓逻辑：
    1. 检查MACD大盘风险信号
    2. 检查RSRS市场强弱
    3. 检查是否空仓月
    4. 执行换股操作
    """
    config = StrategyConfig

    # 1. 检查MACD大盘风险
    if not is_market_safe():
        log.warn("【MACD风险】大盘存在顶背离信号，暂停开新仓")
        return

    # 2. 检查RSRS极弱情况
    rsrs_ratio = get_rsrs_position_ratio()
    if rsrs_ratio == 0.0:
        log.warn(f"【RSRS极弱】标准分 {g.rsrs_score:.2f} < -1.5，暂停开新仓")
        # 清空现有持仓
        for stock in list(context.portfolio.positions.keys()):
            position = context.portfolio.positions[stock]
            if stock not in g.yesterday_limit_up_list:  # 涨停股不卖
                log.info(f"RSRS防御清仓: {stock}")
                close_position(position)
        return

    # 3. 检查是否空仓月
    if g.is_empty_month:
        log.info("【空仓月】不执行调仓")
        return

    # 4. 获取目标股票池
    g.target_list = get_stock_list(context)
    target_stocks = g.target_list[:config.STOCK_NUM]

    if not target_stocks:
        log.warn("目标池为空，跳过调仓")
        return

    log.info(f"【周调仓】目标持仓: {target_stocks}")

    # 5. 卖出不在目标池且非昨日涨停的股票
    for stock in g.hold_list:
        if stock not in target_stocks and stock not in g.yesterday_limit_up_list:
            log.info(f"调仓卖出 {stock}")
            position = context.portfolio.positions[stock]
            close_position(position)
        else:
            log.info(f"继续持有 {stock}")

    # 6. 买入目标股票（仓位由RSRS和MA20共同决定）
    buy_stocks(context, target_stocks)

    # 7. 更新本周已买入列表
    g.bought_this_week = [p.security for p in context.portfolio.positions.values()]


def buy_stocks(context, target_list):
    """
    批量买入股票（带大盘择时仓位调整）
    """
    config = StrategyConfig

    # 大盘择时：判断是否需要降低仓位
    cash_ratio = _calculate_position_ratio(context)

    if not target_list:
        return

    # 在交易前进行实时涨跌停检查（这才是有效的检查时机）
    target_list = filter_limitup_stock(context, target_list)
    target_list = filter_limitdown_stock(context, target_list)
    
    # 如果所有股票都因为涨跌停被剔除了，直接返回，避免除以零
    if not target_list:
        log.info("【取消买入】目标股票全部涨停或跌停，无可买标的")
        return

    # 计算单只股票目标市值
    target_value = context.portfolio.total_value * cash_ratio
    single_value = target_value / len(target_list)

    for stock in target_list:
        position = context.portfolio.positions[stock]

        # 新开仓
        if position.total_amount == 0:
            open_position(stock, single_value)
            if stock not in g.bought_this_week:
                g.bought_this_week.append(stock)

        # 持仓跟随：更新ATR止损位
        elif position.total_amount > 0:
            _update_atr_stop_loss(context, stock)

        # 检查持仓数量限制
        if len(context.portfolio.positions) >= config.STOCK_NUM:
            break


def _calculate_position_ratio(context):
    """
    根据大盘状态动态调整仓位比例
    综合考虑：
    1. MA20均线位置（原有逻辑）
    2. RSRS强弱信号（新增）

    最终仓位 = min(MA20仓位, RSRS仓位)
    """
    config = StrategyConfig

    # 1. MA20仓位判断
    ma20_ratio = 1.0
    try:
        df = attribute_history(config.MARKET_INDEX, config.MARKET_MA_PERIOD, '1d', ['close'])
        ma20 = df['close'].mean()
        current_price = get_current_data()[config.MARKET_INDEX].last_price

        if current_price > ma20:
            log.info(f"【MA20满仓】指数 {current_price:.2f} > MA20 {ma20:.2f}")
            ma20_ratio = 1.0
        else:
            log.info(f"【MA20半仓】指数 {current_price:.2f} < MA20 {ma20:.2f}")
            ma20_ratio = config.DEFENSIVE_CASH_RATIO
    except:
        log.warn("大盘数据获取失败，MA20默认满仓")
        ma20_ratio = 1.0

    # 2. RSRS仓位判断
    rsrs_ratio = get_rsrs_position_ratio()

    # 3. 取两者较小值（双重防御）
    final_ratio = min(ma20_ratio, rsrs_ratio)

    if final_ratio < 1.0:
        log.info(f"【综合仓位】MA20: {ma20_ratio:.1f}, RSRS: {rsrs_ratio:.1f}, 最终: {final_ratio:.1f}")

    return final_ratio


def _update_atr_stop_loss(context, stock):
    """更新ATR移动止损位（只涨不跌）"""
    config = StrategyConfig

    df = attribute_history(stock, config.ATR_PERIOD + 1, '1d', ['high', 'low', 'close'])

    if len(df) <= config.ATR_PERIOD:
        return

    atr_value = MyTT.ATR(df.high.values, df.low.values, df.close.values, config.ATR_PERIOD)[-1]
    current_price = get_current_data()[stock].last_price
    new_stop = current_price - config.ATR_MULTIPLIER * atr_value

    if stock not in g.stop_loss_prices:
        g.stop_loss_prices[stock] = new_stop
        log.info(f"[{stock}] 初始化ATR止损位: {new_stop:.2f}")
    else:
        old_stop = g.stop_loss_prices[stock]
        if new_stop > old_stop:
            g.stop_loss_prices[stock] = new_stop
            log.info(f"[{stock}] 止损位上移: {old_stop:.2f} -> {new_stop:.2f}")


def open_position(stock, value):
    """
    开仓函数
    返回: 是否成交成功
    """
    order_obj = order_target_value(stock, value)

    if order_obj is not None and order_obj.filled > 0:
        # 清理旧状态
        _cleanup_stock_status(stock)

        # 初始化止损位
        _initialize_stop_loss(stock)

        log.info(f"开仓成功: {stock} 成交 {order_obj.filled} 股")
        return True

    return False


def _initialize_stop_loss(stock):
    """初始化股票的止损位"""
    config = StrategyConfig

    df = attribute_history(stock, config.ATR_PERIOD + 1, '1d', ['high', 'low', 'close'])

    if len(df) > config.ATR_PERIOD:
        atr_value = MyTT.ATR(df.high.values, df.low.values, df.close.values, config.ATR_PERIOD)[-1]
        current_price = get_current_data()[stock].last_price
        g.stop_loss_prices[stock] = current_price - config.ATR_MULTIPLIER * atr_value
        log.info(f"[{stock}] 初始ATR止损: {g.stop_loss_prices[stock]:.2f}")
    else:
        # 数据不足时使用备用止损
        current_price = get_current_data()[stock].last_price
        g.stop_loss_prices[stock] = current_price * config.FALLBACK_STOPLOSS
        log.warn(f"[{stock}] ATR数据不足，使用固定止损: {g.stop_loss_prices[stock]:.2f}")


def close_position(position):
    """
    平仓函数
    返回: 是否成交成功
    """
    stock = position.security
    order_obj = order_target_value(stock, 0)

    if order_obj and order_obj.status == OrderStatus.held and order_obj.filled == order_obj.amount:
        _cleanup_stock_status(stock)
        return True

    return False


def _cleanup_stock_status(stock):
    """清理股票相关状态（止损价、减仓标记等）"""
    if stock in g.stop_loss_prices:
        del g.stop_loss_prices[stock]


# ============================================================================
# 第五部分：止盈止损模块
# ============================================================================

def execute_stop_logic(context):
    """
    主止损函数（每日10:00执行）
    包含：
    1. 翻倍止盈
    2. ATR移动止损
    3. 时间止损
    """
    config = StrategyConfig

    for stock in list(context.portfolio.positions.keys()):
        position = context.portfolio.positions[stock]

        if position.total_amount == 0:
            continue

        current_price = position.price
        avg_cost = position.avg_cost

        # 更新ATR止损位
        _update_atr_trailing_stop(stock, current_price, avg_cost)

        # 获取当前止损位
        stop_price = g.stop_loss_prices.get(stock, avg_cost * config.FALLBACK_STOPLOSS)

        # 1. 翻倍止盈
        if current_price >= avg_cost * config.PROFIT_TARGET:
            log.info(f"【翻倍止盈】{stock} 收益 {(current_price/avg_cost - 1)*100:.2f}%")
            order_target_value(stock, 0)
            _cleanup_stock_status(stock)
            continue

        # 2. ATR动态止损
        if current_price < stop_price:
            log.info(f"【ATR止损】{stock} 现价 {current_price:.2f} < 止损位 {stop_price:.2f}")
            order_target_value(stock, 0)
            _cleanup_stock_status(stock)
            g.sell_reason = 'stoploss'
            continue

        # 3. 时间止损
        held_days = _get_held_days(context, stock)
        if held_days >= config.TIME_STOPLOSS_DAYS:
            profit_rate = (current_price / avg_cost) - 1
            if profit_rate < config.TIME_STOPLOSS_PROFIT:
                log.info(f"【时间止损】{stock} 持仓 {held_days} 天，收益率 {profit_rate*100:.2f}%")
                order_target_value(stock, 0)
                _cleanup_stock_status(stock)


def _update_atr_trailing_stop(stock, current_price, avg_cost):
    """更新ATR移动止损位（仅在价格上涨时上移）"""
    config = StrategyConfig

    df = attribute_history(stock, config.ATR_PERIOD + 1, '1d', ['high', 'low', 'close'])

    if len(df) <= config.ATR_PERIOD:
        return

    atr_value = MyTT.ATR(df.high.values, df.low.values, df.close.values, config.ATR_PERIOD)[-1]
    new_stop = current_price - config.ATR_MULTIPLIER * atr_value

    # 初始化止损位
    if stock not in g.stop_loss_prices:
        g.stop_loss_prices[stock] = avg_cost - config.ATR_MULTIPLIER * atr_value

    # 只涨不跌原则
    if new_stop > g.stop_loss_prices[stock]:
        old_stop = g.stop_loss_prices[stock]
        g.stop_loss_prices[stock] = new_stop
        log.debug(f"[{stock}] 止损上移: {old_stop:.2f} -> {new_stop:.2f}")


def _get_held_days(context, stock):
    """计算持仓天数"""
    if stock in context.portfolio.positions:
        position = context.portfolio.positions[stock]
        buy_date = position.init_time.date()
        current_date = context.current_dt.date()
        return (current_date - buy_date).days
    return 0


# ============================================================================
# 第六部分：特殊交易日处理
# ============================================================================

def prepare_stock_list(context):
    """
    盘前准备（每日9:05执行）
    1. 更新持仓列表
    2. 识别昨日涨停股
    3. 判断是否空仓月
    """
    # 更新当前持仓
    g.hold_list = [p.security for p in context.portfolio.positions.values()]

    # 识别昨日涨停股
    g.yesterday_limit_up_list = _get_yesterday_limit_up_stocks(context)

    # 判断是否空仓月
    g.is_empty_month = _is_empty_month(context)


def _get_yesterday_limit_up_stocks(context):
    """获取昨日涨停的持仓股票"""
    if not g.hold_list:
        return []

    df = get_price(
        g.hold_list,
        end_date=context.previous_date,
        frequency='daily',
        fields=['close', 'high_limit'],
        count=1,
        panel=False,
        fill_paused=False
    )

    limit_up_df = df[df['close'] == df['high_limit']]
    return list(limit_up_df.code)


def _is_empty_month(context):
    """判断是否处于空仓月（1月或4月）"""
    if not StrategyConfig.EMPTY_MONTHS:
        return False

    today = context.current_dt.strftime('%m-%d')
    return ('01-01' <= today <= '01-30') or ('04-01' <= today <= '04-30')


def trade_afternoon(context):
    """
    尾盘交易逻辑（每日14:50执行）
    1. 检查昨日涨停股是否打开
    2. 补仓逻辑（涨停打开后的余额利用）
    """
    if g.is_empty_month:
        return

    check_limit_up_stocks(context)
    check_remaining_cash(context)


def check_limit_up_stocks(context):
    """检查昨日涨停股是否继续涨停"""
    if not g.yesterday_limit_up_list:
        return

    now_time = context.current_dt

    for stock in g.yesterday_limit_up_list:
        df = get_price(
            stock,
            end_date=now_time,
            frequency='1m',
            fields=['close', 'high_limit'],
            count=1,
            panel=False,
            fill_paused=True
        )

        current_price = df.iloc[0, 0]
        high_limit = df.iloc[0, 1]

        if current_price < high_limit:
            log.info(f"[{stock}] 涨停打开，卖出")
            position = context.portfolio.positions[stock]
            close_position(position)
            g.sell_reason = 'limitup'
        else:
            log.info(f"[{stock}] 继续涨停，持有")


def check_remaining_cash(context):
    """
    补仓逻辑：
    如果因涨停打开卖出，次日用余额补仓
    如果因止损卖出，下周再说
    """
    if g.sell_reason == 'limitup':
        g.hold_list = [p.security for p in context.portfolio.positions.values()]

        if len(g.hold_list) < StrategyConfig.STOCK_NUM:
            # 过滤掉本周已买入的股票
            candidate_list = [s for s in g.target_list if s not in g.bought_this_week]
            target_stocks = candidate_list[:StrategyConfig.STOCK_NUM]

            log.info(f"余额补仓: {context.portfolio.cash:.2f} 元，目标: {target_stocks}")
            buy_stocks(context, target_stocks)

        g.sell_reason = ''

    elif g.sell_reason == 'stoploss':
        log.info("止损后余额，下周再交易")
        g.sell_reason = ''


def close_account(context):
    """空仓月清仓逻辑（每日14:55执行）"""
    if g.is_empty_month and g.hold_list:
        log.info("【空仓月清仓】")
        for stock in g.hold_list:
            position = context.portfolio.positions[stock]
            close_position(position)
            log.info(f"卖出 {stock}")


# ============================================================================
# 第七部分：报告与监控
# ============================================================================

def print_position_info(context):
    """周五打印持仓报告"""
    if not context.portfolio.positions:
        print("当前无持仓")
        return

    print("\n" + "="*60)
    print(f"{'持仓报告':<20} {context.current_dt.date()}")
    print("="*60)

    for position in context.portfolio.positions.values():
        stock = position.security
        cost = position.avg_cost
        price = position.price
        ret = (price / cost - 1) * 100
        value = position.value
        amount = position.total_amount

        print(f"代码: {stock}")
        print(f"成本价: {cost:.2f}")
        print(f"现价: {price:.2f}")
        print(f"收益率: {ret:.2f}%")
        print(f"持仓: {amount} 股")
        print(f"市值: {value:.2f}")
        print("-" * 60)

    print("="*60 + "\n")
