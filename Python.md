# Python

## Python基础

### python文件执行方式

```python
python test.py
./test.py #这种方式文件头要加 "#!/usr/bin/env python3"
```

### 数据类型

1)整数：无大小限制
			1000可以写为1_000,0xff00可以写为0xff_00
		注意：整数的运算是精确的,如7/5=1.4
		
	
	2)浮点数：运算可能有误差
	
	3)字符串：	
		表示方式：单引号'',双引号"".三引号"""或''',其中三引号可以跨行
		转义字符：\
			可以在字符串前加上r来表示字符串内部默认不转义
			print(r'fjdi\n')输出：fjdi\n
			
	4)布尔值:True   False
	可以进行 and or not运算
	
	5)空值：None,不能理解为0，None是一个特殊的空值
	6)常量：全部大写的变量名表示常量,但其实仍然可以修改，只是一个习惯上的写法


### 字符串与编码

	1)
			ord():获取字符的整数表示，ord('A')->65
			chr():数字转为对应字符,chr(66)->'B'
			
		2)在网络传输或保存在磁盘上，就需要把str变为以字节为单位的bytes
			对bytes类型用带b前缀的单引号或双引号
			x=b'ABC'
			bytes的每个字符都只占一个字节
			
		3)encode():str通过encode()转为指定编码的bytes
			'ABC'.encode('ascii')->b'ABC'
			
		4)decode():从网络或磁盘中读取数据时，需要将bytes转为str
			b'ABC'.decode('ascii')->'ABC'
			如果bytes中包含无法解码的字节，decode()方法会报错
			如果bytes中只有一小部分无效的字节，可以传入errors='ignore'忽略错误的字节：
			b'\xe4\xb8\xad\xff'.decode('utf-8', errors='ignore')
			
		5)len():计算str的字符数，计算bytes的字节数
			len(b'\xe4\xb8\xad\xe6\x96\x87')->6
			
		6)格式化字符串：
			a.print('%2d-%02d'%(3,1))
			b.%s永远起作用:
				print('Age: %s. Gender: %s' % (25, True))->'Age: 25. Gender: True'
			c.转义：%
				print('%s %%'%7)->7%

可以用in来判断字母是否在字符串中

```python
s='abc'
print('a' in s)		#True
```



### 除法

1)/结果为浮点数，9/3=3.0
2)//结果为整数，10//3=3

### 不可变类型与可变类型的赋值与修改

不可变类型与可变类型都说的是python`内置的数据类型`，而非自定义出的变量

#### 不可变类型

不可变变量：str,number,tuple

可变：list,dict,set

```python
#赋值
a='ABC'
b=a
a='XYZ'
print(a)#XYZ
print(b)#ABC
#不可变类型不能修改
```

执行`a = 'ABC'`，解释器创建了字符串`'ABC'`和变量`a`，并把`a`指向`'ABC'`：

![py-var-code-1](https://liaoxuefeng.com/books/python/basic/data-types/step-1.png)

执行`b = a`，解释器创建了变量`b`，并把`b`指向`a`指向的字符串`'ABC'`：

![py-var-code-2](https://liaoxuefeng.com/books/python/basic/data-types/step-2.png)

执行`a = 'XYZ'`，解释器创建了字符串'XYZ'，并把`a`的指向改为`'XYZ'`，但`b`并没有更改：

![py-var-code-3](https://liaoxuefeng.com/books/python/basic/data-types/step-3.png)

所以，最后打印变量`b`的结果自然是`'ABC'`了。

#### 可变类型

`````python
l=[1,2,3]
l2=l
l.append(4)
print(l)  #[1, 2, 3, 4]
print(l2) #[1, 2, 3, 4]
l=[4,5,6]
print(l)  #[4,5,6]
print(l2) #[1, 2, 3, 4]
`````

从上面的情况，我们可以看出，在python中，给一个变量赋值另一个变量相当于引用，并不是像c++一样的拷贝，故修改一个会影响另一个。

### 函数

#### print('1','2')

多个字符串用','隔开，打印时遇到','会输出空格

#### input()

输入换行符结束，返回str

#### int()

input的返回值是str

```python
s = input('birth: ')
birth = int(s)
```

可以用int()将str转为int

注意：`int()`函数发现一个字符串并不是合法的数字时就会报错

### list

**list中元素类型可以不同**

**list中可以含list，['python', 'java', ['asp', 'php'], 'scheme']**

**注意外层List只有4个元素**

```plain
classmates = ['Michael', 'Bob', 'Tracy']
1)追加元素:append()
2)取最后一个元素:classmates[-1]
	倒数第二个:classmates[-2]
3)insert(位置，元素)
4)删除末尾元素:pop()
5)删除指定元素：pop(i),i是索引
```

### tuple(元组)

#### tuple一旦初始化就不能修改

```plain
1)t=('Michael', 'Bob', 'Tracy')不可更改
```

#### 定义只有一个元素的tuple:

​	t1=(1,)
​      t2=("fdjis",)
​	因为(1)可以表示数学里的运算符，<u>所以为避免歧义要加逗号</u>
​	在输出一个元素的tuple时也会带逗号:
​      (1,)
​      ('fdjis',)

#### "可变"tuple

```python
>>> t = ('a', 'b', ['A', 'B'])
>>> t[2][0] = 'X'
>>> t[2][1] = 'Y'
>>> t
('a', 'b', ['X', 'Y'])
```

我们先看看定义的时候tuple包含的3个元素：

![tuple-1](https://liaoxuefeng.com/books/python/basic/list-tuple/step-1.png)

当我们把list的元素`'A'`和`'B'`修改为`'X'`和`'Y'`后，tuple变为：

![tuple-2](https://liaoxuefeng.com/books/python/basic/list-tuple/step-2.png)



表面上看，tuple的元素确实变了，但其实变的不是tuple的元素，而是list的元素。tuple所谓的“不变”是说，tuple的每个元素，<u>指向永远不变</u>。即指向`'a'`，就不能改成指向`'b'`，指向一个list，就不能改成指向其他对象，但指向的这个list本身是可变的！

### 条件判断

`if`判断条件还可以简写，比如写：

```python
if x:
    print('True')
```



只要`x`是非零数值、非空字符串、非空list等，就判断为`True`，否则为`False`。

### 模式匹配

#### 普通匹配

```python
age=15
match age:
	case x if x<10:
		print(f'< 10 years old: {x}')
	case 10:
		print('10 years old.')
	case 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18:
		print('11~18 years old.')
	case _:
		print('not sure.')
```

`x if x<10`：如果age<15时把值赋给x

`case _`：任意值

`11 | 12 | 13 | 14 | 15 | 16 | 17 | 18`：匹配多个值

#### 匹配列表

我们假设用户输入了一个命令，用`args = ['gcc', 'hello.c']`存储，下面的代码演示了如何用`match`匹配来解析这个列表：

```python
args = ['gcc', 'hello.c', 'world.c']
# args = ['clean']
# args = ['gcc']

match args:
    # 如果仅出现gcc，报错:
    case ['gcc']:
        print('gcc: missing source file(s).')
    # 出现gcc，且至少指定了一个文件:
    case ['gcc', file1, *files]:
        print('gcc compile: ' + file1 + ', ' + ', '.join(files))
    # 仅出现clean:
    case ['clean']:
        print('clean')
    case _:
        print('invalid command.')
```



第一个`case ['gcc']`表示列表仅有`'gcc'`一个字符串，没有指定文件名，报错；

第二个`case ['gcc', file1, *files]`表示列表第一个字符串是`'gcc'`，第二个字符串绑定到变量`file1`，后面的任意个字符串绑定到`*files`（符号`*`的作用将在[函数的参数](https://liaoxuefeng.com/books/python/function/parameter/index.html)中讲解），它实际上表示至少指定一个文件；

第三个`case ['clean']`表示列表仅有`'clean'`一个字符串；

最后一个`case _`表示其他所有情况。

### 循环

#### for循环

```python
names=['mich','bob','tracy']
for name in names:
    print('name')
```

把`names`每个元素一次代入name

#### range()与list()

**range(x)是range(0,x)的简写**

```python
range(5)#生成从0开始小于5的整数序列，即0,1,2,3,4
list(range(5))#[0, 1, 2, 3, 4]
sum=0
for i in range(5):
    sum+=i
```

#### while循环

```python
n=99
while n>0:
    print(n)
    n-=2
```

### 字典dict(map)(哈希)

```python
d={'mich':95,'bob':75}
print(d['mich'])
#放入
d['Adam']=67
```

1.<u>dict的键是不能重复的</u>，重复插入相同的键，它的值会被覆盖

2.如果Key不存在，dict会报错

3.in与get()

```python
>>>'thomas' in d
False
>>>d.get('thomas')#如果key不存在，默认返回None
>>>d.get('thomas',-1)#也可以自己指定失败时的返回值
-1
```

4.删除pop(key)

```python
>>>d.pop('bob')
75
```

5.items()

注意：

**dict内部存放的顺序和key放入的顺序是没有关系的**

### set(无序不重复集合)

set只存储key,key不能重复

```pytho
s={1,2,3}
s=set([1,2,3])#list作为输入


#重复元素自动过滤
s = {1, 1, 2, 2, 3, 3}
print(s)#{1, 2, 3}

#添加与删除
s.add(4)
s.remove(1)

#计算交集与并集
s1 = {1, 2, 3}
s2 = {2, 3, 4}
s3=s1&s2
print(s3)       #{2,3}
print(s1|s2)    #{1,2,3,4}
```

### 不可变对象

对于不可变对象，比如str，对str进行操作呢：

```plain
>>> a = 'abc'
>>> a.replace('a', 'A')
'Abc'
>>> a
'abc'
```



虽然字符串有个`replace()`方法，也确实变出了`'Abc'`，但变量`a`最后仍是`'abc'`，应该怎么理解呢？

我们先把代码改成下面这样：

```plain
>>> a = 'abc'
>>> b = a.replace('a', 'A')
>>> b
'Abc'
>>> a
'abc'
```



要始终牢记的是，`a`是变量，而`'abc'`才是字符串对象！有些时候，我们经常说，对象`a`的内容是`'abc'`，但其实是指，`a`本身是一个变量，它指向的对象的内容才是`'abc'`：

```
┌───┐     ┌───────┐
│ a │────▶│ 'abc' │
└───┘     └───────┘
```

当我们调用`a.replace('a', 'A')`时，实际上调用方法`replace`是作用在字符串对象`'abc'`上的，而这个方法虽然名字叫`replace`，但却没有改变字符串`'abc'`的内容。相反，`replace`方法创建了一个新字符串`'Abc'`并返回，如果我们用变量`b`指向该新字符串，就容易理解了，变量`a`仍指向原有的字符串`'abc'`，但变量`b`却指向新字符串`'Abc'`了：

```
┌───┐     ┌───────┐
│ a │────▶│ 'abc' │
└───┘     └───────┘
┌───┐     ┌───────┐
│ b │────▶│ 'Abc' │
└───┘     └───────┘
```

所以，对于不变对象来说，调用对象自身的任意方法，也不会改变该对象自身的内容。相反，这些方法会创建新的对象并返回，这样，就保证了不可变对象本身永远是不可变的。

## 函数

### 定义函数

```python
def my_abs(x):
    return abs(x)
```

#### 空函数

```python
def nop():
    pass

if age>10:
    pass
```

pass的作用是填补代码块，使不出现语法错误

#### 参数检查

调用函数时，ython解释器会自动检查参数个数，但<u>不会检查参数类型</u>

```py
def my_abs(x):
    if not isinstance(x,(int,float)):
        raise TypeError('bad operand type')
    if x>0:
        pass
```

#### 返回多个值

```python
def move(x, y, step, angle=0):
    nx = x + step * math.cos(angle)
    ny = y - step * math.sin(angle)
    return nx,ny


x,y=move(100,100,60,math.pi/6)
print(x,y)     #151.96152422706632 70.0
```

**本质:**

​	python的返回值其实是单一值，类型时tuple,但是在语法上，返回一个tuple可以省略括号，<u>而多个变量可以同时接收一个tuple，按位置顺序依次赋值</u>

#### 默认参数、可变参数、关键字参数

```python
def enroll(name, gender, age=6, city='Beijing'):
    print('name:', name)
    print('gender:', gender)
    print('age:', age)
    print('city:', city)
    
#当不安顺序提供默认参数时，需要把参数名写上  
enroll('bob','m',city='tianjin')
```

**当默认参数为可变对象时**

```python
def add_end(L=[]):
    L.append('END')
    return L

>>> add_end()
['END']
>>> add_end()
['END', 'END']
>>> add_end()
['END', 'END', 'END']
```

出现以上情况的原因是：

python在函数定义时，默认参数`L`的值就被计算出来了，即`[]`，因为默认参数L是一个变量，它指向`[]`，每次调用该函数时，如果改变了`L`的内容，那么下次调用时，默认参数的内容就变了

所以，<u>默认参数尽量指向不可变对象</u>



修改以上函数：

```python
def add_end(L=None):
    if L is None:
        L = []
    L.append('END')
    return L
```

## 高级特性

### 切片

切片规则：
List['start''stop''step']
左闭右开，即包含start不包含stop

```python
L = ['Michael', 'Sarah', 'Tracy', 'Bob', 'Jack']

#如果第一个索引是0，则可以省略
>>>L[:3]#0,1,2
['Michael', 'Sarah', 'Tracy']
>>>l[1,3]
['Sarah', 'Tracy']

#python还支持倒数切片
>>>L[-2:]#从倒数第二个开始一直到末尾
['Bob', 'Jack']
>>>L[-2,-1]#从倒二到倒一，但不包含倒一
['Bob']
```

注意：

​	倒数切片的时候依然是**从左往右**的顺序

```python
L=List(range(100))
>>>L[:10:5]
[0,5]
>>>L[:]#什么都不写就是复制一份
```

<u>tuple也可以进行切片</u>

<u>字符串也可以进行切片</u>

### 迭代(for循环)

#### 使用迭代

```python
d = {'a': 1, 'b': 2, 'c': 3}
for key in d:
    print(key)
```

<u>默认情况下，dict迭代的是key</u>

如果要迭代value或者同时迭代key和value

```python
#迭代value
for value in d.values():
    print(value)
#迭代key和value
for key,value in d.items():
    print(key,value)
```

#### 判断迭代

```python
from collections.abc import Iterable
>>>isinstance('abc',Iterable)
True
```

#### 实现下标循环

使用enumerate把list变成索引-元素对

```python
for i,value in enumerate(List(['A', 'B', 'C'])):
    print(i,value)
    
0 A
1 B
2 C   
```

### 列表生成式

#### 基本用法

```python
>>>[x*x for x in range(1,11)]
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```

把range的值依次赋给x,，然后for前面的表达式计算出值



双层循环

```python
>>>[x+y for x in 'ABC' for y in 'XYZ']
['AX', 'AY', 'AZ', 'BX', 'BY', 'BZ', 'CX', 'CY', 'CZ']
```



#### 加入判断

##### 在for后加判断

<u>在for后加判断是过滤条件</u>

<u>在for后加判断**不能**在if后加else</u>

```python
>>>[x*x for x in range(1,11) if x%2==0]
[4, 16, 36, 64, 100]
```

该语句的意思是：

​	1到10的数字，先判断x%2==0,如果通过,那么执行前面的表达式,否则丢弃



##### 在for前加判断

<u>在for前加判断是表达式的一部分</u>

<u>加判断必须加else,因为它必须计算出一个结果</u>

```python
>>>[x*x if x%2=0 else -x for x in range(1,11)]
[4, 16, 36, 64, 100]
```

该语句的意思是：

​	1到10的数字，全部给到前面的表达式，如果x%2==0,那么执行x*x,否则执行-x,所以`else`是**必须**加的

### 生成器(generator)

#### 创建方法1：修改列表生成式

把列表生成式的方括号改为圆括号

```python
g=(x*x for x in range(10))
```

要打印generator的元素，可以使用`next()`

```python
>>> next(g)
0
>>> next(g)
1
>>> next(g)
4
...
>>> next(g)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

每次调用`next()`generator会计算出下个元素的值，直到计算到最后一个元素时，抛出`StopIteration`的错误

使用for循环来调用:

```python
for n in g:
    print(n)
0
1
...
49
64
81
```

这样调用generator不需要担心`StopIteration`错误





#### 创建方法2：使用函数

```python
def fib(max):
    #x是次数,a和b是斐波那契数列的第一二个元素
    x,a,b=0,0,1
    if(x<max):
        print(b)
        a,b=b,a+b
        x+=1
    return 'done'
```

这是一个生成斐波那契数列的函数

注意：

​	<u>a,b=b,a+b 这里的b,a+b其实是一个tuple即(b,a+b)，但是只有一个tuple时括号可省略</u>



要将函数变为generator，只需要将`print(b)`改为`yield b`

```python
def fib(max):
    #x是次数,a和b是斐波那契数列的第一二个元素
    x,a,b=0,0,1
    if(x<max):
        yield b
        a,b=b,a+b
        x+=1
    return 'done'
```

调用函数式的generator，首先需要创建一个对象

多次调用generator函数会创建多个**相互独立**的generator

```python
f=fib(6)#创建一个generator对象
f2=fib(6)#创建了一个新的对象，和上面的f相互独立
```

调用时，可以通过`next()`或者`循环`来调用

#### 生成器的执行规则

在generator函数执行过程中,遇到`yield`就中断，下次执行时从上次中断的`yield`语句开始执行

```python
>>>for n in fib(6):#把yield的返回值赋给n
  	print(n)
    
1
1
2
3
5
8
```

但是用for循环调用generator时，发现拿不到`return`语句的返回值,要想拿到返回值，必须捕获`StopIteration`错误，返回值包含在`StopIteration`的`value`中

```python
>>> g = fib(6)
>>> while True:
...     try:
...         x = next(g)
...         print('g:', x)
...     except StopIteration as e:
...         print('Generator return value:', e.value)
...         break
...
g: 1
g: 1
g: 2
g: 3
g: 5
g: 8
Generator return value: done
```

### 迭代器iterator

可以直接作用于`for`的数据类型分两类

一类是集合类型，如`list`、`tuple`、`dict`、`set`、`str`等

一类是`generator`，包括生成器和带`yield`的generator function

这些可以直接作用于`for`循环的对象统称为可迭代对象:**iterable**



而生成器不但可以用于`for`，还可以被`next`不断调用，最后抛出`StopIteration`错误

可以被`next()`函数调用并不断返回下一个值的对象称为迭代器:**Iterator**

生成器都是`Iterator`对象，但`list`、`dict`、`str`虽然是`Iterable`，却不是`Iterator`。

把`list`、`dict`、`str`等`Iterable`变成`Iterator`可以使用`iter()`函数：

```python
>>> isinstance(iter(['1','2']), Iterator)
True
>>> isinstance(iter('abc'), Iterator)
True
```

#### 小结

凡是可作用于`for`循环的对象都是`Iterable`类型；

凡是可作用于`next()`函数的对象都是`Iterator`类型，它们表示一个惰性计算的序列；

集合数据类型如`list`、`dict`、`str`等是`Iterable`但不是`Iterator`，不过可以通过`iter()`函数获得一个`Iterator`对象。

Python的`for`循环本质上就是通过不断调用`next()`函数实现的，例如：

```python
for x in [1, 2, 3, 4, 5]:
    pass
```

实际上完全等价于：

```python
# 首先获得Iterator对象:
it = iter([1, 2, 3, 4, 5])
# 循环:
while True:
    try:
        # 获得下一个值:
        x = next(it)
    except StopIteration:
        # 遇到StopIteration就退出循环
        break
```

注意：

`Iterator`是惰性的，只有在需要返回下一个数据时它才会计算，所以我们不能提前知道序列的长度，只能不断通过`next()`函数实现按需计算下一个数据。

## 函数式编程

### map/reduce

#### map

`map()`函数接收两个参数，一个是`函数名`，一个是`Iterable`,map将传入的函数依次作用在iterable的`每个元素`上，并将新结果作为`Iterator`返回

```python
l=[1,2,3,4,5]
def f(x):
    return x*x
print(list(map(f,l)))
#结果:[1, 4, 9, 16, 25]
```

map返回的是`Iterator`，Iterator是惰性的，因此通过`list()`函数让它把整个序列都计算出来

<u>**注意：**</u>

map将传入的函数依次作用在iterable的`每个元素`上

```python
L1 = ['adam', 'LISA', 'barT']
list(map(normalize, L1))
#以上会依次把'adam', 'LISA', 'barT'依次传入normalize
L1 = 'adam'
list(map(normalize, L1))
#以上会把 'a'、'd'、'a'、'm'依次传入
```



#### reduce

`reduce()`也要两个参数，第一个是函数，第二个是`Iterable`,这个函数必须`接收两个参数`,reduce会把函数结果继续和序列的下一个参数做计算，最后返回一个结果

```python
from functools import reduce

def fn(x,y):
    return x*10+y
l=[1,3,5,7,9]
print(reduce(fn,l))
#结果:13579
```

计算过程：

第一次:向fn传入`1`和`3`,计算出13

第二次：传入`上一次结果13`和序列下一个数5，计算结果，依次类推

### filter()

和`map()`类似，`filter()`也接收一个函数和一个序列。和`map()`不同的是，`filter()`把传入的函数依次作用于每个元素，然后根据返回值是`True`还是`False`决定保留还是丢弃该元素。

例如，在一个list中，删掉偶数，只保留奇数，可以这么写：

```python
def is_odd(n):
    return n % 2 == 1

list(filter(is_odd, [1, 2, 4, 5, 6, 9, 10, 15]))
# 结果: [1, 5, 9, 15]
```

### sorted()

#### key

sorted()用于排序，它可以接收一个`key`来自定义排序，

```python
sorted([36, 5, -12, 9, -21], key=abs)
#结果：[5, 9, -12, -21, 36]
```

key指定的函数将作用于list的每一个元素上，并根据key函数返回的结果进行排序:

```
keys sort   => [5, 9,  12,  21, 36]
                |  |    |    |   |
result sort => [5, 9, -12, -21, 36]
```

**注意：**

​	key的函数<u>不会改变原有的值</u>，只是计算出结果用于对比排序

#### reverse

要进行反向排序，不必改动key函数，可以传入第三个参数`reverse=True`：

```python
sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower, reverse=True)
#结果：['Zoo', 'Credit', 'bob', 'about']
```

#### 练习

请用`sorted()`对上述列表分别按名字排序：

```python
L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]

def by_name(t):
    pass

L2 = sorted(L, key=by_name)
print(L2)
```

### 返回函数

```python
def lazy_sum(*args):
    def sum():
        ax = 0
        for n in args:
            ax = ax + n
        return ax
    return sum
```

以上，我们通过可变参定义了一个求和函数，但是它的返回值并不是值，而是函数

当我们调用lazy_sum返回的函数时，才真正计算结果

```python

>>> f = lazy_sum(1, 3, 5, 7, 9)
>>> f
<function lazy_sum.<locals>.sum at 0x101c6ed90>
>>> f()
25
```

再注意一点，当我们调用`lazy_sum()`时，每次调用都会返回一个新的函数，即使传入相同的参数

#### 闭包

以上情况我们称之为`闭包`

##### 例一

```python
def count():
    fs = []
    for i in range(1, 4):
        def f():
             return i*i
        fs.append(f)
    return fs

f1, f2, f3 = count()
```

以上函数，每一次循环都创建了一个新的函数

你可能认为调用`f1()`，`f2()`和`f3()`结果应该是`1`，`4`，`9`，但实际结果是：

```plain
>>> f1()
9
>>> f2()
9
>>> f3()
9
```

原因在于：

函数f()定义在循环中，而循环是将range中的元素依次赋给`变量i`，而返回函数都`引用`了变量`i`,这个`i`是随着循环改变的,当三个函数都返回时，它们所引用的`i`变成了3，所以他们的结果是9

##### 例二

```python
def test():
    i=0
    def test1():
        nonlocal i
        i+=1
        return i
    def test2():
        nonlocal i
        i+=1
        return i
    return test1,test2

x,y=test()
print(x())
print(y())
#结果：
#1
#2
```

所以注意：

**一般情况下返回函数不要引用任何循环变量，或者后续会发生变化的变量。**

#### nonlocal

如果想在内层函数中修改外层函数的变量，要使用nonlocal申明，否则报错

```python
def inc():
    x = 0
    def fn():
        nonlocal x   #必须加，否则报错
        x = x + 1
        return x
    return fn
```

注意：

以4.4.2为例，当 `inc` 函数返回内部的 `fn` 函数时，虽然 `inc` 函数的执行已经结束，但内部 `fn` 函数仍然引用着外部的 `x` 变量。Python 会为闭包（这里就是 `fn` 函数）保留它所引用的外部变量（`x`）的上下文环境，不会因为外部函数（`inc`）执行结束而将这些变量销毁,直到 `fn` 函数本身被销毁，`x` 才会被垃圾回收

### 偏函数

`functools.partial`是帮助固定函数的某些参数的

如int('1133',base=2)

```python
int2=functools.partial(int,base=2)
print(int2('100'))
#结果：4
```

如max(10,...)

```python
max2=functools.partial(max,10)
```

实际上，会把`10`自动加到左边

```python
max2(5,6,7)
#相当于：
max(10,5,6,7)
```

最后，创建偏函数时可以接收`函数对象`、`*args`和`**kw`3个参数

## 模块

在Python中，一个.py文件就称之为一个模块（Module）。

我们可以通过包来组织模块，避免冲突。每一个包目录下面都会有一个`__init__.py`的文件，这个文件是必须存在的，否则，Python就把这个目录当成普通目录，而不是一个包。`__init__.py`可以是空文件，也可以有Python代码，因为`__init__.py`本身就是一个模块，而它的模块名就是`包名`。

类似的，可以有多级目录，组成多级层次的包结构。比如如下的目录结构：

```
mycompany
 ├─ web
 │  ├─ __init__.py
 │  ├─ utils.py
 │  └─ www.py
 ├─ __init__.py
 ├─ abc.py
 └─ utils.py
```

两个`__init__.py`模块的模块名为`mycompany`和`mycompany.web`，文件`www.py`的模块名就是`mycompany.web.www`，两个文件`utils.py`的模块名分别是`mycompany.utils`和`mycompany.web.utils`。

### 使用模块

**hello.py**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'Michael Liao'

import sys

def test():
    args = sys.argv
    if len(args)==1:
        print('Hello, world!')
    elif len(args)==2:
        print('Hello, %s!' % args[1])
    else:
        print('Too many arguments!')

if __name__=='__main__':
    test()
```

第一行注释:让hello.py可以在Linux上运行

第二行：使用utf8编码

第四行：模块代码的第一个字符串都被视为文档注释

第六行：`__author__`变量把作者写进去

以上是Python模块的标准文件模版

```python
if __name__=='__main__':
    test()
```

当我们直接运行`hello.py`模块时，即python hello.py时，python解释器会把特殊变量`__name__`置为`__main__`,而如果是在其他地方导入`hello`模块,则不会，因此，这种if测试常见于运行测试

### 作用域与下划线_

以单下划线开头 ,如`_foo` 代表不能直接访问的类属性，需通过类提供的接口进行访问，不能用 `from xxx import` 而导入。

以双下划线开头的 `__foo`代表类的私有成员,不能直接被引用

类似`__xxx__`的变量是特殊变量，可以直接被引用，但是有特殊用途，如`__name__`，`__main__`等，`hello`模块的文档注释也可以用特殊变量`__doc__`来访问

## 面向对象

### 类与实例

```python
class Student(object):
    #object表示从哪个类继承，如果没有就选object,所有类都继承自object
    def __init__(self, name, score):
        #__init__的第一个参数永远是self，代表创建的实例本身，self是自动传入的
        #有了__init__函数，在创建实例时，就必须传入和__init__方法匹配的参数
        self.name = name
        self.score = score
        
    #在类中定义函数，第一个参数永远是self
    def print_score(self):
        print('%s: %s' % (self.name, self.score))
        
        
bart=Student()
bart.age=19 #可以自由地给一个实例绑定属性
```

### 访问限制

如果要让内部属性不被外部访问，可以把属性的名称前加上两个下划线`__`，在Python中，实例的变量名如果以`__`开头，就变成了一个私有变量（private），只有内部可以访问，外部不能访问。可以给对应变量增加`get`和`set`方法

```python
class Student(object):
    def __init__(self, name, gender,age):
        self.name = name
        self.__gender = gender
        self._age=age
    
    def get_gender(self):
        return self.__gender
```

有些时候，你会看到以一个下划线开头的实例变量名，比如`_age`，这样的实例变量外部是可以访问的，但是，按照约定俗成的规定，当你看到这样的变量时，意思就是，“虽然我可以被访问，但是，请把我视为私有变量，不要随意访问”。

最后注意下面的这种***错误写法***：

```python
stu=Student('a','a',18)
stu.__gender='b'
print(stu.__gender)
print(stu.get_gender())
#结果：
b#返回新设置的
a#返回实例本来的
```

表面上看，成功设置了`stu`实例的__gender,但实际上是给`stu`实例新增了一个`__gender`变量，而原来的`__gender`已经被解释器修饰为了其他名称

### 继承与多态

和c++一样，要注意的只有一点：

```python
#父类和子类
class Animal(object):
    def run(self):
        print('Animal is running...')
        
class Dog(Animal):
    def run(self):
        print('Dog is running...')

class Cat(Animal):
    def run(self):
        print('Cat is running...')
 
#新的类
class Timer(object):
    def run(self):
        print('Start...')
        
#现在实现一个方法
def run_once(animal):
    animal.run()

run_once(Animal())
run_once(Dog())
run_once(Cat())
run_once(Timer())
#结果
Animal is running...
Dog is running...
Cat is running...
Start...
```

从上面的输出结果，我们可以看出，对于python这样的`动态语言`来说，<u>我们只需要保证传入的对象中有相对应的方法，就可以实现像多态一样的语法，而不需要必须继承自同一个父类</u>

这就是动态语言的“**鸭子类型**”，它并不要求严格的继承体系，一个对象只要“看起来像鸭子，走起路来像鸭子”，那它就可以被看做是鸭子。

### 获取对象信息

#### type()

```python
#type返回对应的class类型
>>> type(123)
<class 'int'>
>>> type('str')
<class 'str'>
```

### isinstance()

```python
a=1
isinstance(a,int)
#也可以判断一个变量是否是某些类型中的一个
isinstance([1,2,3],(list,tuple))
```

### 使用dir()

如果要获得一个对象的所有属性和方法，可以使用`dir()`函数，它返回`一个包含字符串的list`

```python
>>> dir('ABC')
['__add__', '__class__',..., '__subclasshook__', 'capitalize', 'casefold',..., 'zfill']
```

类似`__xxx__`的函数都有特殊用途，比如`__len__`方法返回长度。在python中，如果你调用`len()`函数视图获取一个对象的长度，实际上，len()会自动去调用该对象的`__len__()`方法

```python
len('abc')
'abc'.__len__()
#以上两个方法等价
```

所以，如果我们自定义的类也想使用`len(obj)`，就在类中定义一个`__len__()`方法

这里每个有`__len__`方法的类都可以调用`len()`,就是上面提到的**鸭子类型**

#### getattr()、setattr()、hasattr()

配合`getattr()`、`setattr()`以及`hasattr()`，我们可以直接操作一个对象的状态

```python
>>> class MyObject(object):
...     def __init__(self):
...         self.x = 9
...     def power(self):
...         return self.x * self.x
>>> obj = MyObject()


>>>hasattr(obj,'y')#obj有没有y属性
False
>>>setattr(obj,'y',19)#给obj设置y属性
>>>getattr(obj,'y')#获取obj的y属性
19
```

如果试图获取不存在的属性，会抛出AttributeError错误，我们可以在调用`getattr()`时设置一个默认值，如果属性不存在，就返回默认值

```python
>>> getattr(obj, 'z', 404) # 获取属性'z'，如果不存在，返回默认值404
404
```

同时，也可以获取对象的方法，

```python
>>> hasattr(obj,'power') # 有属性'power'吗？
True
>>> fn=getattr(obj,'power')# 获取属性'power'并赋值到变量fn
>>> fn() # 调用fn()与调用obj.power()是一样的
```

### 实例属性和类属性

#### 实例属性

通过`self`和`实例对象`定义的属性，都是实例属性，它是属于实例的

#### 类属性

直接在<u>类的定义中显式定义的属性</u>，是类属性

```python
class Student(object):
    name='Student'

```

类属性可以直接通过类名访问，所有实例都可以访问到

```python
s=Student()
print(s.name)               #Student
print(Student.name)         #Student
s.name='a'      #这是给实例s绑定了属性name，并不影响类属性，但是实例属性优先级高					于类属性，所以类属性会被屏蔽
print(s.name)				#a
print(Student.name)			#Student
del s.name 				#可以删除实例属性
print(s.name)  				#实例属性就可以显示出来了
```

#### 总结

实例属性属于各个实例，互补干扰

类属性属于类，所有实例共享

## 面向对象高级

### 使用`__slots_`

我们可以给类或者实例绑定任何属性和方法

```python
class Student(object):
    pass

s=Student()
s.name='a'

def set_age(self,age):
    self.age=age
#绑定函数要用MethodType
from types import MethodType
s.set_age=MethodType(set_age,s)
s.set_age(10)
print(s.age)  #10
```

给实例绑定的方法，对另一个实例不起作用

为了给所有实例都绑定方法，可以给`class`绑定方法

```python
def set_score(self, score):
	self.score = score
    
Student.set_score=set_score
```

#### `__slots_`

如果要限制实例的属性，如，只允许给类Student的实例添加`name`和`age`属性

为了达到这一目的，我们可以在定义`class`时，定义一个特殊变量`__slots_`，来限制`class`实例能添加的属性

```python
class Student(object):
    __slots__=('name','age')
```

**注意：**

​    使用`__slots_`做的限制只在当前类的实例起作用，对其子类不起作用

   但如果在子类也定义了`__slots_`，那么子类允许定义的属性就是自身的`__slots__`再加上父类的`__slots__`

### @property

一般来说对于一个对象的属性，我们设置它的读、写、删除操作要写：get_xxx,set_xxx,del_xxx，并进行调用

但是我们可以用`@property`把这些操作修饰起来，在调用时就可以像访问属性一样调用

```python
class Student(object):
    def __init__(self,age):
        self._age=age
    @property
    def age(self):
        return self._age
    @age.setter
    def age(self,age):
        self._age=age
    @age.deleter
    def age(self):
        del self._age
#使用
s=Student(10)
print(s.age)
s.age=10
del s.age
```

如上，使用`@property`就可以在调用时直接使用属性名来读写删除属性
注意：

​    1.可以省略.setter方法，让属性变成`只读属性`

​    2.如果属性名和方法名相同，可能会触发递归调用，如调用`s.age`会调用`self.age`,`self.age`又会调用它自身，所以，一般在属性名前加一个`__`下划线来避免名称重复，如上面，`@property`的方法用的是`age`,而真正的属性名是`_age`

### 枚举类

#### 使用枚举类

```python
from enum import Enum
Month=Enum('Month',('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
```

这样，就获得了名称为`Month`的枚举类，可以中`Month.Jan`来引用一个常量

```python
for name,member in Month.__members__.items():
    print(name,'->',member.value)
```

`value`属性是自动赋给成员的`int`常量，默认从`1`开始计数

#### 自定义Enum:

```python
from enum import Enum,unique

@unique
class Weekday(Enum):
    Sun=0
    Mon = 1
    Tue = 2
```

`@unique`可以帮助我们检查保证没有重复值

#### 访问枚举类型的方法

```python
print(Weekday.Sun)       		#Weekday.Sun
print(Weekday['Sun'])			#Weekday.Sun
print(Weekday.Sun.value)		#0
print(Weekday(0))				#Weekday.Sun
print(Weekday.Sun==Weekday(0)) 	#True
```

可见，既可以用名称引用枚举常量，又可以根据value值获得枚举常量(枚举常量指的是Sun,Mon等)

## IO编程

### 文件读写

#### 读文件

使用`open`函数，传入文件名和标识符
`'r'`表示读，`'rb'`按二进制读

```python
f=open('/User/test.txt','r')
f = open('/Users/michael/test.jpg', 'rb')
f.read()
f.read(size)
f.readline()
f.readlines()
f.close()
```

`read()`函数会一次读取文件的所有内容，用一个`str`对象表示

`read(size)`每次最多读取size个字节内容

`readline()`一次读一行

`readlines()`一次读取所有内容并返回`list`

#### 字符编码

```python
f = open('/Users/michael/gbk.txt', 'r', encoding='gbk')
f = open('/Users/michael/gbk.txt', 'r',encoding='gbk',errors='ignore')
```

要读取非utf-8编码的文本文件，需要给`open()`函数传入`encoding`参数

如果遇到文件中夹杂一些非法编码字符，可以给`open()`函数传入`errors`参数

<u>注意：</u>

​    **不要忘记调用`close()`方法**

#### with语句

如果文件不存在，`open()`函数会抛出`IOError`的错误，我们可以通过`with`语句来处理：

```python
with open('path/test.txt','r') as f:
    f.read()
```

使用`with`语句可以不必调用`close()`方法

#### 写文件

调用`open()`时，传入`'w'`或者`'wb'`

```python
f = open('/Users/michael/test.txt', 'w')
f.write('Hello, world!')
```

当我们写文件时，操作系统不会立即将数据写入磁盘，而是放入内存缓存起来，空闲时再写入。只有调用`close()`方法时，才会保证把所有数据写入磁盘，忘记调用`close()`可能导致只写了一部分数据到磁盘。所以，使用`with`语句是个好方法。

`````python
with open('User.txt','w') as f:
    f.write('hello')
`````

要写入特定编码的文本文件，可以传入`encoding`参数

`````python
f.open('a.txt','a')
`````

<u>注意：</u>

**`w`参数是会覆盖原有文件内容，然后多次调用write()是在前一次write的基础上追加**

**如果要追加到原始内容之后，应选择`a`**

### StringIO和BytesIO

#### StringIO

`StringIO`用于在内存中读写`str`

读取和写入操作和读写普通文件一样

`````python
from io import StringIO
f=StringIO()
f.write('hello')
f.write(' ')
f.write('world!')
print(f.getvalue())
#hello world!
`````

`getvalue()`方法用于获得写入后的`str`

也可以用`str`初始化一个`StringIO`

`````
f = StringIO('Hello!\nHi!\nGoodbye!')
s=f.read()
`````



#### BytesIO

如果要操作二进制数据，就需要使用`BytesIO`。

`````python
from io import BytesIO
f=BytesIO()
f.write('中文'.encode('utf-8'))
`````

注意：

   写入的不是`str`，而是经过utf-8编码的`bytes`

