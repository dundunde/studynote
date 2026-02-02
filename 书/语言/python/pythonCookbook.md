## 数据结构与算法

### 解压序列赋值给多个变量

任何序列(或者可迭代对象)，都可以通过简单赋值语句解压并赋值给多个变量，但是注意**变量数量必须和序列元素数量相等**

```python
>>> p = (4, 5)
>>> x, y = p
>>> x
4
>>> y
5

>>> data = [ 'ACME', 50, 91.1, (2012, 12, 21) ]
>>> name, shares, price, date = data
>>> name
'ACME'
>>> date
(2012, 12, 21)

>>> name, shares, price, (a, b, c) = data
>>> a
2012
>>> b
12
>>> c
21

# 错误写法
name, shares, price, a, b, c = data
```

> 注意：以上错误写法之所以错误，是因为**元素个数要和可迭代对象元素个数相同**，虽然 data 中有一个 tuple ，它里面有三个元素，但也只能这样写：
>
>  ` name, shares, price, (a, b, c) = data` 
>
> 让 (a, b , c) 组成一个 tuple ,然后当赋值进行到 data 中的 tuple 时，tuple 与 (a,b,c) 对应，然后内部元素会依次赋值给 a,b,c， 同时**要注意个数相等**



**同时，这种语法也可以用在字符串上**

```python
>>> s = 'Hello'
>>> a, b, c, d, e = s
>>> a
'H'
>>> b
'e'
>>> e
'o'
```

有时，你可能只想要使用一部分，那么可以这样做：

```python
data = [1, 2, 3]
_, a, b = data
```

#### 星号表达式

如果接收可迭代对象的变量个数与可迭代对象元素数量不匹配，就会出现异常，那么怎么才能从一个含有5个元素的可迭代对象中解压出三个元素来：

**可以使用 python 的星号表达式**

```python
first, *middle, last = [1, 2, 3, 4]
middle ===> [2,3]
```

```python
>>> record = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')
>>> name, email, *phone_numbers = record
>>> name
'Dave'
>>> email
'dave@example.com'
>>> phone_numbers
['773-555-1212', '847-555-1212']

```

**值得注意的是：**使用信号表达式的变量是**列表类型**，如果有 0 个元素， **那么就是一个空的列表，不论如何它都是列表**

```python
records = [
('foo', 1, 2),
('bar', 'hello'),
('foo', 3, 4),
]

def do_foo(x, y):
	print('foo', x, y)
    
def do_bar(s):
	print('bar', s)
    
for tag, *args in records:
    if tag == 'foo':
    	do_foo(*args)
    elif tag == 'bar':
    	do_bar(*args)

```

再来看以上代码，首先使用 `for in` 语句将每次将一个 tuple 赋值给 tag, *args ，如果tag == 'foo',那么调用 `do_foo`，但是注意这里的调用方式使用了 *args，按之前所说它应该是列表，但是函数却要求是两个变量，让我们一步步拆解代码执行到 `do_foo(*args)` 发生了什么：

##### 1. 循环赋值 (Packing)

在 `for tag, *args in records:` 这一行：

- 当遇到 `('foo', 1, 2)` 时：
    - `tag` 被赋值为 `'foo'`
    - `args` 捕获了剩余的元素，变成了列表：**`[1, 2]`**

##### 2. 函数调用 (Unpacking)

接着代码执行到 `do_foo(*args)`。这里的 `*` 起到了至关重要的作用：

- **如果不加星号：** `do_foo(args)`
    - 等同于 `do_foo([1, 2])`。
    - Python 会尝试把整个列表 `[1, 2]` 传给第一个参数 `x`。
    - **结果：** 报错（TypeError），因为函数需要 `x` 和 `y` 两个参数，但你只给了一个（即那个列表）。
- **加上星号：** `do_foo(*args)`
    - Python 看到 `*`，明白你要进行**解包**。
    - 它会将列表 `[1, 2]` 中的元素依次取出。
    - 它将 `1` 传给 `x`。
    - 它将 `2` 传给 `y`。
    - 等同于调用：**`do_foo(1, 2)`**。

##### 总结：这段代码里的两个 `*`

这段代码之所以经典，是因为它同时展示了星号 `*` 的两种相反用法：

| **代码位置**   | **语法** | **作用**                                                   | **术语**                    |
| -------------- | -------- | ---------------------------------------------------------- | --------------------------- |
| **For 循环中** | `*args`  | **收集 (Gather)**：把多余的元素全抓进一个列表里。          | Extended Iterable Unpacking |
| **函数调用中** | `*args`  | **打散 (Scatter)**：把列表里的元素拿出来，一个个传给函数。 | Argument Unpacking          |

