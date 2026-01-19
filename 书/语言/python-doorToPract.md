## python基础

### 字符串

#### 修改字符串大小写

1. 首字母大写：.title()
2. 全大写，全小写：.upper , .lower()

- 注意：以上函数都不修改变量本身的值，而是返回一个新的变量

```python
name = 'ada'
print(name.title())
print(name.upper())
print(name.lower())
```

#### 删除空白

1. 删除两端空白： .strip()
2. 删除左空白，右空白: .lstrip() , .rstrip()

- 注意：删除空白操作会保持原有字符串不变，返回一个新字符串

#### 删除前缀

删除前缀： .removeprefix()

```python
nos_url = 'http://nos.com'
print(nos_url.removeprefix('http://'))
```

- 注意：.removeprefix()和删除空白操作一样，都保持原有字符串不变

#### 使用print输出多行

当字符串很长时，需要分多行书写，可以在合适位置分行，在行尾加上引号，在之后的行的行首缩进并加上引号,这样，python会自动合并括号内的所有字符串

```python
print("hello "
     "world")
输出:
   hello world 
```



### 数

#### 整数

1. Python中两个乘号(**)，代表幂运算

    ```python
    10**2   ===>   100
    ```

#### 浮点数

1. 两个整数相除总是浮点数

    ```python
    4/2   ===>   2.0
    ```

#### 下划线

在python中，可以使用下划线分隔数字，使更容易辨别数字**(下划线不影响数字的值)**

```python
universe_age = 14_00_00
print(universe_age)   ===>   140000
```

#### 同时给多个变量赋值

```python
x, y, z = 0, 0, 0
```

python会按顺序把值赋给对应变量，只要变量数和值个数相同

####  常量

python中没有内置常量，但一般用**全大写字母**来指出某个变量应被视为常量

```python
MAX_CONNECTIONS = 5000
```

### 列表

一个列表可以存储不同种类的元素

#### 访问列表元素

1. 使用索引访问

2. **要访问最后一个元素，可以使用-1,倒数第二个使用-2，以此类推**

    ```python
    motorcycles = ['honda', 'yamaha', 'suzuki']
    motorcycles[-1]   ===>   'suzuki'
    motorcycles[-2]   ===>   'yamaha'
    motorcycles[-3]   ===>   'honda'
    ```

#### 修改、添加、删除元素

1. 修改

    ```python
    motorcycles = ['honda', 'yamaha', 'suzuki']
    # 修改
    motorcycles[0] = 'ducati'
    ```

2. 添加

    - 从末尾添加 .append
    - 从中间插入 .insert

    ```python
    motorcycles = ['honda', 'yamaha', 'suzuki']
    motorcycles.append('1')
    motorcycles.insert(0,'2')
    ```

3. 删除

    - del语句 ：根据索引删除元素
    - pop() ：默认**弹出并返回**给你**列表尾部**元素,也可弹出**对应索引**的元素
    - remove() ：根据值删除元素,但是**remove只会删除第一个它找到的元素**，如果要删除多个要用循环

```python
motorcycles = ['honda', 'yamaha', 'suzuki']
del motorcycles[0]
print(motorcycles)   ===>   ['yamaha', 'suzuki']

# pop()
popped_motorcycle = motorcycles.pop()
print(motorcycles) ===>   'suzuki'
motorcycles.pop(0) # 弹出索引为0的元素

# remove()
motorcycles.remove('yamaha')
```



#### 管理列表

1. 对列表排序：sort()

    - 注意：sort()函数**会修改原有List的排列顺序**
    - 如果想要反向排序，可在参数中传递reverse = True

    ```python
    cars = ['bmw', 'audi', 'toyota', 'subaru']
    cars.sort()
    cars.sort(reverse = True)
    ```

2. sorted()：如果不想修改原有顺序，可以使用sorted()函数

    ```python
    cars = ['bmw', 'audi', 'toyota', 'subaru']
    sorted(cars)
    ```

3. 反转列表：reverse()

    - 注意：reverse()**会修改原有list的顺序**

    ```python
    cars = ['bmw', 'audi', 'toyota', 'subaru']
    cars.reverse()
    ```

4. 列表长度：len()

    ```python
    cars = ['bmw', 'audi', 'toyota', 'subaru']
    len(cars)   ===>   4
    ```


#### 

