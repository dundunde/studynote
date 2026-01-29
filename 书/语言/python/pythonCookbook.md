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

















































































