### deque

```python
from collections import deque

>>> q = deque()
>>> q.append(1)
>>> q.append(2)
>>> q.append(3)
>>> q
deque([1, 2, 3])
>>> q.appendleft(4)
>>> q
deque([4, 1, 2, 3])
>>> q.pop()
3
>>> q
deque([4, 1, 2])
>>> q.popleft()
4
```

使用 `deque(maxlen=5)` 会创建一个固定大小的队列，如果没有指定大小会得要一个无限大小的队列，当新元素加入并且队列已满时，最左端元素会被自动移除

### defaultdict

defaultdict的特征时它会自动初始化每个 `key` 刚开始对应的值

```python
from collections import defaultdict

dict_list = defaultdict(list)
dict_set = defaultdict(set)

dict_list['a'].append(1)
dict_list['a'].append(1)
dict_list['b'].append(2)
dict_list['c'].append(3)

print(dict_list)
# 输出:
# defaultdict(<class 'list'>, {'a': [1, 1], 'b': [2], 'c': [3]})
```

> 需要注意的是，`defaultdict` 会自动为将要访问的键创建值(**就算字典中并不存在这样的键**)，比如上面的 dict_list['a'] ，**我们之前并没有向字典插入 'a'，但是 defaultdict 帮我们自动插入了键以及对应类型的值，所以可以成功访问到默认值 list ，并向他添加元素，而如果是普通字典(dict)，当我们要直接访问一个不存在的键时会抛出异常**



### zip函数

`zip` 函数的作用是**将多个可迭代对象中对应的元素打包成一个个元组**

```python
names = ["Alice", "Bob", "Charlie"]
ages = [24, 30, 18]

zipped = zip(names, ages)

# 注意：Python 3 中 zip 返回的是一个迭代器，直接打印看不到内容
# 需要转换成 list 才能看到结果
print(list(zipped))
#输出：
# [('Alice', 24), ('Bob', 30), ('Charlie', 18)]
```

#### 需要注意的点

1. 如果传入的列表长度不一，`zip` 会以**最短**的那个列表为准，**多余元素会被丢弃**

2. **支持多个参数：** 你可以同时 zip 三个、四个甚至更多的列表。

    ```python
    nums = [1, 2]
    letters = ['a', 'b']
    symbols = ['!', '@']
    
    print(list(zip(nums, letters, symbols)))
    ```



### 字典运算

怎样在数据字典中执行一些计算操作（比如求最小值、最大值、排序等等）？

```python
prices = {
'ACME': 45.23,
'AAPL': 612.78,
'IBM': 205.55,
'HPQ': 37.20,
'FB': 10.75
}
```

#### 字典默认的数学行为

1. **如果我们直接对 `dict` 进行数学运算(如 min(),max() 等)，那么它们仅仅作用于键**，如：

    ```python
    min(prices) # Returns 'AAPL'
    max(prices) # Returns 'IBM'
    ```

    我们对字典直接进行 `min()` 或者 `max()` ，那么Python 默认迭代的是字典的 **键 (keys)**

2. 如果我们想要得到**字典中值的最大值或最小值对应的键**

    ```python
    min(prices, key=lambda k: prices[k]) # Returns 'FB'
    max(prices, key=lambda k: prices[k]) # Returns 'AAPL'
    ```

    > 过程：
    >
    > `min()` 函数依次遍历字典的每个键（'ACME', 'AAPL', 'IBM' 等），并将这个键传递给 `key` 参数指定的函数，`lambda k: prices[k]` 中的参数 `k` 会依次接收到：`'ACME'`, `'AAPL'`, `'IBM'`, `'HPQ'`, `'FB'`，然后通过键去查找对应的 **值 (Value) **并返回，然后 `min()` 使用该值进行判断，**找到最小值对应的键**
    >
    > 注意：**这里寻找的仍然是键，只不过是把判断基准从键换成了键对应的值**

3. 如果还想要得到最小值，你又得执行一次查找操作。比如：

    ```python
    min_value = prices[min(prices, key=lambda k: prices[k])
    ```

    这样做实在太麻烦







**如果需要同时得到最小键和对应的值，通常需要使用 `zip()` 函数现将键和值反转过来**

#### 通过键查找字典最大最小值

```python
min_price = min(zip(prices.values(), prices.keys()))
# min_price is (10.75, 'FB')
max_price = max(zip(prices.values(), prices.keys()))
# max_price is (612.78, 'AAPL')
```