1. 遍历列表

    ```python
    cars = ['bmw', 'audi', 'toyota', 'subaru']
    for car in cars:
        print(car)
    ```

2. 使用**range()**

    > 注意：**range()函数左闭右开**

    ```python
    for i in range(1,3):
        print(i)
    # 1,2
    ```

3. 使用range创建List

    ```python
    numbers = list(range(1,5))
    # [1,2,3,4]
    
    
    ```

    - 也可以给range设置步长

        ```python
        numbers = list(range(1,10,2))
        # 1,3,5,7,9
        ```

4. 对数值列表执行简单统计

    ```python
    numbers = [1,2,3]
    max(nembers)
    min(nembers)
    sum(nembers)
    ```

5. 列表推导式

    ```python
    numbers = [i*2 for i in range(1,10)]
    # 把从1到9的数依次赋给i，然后执行i*2，再把i*2的结果添加到列表
    ```

6. **切片**

    > **切片使用索引,依然是左闭右开区间**

    ```python
    cars = [1,2,3,4,5]
    cars_slice = cars[0:3] ===> [1,2,3]
    ```

    - 如果省略开头的数字，则默认从列表开头开始
    - 如果省略结尾数字，则默认从开到列表结尾的所有元素(包括最后一个)

    ```python
    cars = [1,2,3]
    cars_1 = cars[:2] ===> [1,2]
    cars_2 = cars[1:] ===> [2,3]
    ```

    - 前面(1.3.1)我们提到，可以使用负数索引

    ```python
    cars = [1,2,3]
    cars_3 = cars[-2:] ===> [2,3]
    ```

    ​	上述代码表示从倒数第二个元素开始到结尾的全部

    > ​	**记住不论使用负数还是正数索引，切片都是左闭右开区间**

    - 也可以在方括号内指定第三个值，也就是步长

        ```python
        cars = [1,2,3,4,5]
        cars_4 = cars[::2] ===> [1,3,5]
        ```

    **注意：**

    > **使用切片得到的是一个全新的List**
    >
    > ```python
    > cars = [1,2,3,4,5]
    > cars_4 = cars[::2]
    > cars_5 = cars
    > ```
    >
    > **以上，cars_4是新List,而cars_5指向了cars，cars_5和cars本质上是一个东西**


#### 判断元素是否在列表中

```python
cars = [1,2,3,4,5]
if 2 in cars:
    print(2)
```

#### 确定列表非空(条件表达式)

```python
cars = []
if cars:
    print('not null')
else :
    print ('null')
```

**当if将变量名作为条件表达式时，列表中如果有元素返回True,没有元素返回Flase**

> **对于数字0，空值None，空字符串('',""),空列表，空元组，空字典以及None，if都会返回False**

### 元组

**元组的元素是不可变的**

1. 定义与访问元组

    元组使用圆括号，不能修改值

    元组访问元素方法和列表一样

```python
dimensions = (200,5)
dimensions[0] = 100 ===> '错误'
```

**如果定义只有一个元素的元组，后面要跟一个逗号**,如果不加逗号，那么看起来就和运算符'()'一样，编译器会判断它是运算符而不是元组

```python
dimensions = [1,]
```

虽然不能修改元组中的元素，但是可以这样：

```python
dimen_1 = (1,2)
dimen_1 = (2,3)
```

这样做并没有修改元组中的元素，而是把变量dimen_1指向了一个新的元组，并未修改旧元组

### 字典

1. **字典中的元素按照其添加顺序排序**

2. 定义多行字典

    当字典有多行时，先左括号然后换行，然后缩进4个空格再写键值对以此类推

    **注意：最后一个键值对后面可以跟逗号**

    ```python
    user_0 = {
        'username': 'efermi',
        'first': 'enrico',
        'last': 'fermi',
    }
    ```

3. 删除字典元素(**del语句**)

    ```python
    alien_0 = {'color': 'green', 'points': 5}
    del alien_0['color']
    ```

4. 获取元素

    - 使用中括号

        ```python
        alien_0 = {'color': 'green', 'points': 5}
        point = =alien_0['points']
        ```

    - **使用get方法(推荐)**

        当尝试用get元素时，可以指定第二个参数，当键不存在时会返回该值，get方法可以避免键不存在时引发的错误

        > **注意：如果使用get获取不存在的元素，且没有指定第二个参数，那么get返回None**

        ```python
        alien_0 = {'color': 'green', 'points': 5}
        name = alien_0.get('name','no name')
        ```

