## 基本安装过程

### 读博客

[2025最新版Windows平台VSCode通过Cmake开发Qt项目_vscode开发qt-CSDN博客](https://blog.csdn.net/weixin_74027669/article/details/142960155)

[[good\]vscode中qt环境配置包括qt和cmake安装 - 风中狂笑 - 博客园](https://www.cnblogs.com/dogingate/p/17894454.html)

按以上博客中的内容配置环境，不用管第一篇文章中的ninja和第二篇文章中改json的操作，只管最基本的插件安装和设置里的配置以及创建项目的过程

> 如果项目构建能成功但是窗口弹不出来，看看系统环境变量有没有配置qt对应的路径

### 优化VSCode找不到包含路径以及智能提示缓慢问题

#### 解决路径问题

路径问题很好解决，这里主要用Ninja

##### 安装Ninja

1. 去 [Ninja GitHub Release](https://github.com/ninja-build/ninja/releases) 下载 `ninja-win.zip`。

2. 解压得到 `ninja.exe`。

3. 把它放到一个环境变量 Path 包含的目录里（或者随便放一个地方，然后把那个文件夹路径加到系统环境变量 Path 中）。

4. 在VS Code 设置中搜索cmake.generator,在 "CMake: Generator" 的输入框中，填写 **`Ninja`** (注意大小写)。

5. 或者，你可以在你的 `.vscode/settings.json` 里直接添加一行：

    ```python
    "cmake.generator": "Ninja"
    ```

6. 清理并重新配置(这一步非常重要，因为切换生成器必须彻底清理旧的缓存),**删除 build 文件夹**。

7. **重新配置**：

    - 打开 VS Code。
    - 按下 `Ctrl + Shift + P`。
    - 输入并选择 **`CMake: Configure`**。

**观察输出：** 在 VS Code底部的 Output (输出) 窗口中，看第一行左右，应该会显示类似： `Check for working C compiler: .../cl.exe -- works` 并且不会再生成 `.sln` 文件了。

此时，去 `build` 文件夹里看一眼，**`compile_commands.json` 应该已经躺在那里了**。

##### 配置包含目录

1. 在CMakeLists.txt中的project(...)行之后加上以下代码:

    ```python
    set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
    ```

    编译之后，会在`build` 目录下会多出一个 `compile_commands.json` 文件。

    注意这个指令**只对** `Ninja` 或 `Makefile` 生成器有效。 默认的 Visual Studio 生成器（在build目录下生成 `.sln` 和 `.vcxproj` 的那个）**不支持**生成 `compile_commands.json`。所以需要安装Ninja。

2. 生成完compile_commands.json后直接进行下一节(1.2.1.3)，配置完clangd后包含路径会一并被找到。



##### 优化智能提示

1. 准备 `compile_commands.json` ，即确保你已经在 `CMakeLists.txt` 中加了 `set(CMAKE_EXPORT_COMPILE_COMMANDS ON)` 并且 `build` 目录下生成了该 json 文件（我们在上一节已经做过了）。
2. 安装 Clangd 插件，在 VS Code 插件市场搜索 **`clangd`** (作者是 LLVM) 并安装。然后安装Clangd [Releases · llvm/llvm-project](https://github.com/llvm/llvm-project/releases)
3. 安装clangd可以勾选添加环境变量，如果没有勾选，那么你需要手动告诉插件 `clangd` 在哪：
    - 设置搜索 `clangd.path`。
    - 填入：`D:\Tools\LLVM\bin\clangd.exe`。
4. **禁用微软插件的 IntelliSense (避免冲突)**
    - 你不需要卸载微软的 C/C++ 插件（你需要它来调试/Debug），但你需要关掉它的代码提示功能，把舞台让给 Clangd。
    - 打开 VS Code 设置 (`Ctrl + ,`)。
    - 搜索 `C_Cpp.intelliSenseEngine`。
    - 将其设置为 **`disabled`**。
5. **配置 Clangd 参数**
    - 在设置中搜索 `clangd.arguments`。
    - 点击 "Add Item"，添加以下几项关键参数（让提示更智能）：
        - `--compile-commands-dir=${workspaceFolder}/build` (告诉它去哪里找 json)
        - `--background-index` (后台建立索引)
        - `--completion-style=detailed` (更详细的提示)
        - `--header-insertion=never` (防止它自动乱加头文件，Qt项目中这个有时候会帮倒忙)
6. **重启 VS Code**
    - 重启后，你会看到底部状态栏左侧出现 `clangd: indexing`。等它索引完（Qt 项目第一次可能要几十秒）。

### 找不到kit或者Kit明明是对的但是显示[找不到工具包...建议你重新扫描工具包]

找不到kit或者Kit明明是对的但是显示[找不到工具包...建议你重新扫描工具包]

重置构建套件 (最关键)

1. **删除旧缓存**：
    - 关闭 VS Code。
    - 进入项目文件夹，**彻底删除** `build` 文件夹。
    - 进入 `.vscode` 文件夹，删除 `cmake-kits.json`（如果有）。
    - Windows 资源管理器地址栏输入 `%LocalAppData%/CMakeTools`，回车，把里面的 `cmake-tools-kits.json` 删掉（或者重命名备份）。这是 VS Code 的全局缓存，删了让它重新找。
2. **重新扫描**：
    - 打开 VS Code。
    - 按下 `Ctrl + Shift + P`。
    - 输入并选择 **`CMake: Scan for Kits`** (扫描构建套件)。
    - **观察右下角**，等待提示“Found X kits”。
3. **选择正确的架构**：
    - 按 `Ctrl + Shift + P` -> **`CMake: Select a Kit`**。
    - **千万小心选择**：
        - 不要选带红色感叹号或灰色的。
        - 选择类似 **`Visual Studio Community 2022 Release - amd64`** 的选项。
        - **注意：** 必须选 **`amd64`** (或 `x64`)，不要选 `x86`，也不要选 `x86_amd64`，除非你非常确定你要交叉编译。