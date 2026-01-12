## python基础

### 字符串

#### 修改字符串大小写

1. 首字母大写：.title()
2. 全大写，全小写：.upper , .lower()

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

    















