5. 遍历字典

    - 遍历**所有键值对**

        **items()方法返回字典中所有键值对的列表**

        ```python
        user_0 = {
            'username': 'efermi',
            'first': 'enrico',
            'last': 'fermi',
        }
        
        for k,v in user_0.items():
            print(...)
        ```

    - 遍历**所有键**

        **当遍历字典时本身时会默认遍历所有的键(如下方代码中第二个for循环)**

        ```python
        favorite_languages = {
            'jen': 'python',
            'sarah': 'c',
            'edward': 'rust',
            'phil': 'python',
        }
        
        for k in favorite_languages.keys():
            print(k)
        for k in favorite_languages:
            print(k)
        ```

    - 遍历字典中所有的值

        ```python
        favorite_languages = {
            'jen': 'python',
            'sarah': 'c',
            'edward': 'rust',
            'phil': 'python',
        }
        
        for language in favorite_languages.values():
            print(language)
        ```

        如果你想过滤掉值中的重复项，可以使用集合set

        ```python
        for language in set(favorite_languages.values()):
            print(language)
        ```

### input

1. 使用input()获取用户输入

    ```python
    message = input("please input your age: ")
    print(message)
    ```

    > **注意：获取的输入都是str类型，如果输入的是数，可以通过int()来转换**



### 函数

#### 函数定义与函数参数

1. 函数定义

    ```python
    def greet_user():
        """简单问候语"""
        print('hello!')
    ```

    紧跟着函数定义的是**文档字符串**，描述了函数是做什么的，python在为程序的函数生成文档时，会查找紧跟在函数定义后的字符串，它用三个双引号引起

2. 函数的位置实参和关键字实参

    ```python
    def describe_pet(animal_type, pet_name):
     """显示宠物的信息"""
     print(f"\nI have a {animal_type}.")
     print(f"My {animal_type}'s name is {pet_name.title()}.")
    
    describe_pet('hamster', 'harry')
    describe_pet(animal_type='hamster', pet_name='harry')
    describe_pet(pet_name='harry', animal_type='hamster')
    ```

    以上是位置实参和关键字实参的用法，**位置实参必须严格按照形参的位置摆放，而关键字实参可以通过指定形参名来忽略摆放顺序**

    

3. 等效的函数调用

    我们在调用函数时**既可以使用位置实参，也可以使用关键字实参**

    ```python
    def describe_pet(pet_name, animal_type='dog'):
        pass
    
    # 一条名为 Willie 的小狗
    describe_pet('willie')
    describe_pet(pet_name='willie')
    # 一只名为 Harry 的仓鼠
    describe_pet('harry', 'hamster')
    describe_pet(pet_name='harry', animal_type='hamster')
    describe_pet(animal_type='hamster', pet_name='harry')
    ```

    > **注意：当全部使用关键字参数时可以忽略参数顺序，但是混合使用位置参数和关键字参数时需要注意位置关系，位置参数应该放在关键字参数之前**

    

4. 默认值

    ```python
    def describe_pet(pet_name, animal_type='dog'):
     """显示宠物的信息"""
     print(f"\nI have a {animal_type}.")
     print(f"My {animal_type}'s name is {pet_name.title()}.")
    ```

    > **注意：当使用默认值时，必须在形参列表中先列出没有默认值的**
    > **形参，再列出有默认值的形参。**

#### 函数参数默认传的是引用

```python
def print_models(unprinted_designs, completed_models):
 """
 模拟打印每个设计，直到没有未打印的设计为止
 打印每个设计后，都将其移到列表 completed_models 中
 """
 while unprinted_designs:
 current_design = unprinted_designs.pop()
 print(f"Printing model: {current_design}")
 completed_models.append(current_design)

 unprinted_designs = ['phone case', 'robot pendant',
'dodecahedron']
 completed_models = []
 print_models(unprinted_designs, completed_models)
```

在上面的实例中，将*unprinted_designs*直接传给了函数，**这传递的是变量的引用，函数中对变量的修改会作用到变量本身**

**如果不想传递自身，可以给函数传递一个变量的副本，这样函数中的修改就不是作用到变量本身**

```python
print_models(unprinted_designs[:], completed_models)
```

