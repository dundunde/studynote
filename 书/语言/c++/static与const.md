## static

static 修饰的变量是`静态变量`

static 的初始值在**编译**时确定,在运行时能够动态修改其值

## const 

const 修饰的变量是常量

const 一般在**编译期间**确定值



## const 

### const 基础属性

#### 常量可以用来定义数组大小

整型常量可以用来定义数组大小，因为它在编译期确定值

```c++
static const int NumTurns = 5;

int scores[NumTurns];
```

#### 常量会发生`常量折叠`

若 `const` 变量由字面量/编译期常量初始化（如 `const int a = 10;`），编译器在生成代码时**直接替换所有使用处为字面值**

- 示例：`cout << a;` → 编译后变为 `cout << 10;`

#### 常量内存分配策略

- **整型常量**一般不分配内存，但是如果代码中对它取了地址(`&a`)，才会分配内存
    - 注意这里，整型常量一般不分配内存，但是对它取地址会让编译器为其分配内存，**此时常量折叠仅作用于 \*未涉及地址的使用场景\*，二者可共存。**
- 非整型常量(`const double`)会分配内存
- `extern` 时会分配内存

#### 全局const 和 局部const

- 全局 `const` 默认放入 `.rodata`（只读数据段）



#### 特殊情况

常量一般是编译期确定值，但有特殊情况：

| 场景                                           | 编译期作用             | 运行期作用                                                   |
| :--------------------------------------------- | :--------------------- | :----------------------------------------------------------- |
| **运行期常量** `const int y = getUserInput();` | 检查“初始化后不可修改” | 初始化值在运行时计算，内存标记为只读（但C++标准不强制硬件保护） |



## 类中const

在类中，所有不加 `static` 的**成员常量**都可以在类内赋值

**类中的const成员都可以取到地址**

```c++
class MyClass {
public:
    const int a = 5;
    const double b = 5;
    const std::string name{ "name"};
};

int main() {
    MyClass obj;
    const int* p = &obj.a; // ✅ 合法：成功获取地址
    const double* q = &obj.b; // ✅ 合法：成功获取地址
    std::cout << *p;       // 输出 5
    // *p = 10;            // ❌ 编译错误：不能通过 const 指针修改
}
```





## 类中static

**所有的static成员变量（不加const）都必须在类外定义**



## 类中static const

```python
class MyClass {
public:
    static const int a = 5;
    static const double b;	 // 仅声明（不可赋值！）
    static const std::string NAME;	 // 仅声明（不可赋值！）
};
const double MyClass::b = 5.0;
const std::string MyClass::NAME = "Player"; 
```

### 关于类内初始化

在类中，加 `static const`的成员中，只有**整型族(`long，int,short,char,bool等`)**可以在类内赋值，而`double`, `float`, `std::string`, `自定义对象`等等只能在类外赋值



### 关于取地址

#### 成员a不能取地址

c++对`静态常量整型 / 枚举类型`静态成员有特殊豁免：允许在类内直接初始化。此时编译器会将`a`视为**编译期常量**，在编译期会发生替换(`3.1.1提到的常量折叠`)，**把变量a直接替换为字面量5**，所以说`a`没有实际内存，不能取地址。若要对`a`取地址，必须补充`a`的类外定义。

```c++
const int MyClass::a;
// 不用赋值，以为类内已经初始化
```



#### 成员b可以取地址

因为除了`静态常量整型 / 枚举类型` 外，其他`类中静态常量`都需要在**类外初始化**，所以可以取到地址



### 总结

由上面可以看出，在**类内部初始化的整型族static const 成员**，并不能算严格意义上的定义，**声明（Declaration）** 告诉编译器：“这个名字存在，它是这个类型。” 而 **定义（Definition）** 告诉编译器：“请为这个变量分配内存。”

C++ 对 **`static const` 的整型（integral type，如 int, char, bool）** 开了一个特例：允许你在**类内部**声明时直接赋值。

```c++
static const int a = 5; 
```

此时，编译器将 `a` 放进了符号表，并且知道它的值是 5。

- 如果只是用它来指定数组大小 `int scores[a];`，编译器会进行**常量折叠（Constant Folding）**。它直接把 `a` 替换成 `5`。不需要在内存中为 `a` 分配地址。
- 因为没有分配内存地址（或者说编译器不需要它的地址），所以从严格意义上讲，它只是一个**声明**。

如果需要取地址，就需要像6.2.1一样，在.cpp中补充一个不带数值的定义

```c++
const int MyClass::a;
```





## 题外话

### 类中定义（类中初始化）

```c++
class MyClass {
public:
    const std::string name("name"); 	# ❌ 错误
};
```



我们之前提到，`非static` 的const 成员可以在类内定义(类内初始化)，上述错误原因在于：

在 C++ 类内部直接定义成员变量时，**不能使用圆括号 `()` 进行初始化**。因为**编译期会把它错认为函数声明，或者说编译器会感到困惑：这是在定义变量？还是在声明一个函数？**所以在类中初始化成员，有两种方式：

**方案 1：使用等号 `=` (拷贝初始化)** 这是最自然、最推荐的写法。

```c++
class Book {
    const std::string authorName = "Scott Meyers";
};
```

**方案 2：使用花括号 `{}` (列表初始化)**

```c++
class Book {
    const std::string authorName{"Scott Meyers"};
};
```



以上问题是著名的**歧义解析问题**（Most Vexing Parse 的变体）。

当编译器在类里看到 `Type name( ... );` 这种格式时，它会优先倾向于认为**你是在声明一个成员函数**。 虽然 `"Scott Meyers"` 是一个字符串字面量，不是类型，理论上构不成合法的函数参数类型，但在语法解析阶段，C++ 标准直接规定了：**类内成员初始值（In-class member initializer）禁止使用圆括号**，以彻底杜绝这种歧义的可能性。

> 当然，以上问题仅限于**类成员变量的<u>类内默认初始化</u>**的时候，在**类外(`命名空间中、全局作用域中`)、函数内**，都可以使用圆括号进行初始化。



### 关于函数中定义函数的问题

如果不适用 **Lambda 表达式**，那么函数中不能嵌套定义方法`(这也可以看做是可以在函数中使用圆括号初始化变量的一个原因)`



虽然函数中不可以嵌套函数，但函数中允许**定义局部类**，并在该类中定义成员函数。

```c++
void outerFunction() {
    class Local {
    public:
        static void inner() {
            // 执行逻辑
        }
    };

    Local::inner(); // 调用内部逻辑
}
```







## 遗留问题

### 关于constexpr的使用

### 如果是类中static的带constexpr的成员变量，有哪些需要类外定义