> 需要注意的是，在计算操作中使用到了 (**值**，键) 对，当多个 (**值**，键) 拥有相同的值的时
> 候，键会决定返回结果。比如，在执行 min() 和 max() 操作的时候，如果恰巧最小或
> 最大值有重复的，那么拥有最小或最大键的实体会返回：
>
> ```python
> >>> prices = { 'AAA' : 45.23, 'ZZZ': 45.23 }
> >>> min(zip(prices.values(), prices.keys()))
> (45.23, 'AAA')
> >>> max(zip(prices.values(), prices.keys()))
> (45.23, 'ZZZ')
> ```
>
> 

#### 通过键排序字典

```python
prices_sorted = sorted(zip(prices.values(), prices.keys()))
# prices_sorted is [(10.75, 'FB'), (37.2, 'HPQ'),
# (45.23, 'ACME'), (205.55, 'IBM'),
# (612.78, 'AAPL')]
```

注意：如果 写` sorted(prices, key=lambda k:prices[k])` 那么它的输出是 `['FB', 'HPQ', 'ACME', 'IBM', 'AAPL']` ，也就是**按键对应的值进行排序的键序列**



> 1. 需要注意的是，迭代器只能访问一次，一旦迭代器走完了全程，那么就不能再访问，如以下示例：
>
>     ```python
>     prices_and_names = zip(prices.values(), prices.keys())
>     print(min(prices_and_names)) # OK
>     print(max(prices_and_names)) # ValueError: max() arg is an empty sequence
>     ```
>
>     
>
> 2. **迭代器只能向前走，不能后退**
>
> ```python
> price_zip = zip(prices.values(),prices.keys())
> next(price_zip)
> next(price_zip)
> print(max(price_zip))
> # 输出：
> # (205.55, 'IBM')
> ```
>
> 这里找到的最大值是 `(205.55, 'IBM')` ，因为在 `max()` 之前，迭代器已经走过两次，那么 `max()` 时只能从迭代器现有位置向前走，而不能回头去比较走过的两个元素。



#### 查找两字典的相同点

```python
a = {
'x' : 1,
'y' : 2,
'z' : 3
}

b = {
'w' : 10,
'x' : 11,
'y' : 2
}
```

为了寻找两个字典的相同点，可以简单的在两字典的 keys() 或者 items() 方法返
回结果上**执行集合操作**。

```python
# Find keys in common
a.keys() & b.keys() # { 'x', 'y' }
# Find keys in a that are not in b
a.keys() - b.keys() # { 'z' }
# Find (key,value) pairs in common
a.items() & b.items() # { ('y', 2) }

```



如果想要**用现有字典构造一个排除指定键的新字典**：

```python
c = {key:a[key] for key in a.keys() - {'z', 'w'}}
```



#### 总结

1. 字典支持数学操作(`min,max`等)，但是Python**默认操作的是键**，如果想要得到**键和值**，可以使用**zip函数**

2. 字典的 `keys` 和 **`items`** 支持**集合操作**(**并、交、差运算**)，但是 **`values()`不完全支持**。

    - **唯一性（Uniqueness）的缺失**：因为**values**不能保证所有的值互不相同，而集合（Set）在数学和 Python 中的定义都要求**元素必须是唯一的**

    -  **可哈希性（Hashability）的限制**：Python 的集合操作依赖于元素的哈希值（Hash Value）来快速比对和存储，所以要放入集合（set）中的元素，或者要进行集合运算的元素，必须是**可哈希的**，如果字典的值是**可变对象**(`list,dict`)等不可哈希对象，就不能参与集合运算

        如果你确定你的字典值都是**可哈希的**（例如都是数字或字符串），并且你不介意丢失重复值，你可以手动转换：

        ```python
        d1 = {'a': 1, 'b': 2}
        d2 = {'c': 2, 'd': 3}
        
        # 手动转换为 set 进行交集运算
        common_values = set(d1.values()) & set(d2.values())
        print(common_values) # 输出: {2}
        ```

        

### namedtuple

`collections.namedtuple` 是一个工厂方法，它会返回**标准元组的子类**，你需要传递类名和需要的字段给它，然后该方法会返回一个类

```python
import collections

# 创建一个叫 'Card' 的类，包含 'rank' 和 'suit' 两个属性
Card = collections.namedtuple('Subscriber', ['addr', 'joined'])

# 实例化
beer_card = Card('jonesy@example.com', '2012-10-19')

print(beer_card.addr) # 输出 'jonesy@example.com'
```

使用 `namedtuple` 得到的类是一个只有属性没有方法的简单类，它是**标准元组的子类**，所以也**支持普通元组操作，如索引和解压**

```python
print(len(beer_card)) # 2
addr, joined = beer_card
print(addr) # jonesy@example.com
```





















































