#### 任意数量实参（*args,**kwargs）

##### 任意数量位置实参(*args)

```python
def make_pizza(*toppings):
 """打印顾客点的所有配料"""
 print(toppings)
make_pizza('pepperoni')
make_pizza('mushrooms', 'green peppers', 'extra cheese')

输出:
('pepperoni',)
('mushrooms', 'green peppers', 'extra cheese')
```

形参*toppings中的星号让Python创建一个名为toppings的**元组**,该元组接收传给toppings的所有值

> **注意：在使用任意数量实参时，代码任意数量实参的形参应发在位置实参和关键字实参的后面**

#### 任意数量关键字实参

```python
def build_profile(first, last, **user_info):
    """创建一个字典，其中包含我们知道的有关用户的一切"""
    user_info['first_name'] = first
    user_info['last_name'] = last
    return user_info

user_profile = build_profile('albert', 'einstein',
                            location='princeton',
                            field='physics')
print(user_profile)

#输出：
{'location': 'princeton', 'field': 'physics', 'first_name': 'albert', 'last_name': 'einstein'}
```

形参**user_info的两个星号会让Python创建一个名为user_info的**字典**，该字典包含它所收到的所有键值对，可以像访问普通字典一样使用它，它本来就是一个字典

#### 参数定义顺序

参数定义顺序的黄金法则:

1. 位置参数
2. 默认参数
3. 可变位置参数*args
4. 关键字参数
5. 可变关键字参数**kwargs



**即：常规参数 $\rightarrow$ `*args` $\rightarrow$ 命名关键字 $\rightarrow$ `**kwargs`**

```python
def mixed_function(
    	pos1, pos2, default_p="A",
    	*args, key_only, **kwargs):
    pass
```



#### 函数编写指南

1. 函数名应见名知义，且**只使用小写字母和下划线**

2. **给模块命名也遵循上述约定**

3. 每个函数都应包含简要阐释其功能的注释，该注释应紧跟在函数定义后面，并采用文档字符串格式(三个双引号)

4. 在给形参默认值时，等号路边不要有空格，函数调用也一样，

    同时，在逗号后面要加一个空格

    ```python
    def function_name(parameter_0, parameter_1='default value')
    
    function_name(value_0, parameter_1='value')
    ```

5. 如果参数过多，可在函数定义处输入左括号然后回车，然后按两下制表符来缩进两次(两个缩进是为了和一个缩进的函数体区分开来)，右括号放在最后一行的参数后面

    ```python
    def function_name(
    		parameter_0, parameter_1, parameter_2,
    		parameter_3, parameter_4, parameter_5):
    ```

    

6. 所有import语句应该放在文件开头。唯一的例外是，你要在文件开头使用注释来描述整个程序。

### 模块

**首先：一个.py文件就是一个模块**

#### 导入模块

假设有一个 pizza.py 文件，里面有一个 make_pizza(size, *toppings) 函数，现在把它导入到正在编写的程序

需要在 pizza.py 同级目录创建一个文件，然后代码如下：

```python
import pizza

# 调用pizza模块中的make_pizza函数
pizza.make_pizza(...)
```

当运行该文件时，import 语句会让Python打开 pizza.py 文件并把所有函数复制到当前程序

#### 导入函数

可以只导入模块中的特定函数，继续以1.8.1代码为例

```python
from pizza import make_pizza

make_pizza(...)
```

如果使用这种方式，那么调用导入的函数时无需使用点号(.)

#### 使用as指定别名

如果导入的东西名称太长或者与现有程序有名称冲突，可以指定别名

1.  make_pizza() 函数指定别名 mp()

    ```python
    from pizza import make_pizza as mp
    
    mp(...)
    ```

2. 给 pizza 模块指定别名 p

```python
import pizza as p
```

#### 导入模块中的所有函数

使用星号(*)导入模块中的所有函数

```python
from pizza import *

make_pizza(...)
```

这里无需使用点号(.)，因为本质上这是直接导入函数（见1.8.2）

> **注意：不推荐使用这种导入方式，因为Python 可能会因为遇到多个名称相同的函数或变量而覆盖函数，而不是分别导入所有的函数。**
>
> **最佳做法是要么只导入需要的函数，要么导入模块，用模块名加方法名(如 pizza.make_pizza() (见1.8.1节))来调用**



























