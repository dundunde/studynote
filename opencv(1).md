# opencv

## 图像入门

### 图片操作

#### imread(path:str,flags:int)

path:图像路径

flags:读取图像方式

- cv.IMREAD_COLOR： 加载**彩色图像**。<u>透明度会被忽视</u>。它是**默认**标志。
- cv.IMREAD_GRAYSCALE：以**灰度**模式加载图像
- cv.IMREAD_UNCHANGED：加载图像，**包括alpha通道**

注意，<u>你可以分别简单地传递整数1、0或-1</u>。

#### imshow(winname:str,mat:UMat)

- winname:窗口名
- mat:图像

#### waitkey(delay:int)

- delay:等待多少毫秒

#### imwrite(filename:str,img:UMat)

- filename:要保存成的文件名
- img:图片

### 域的概念

#### 空间域

1. 空间域指的是图像本身。即由像素点在二维平面（x轴和y轴）上的排列所构成的直接表示。
2. **关注点**：每个像素点的**位置** 和该位置的**亮度/颜色值**。
3. 常见操作：
    - **点运算**：调整亮度、对比度、伽马校正。每个新像素值只取决于它原来的值。
    - **邻域运算（滤波）**：模糊、锐化、边缘检测。

#### 时间域

对于**单张静态图片**来说，没有时间维度，所以不涉及时间域。但是，对于**视频**来说，视频是由一帧帧图像按时间顺序排列而成的。因此，视频信号就是在时间域上变化的信号。每一帧图像是空间域信息，而帧与帧之间的变化就是时间域信息。

**核心思想：**
在时间域中，我们分析的是**像素值如何随时间变化**。我们关注的是“什么时候”和“如何变化”。

**常见的时间域操作：**

- **帧间差分**：检测连续帧之间的变化，用于运动目标检测。
- **光流**：计算像素从一个帧到下一个帧的运动矢量。
- **时间滤波**：对视频中同一位置在不同时间上的像素值进行平滑，用于视频降噪。

#### 频率域/频域

频域提供了一个完全不同的视角来看待图像。它不是将图像看作像素的集合，而是将其分解为**不同频率、幅度和相位的正弦波（或余弦波）的组合**。

- **高频成分**：对应图像中**变化剧烈**的部分，如**边缘、细节、噪声**。这些地方的像素值在很短的距离内差异很大。
- **低频成分**：对应图像中**变化平缓**的部分，如**大面积的平滑区域、背景**。
- **零频率**：变化速度为 0，即 “不变化” 的部分，也就是信号的恒定分量。

**常见的频域操作：**

- **低频滤波（低通滤波）**：只允许低频通过，会**模糊图像**、**平滑噪声**。
- **高频滤波（高通滤波）**：只允许高频通过，会**锐化图像**、**突出边缘**。
- **带阻/带通滤波**：去除或保留特定频率范围，常用于**去除周期性噪声**（如传感器条纹噪声）。

| 域         | 关注点             | 基本单元   | 主要操作             | 适用对象       |
| :--------- | :----------------- | :--------- | :------------------- | :------------- |
| **空间域** | 像素的位置和值     | 像素       | 点运算、**卷积**滤波 | 静态图像       |
| **时间域** | 像素值随时间的变化 | 帧         | 帧差分、光流         | 视频序列       |
| **频域**   | 图像的频率成分     | **正弦波** | 滤波（低通、高通等） | 静态图像、视频 |



### 二进制图像和二值图

在图像处理领域，**二进制图像（Binary Image）和二值图是同一个概念的不同称呼**，二者完全等价，指的是仅包含两种像素值的图像。

**具体说明**

- **定义核心**：无论是 “二进制图像” 还是 “二值图”，都描述了一种图像类型 —— 图像中的每个像素只能取两种可能的数值（通常为 **0 和 1**，或 **0 和 255** 等），分别代表黑色和白色（或其他两种对比色）。
- **名称由来**：“二进制” 强调其像素值基于二进制逻辑（非 0 即 1），而 “二值” 则直接点明图像只有两种取值状态，本质上是对同一概念的不同表述。

例如，经过阈值分割处理后，图像中只有黑色（0）和白色（255）两种像素，这样的图像既可以称为二进制图像，也可以称为二值图。



## 视频入门

### 读取视频VideoCapture()

- 参数：可以是设备索引或视频文件名

    `````python
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
     print("Cannot open camera")
     exit()
    while True:
     # 逐帧捕获
     ret, frame = cap.read()
     # 如果正确读取帧，ret为True
     if not ret:
     print("Can't receive frame (stream end?). Exiting ...")
     break
        
    `````

#### cap.get(),cap.set()

可以用`cap.get(propId) `方法访问该视频的某些功能，其中propId是0到18之间的一个数字。每个数字表示视频的**属性**（如果适用于该视频）

其中一些值可以使用 `cap.set(propId，value) `进行修改

`````python
#获取图像宽度和高度
cap.get(cv.CAP_PROP_FRAME_WIDTH)
cap.get(cv.CAP_PROP_FRAME_HEIGHT)
#修改
cap.set(cv.CAP_PROP_FRAME_WIDTH,320)
`````

<u>最后，别忘了**cap.release()**</u>

### 保存视频VideoWriter()

VideoWriter(filename: str, fourcc: int, fps: float, frameSize: cv2.typing.Size, isColor: bool)

其中`fourcc`是指定视频编码器的4字节代码

`````python
cap=cv.VideoCapture(0)
#videowriter
fourcc=cv.VideoWriter_fourcc('XVID')
out=cv.VideoWriter('output.avi',fourcc,20.0,(640,480))
ret,frame=cap.read()
out.write(frame)

#释放
cap.release()
out.release()
`````

## 核心操作

### 图像基本操作

#### 访问和修改像素值

在opencv中，图像一般是`BGR`格式，每个通道范围`0~255`

一般彩色图像读进内存之后是一个`h * w * c`的矩阵，其中h为图像高(相当于矩阵的行)，w为图像宽(相当于矩阵列)，c为通道数

`````python
img=cv.imread('img.jpg')
#shape返回高，宽，通道数
h,w,c=img.shape
#访问像素值
>>>img[100,100]
array([  0, 255, 255], dtype=uint8)
#修改
>>>img[100,100]=[255,255,255]
`````

- shape返回**高、宽、通道数**,如果是灰度图，则**仅包含高和宽**
- size返回**总像素数**
- dtype返回**图像数据类型**

##### 在python中

简单的访问每个像素和修改非常缓慢，建议使用Numpy中的item和itemset更好

`````python
#访问 红色通道 的值
>>>img.item(10,10,2)
59

#修改 红色通道 的值
>>>img.itemset((10,10,2),100)
>>>img.item(10,10,2)
100
`````

#### 感兴趣区域

选择一块区域并将其复制到图像中的另一个区域

`````python
subimg=img[280:340,330:390]
img[273:333,100:160]=subimg
`````

`````c++
//c++中
cv::Mat img = cv::imread("sample_image.jpg");
cv::Rect roiRect(0,0,200,200);
cv::Mat roiImg=img(roiRect)
`````

#### 拆分和合并通道

`````python
#拆分
b,g,r=cv.split(img)
#合并
img=cv.merge((b,g,r))

#拆分
b=img[:,:,0]
#将red值都设置为0
img[:,:,2]=0
`````

#### 制作图像边界CV.copyMakeBorder()

- src-输入的图像

- top,bottom,left,right-上下左右四个方向上的边界拓宽的值

- borderType-定义要添加的边框类型的标志。它可以是以下类型：

    > - [CV.BORDER_CONSTANT](https://docs.opencv.org/4.0.0/d2/de8/group__core__array.html#gga209f2f4869e304c82d07739337eae7c5aed2e4346047e265c8c5a6d0276dcd838)- 添加一个恒定的彩色边框。该值应作为下一个参数value给出。
    > - [CV.BORDER_REFLECT](https://docs.opencv.org/4.0.0/d2/de8/group__core__array.html#gga209f2f4869e304c82d07739337eae7c5a815c8a89b7cb206dcba14d11b7560f4b)-边框将是边框元素的镜像反射，如下所示：fedcba|abcdefgh|hgfedcb
    > - [CV.BORDER_REFLECT_101](https://docs.opencv.org/4.0.0/d2/de8/group__core__array.html#gga209f2f4869e304c82d07739337eae7c5ab3c5a6143d8120b95005fa7105a10bb4)或者[ CV.BORDER_DEFAULT](https://docs.opencv.org/4.0.0/d2/de8/group__core__array.html#gga209f2f4869e304c82d07739337eae7c5afe14c13a4ea8b8e3b3ef399013dbae01)-与上面相同，但略有改动，如下所示： gfedcb | abcdefgh | gfedcba
    > - [CV.BORDER_REPLICATE ](https://docs.opencv.org/4.0.0/d2/de8/group__core__array.html#gga209f2f4869e304c82d07739337eae7c5aa1de4cff95e3377d6d0cbe7569bd4e9f)-最后一个元素被复制，如下所示： aaaaaa | abcdefgh | hhhhhhh
    > - [CV.BORDER_WRAP](https://docs.opencv.org/4.0.0/d2/de8/group__core__array.html#gga209f2f4869e304c82d07739337eae7c5a697c1b011884a7c2bdc0e5caf7955661)-不好解释，它看起来像这样： cdefgh | abcdefgh | abcdefg

- value- 如果边框类型为[CV.BORDER_CONSTANT](https://docs.opencv.org/4.0.0/d2/de8/group__core__array.html#gga209f2f4869e304c82d07739337eae7c5aed2e4346047e265c8c5a6d0276dcd838)，则这个值即为要设置的边框颜色

`````python
img1 = CV.imread('OpenCV-logo.png')
replicate = CV.copyMakeBorder(img1,10,10,10,10,CV.BORDER_REPLICATE)
reflect = CV.copyMakeBorder(img1,10,10,10,10,CV.BORDER_REFLECT)
`````

### 图像的算术运算

#### 加法`cv.add()`

注意：opencv的add()是饱和运算,所以尽可能选择Opencv函数

`````python
>>> x = np.uint8([250])
>>> y = np.uint8([10])

>>> print(cv.add(x,y)) #250 + 10 =260 => 255
[[255]]
`````

#### 图像混合`cv.addWeighted()`

公式：dst=α⋅img1+β⋅img2+γ

`````python
img1 = cv.imread('ml.png')
img2 = cv.imread('opencv-logo.png')
dst = cv.addWeighted(img1,0.7,img2,0.3,0)
`````

#### 按位操作

按位 AND，OR，NOT 和 XOR 运算。

假如我想加一个OpenCV的 logo在一个图像上就可以使用按位操作

`````python
#加载两张图片
img1 = cv.imread('messi5.jpg')
img2 = cv.imread('opencv-logo-white.png')
#我想在左上角放置一个logo，所以我创建了一个 ROI,并且这个ROI的宽和高为我想放置的logo的宽和高
rows,cols,channels = img2.shape
roi = img1 [0:rows,0:cols]
#现在创建一个logo的掩码，通过对logo图像进行阈值，并对阈值结果并创建其反转掩码
img2gray = cv.cvtColor(img2,cv.COLOR_BGR2GRAY)
ret,mask = cv.threshold(img2gray,10,255,cv.THRESH_BINARY)
mask_inv = cv.bitwise_not(mask)
#现在使 ROI 中的徽标区域变黑
img1_bg = cv.bitwise_and(roi,roi,mask = mask_inv)
#仅从徽标图像中获取徽标区域。
img2_fg = cv.bitwise_and(img2,img2,mask = mask)
#在 ROI 中放置徽标并修改主图像
dst = cv.add(img1_bg,img2_fg)
img1 [0:rows,0:cols] = dst
cv.imshow('res',img1)
cv.waitKey(0)
cv.destroyAllWindows()
`````

#### 乘法与矩阵乘法

在 OpenCV 中，矩阵的运算需要区分两种不同的乘法：

1. **逐元素相乘**（Hadamard 积）：使用 `*` 运算符，直接对两个同尺寸矩阵的对应元素进行相乘。
2. **矩阵乘法**（线性代数中的矩阵乘积）：需要使用专门的函数实现，具体有两种方式：
    - 使用 `cv2.matMul()` 函数
    - 使用 NumPy 的 `np.dot()` 函数（OpenCV 矩阵本质上是 NumPy 数组）

#### 比较操作

```python
res=cv.imread('1.jpg',0)
threshold=100
mask=res>=threshold
```

`res >= threshold` 是一个逐元素的比较操作，它对 `res` 矩阵中的**每个元素**进行独立判断，如果 `res[i,j] >= threshold`，则该位置结果为`1`，如果 `res[i,j] < threshold`，则该位置结果为 `0`



## 图像处理

### 更改颜色空间

`````python
img=cv.imread('img.jpg')
hsv_img=cv.cvtColor(img,cv.COLOR_BGR2HSV)
`````

注意：

> ​    *对于 HSV, `色调(Hue)`范围为 [0,179], `饱和度(Saturation)`范围为 [0,255] ，`明亮度(Value)`为 [0,255]. 不同的软件使用不同的比例. 所以如果你想用 OpenCV 的值与别的软件的值作对比，你需要**归一化**这些范围。*



### 目标追踪

`````python
img=cv.imread("D:\\Downloads\\4-1-1.jpg")
hsv=cv.cvtColor(img,cv.COLOR_BGR2HSV)

low_blue=np.array([110,50,50])
up_blue=np.array([130,255,255])

mask=cv.inRange(hsv,low_blue,up_blue)

res=cv.bitwise_and(img,img,mask=mask)

cv.namedWindow('res',cv.WINDOW_NORMAL)
cv.imshow('res',res)
`````



![图片](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/4-1-1.jpg)

#### 如何找到hsv值

要从bgr值找到hsv值，同样使用`cv.cvtColor()`

`````python
green=np.uint8([[0,255,0]])
hsv_green=cv.cvtColor(green,cv.COLOR_BGR2HSV)
print(hsv_green)
`````

### 图像的几何变换

​    OpenCV 提供了两个变换函数，`cv.warpAffine`和 `cv.warpPerspective`，可以进行各种转换。 `cv.warpAffine`采用 **2x3** 变换矩阵，而 `cv.warpPerspective`采用 **3x3** 变换矩阵作为输入。

#### 缩放`resize()`

使用`cv.resize()`函数调整大小，可以指定大小，也可以指定比例因子，同时可以使用<u>不同的插值方法</u>。

对于下采样(缩小)，最合适的插值方法是 `cv.INTER_AREA` 对于上采样(放大),最好的方法是 `cv.INTER_CUBIC`（速度较慢）和 `cv.INTER_LINEAR` (速度较快)。默认情况下，所使用的插值方法都是 `cv.INTER_AREA`。

`````python
import cv2 as cv
img = cv.imread('messi5.jpg')

res = cv.resize(img,None,fx=2, fy=2, interpolation = cv.INTER_CUBIC)

height, width = img.shape[:2]
res = cv.resize(img,(2*width, 2*height), interpolation = cv.INTER_CUBIC)
`````

#### 平移变换

平移矩阵形式如下：

![图片](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/Geometric_Transformations_fomula_1.png)

`````python
img = cv.imread('messi5.jpg',0)
rows,cols = img.shape
M = np.float32([[1,0,100],[0,1,50]])
dst = cv.warpAffine(img,M,(cols,rows))
cv.imshow('img',dst)
`````

**![图片](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/Geometric_Transformations_1.jpg)**

**注意：**

`cv.warpAffine` 函数的第三个参数是输出图像的大小，其形式应为（宽度、高度）。记住宽度=列数，高度=行数。

#### 旋转

以**θ**角度旋转图片的矩阵为：![图片](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/Geometric_Transformations_fomula_2.png)

但 Opencv 提供了可变旋转中心的比例变换，所以你可以在任意位置旋转图片，修改后的转换矩阵为：![图片](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/Geometric_Transformations_fomula_3.png)

![图片](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/Geometric_Transformations_fomula_4.png)

为了找到这个转换矩阵，可以用`cv.getRotationMatrix2D`

`````python
img = cv.imread('messi5.jpg',0)
rows,cols = img.shape
# cols-1 and rows-1 are the coordinate limits.
M = cv.getRotationMatrix2D(((cols-1)/2.0,(rows-1)/2.0),90,1)
dst = cv.warpAffine(img,M,(cols,rows))
`````

![图片](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/Geometric_Transformations_2.jpg)

#### 仿射变换

在仿射变换中，原图像所有的平行线在输出图像中**仍然是平行的**。为了找到变换矩阵，需要从输入图像中取三个点以及它们在输出图像中的对应位置。然后通过`cv.getAffineTransform`创建一个2x3矩阵。

`````python
img = cv.imread('drawing.png')
rows,cols,ch = img.shape
pts1 = np.float32([[50,50],[200,50],[50,200]])
pts2 = np.float32([[10,100],[200,50],[100,250]])
M = cv.getAffineTransform(pts1,pts2)
dst = cv.warpAffine(img,M,(cols,rows))
plt.subplot(121),plt.imshow(img),plt.title('Input')
plt.subplot(122),plt.imshow(dst),plt.title('Output')
plt.show()
`````

![图片](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/Geometric_Transformations_3.jpg)

#### 透视变换

对于透视变换需要一个**3x3矩阵**，在变换之后，**直线也将保持直线**。要找到这个变换矩阵，需要输入原图像的**4个点**及它们在输出图像上的对应点坐标。在这四个点中，任意三个点**不共线**。

可以通过`cv.getPerpectiveTransform`找到该矩阵。3x3要使用`cv.warpPerpective`

`````python
img = cv.imread('sudoku.png')
rows,cols,ch = img.shape
pts1 = np.float32([[56,65],[368,52],[28,387],[389,390]])
pts2 = np.float32([[0,0],[300,0],[0,300],[300,300]])
M = cv.getPerspectiveTransform(pts1,pts2)
dst = cv.warpPerspective(img,M,(300,300))
plt.subplot(121),plt.imshow(img),plt.title('Input')
plt.subplot(122),plt.imshow(dst),plt.title('Output')
plt.show()
`````

![图片](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/Geometric_Transformations_4.jpg)

### 图像阈值

#### 简单阈值法`cv.threshold`

如果像素值大于阈值，则会被赋为一个值（可能为白色），否则会赋为另一个值（可能为黑色）。

**参数：**

1. 源图像，它应该是**灰度图像**。
2. 阈值，用于对像素值进行分类。
3. maxval，它表示像素值大于（有时小于）阈值时要给定的值。
4. 阈值类型，是枚举值。不同的类型有：

![img](https://img-blog.csdn.net/20170810122741046?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxMjU2Njc1MQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

生成关系如下

![img](https://img-blog.csdn.net/20170810122752738?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvdTAxMjU2Njc1MQ==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

**返回值：**

1. retval:所使用的阈值
2. 生成的阈值图像

```python
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
img = cv.imread('gradient.png',0)
ret,thresh1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
ret,thresh2 = cv.threshold(img,127,255,cv.THRESH_BINARY_INV)
ret,thresh3 = cv.threshold(img,127,255,cv.THRESH_TRUNC)
ret,thresh4 = cv.threshold(img,127,255,cv.THRESH_TOZERO)
ret,thresh5 = cv.threshold(img,127,255,cv.THRESH_TOZERO_INV)
titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]
for i in xrange(6):
    plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()
```

![图片](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/Image_Thresholding_1.png)

#### 自适应阈值`adaptiveThreshold()`

自适应阈值会计算图像中的小区域的阈值

参数(这里只说重要的三个)：

**adaptiveMethod: int**决定了如何计算阈值

- `cv.ADAPTIVE_THRESH_MEAN_C` 阈值是指邻近地区的平均值。
- `cv.ADAPTIVE_THRESH_GAUSSIAN_C`阈值是权重为高斯窗的邻域值的加权和。

**blockSize: int**

计算阈值的区域的大小

**C: float**

从计算出的阈值中减去C

`````python
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
img = cv.imread('sudoku.png',0)
img = cv.medianBlur(img,5)
ret,th1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
th2 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C,\
            cv.THRESH_BINARY,11,2)
th3 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv.THRESH_BINARY,11,2)
titles = ['Original Image', 'Global Thresholding (v = 127)',
            'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
images = [img, th1, th2, th3]
for i in xrange(4):
    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()
`````

![图片](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/Image_Thresholding_2.png)

#### Otsu二值化

在之前的简单阈值中，我们使用了一个任意阈值，但是我们不知道该阈值好还是不好，只能用试错法，但如果图像是一个**双峰图像**（双峰图像是一个直方图有两个峰值的图像，参照下图中(2,0)和(2,1)图），我们可以取**两个峰值中间的值**作为阈值(因为该图像的像素点呈双峰分布，取中间值做阈值可以把像素点有效地进行划分)

Otsu二值化：自动从双峰图像的直方图中计算出合适的阈值（对于非双峰图像，二值化将不准确。）

我们依旧使用`cv.threshold`，但需要额外传递`cv.THRESH_OTSU`,对于阈值，**传0**即可。然后该函数会找到合适的阈值，**并把阈值作为输出retval返回**(如果不使用 otsu 二值化，则 retval 与你使用的阈值相同)

```python
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
img = cv.imread('noisy2.png',0)
# 全局阈值
ret1,th1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
# Otsu 阈值
ret2,th2 = cv.threshold(img,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
# 经过高斯滤波的 Otsu 阈值
blur = cv.GaussianBlur(img,(5,5),0)
ret3,th3 = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
# 画出所有的图像和他们的直方图
images = [img, 0, th1,
          img, 0, th2,
          blur, 0, th3]
titles = ['Original Noisy Image','Histogram','Global Thresholding (v=127)',
          'Original Noisy Image','Histogram',"Otsu's Thresholding",
          'Gaussian filtered Image','Histogram',"Otsu's Thresholding"]
for i in xrange(3):
    plt.subplot(3,3,i*3+1),plt.imshow(images[i*3],'gray')
    plt.title(titles[i*3]), plt.xticks([]), plt.yticks([])
    plt.subplot(3,3,i*3+2),plt.hist(images[i*3].ravel(),256)
    plt.title(titles[i*3+1]), plt.xticks([]), plt.yticks([])
    plt.subplot(3,3,i*3+3),plt.imshow(images[i*3+2],'gray')
    plt.title(titles[i*3+2]), plt.xticks([]), plt.yticks([])
plt.show()

```

![图片](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/Image_Thresholding_3.png)

### 滤波

图像可以通过各种**低通滤波器(LPF)**、**高通滤波器(HPF)**进行过滤。`LPF`有助于消除噪音、模糊图像，`HPF`有助于在图像中找到边缘。

opencv提供了cv.filter2D()用于将图像与内核进行卷积。

```cpp
void cv::filter2D(InputArray   src,
                  OutputArray  dst,
                  int          ddepth,
                  InputArray   kernel,
                  Point        anchor=Point(-1, -1),
                  double       delta=0,
                  int          borderType=BORDER_DEFAULT
                  )
```

> ddepth:期望深度，填-1即可
>
> kernel：卷积核
>
> anchor：锚点
>
> borderType：border 的生成方式，如下图，注意两点：
>
> - `cv.BORDER_WARP` 在这个函数里面是不支持的；
> - `cv.BORDER_CONSTANT` 会将边缘取为 0（黑色），而且没法改，因为原函数并没有留出相关的接口。

![border from opencv document](https://i-blog.csdnimg.cn/blog_migrate/ee820dba0a9ecb1c15eb994720b13e79.jpeg#pic_center)

如以下是一个内核，将该内核中心与一个像素对齐，然后将该内核范围内的 25 个像素乘以矩阵中对应的值再相加，最后他们的总和乘以1/25，并用新的平均值替换这个25x25窗口的中心像素。然后继续对图像中的所有像素执行此操作。

![图片](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/Smoothing_Images_1.png)

```python
img = cv.imread('opencv_logo.png')
kernel = np.ones((5,5),np.float32)/25
dst = cv.filter2D(img,-1,kernel)
```

#### 图像模糊(图像平滑)

图像模糊是通过`低通滤波器`实现的。它有助于`消除噪音`、`边缘`

##### 均值模糊

这是通过**归一化**的滤波器内核与图像卷积来完成的。

归一化指的是`4.5节`第一个图那样，所有的像素相加之后要除以核的大小

函数有：`cv.blur()`和`cv.boxFilter()`

```python
img = cv.imread('opencv-logo-white.png')
#使用5x5的核
blur = cv.blur(img,(5,5))
```

![图片](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/Smoothing_Images_4.png)

> **注意：**
>
>    **如果不适用归一化的滤波，请使用`cv.boxFilter()`并传入normalize=False参数**

##### 高斯模糊`cv.GaussianBlur()`

应该指定内核的`宽度`和`高度`,它应该是`正数且是奇数`(奇数才只有一个中位数)，以及x,y方向的标准偏差`sigmax`和`sigmay`。如果只指定sigmax，则 sigmay 与 sigmax 相同。如果这两个值都是0，那么它们是根据内核大小计算出来的。

高斯模糊是消除图像高斯噪声的有效方法。

如果需要，可以使用`cv.getGaussianKernel()`创建高斯核

```python
blur = cv.GaussianBlur(img,(5,5),0)
```

##### 中值滤波`cv.medianBlur()`

取内核区域下`所有像素的中间值`，将中央元素替换为该中值。这对椒盐噪声非常有效。它的内核大小是一个`正的奇数整数`

```python
median = cv.medianBlur(img,5)
```

![图片](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/Smoothing_Images_6.png)

##### 双边滤波`cv.bilateralFilter()`

双边滤波在`保持边缘锐利`的同时，对噪声去除非常有效。但与其他过滤器相比，操作速度较慢。

高斯滤波器取像素周围的邻域并找到其高斯加权平均值。该高斯滤波器是一个空间函数，即在滤波时考虑相邻像素。但是它不考虑像素是否具有几乎相同的强度，也不考虑像素是否是边缘像素。所以它也会模糊边缘

双边滤波器在空间上也采用高斯滤波器，而另一个高斯滤波器则是像素差的函数。空间的高斯函数确保模糊只考虑邻近像素，而强度差的高斯函数确保模糊只考虑与中心像素强度相似的像素。所以它保留了边缘，因为边缘的像素会有很大的强度变化。

```cpp
void bilateralFilter( InputArray src, 
                      OutputArray dst, 
                      int d,
                      double sigmaColor, 
                      double sigmaSpace,
                      int borderType = BORDER_DEFAULT );
```

> - 第一个参数，InputArray类型的src，输入图像，即源图像，需要为8位或者浮点型单通道、三通道的图像。
> - 第二个参数，OutputArray类型的dst，即目标图像，需要和源图片有一样的尺寸和类型。
> - 第三个参数，int类型的d，表示在过滤过程中每个像素邻域的直径。如果这个值我们设其为非正数，那么OpenCV会从第五个参数sigmaSpace来计算出它来。
> - 第四个参数，double类型的sigmaColor，颜色空间滤波器的sigma值。这个参数的值越大，就表明该像素邻域内有更宽广的颜色会被混合到一起，产生较大的半相等颜色区域。
> - 第五个参数，double类型的sigmaSpace坐标空间中滤波器的sigma值，坐标空间的标注方差。他的数值越大，意味着越远的像素会相互影响，从而使更大的区域足够相似的颜色获取相同的颜色。当d>0，d指定了邻域大小且与sigmaSpace无关。否则，d正比于sigmaSpace。
> - 第六个参数，int类型的borderType，用于推断图像外部像素的某种边界模式。注意它有默认值BORDER_DEFAULT。

```python
blur = cv.bilateralFilter(img,9,75,75)
```

![图片](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/Smoothing_Images_7.png)

### 形态转换







### 图像梯度

梯度滤波器是高通滤波器的一种。**梯度滤波器的核心目的是：检测图像中的变化（可以看成是检测边缘，因为边缘处的梯度值大）**

它本质上反映了图像中像素灰度值的**变化率**和**变化方向**，是衡量图像局部区域明暗变化剧烈程度的关键指标。

#### 梯度在图像处理中的意义

梯度检测的核心目的是**捕捉图像中的边缘信息**，而梯度的特性直接支撑了这一目标：

- **梯度大小与边缘强度**：梯度大小越大，说明该位置的灰度值变化越剧烈，越可能是图像中的边缘（如物体轮廓、纹理边界等）。
- **梯度方向与边缘方向**：梯度方向指向灰度值增加最快的方向，而边缘的走向与梯度方向垂直。例如，梯度方向为 90°（向上）时，边缘可能是水平的。

#### sobel算子

sobel算子，主要用作边缘检测，是离散差分算子，用来运算图像梯度函数的灰度近似值。在图像的任何一点使用此算子，将会产生对应的梯度矢量或者法矢量。

> *Sobel(src,ddepth,dx,dy[,dst[,ksize[,scale[,delta[,borderType]]]]])*
>
> src参数表示输入需要处理的图像。
> ddepth参数表示输出图像深度，针对不同的输入图像，输出目标图像有不同的深度。（一般源图像都为CV_8U，为了避免溢出，一般ddepth参数选择CV_32F）
> dx参数表示x方向上的差分阶数，1或0 。
> dy参数表示y 方向上的差分阶数，1或0 。
> dst参数表示输出与src相同大小和相同通道数的图像。
> ksize参数表示Sobel算子的大小，必须为1、3、5、7。
> scale参数表示缩放导数的比例常数，默认情况下没有伸缩系数。
> delta参数表示一个可选的增量，将会加到最终的dst中，同样，默认情况下没有额外的值加到dst中。
> borderType表示判断图像边界的模式。这个参数默认值为cv2.BORDER_DEFAULT。

#### 拉普拉斯算子(Laplacian)

> *Laplacian(src, ddepth[, dst[, ksize[, scale[, delta[, borderType]]]]])*
>
> src参数表示输入需要处理的图像。
> ddepth参数表示输出图像深度，针对不同的输入图像，输出目标图像有不同的深度。（一般源图像都为CV_8U，为了避免溢出，一般ddepth参数选择CV_32F）
> dst参数表示输出与src相同大小和相同通道数的图像。
> ksize参数表示用于计算二阶导数滤波器的孔径大小，大小必须是正数和奇数。
> scale参数表示计算拉普拉斯算子值的比例因子，默认情况下没有伸缩系数。
> delta参数表示一个可选的增量，将会加到最终的dst中，同样，默认情况下没有额外的值加到dst中。
> borderType表示判断图像边界的模式。这个参数默认值为cv2.BORDER_DEFAULT。

```python
img = cv.imread('dave.jpg',0)

sobel_x=cv.Sobel(img,cv.CV_32F,1,0)#x方向求导
sobel_y=cv.Sobel(img,cv.CV_32F,0,1)#y方向求导
lap=cv.Laplacian(img,cv.CV_64F)

sobel_x_abs=cv.convertScaleAbs(sobel_x)
sobel_y_abs=cv.convertScaleAbs(sobel_y)
lap_abs=cv.convertScaleAbs(lap)


cv.imshow('img',img)
cv.imshow('sobel_x_abs',sobel_x_abs)
cv.imshow('sobel_y_abs',sobel_y_abs)
cv.imshow('lap_abs',lap_abs)
```

![操作结果](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/Image_Gradients_5.png)

注意：

​    在梯度计算时我们把输出图像的数据类型设为了更高的格式,如CV_32F,CV_64F,这是因为求导会有斜率(见下方描述)，斜率会有正负，如果设置输出格式为CV_8U的话会导致负值被截断为0（因为负数无法表示），而正值超过255时也会被截断为255。因此，只有正梯度会被保留，负梯度会丢失，从而导致边缘检测中丢失白黑过渡的边缘。

> **黑白过渡**为正值：在灰度图像中，黑色像素值接近0，白色像素值接近255。当像素值从黑到白增加时，梯度（一阶导数）为正值。
>
> **白黑过渡**（从白色到黑色）：当像素值从白到黑减少时，梯度为负值。例如，从右到左（白到黑）时，梯度为负。

为了保留完整的梯度信息，建议将输出数据类型保持为更高的精度，如果需要的话，可以取绝对值再转换回`cv.CV_8U`(上面代码中的convertScaleAbs)，这样负梯度值也会被转换为正值，从而保留边缘信息。

> 需要转为CV_8U的场景：
>
> imshow:该期望的图像数据类型是 `cv.CV_8U`（8位无符号整数，范围0-255）
>
> 直接显示浮点图像会导致：
>
> - 负值和大于1的值被截断或显示异常
> - 图像看起来几乎全黑或全白，无法正确显示梯度信息
> - `cv.imshow`显示图像时，如果图像是浮点数，OpenCV会假设像素值在0到1之间（如果值大于1，则显示为白色）。因此，直接显示浮点图像会导致大部分图像为白色或黑色，无法正确显示梯度。

#### 丢失边缘与不丢失的对比

```python
img = cv.imread('box.png',0)
# Output dtype = cv.CV_8U
sobelx8u = cv.Sobel(img,cv.CV_8U,1,0,ksize=5)#第二张图
# Output dtype = cv.CV_64F. Then take its absolute and convert to cv.CV_8U
sobelx64f = cv.Sobel(img,cv.CV_64F,1,0,ksize=5)
abs_sobel64f = cv.convertScaleAbs(sobelx64f)#第三张图
```

![图片](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/Image_Gradients_3.png)

#### Scharr算子(Sobel算子的增强版，效果更突出)

```python
grad_x = cv.Scharr(image, cv.CV_32F, 1, 0)   #对x求一阶导
    grad_y = cv.Scharr(image, cv.CV_32F, 0, 1)   #对y求一阶导
    gradx = cv.convertScaleAbs(grad_x)  #用convertScaleAbs()函数将其转回原来的uint8形式
    grady = cv.convertScaleAbs(grad_y)
    cv.imshow("gradient_x", gradx)  #x方向上的梯度
    cv.imshow("gradient_y", grady)  #y方向上的梯度
```

OpenCV的Laplacian函数原型为：

> *Laplacian(src, ddepth[, dst[, ksize[, scale[, delta[, borderType]]]]])*
> src参数表示输入需要处理的图像。
> ddepth参数表示输出图像深度，针对不同的输入图像，输出目标图像有不同的深度。（一般源图像都为CV_8U，为了避免溢出，一般ddepth参数选择CV_32F）
> dst参数表示输出与src相同大小和相同通道数的图像。
> ksize参数表示用于计算二阶导数滤波器的孔径大小，大小必须是正数和奇数。
> scale参数表示计算拉普拉斯算子值的比例因子，默认情况下没有伸缩系数。
> delta参数表示一个可选的增量，将会加到最终的dst中，同样，默认情况下没有额外的值加到dst中。
> borderType表示判断图像边界的模式。这个参数默认值为cv2.BORDER_DEFAULT。

### Canny边缘检测

Canny的步骤：

#### 降噪

使用 5x5 高斯滤波器去除图像中的噪声

#### 寻找图像的强度梯度和方向

在水平和垂直方向上用 Sobel 内核对平滑后的图像进行滤波，以获得水平方向（[![G_x](https://latex.codecogs.com/png.latex?G_x)](https://www.codecogs.com/eqnedit.php?latex=G_y)）和垂直方向（[![G_y](https://latex.codecogs.com/png.latex?G_y)](https://www.codecogs.com/eqnedit.php?latex=G_y)）的一阶导数。从这两个图像中，我们可以找到每个像素的边缘梯度(G)和梯度方向(θ)

![img](https://img-blog.csdn.net/20140707092033453?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvcG9lbV9xaWFubW8=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

梯度方向始终垂直于边缘，它被近似到四个可能角度之一(一般为0, 45, 90, 135)

#### 非最大抑制

在获得梯度幅度和方向之后，完成图像的全扫描以去除可能不构成边缘的任何不需要的像素。为此，在每个像素处，检查像素是否是其在梯度方向上的邻域中的局部最大值。![nms.jpg](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/Image_canny_nms.jpg)

A 点位于边缘（垂直方向）。梯度方向与边缘垂直。 B 点和 C 点处于梯度方向。因此，用点 B 和 C 检查点 A，看它是否形成局部最大值。如果是这样，则考虑下一阶段，否则，它被抑制（归零）。

简而言之，您得到的结果是具有“细边”(候选边缘)的二进制图像。

#### 滞后阈值

这个阶段决定哪些边缘都是边缘，哪些边缘不是边缘。为此，我们需要两个阈值，minVal 和 maxVal。强度梯度大于 maxVal 的任何边缘肯定是边缘，而 minVal 以下的边缘肯定是非边缘，因此被丢弃。位于这两个阈值之间的人是基于其连通性的分类边缘或非边缘。如果它们连接到“可靠边缘”像素，则它们被视为边缘的一部分。否则，他们也被丢弃。见下图：![hysteresis.jpg](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/Image_canny_hysteresis.jpg)

边缘 A 高于 maxVal，因此被视为“确定边缘”。虽然边 C 低于 maxVal，但它连接到边 A，因此也被视为有效边，我们得到完整的曲线。但是边缘 B 虽然高于 minVal 并且与边缘 C 的区域相同，但它没有连接到任何“可靠边缘”，因此被丢弃。因此，我们必须相应地选择 minVal 和 maxVal 才能获得正确的结果。

在假设边是长线的情况下，该阶段也消除了小像素噪声。所以我们最终得到的是图像中的强边缘。

```python
img = cv.imread('messi5.jpg',0)
edges = cv.Canny(img,100,200)
```

![canny1.jpg](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/Image_canny_2.jpg)

> cv.Canny( image, threshold1, threshold2[, apertureSize[, L2gradient]])
>
> 第一个参数，InputArray类型的image，输入图像，即源图像，填Mat类的对象即可，且需为单通道8位图像。
> 第三个参数，double类型的threshold1，第一个滞后性阈值。
> 第四个参数，double类型的threshold2，第二个滞后性阈值。
> 第五个参数，int类型的apertureSize，表示应用Sobel算子的内核大小，其有默认值3。
> 第六个参数，bool类型的L2gradient，它指定用于查找梯度幅度的方程式。如果为`True`，则使用上面提到的更精确的公式，否则使用以下函数：Edge_Gradient(G)=|Gx|+|Gy|。默认情况下，它为`False`。

### 图像金字塔

底部为最高分辨率图像，而顶部为最低分辨率图像

- **高斯金字塔(Gaussian pyramid):** 用来向下采样
- **拉普拉斯金字塔(Laplacian pyramid):** 用来从金字塔低层图像重建上层未采样图像，可以对图像进行最大程度的还原，配合高斯金字塔一起使用。

#### 高斯金字塔

　**高斯金字塔主要用于下采样**(注意下采样其实是**由金字塔底部向上采样，分辨率降低，它和我们理解的金字塔概念相反**；)。高斯金字塔是最基本的图像塔。原理：首先将原图像作为最底层图像 level0（高斯金字塔的第0层），利用**高斯核（5*5）对其进行卷积**，然后对卷积后的图像进行**下采样（去除偶数行和列）**得到上一层图像G1(所以结果只有原图的**1/4**)，将此图像作为输入，重复卷积和下采样操作得到更上一层的图像，反复迭代多次，形成一个金字塔形的图像数据结构，即高斯金字塔。

函数:

`cv.pyrDown()`:下采样，分辨率降低

`cv.pyrUp()`：上采样，分辨率升高

```python
img=cv.imread("D:\\Downloads\\shot.jpg")
lev1=cv.pyrDown(img)
lev1_up=cv.pyrUp(lev1)
```

一旦降低了分辨率，就会丢失信息。即使再重新上采样回去，也无法回到原来的图<img src="https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/Image_pyramid_messipyr.jpg" style="zoom:50%;" />

#### 拉普拉斯金字塔

拉普拉斯金字塔用于重建图形，也就是预测残差，对图像进行最大程度的还原，比如一幅小图像重建为一幅大图。(在高斯金字塔的下采样中，图像经过卷积和下采样操作会丢失部分高频细节信息，可以搭配拉普拉斯金字塔来上采样重建图像)

原理：拉普拉斯金字塔中的第 i 层，等于**“高斯金字塔中的第 i 层”**与**“高斯金字塔中的第 i+1 层的向上采样(由高层图像得到低层图像)结果”**之差。

在使用拉普拉斯金字塔操作中，实际上也就实现了上采样的过程

①：首先，将图像在每个方向扩大为原来的两倍，新增的行和列以0填充(0)

②：使用先前同样的内核(乘以4)与放大后的图像卷积，获得 “新增像素” 的近似值。

```python
#4.9.1代码延续
lpls=cv.subtract(img,lev1_up)
```

### 直方图

#### 直方图有关的术语

- BINS:横坐标的区间数，如BINS=256,意味着将 0~255 的灰度范围划分为 256 个区间，每个区间只包含 1 个灰度值；BINS=10时，有10个区间，每个区间包含256/10个灰度值
- DIMS:要收集参数的数量。如果只收集灰度图数据的灰度数据，那么就是1
- 范围：要收集的数据的值的范围。如[0,256]

#### 计算

`cv.calcHist()`函数用于查找直方图

> cv.calcHist(images, channels, mask, histSize, ranges[, hist[, accumulate]])
>
> images:原图像。应放在方括号中，如[img]
>
> channels:以方括号给出，它是我们要计算直方图的通道的索引。如果输入为灰度图像，则其值为[0]。对于彩色图像，您可以传递[0]，[1]或[2]分别计算蓝色，绿色或红色通道的直方图。
>
> mask:遮罩。可以用于查找图像特定区域的直方图
>
> histSize:BIN计数。需要放在方括号中，[256]
>
> ranges:数值范围。

```python
img = cv.imread('home.jpg',0)
# create a mask
mask = np.zeros(img.shape[:2], np.uint8)
mask[100:300, 100:400] = 255
masked_img = cv.bitwise_and(img,img,mask = mask)
# Calculate histogram with mask and without mask
# Check third argument for mask
hist_full = cv.calcHist([img],[0],None,[256],[0,256])
hist_mask = cv.calcHist([img],[0],mask,[256],[0,256])
plt.subplot(221), plt.imshow(img, 'gray')
plt.subplot(222), plt.imshow(mask,'gray')
plt.subplot(223), plt.imshow(masked_img, 'gray')
plt.subplot(224), plt.plot(hist_full), plt.plot(hist_mask)
plt.xlim([0,256])
plt.show()
```

查看结果。在直方图中，蓝线表示完整图像的直方图，绿线表示遮蔽区域的直方图。

![histogram_masking.jpg](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/4.10.4-histogram_masking.jpg)

### 直方图均衡

#### 定义

直方图均衡

- 直方图均衡化是图像处理领域中利用图像直方图对**对比度进行调整**的方法。这种方法通常用来增加许多图像的全局对比度，尤其是当图像的有用数据的对比度相当接近的时候。
- 为了更清楚地说明，从上图可以看出，像素似乎聚集在可用强度范围的中间。直方图均衡化所做的是*扩展*此范围。请看下图：绿色圆圈表示*像素不足*的强度值。应用均衡化后，我们将得到中间图所示的直方图。右图显示了结果图像。

![img](https://docs.opencv.ac.cn/4.11.0/Histogram_Equalization_Theory_1.jpg)

#### 直方图均衡

函数：`cv.equalizeHist()`它的输入是灰度图像，输出是我们的直方图均衡图像。

```python
img = cv.imread('wiki.jpg',0)
equ = cv.equalizeHist(img)
```

![equalization_opencv.jpg](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/4.10.7-equalization_opencv.jpg)

#### CLAHE(对比度受限的自适应直方图均衡)

上面提到的均衡化考虑了图像整体对比度，通常情况下，这并不是一个好主意，这时就需要用到**自适应直方图均衡**。

在**自适应直方图均衡**(AHE)中，图像将被分成被称为`tiles`的小块中(opencv中默认是8x8)，然后再对每一个小块分别进行直方图均衡化。

但使用AHE时**如果有噪音，它将被放大**，为了避免这种情况，我们应用了**对比度受限的自适应直方图均衡**（CLAHE），以下是CLAHE工作过程。

1. **图像分块**：将图像划分为多个8x8的Tile。
2. **为每个Tile的直方图**：为每一个小Tile计算其亮度直方图。这个直方图就是由一系列Bin组成的，每个Bin记录了该Tile内像素亮度落在某个区间的数量。
3. **裁剪直方图（Clipping the Histogram）**：这是最关键的一步！
    - 检查Tile的直方图中的**每一个Bin**。
    - **如果Bin的计数值超过了阈值（40），就把超出的部分“剪掉”**。
        - 例如，某个Bin的计数值是100，Clip Limit是40，那么我们就把它“裁剪”到40，多出的60被剪掉。
4. **重新分配**：**把从所有Bin上“剪下来”的像素计数总和，均匀地重新分配到所有的Bin上**。
    - 假设我们从各个Bin上一共剪掉了总共200个像素计数。
    - 这200个像素计数会被平均地加到所有的Bin上（比如有256个Bin，每个Bin就大约增加 `200/256 ≈ 0.78`）。
    - 之前那个被裁剪的Bin，值从40变成了 `40 + 0.78 = 40.78`。
    - 一个原本计数很低的Bin（比如是5），现在变成了 `5 + 0.78 = 5.78`。
5. **均衡化**：使用这个经过“裁剪”和“重新分配”后得到的、新的直方图，来为这个Tile计算直方图均衡变换函数。<u>均衡后，如果要消除图块边界中的伪影，请应用双线性插值。</u>

> retval = cv.createCLAHE( clipLimit=40,tileGridSize=（8,8）)
>
> clipLimit：对比度限制，默认40.0
>
> tileGridSize:块的大小，默认（8,8）

```python
img = cv.imread('tsukuba_l.png',0)
# create a CLAHE object (Arguments are optional).
clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
cl1 = clahe.apply(img)
cv.imwrite('clahe_2.jpg',cl1)
```

<img src="https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/4.10.9-clahe_2.jpg" alt="clahe_2.jpg" style="zoom: 80%;" />

### 2D直方图

之前，我们计算并绘制了一维直方图。之所以称为一维，是因为我们仅考虑一个特征，即像素的灰度强度值。但是在二维直方图中，您要考虑两个特征。通常，它用于查找颜色直方图，其中两个特征是每个像素的色相和饱和度值。

要计算2D直方图依旧使用`cv.calcHist`进行计算，我们需要将图像从BGR转换为HSV。其参数要做如下修改：

- channels = [0,1]， 因为我们需要同时处理H和S平面。
- bins = [180,256] 对于H平面为180，对于S平面为256。
- range= [0,180,0,256] 色相值介于0和180之间，饱和度介于0和256之间。

```python
img = cv.imread('home.jpg')
hsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)
hist = cv.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
```

#### 绘制2D直方图

##### 使用`cv.imshow()`

我们得到的结果是尺寸为180x256的二维数组。因此，可以使用 `cv.imshow`函数像平常一样显示它们。它将是一幅灰度图像。

##### 使用Matplotlib

我们可以使用 `matplotlib.pyplot.imshow()`函数绘制具有不同颜色图的2D直方图。它使我们对不同的像素密度有了更好的了解.

**注意** 使用此功能时，请记住，插值标记应最接近以获得更好的结果。

```python
img = cv.imread('home.jpg')
hsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)
hist = cv.calcHist( [hsv], [0, 1], None, [180, 256], [0, 180, 0, 256] )
plt.imshow(hist,interpolation = 'nearest')
plt.show()
```

下面是输入图像及其颜色直方图。X轴显示S值，Y轴显示色相。

![2dhist_matplotlib.jpg](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/4.10.10-2dhist_matplotlib.jpg)

在直方图中，您可以在H = 100和S = 200附近看到一些较高的值。它对应于天空的蓝色。同样，在H = 25和S = 100附近可以看到另一个峰值。它对应于宫殿的黄色。

### 直方图反投影

用于**图像分割**或**在图像中查找感兴趣的对象**。用什么来查找呢？用直方图。

直方图在一定程度上可以反应图像的特征，我们截取一个有固定特征的样例，比如草地，然后计算该块草地的直方图，然后用这个直方图去和整幅图像的直方图做对比，根据一定的判断条件，就能得出相似的即为草地。

<img src="https://picx.zhimg.com/v2-fedc78ead78c109c2715ce99c7180e2b_1440w.jpg" alt="img" style="zoom:67%;" />

步骤：

- 将感兴趣区域和原图转成hsv格式
- 计算感兴趣区域hsv格式的2d直方图
- 对计算出的2d直方图进行归一化
- 计算反投影

> dst=cv.calcBackProject(images, channels, hist, ranges, scale[, dst])
>
> images:输入的图像，形如[img]
>
> channels:需要统计图像的通道索引即第几个通道
>
> hist:直方图
>
> rnages:直方图中 x 轴的取值范围。
>
> scale:缩方因子，默认1

```python
#感兴趣区域：草地
roi = cv.imread('rose_red.png')
hsv = cv.cvtColor(roi,cv.COLOR_BGR2HSV)

img = cv.imread('rose.png')
img_hsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)
# calculating object histogram
roihist = cv.calcHist([hsv],[0, 1], None, [180, 256], [0, 180, 0, 256] )
# normalize histogram and apply backprojection
cv.normalize(roihist,roihist,0,255,cv.NORM_MINMAX)
dst = cv.calcBackProject([img_hsv],[0,1],roihist,[0,180,0,256],1)
```







## 轮廓

轮廓可以简单地解释为连接具有相同颜色或强度的所有连续点(沿边界)的曲线。

- 找轮廓请使用二进制图像(即二值图)，因此，在找到轮廓之前，请应用阈值或 **Canny** 边缘检测。
- 在OpenCV中，找到轮廓就像从黑色背景中找到白色物体。因此请记住，要找到的对象应该是白色，背景应该是黑色。

### 找到并绘制轮廓

> contours, hierarchy=cv.findContours(image, mode, method[, contours[, hierarchy[, offset]]])
>
> image:原图像
>
> mode:轮廓检索模式
>
> method:轮廓逼近方法
>
> 返回值：
>
> 轮廓：图像中所有轮廓的列表，列表中每一项都是数组，记录了点的坐标
>
> 层次



> image=cv.drawContours(image, contours, contourIdx, color[, thickness[, lineType[, hierarchy[, maxLevel[, offset]]]]])
>
> image:原图像(**在原图像上绘制**)
>
> contours:轮廓列表
>
> contourIdx:轮廓的索引(**-1时表示绘制所有轮廓**)
>
> color:颜色
>
> thickness:线条厚度

```python
img=cv.imread("D:\\Downloads\\shot.jpg")

#边缘检测(因为寻找轮廓要二值图)
border=cv.Canny(img,100,200)

#寻找轮廓
contours,hierarchy=cv.findContours(border,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)

#绘制所有轮廓
#cv.drawContours(img,contours,-1,(0,255,0),1)

#绘制单个轮廓，用下面这种方式好一点

#先挑出需要绘制的轮廓，再传进去
cnt=contours[3]
cv.drawContours(img,[cnt],0,(0,255,0),1)

cv.imshow('contours',img)
```

<img src="C:\Users\Administrator\Desktop\image-20250829144710613.png" alt="image-20250829144710613" style="zoom: 67%;" /><img src="C:\Users\Administrator\Desktop\image-20250829144739933.png" alt="image-20250829144739933" style="zoom:67%;" />

#### mode(检测轮廓的方法)

`cv.findContours`的第二个参数

- RETR_EXTERNAL：只检测外轮廓。忽略轮廓内部的洞。
- RETR_LIST：检测所有轮廓，但不建立继承(包含)关系。
- RETR_TREE：检测所有轮廓，并且建立所有的继承(包含)关系。
- RETR_CCOMP：检测所有轮廓，但是仅仅建立两层包含关系。

#### method轮廓逼近方法

`cv.findContours`的第三个参数

- `cv.CHAIN_APPROX_NONE `:把轮廓上所有的点存储。
- `cv.CHAIN_APPROX_SIMPLE `:压缩水平的、垂直的和斜着的部分，**只保留他们的拐点部分**

![Image](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/4.9.1-none.jpg)

### 轮廓近似

函数：`cv.approxPolyDP`

- 第一个参数：轮廓
- 第二个参数：精度(从轮廓到近似轮廓的最大距离)
- 第三个参数：指定曲线是否闭合

```python
img_color=cv.imread("D:\\Downloads\\8.png")
img=cv.imread("D:\\Downloads\\8.png",0)

#二值化
ret,thresh=cv.threshold(img,100,255,cv.THRESH_BINARY)

#寻找轮廓
contours,c=cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)
cnt=contours[0]
print(len(contours))

#轮廓近似

#精度(从轮廓到近似轮廓的最大距离)
epsilon=0.01*cv.arcLength(cnt,True)

approx=cv.approxPolyDP(cnt,epsilon,True)
#绘制轮廓近似
cv.drawContours(img_color,[approx],-1,(0,255,0),3)
cv.imshow('img_color',img_color)

cv.waitKey(0)
```

![image-20250829160823839](C:\Users\Administrator\Desktop\image-20250829160823839.png)

### 凸包

简单来说，给定二维平面上的点集，凸包就是将最外层的点连接起来构成的凸多边形，它是**能包含点集中所有点**的。

> hull=cv.convexHull(points[, hull[, clockwise[, returnPoints]]])
>
> points:输入的点集
>
> hull:输出找到的凸包
>
> clockwise:为True时，输出的凸包为顺时针方向，否则为逆时针方向
>
> returnPoints:凸包返回形式，默认值为true,返回点坐标的形式，否则返回对应点的索引

```python
img_color=cv.imread("D:\\Downloads\\7.png")
img=cv.cvtColor(img_color,cv.COLOR_BGR2GRAY)

# 去除干扰
blurred = cv.GaussianBlur(img, (5, 5), 0)
_, thresh = cv.threshold(blurred, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
kernel = np.ones((3, 3), np.uint8)
opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=2)
# 形态学膨胀获取确定的背景区域
sure_bg = cv.dilate(opening, kernel, iterations=3)

# 边缘检测（使用处理后的图像）
edge = cv.Canny(sure_bg, 150, 180)
cv.imshow('edge', edge)

#寻找轮廓
contours,c=cv.findContours(sure_bg,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)
print(len(contours))
cnt=contours[0]

#寻找轮廓的凸包
hull=cv.convexHull(cnt)

#绘制凸包
cv.drawContours(img_color,[hull],-1,(0,0,255),2)

cv.imshow('img_color',img_color)
```

<img src="C:\Users\Administrator\Desktop\image-20250829164555732.png" alt="image-20250829164555732" style="zoom:50%;" />轮廓

<img src="C:\Users\Administrator\Desktop\image-20250829164231363.png" alt="image-20250829164231363" style="zoom:50%;" />凸包

#### 检查凸度

`cv.isContourConvex()`检查曲线是否为凸多边形，返回True或False

```python
k = cv.isContourConvex(hull)
print(k)
#True
```

#### 凸度缺陷

**在寻找凸包时，我们必须传递returnPoints = False，以便寻找凸缺陷。**

如果用returnPoints = True来寻找凸包，得到以下值：[[[234 202]]，[[51 202]]，[[51 79]]，[[234 79]]]，它们是四个角矩形的点。现在，如果用returnPoints = False执行相同的操作，则会得到以下结果：[[129]，[67]，[0]，[142]]。这些是**轮廓(contours)中相应点的索引**。例如，检查第一个值：cnt [129] = [[234，202]]与第一个结果相同(对于其他结果依此类推)。

也就是说在寻找凸包`convexHull`时传递`returnPoints = False`,得到的结果是轮廓的点的索引，便于寻找凸包缺陷。

##### 定义

凸包与轮廓之间的部分称为凸缺陷。**原始图形的凸包**减去 **原始图形的轮廓**，得到的那部分就是凸包缺陷，或者说叫凹进去的部分。

如下图所示原始图形是五边形，绿框就是得到的凸包，减去它的轮廓，就是红色边框三角形部分，它就是凸包的缺陷。<img src="https://i-blog.csdnimg.cn/blog_migrate/042de492e0c2000a6320702cd102d607.png" alt="在这里插入图片描述" style="zoom: 50%;" />

##### 函数

> convexityDefects=cv.convexityDefects(contour, convexhull[, convexityDefects])
> 第一个参数：轮廓
>
> 第二个参数：凸包
>
> 返回值：数组。其中每行包含[起点，终点，最远点，到最远点的近似距离]。记住：前三个值都是参数**contour的索引**，**contour是一个三维数组**

```python
img = cv.imread('star.jpg')
img_gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
ret,thresh = cv.threshold(img_gray, 127, 255,0)
contours,hierarchy = cv.findContours(thresh,2,1)
cnt = contours[0]
hull = cv.convexHull(cnt,returnPoints = False)
defects = cv.convexityDefects(cnt,hull)
for i in range(defects.shape[0]):
    s,e,f,d = defects[i,0]
    start = tuple(cnt[s][0])#起点
    end = tuple(cnt[e][0])#终点
    far = tuple(cnt[f][0])#最远点
    cv.line(img,start,end,[0,255,0],2)
    cv.circle(img,far,5,[0,0,255],-1)
cv.imshow('img',img)
cv.waitKey(0)
cv.destroyAllWindows()
```

![errors.jpg](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/4.9.12-defects.jpg)

### 轮廓特征

#### 图像矩

矩可帮助您计算某些特征，例如物体的重心，物体的面积等

函数`cv.moments`返回轮廓的所有矩值的字典

```python
img=cv.imread("D:\\Downloads\\shot.jpg")

#边缘检测
border=cv.Canny(img,100,200)
#寻找轮廓
contours,hierarchy=cv.findContours(border,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
#计算矩
cnt=contours[0]
M=cv.moments(cnt)
print(M)
{'m00': 0.0, 'm10': 0.0, 'm01': 0.0, 'm20': 0.0, 'm11': 0.0, 'm02': 0.0, 'm30': 0.0, 'm21': 0.0, 'm12': 0.0, 'm03': 0.0, 'mu20': 0.0, 'mu11': 0.0, 'mu02': 0.0, 'mu30': 0.0, 'mu21': 0.0, 'mu12': 0.0, 'mu03': 0.0, 'nu20': 0.0, 'nu11': 0.0, 'nu02': 0.0, 'nu30': 0.0, 'nu21': 0.0, 'nu12': 0.0, 'nu03': 0.0}
```

在图像矩中，您可以提取有用的数据，例如面积，质心等

```python
#质心
cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])
#389 273
```

#### 轮廓面积

轮廓区域由函数`cv.contourArea()`或从矩`M['m00']`中给出。

```python
area=cv.contourArea(cnt)
print(area)
area=M['m00']
print(area)
#4.0
#4.0
```

#### 轮廓周长

也称弧长，函数`cv.arcLength()`,第二个参数指定形状是闭合轮廓(True)还是曲线(False)

```python
preimerter=cv.arcLength(cnt,True)
print(preimerter)
#44.14213538169861
```

#### 边界矩形

##### 外接矩形

它不考虑对象的旋转，使用函数`cv.boundingRect()`函数

```python
x,y,w,h = cv.boundingRect(cnt)
cv.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
```

##### 最小外接矩形

在这里，边界矩形是用最小面积绘制的，它考虑了**旋转**，函数`cv.minAreaRect()`。它返回一个Box2D结构，其中包含：**中心(x,y)，(宽，高)，旋转角度**。如果要绘制该矩形，就要获取到该矩形的四个角，可以通过函数`cv.boxPoints()`获得

```python
rect = cv.minAreaRect(cnt)
box = cv.boxPoints(rect)
box = np.int0(box)
cv.drawContours(img,[box],0,(0,0,255),2)
```

<img src="https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/4.9.4-boundingrect.png" alt="boundingrect" style="zoom: 67%;" />

#### 最小外圆

函数`cv.minEnclosingCircle()`,它时一个最小面积完全覆盖对象的圆圈

```python
(x,y),radius = cv.minEnclosingCircle(cnt)
center = (int(x),int(y))
radius = int(radius)
cv.circle(img,center,radius,(0,255,0),2)
```

<img src="https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/4.9.8-circumcircle.png" alt="circumcircle" style="zoom:67%;" />

#### 拟合椭圆

```python
ellipse = cv.fitEllipse(cnt)
cv.ellipse(img,ellipse,(0,255,0),2)
```

<img src="https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/4.9.9-fitellipse.png" alt="fitellipse" style="zoom:67%;" />

#### 拟合线

```python
rows,cols = img.shape[:2]
[vx,vy,x,y] = cv.fitLine(cnt, cv.DIST_L2,0,0.01,0.01)
lefty = int((-x*vy/vx) + y)
righty = int(((cols-x)*vy/vx)+y)
cv.line(img,(cols-1,righty),(0,lefty),(0,255,0),2)
```

![fitline.jpg](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/4.9.10-fitline.jpg)

#### 点与轮廓距离

函数`cv.pointPolygonTest()`,查找图像中的点与轮廓之间的最短距离。

> retval=cv.pointPolygonTest(contour, pt, measureDist)
>
> contour:轮廓
>
> pt:要检查的点的坐标
>
> measureDist:True时寻找带符号的距离。False时查找该点是在轮廓内部还是外部或轮廓上(它分别返回+ 1，-1、0)。

**注意**：如果不想查找距离，请确保第三个参数为False，因为这是一个耗时的过程。因此，将其设置为False可使速度提高2-3倍。

#### 匹配形状

`cv.matchShapes()`**使我们能够比较两个形状或两个轮廓，并返回显示相似性的度量。结果越低，匹配越好。**

```python
img1 = cv.imread('star.jpg',0)
img2 = cv.imread('star2.jpg',0)
ret, thresh = cv.threshold(img1, 127, 255,0)
ret, thresh2 = cv.threshold(img2, 127, 255,0)
contours,hierarchy = cv.findContours(thresh,2,1)
cnt1 = contours[0]
contours,hierarchy = cv.findContours(thresh2,2,1)
cnt2 = contours[0]
ret = cv.matchShapes(cnt1,cnt2,1,0.0)
print( ret )
```

## 傅里叶变换

傅立叶变换用于**分析各种滤波器的频率特性**。对于图像，使用 2D离散傅里叶变换（DFT） **查找频域**。一种称为快速傅里叶变换(FFT)的快速算法用于DFT计算，

### 理论基础

傅里叶变换将图像分解为正弦分量和余弦分量两部分，即将图像**从空间域转换到频域**。

对图像进行傅里叶变换后，会得到图像的**高频和低频信息**。低频信息对应图像内**变化缓慢的灰度分量**。高频信息对应图像内**变化越来越快的灰度分量**，是由灰度的尖锐过渡造成的。

傅里叶变换的目的，就是为了将图像从空间域转换到频域，我们可以在频域内实现对图像内特定对象的处理，然后再对经过处理的频域图像进行逆傅里叶变换得到空间域图像。

### 傅里叶变换函数

> cv.dft(src[, dst[, flags[, nonzeroRows]]]) → dst
>
> flags:转换标识符
>
> cv.DFT_INVERSE：用一维或二维逆变换取代默认的正向变换
> cv.DFT_SCALE：缩放比例标识，根据元素数量求出缩放结果，常与DFT_INVERSE搭配使用
> cv.DFT_ROWS: 对输入矩阵的每行进行正向或反向的傅里叶变换，常用于三维或高维变换等复杂操作
> cv.DFT_COMPLEX_OUTPUT：对一维或二维实数数组进行正向变换，默认方法，结果是**由 2个通道表示的复数阵列，第一通道是实数部分，第二通道是虚数部分**（一般使用这个标识符）
> cv.DFT_REAL_OUTPUT：对一维或二维复数数组进行逆变换，结果通常是一个尺寸相同的复数矩阵

**注意事项：**

- 输入图像需要是**float32**格式，如果不是必须进行转换
- 不能直接用于显示图像。可以使用cv.magnitude()函数将结果变换到灰度[0,255]
- idft(src, dst, flags) 等价于 dft(src, dst, flags=DFT_INVERSE)



#### dft 性能优化

在一定阵列尺寸下，DFT性能较好。当阵列大小为2的幂时，它是最快的。大小为2、3和5的乘积的数组也得到了有效处理。

对于行数和列数都可以分解为 2^p^ ∗ 3 ^q^ ∗ 5 ^r^ 的矩阵的计算性能好。

`cv.getOptimalDFTSize()`可以找到最优DFT尺寸。然后我们根据尺寸来填充图像以获得更好的性能。

#### 中心化

经过函数cv2.dft()的变换后，得到了原始图像的频谱信息。此时，**零频率分量（DC分量）并不在中心位置**，为了处理方便需要**将其移至中心位置**，可以用函数numpy.fft.fftshift()实现。

<u>**把零频分量移到中心位置后，零频分量周围就是低频分量了**</u>。

- 经过`np.fft.fftshift(dft)`处理后，傅里叶变换的结果被 "中心化"
- 图像的**低频成分**（对应图像中变化缓慢的区域，如平滑背景）集中在频域的**中心区域**
- 图像的**高频成分**（对应图像中突变的部分，如边缘、纹理、噪声）分布在频域的**边缘区域**

```python
img=cv.imread('E:\\Downloads\\Edge Downloads\\9.png',0)
rows,cols=img.shape
#获取最佳尺寸
r=cv.getOptimalDFTSize(rows)
c=cv.getOptimalDFTSize(cols)

#填充图像
img_resize=np.zeros((r,c))
img_resize[:rows,:cols]=img
img=img_resize

#傅里叶变换
dft=cv.dft(np.float32(img),flags=cv.DFT_COMPLEX_OUTPUT)

#零频分量在左上角，把它换到中心
dft_shift=np.fft.fftshift(dft)

#将结果转为可显示的
dft_show=20*np.log(cv.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))
#归一化
dft_show= cv.normalize(dft_show, None, 0, 255, cv.NORM_MINMAX, dtype=cv.CV_8U)

cv.imshow('show',dft_show)
```

![fft1.jpg](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/4.11.1-fft1.jpg)

#### `imshow`的注意事项

这里要说明的是上面代码的归一化操作，因为opncv的``cv.imshow()` 函数期望的图像数据类型是 `cv.CV_8U`,**直接显示浮点图像会导致：**

- 当**显示浮点型数组**时，OpenCV 会将值视为 0.0~1.0 范围（而非 0-255）

- 负值和大于1.0的值被截断或显示异常,如大于 1.0 的值在显示时都会被当作 1.0（白色）处理
- 图像看起来几乎全黑或全白，无法正确显示梯度信息

### 图像处理

我们在上面把零频率分量移至频谱图像的中心位置，所以**频率图中心位置附近为低频**

当我们对频率图像进行处理时，我们可以选择生成一张与频率图相同尺寸的滤波

如果是要实现低通滤波，那么我们将**中间区域(LF区)值设为1**，其他设为0，然后与频率矩阵**直接乘**

```python
#接上面的代码


#低通滤波器，与图像的尺寸相同(尺寸是resize过的)
# 中心区域(对应频率图的低频部分)设为1，即保留低频，去除高频
mask=np.zeros((r,c,2),np.uint8)
rows_mid,cols_mid=rows//2,cols//2
mask[rows_mid-30:rows_mid+30,cols_mid-30:cols_mid+30]=1
#应用滤波器，逐元素相乘
dft_shift_masked=dft_shift*mask
```

#### 频域和空域的滤波器区别

**频域滤波 vs 空域滤波**

- **频域中的滤波器**：
    - 它**必须**与**频域图像尺寸相同**（因为要和频域图像逐元素相乘）
    - 作用是直接过滤频域中的频率
- **空域中的滤波器**：
    - 它可以是一个小型卷积核（kernel）
    - 通过与原始图像做卷积运算实现平滑（卷积操作等效于频域中的乘法）

**为什么会有这种差异？**

- **频域滤波**的核心是 "保留哪些频率"，因此需要与频域图像（和原图像同尺寸）一一对应
- **空域滤波**的核心是 "如何混合**相邻像素**"，用小卷积核滑动计算即可，无需与图像同尺寸

两种方法可以达到类似的平滑效果，但频域方法更灵活（可设计复杂的频率响应），而空域方法更高效（适合实时处理）。

### 逆傅里叶变换

> cv.idft(src[, dst[, flags[, nonzeroRows]]]) → dst

```python
#接上面的代码


#将零频率分量恢复到原来的位置
dft_ishift=np.fft.ifftshift(dft_shift_masked)
#逆傅里叶
img_back=cv.idft(dft_ishift)
img_back=cv.magnitude(img_back[:,:,0],img_back[:,:,1])
#归一化
img_show=cv.normalize(img_back,None,0,255,cv.NORM_MINMAX, dtype=cv.CV_8U)
cv.imshow('img_show',img_show)
```

**注意事项：**

1. 我们将零频率分量移至频谱图像的中心位置，那么在进行逆傅里叶变换前，要使用函数numpy.fft.ifftshift()**将零频率分量恢复到原来位置**。
2. 在进行逆傅里叶变换后，得到的值仍旧是复数阵列，需要使用函数`cv2.magnitude()`进行计算。
3. 要`imshow`经过`magnitude()`计算后的图像，需要先归一化

![fft4.jpg](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/4.11.3-fft4.jpg)

#### 振铃效应

使用矩形滤波可能效果并不好，可能出现类似波纹的**振铃效果**(如下图)，**用高斯滤波会好一些**（在频域中使用高斯滤波要使用和频域图尺寸一致的滤波）

<img src="https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/4.11.2-fft2.jpg" alt="fft2.jpg" style="zoom:150%;" />

### 通过傅里叶变换判断高通低通

```python
# simple averaging filter without scaling parameter
mean_filter = np.ones((3,3))
# creating a gaussian filter
x = cv.getGaussianKernel(5,10)
gaussian = x*x.T
# different edge detecting filters
# scharr in x-direction
scharr = np.array([[-3, 0, 3],
                   [-10,0,10],
                   [-3, 0, 3]])
# sobel in x direction
sobel_x= np.array([[-1, 0, 1],
                   [-2, 0, 2],
                   [-1, 0, 1]])
# sobel in y direction
sobel_y= np.array([[-1,-2,-1],
                   [0, 0, 0],
                   [1, 2, 1]])
# laplacian
laplacian=np.array([[0, 1, 0],
                    [1,-4, 1],
                    [0, 1, 0]])
filters = [mean_filter, gaussian, laplacian, sobel_x, sobel_y, scharr]
filter_name = ['mean_filter', 'gaussian','laplacian', 'sobel_x', \
                'sobel_y', 'scharr_x']
fft_filters = [np.fft.fft2(x) for x in filters]
fft_shift = [np.fft.fftshift(y) for y in fft_filters]
mag_spectrum = [np.log(np.abs(z)+1) for z in fft_shift]
for i in xrange(6):
    plt.subplot(2,3,i+1),plt.imshow(mag_spectrum[i],cmap = 'gray')
    plt.title(filter_name[i]), plt.xticks([]), plt.yticks([])
plt.show()
```

![fft5.jpg](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/4.11.5-fft5.jpg)

从图像中，您可以看到每个内核阻止的频率区域以及它经过的区域。从这些信息中，我们可以说出为什么每个内核都是HPF或LPF

## 模版匹配

除了轮廓滤波处理之外，模板匹配可以说是对象检测的最简单形式之一：

- 模板匹配实现简单，只需要2-3行代码
- 模板匹配计算效率高
- 它不需要执行阈值化、边缘检测等操作来生成二值化图像（而轮廓检测处理需要）

当然，模板匹配不是完美的。尽管它有很多优点，但是如果输入图像中存在变化的因素，包括旋转、缩放、视角变化等，模板匹配很容易就会失效。

模板匹配是一种在较大图像中搜索和查找模板图像位置的方法。它在输入图像上滑动模板图像（如在 2D 卷积中），并比较模板图像下的模板和输入图像。它返回一个**灰度图像**，其中每个像素表示**该像素的邻域与模板匹配的程度**。

如果输入图像的大小（WxH）且模板图像的大小（wxh），则输出图像的大小为（W-w + 1，H-h + 1）。得到结果后，可以使用`cv.minMaxLoc()`函数查找结果中**最小值、最大值、最小值位置、最大值位置**。我们可以将**最大值/最小值位置**作为匹配到的区域的**左上角**，取**模版的(w,h)**作为矩形的宽度和高度，得到的矩形就是模版区域。

### 函数

> cv2.matchTemplate(image, templ, method, result=None, mask=None)
>
> *image*:待匹配图像
>
> templ:模版
>
> *method*:
>
> - **TM_SQDIFF**, **TM_CCORR**, **TM_CCOEFF**, **TM_SQDIFF_NORMED**, **TM_CCORR_NORMED**, **TM_CCOEFF_NORMED**
> - 如果使用 cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED那么**最小值坐标作为左上角**，否则**最大值坐标作为左上角**
>
> *result*：可选参数，用于存储每个位置的匹配结果。
>
> *mask*：可选参数，用于定义模板图像中的感兴趣区域。

```python
img = cv.imread('messi5.jpg',0)
img2 = img.copy()
template = cv.imread('template.jpg',0)
w, h = template.shape[::-1]
# All the 6 methods for comparison in a list
methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
            'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
for meth in methods:
    img = img2.copy()
    method = eval(meth)
    # Apply template Matching
    res = cv.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv.rectangle(img,top_left, bottom_right, 255, 2)
    plt.subplot(121),plt.imshow(res,cmap = 'gray')
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(img,cmap = 'gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle(meth)
    plt.show()
```

`cv.TM_CCOEFF`

<img src="https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/Image_match_template_ccoeff_1.jpg" alt="template_ccoeff_1.jpg" style="zoom: 80%;" />

其余省略...

### 多对象匹配

上面我们搜索的图像仅在图中出现一次，如果对象在图像中出现了多次，`cv.minMaxLoc`将不会提供所有匹配点，**这时我们可以使用阈值。**

```python
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
img_rgb = cv.imread('mario.png')
img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
template = cv.imread('mario_coin.png',0)
w, h = template.shape[::-1]
res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
cv.imshow('res.png',img_rgb)
```

![res_mario.jpg](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/Image_match_res_mario.jpg)



## 霍夫变换

### 霍夫线变换

原理：

[霍夫变换直线检测（Line Detection）原理及示例_霍夫变换直线检测原理-CSDN博客](https://blog.csdn.net/leonardohaig/article/details/87907462)

#### 函数

`cv.HoughLines()`函数

> cv.HoughLines(image, rho, theta, threshold[, lines[, srn[, stn[, min_theta[, max_theta]]]]]) -> lines
>
> image:**二进制图像**，所以要先对原图使用阈值或边缘检测
>
> *rho*:ρ的精度。
>
> *theta*:θ的精度。
>
> *threshold*:阈值，得票数高于该值的线才被认为是线，由于投票数取决于线上的点数，所以它代表了应该被检测到的线的最小点数。
>
> 返回值：
>
> *lines*:math:(rho,theta)的数组，ρ以像素为单位，θ以弧度为单位。

```python
img = cv.imread(cv.samples.findFile('sudoku.png'))
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
edges = cv.Canny(gray,50,150,apertureSize = 3)
lines = cv.HoughLines(edges,1,np.pi/180,200)
for line in lines:
    rho,theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    cv.line(img,(x1,y1),(x2,y2),(0,0,255),2)
cv.imwrite('houghlines3.jpg',img)
```

<img src="https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/Image_hough_houghlines3.jpg" alt="houghlines3.jpg" style="zoom:67%;" />

#### 优缺点

优点：Hough直线检测的优点是抗干扰能力强，对图像中直线的殘缺部分、噪声以及其它共存的非直线结构不敏感，能容忍特征边界描述中的间隙，并且相对不受图像噪声的影响

缺点：Hough变换算法的特点导致其时间复杂度和空间复杂度都很高，并且在检测过程中只能确定直线方向，丢失了线段的长度信息(返回值是ρ和θ，表示了一条直线，但是没有长度)。由于霍夫检测过程中进行了离散化，因此检测精度受参数离散间隔制约

### 概率霍夫变换

在霍夫变换中，即使对于只有两个参数的直线，也可以看到它需要大量的计算。概率霍夫变换是对我们看到的霍夫变换的一种优化。它不会考虑所有点。相反，它只考虑足以进行直线检测的随机点子集。我们只需要降低阈值即可。

#### 函数

> cv.HoughLinesP(image, rho, theta,thresh[, lines[, minLineLength[, maxLineGap]]]) ->lines
>
> *maxLineLength*:最小线段长度。短于此长度的线段将被丢弃。
>
> *maxLineGap*:线段之间的最大间隙，以便将(在同一条直线上的)线段视为同一条。
>
> 返回值：
>
> lines:比较好的一点是，它直接返回**直线的两个端点**

```python
img = cv.imread(cv.samples.findFile('sudoku.png'))
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
edges = cv.Canny(gray,50,150,apertureSize = 3)
lines = cv.HoughLinesP(edges,1,np.pi/180,100,minLineLength=100,maxLineGap=10)
for line in lines:
    x1,y1,x2,y2 = line[0]
    cv.line(img,(x1,y1),(x2,y2),(0,255,0),2)
cv.imwrite('houghlines5.jpg',img)
```

<img src="https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/Image_hough_houghlines5.jpg" alt="houghlines5.jpg" style="zoom:67%;" />

### 霍夫圆变换

opencv使用"霍夫梯度法"，它使用边缘的梯度信息。

#### 函数

> cv.HoughCircles(image, method, dp, minDist[, circles[, param1[, param2[, minRadius[, maxRadius]]]]]) ->圆圈
>
> *image*:输入图像，即源图像，8位单通道图像,即**灰度图**
>
> method：定义检测图像中圆的方法。可用的方法有HOUGH_GRADIENT和HOUGH_GRADIENT_ALT
>
> dp：图像像素分辨率与参数空间分辨率的比值（官方文档上写的是图像分辨率与累加器分辨率的比值，它把参数空间认为是一个累加器，毕竟里面存储的都是经过的像素点的数量），dp=1，则参数空间与图像像素空间（分辨率）一样大，dp=2，参数空间的分辨率只有像素空间的一半大；#通过设置dp可以减少计算量
>
> minDist：检测到的圆中心（x,y）坐标之间的最小距离。如果minDist太小，则会保留大部分圆心相近的圆。如果minDist太大，则会将圆心相近的圆进行合并（若两圆心距离 < minDist，则认为是同一个圆）。
>
> param1：canny 边缘检测的高阈值，低阈值被自动置为高阈值的一半，默认为 100；
>
> param1：canny 边缘检测的高阈值，低阈值被自动置为高阈值的一半，默认为 100；
>
> minRadius：半径的最小大小（以像素为单位）默认为 0；
>
> maxRadius：半径的最大大小（以像素为单位）默认为 0。
>
> 返回值：
>
> circles:一个三维数组，如[[[x1, y1, r1], [x2, y2, r2], ..., [xn, yn, rn]]]，**最内层维度的格式为x,y,r**，数值类型是**浮点数**

```python
img = cv.imread('opencv-logo-white.png',0)
img = cv.medianBlur(img,5)
cimg = cv.cvtColor(img,cv.COLOR_GRAY2BGR)
circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT,1,20
             ,param1=50,param2=30,minRadius=0,maxRadius=0)
#结果类型是浮点数，四舍五入一下
circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
cv.imshow('detected circles',cimg)
cv.waitKey(0)
```

![houghcircles2.jpg](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/Image_hough_houghcircles2.jpg)

## 基于分水岭算法的图像分割

任何**灰度图像**都可以看作是一个地形表面，其中**高强度表示山峰，低强度表示山谷**。你开始用不同颜色的水(标签)填充每个孤立的山谷(局部最小值)。随着水位的上升，根据附近的山峰(坡度)，来自不同山谷的水明显会开始合并，颜色也不同。为了避免这种情况，你要在水融合的地方**建造屏障**。你继续填满水，建造障碍，直到所有的山峰都在水下。然后你**创建的屏障将返回你的分割结果**。这就是Watershed背后的“思想”。

> ​    但是这种方法会由于图像中的**噪声或其他不规则性而产生过度分割的结果**。因此OpenCV实现了一个基于标记的分水岭算法，你可以指定哪些是要合并的山谷点，哪些不是。这是一个交互式的图像分割。

### 原理

我们所做的是：给我们知道的对象赋予不同的标签。用一种颜色(或强度)标记我们确定为**前景**或对象的区域，用另一种颜色标记我们确定为**背景**或非对象的区域，最后用0标**记我们不确定的区域**，这是我们的标记。然后应用分水岭算法。然后我们的标记将使用我们给出的标签进行更新，**对象的边界值将为-1**。

**靠近对象中心的区域是前景，而离对象中心很远的区域是背景，剩下的区域是不确定区域。**

### 分割过程

1. 图像二值化
2. 开运算去噪
3. 确定可靠背景(膨胀)(得到背景/最大连通域)
4. 确定可靠前景(距离变换)(分离)(得到种子/前景)
5. 找到未知区域(可靠背景-可靠前景)
6. 标记最大连通域
7. 使用分水岭算法(合并种子和不确定区域、标记边界为-1)

### 函数



### 代码

<img src="https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/Image_watershed_coins.jpg" alt="原始图片" style="zoom:67%;" />

#### 二值化

```python
img=cv.imread("D:\\Downloads\\coins.jpg")
gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
#otsu二值化
ret,binary=cv.threshold(gray,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
```

<img src="https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/Image_watershed_thresh.jpg" alt="Image_watershed_thresh" style="zoom: 80%;" />

#### 开运算去噪

```python
#开运算去噪
opening=cv.morphologyEx(binary,cv.MORPH_OPEN,(3,3),iterations=2)
```

<img src="https://i-blog.csdnimg.cn/blog_migrate/75df01624c7207198774b5abf4b39b5f.png" alt="img" style="zoom:67%;" />

#### 膨胀确定背景区域

膨胀之后，对象扩大，背景减小，此时**对象>原对象**，**背景<原背景**，所以此时的背景**一定是可靠背景**

```python
sure_bg=cv.dilate(opening,(3,3),iterations=3)
```

#### 确定前景区域(得到种子)

**可使用的方法：**

1. 腐蚀：当图像中各个子图(可以理解为对象)**没有连接**时，可以使用**腐蚀**来确定前景对象
2. 距离变换：如果图像内子图**连接在一起**，就很难确定前景对象了，此时可以使用**距离变换函数**

##### 距离变换函数

距离变换函数 cv2.distanceTransform()计算**二值图像**内**任意点到<u>最近</u>背景点**的距离，即计算二值图像中**所有像素点距离其最近的值为 0 的像素点的距离**。当然，如果像素点本身的值为 0，则这个距离也为 0。

距离变换函数 cv2.distanceTransform()的计算结果反映了各个像素与背景（值为0的像素点）的距离关系。

- 如果前景对象的中心（质心）距离值为 0 的像素点距离较远，会得到一个较大的值。
- 如果前景对象的边缘距离值为 0 的像素点较近，会得到一个较小的值。

如果对上述计算结果进行**阈值化**，就可以得到图像内子图的中心、骨架等信息。距离变换函数 cv2.distanceTransform()可以用于计算对象的中心，还能细化轮廓、获取图像前景等，有多种功能。

> `dst=cv2.distanceTransform(src, distanceType, maskSize[, dstType]])`
>
> src ：是 8 位单通道的二值图像。
>
> distanceType 为距离类型参数
>
> ![img](https://img2024.cnblogs.com/blog/3383332/202404/3383332-20240430171336875-316649875.png)
>
> ![img](https://img2024.cnblogs.com/blog/3383332/202404/3383332-20240430171352507-536429681.png)
>
> maskSize 为掩模的尺寸，其可能的值如表所示。需要注意，当 distanceType =cv2.DIST_L1 或 cv2.DIST_C 时，maskSize 强制为 3（因为设置为 3 和设置为 5 及更大值没有什么区别）。![img](https://img2024.cnblogs.com/blog/3383332/202404/3383332-20240430171425089-718013911.png)
>
> dstType 为目标图像的类型，默认值为 CV_32F。
>
> 返回值：
>
> dst 表示计算得到的目标图像，可以是 **8 位或 32 位浮点数**，尺寸和 src 相同,**它的每个像素点的值是该像素到最近背景的距离**，可以大概理解成一张灰度图。



```python
#计算像素到零像素的最短距离
dist_transform=cv.distanceTransform(opening,cv.DIST_L2,5)
#二值化确定前景
ret,sure_fg=cv.threshold(dist_transform,0.7*dist_transform.max(),255,cv.THRESH_BINARY)
#格式转换
sure_fg=np.uint8(sure_fg)
cv.imshow('sure_fg',sure_fg)
```

<img src="https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/Image_watershed_dt.jpg" alt="Image_watershed_dt" style="zoom: 80%;" />

#### 找到未知区域(确定背景-确定前景)

```python
#不确定区域
unknown=cv.subtract(sure_bg,sure_fg)
```

![img](https://i-blog.csdnimg.cn/blog_migrate/cc9138f00220667160ed21f38715f8f5.png)

#### 根据种子标记最大连通域

```python
#根据种子（上面中间的图）标记最大连通域，
ret,markers=cv.connectedComponents(sure_fg)
markers=markers+1
markers[unknown==255]=0
```

1. <u>**分水岭算法的标记规范：0 代表待分割的未知区域，正数代表已确定的不同区域**</u>
2. `cv.connectedComponents(sure_fg)` 返回的标记图`markers`中，**0是背景，种子从1开始递增**
3. 但是我们需要将让`0`表示**未知区域**,所以使用**`markers = markers + 1`**，让背景从0变成1，前景目标编号也相应递增
4. 然后我们使用`markers[unknown==255]=0`让**未知区域标记为0**

```python
#显示各区域（连通域/背景、不确定区域、种子/前景）
def Show_Markers():
    mark = img.copy()
    mark[markers == 1] = (255, 0, 0)    #连通域/背景（蓝）
    mark[markers == 0] = (0, 255, 0)    #不确定区域（绿）
    mark[markers > 1] = (0, 0, 255)     #前景/种子（红）
    cv.imshow('Markers', mark)
```

![img](https://i-blog.csdnimg.cn/blog_migrate/1fa3e0e31af1aea59b6e5016403e4f5f.png)



#### 使用分水岭算法

```python
markers=cv.watershed(img,markers)
```

*使用分水岭算法，边界标记为-1*

```python
#涂色并显示（边界(markers==-1)涂色）
    dst = img.copy()
    dst[markers == -1] = [0, 0, 255]                #边界(-1)涂色
    cv.imshow('dst', dst)
```

![img](https://i-blog.csdnimg.cn/blog_migrate/6ce70ad22813993e471f7f9b9d896b71.png)



## 基于grabcut算法的交互式前景提取

[GrabCut](https://so.csdn.net/so/search?q=GrabCut&spm=1001.2101.3001.7020) 是一种基于图像分割的半监督算法，它在图像分割中通过将前景和背景建模为图像的高斯混合模型（GMM），以此来实现高效且准确的图像分割。GrabCut 结合了 **图像边缘信息** 和 **用户输入的前景/背景框**，可以快速分割出图像中的目标区域。

### 原理

1. 用户在图像上画出**前景矩形框**（**该矩形需要完全框住所有的前景区域**）
2. 算法通过 高斯混合模型（GMM） 对前景和背景进行建模，并初始化。
3. 算法通过 图割 迭代优化，逐步细化前景和背景的分割。
4. 最终得到 前景和背景的分割结果。

但在某些情况下，分割的不是那么理想，比如说，它可能把一些前景区域标成了背景，或者反过来。如果发生了这样的情况，用户需要进行修正。只要在有错误结果的地方“划一下”就行了。“划一下”基本的意思是说，*"这个区域应该是前景，你标记它为背景，在下一次迭代中更正它。

### 函数

> cv2.grabCut(image, mask, rect, bgdModel, fgdModel, iterCount, mode)
>
> 参数	说明
> image      输入图像（必须是 3 通道的图像）。
> mask       掩码图像，如果使用掩码进行初始化，那么mask保存初始化掩码信息；在执行分割的时候，也可以将用户交互所设定的前景与背景保存到mask中，然后再传入grabCut函数；在处理结束之后，mask中会保存结果。mask只能取以下四种值：(若无标记GCD_BGD或GCD_FGD，则结果只有GCD_PR_BGD或GCD_PR_FGD；)
>
> - GCD_BGD（=0），背景；
>
> - GCD_FGD（=1），前景；
> - GCD_PR_BGD（=2），可能的背景；
> - GCD_PR_FGD（=3），可能的前景。
>
>
> rect        用户指定的矩形框，(x, y, width, height)，包含图像的前景区域。
> bgdModel    背景模型,如果为None，函数内部会自动创建一个bgdModel,必须是**单通道浮点型图像**，**且行数只能为1，列数只能为13x5**；。
> fgdModel    前景模型，如果为None，函数内部会自动创建一个fgdModel,必须是**单通道浮点型图像**，**且行数只能为1，列数只能为13x5**
> iterCount   迭代次数，表示算法进行优化的次数。
> mode	工作模式，cv2.GC_INIT_WITH_RECT 或 cv2.GC_INIT_WITH_MASK。

```python
# 1. 读取图像
image = cv2.imread('D:\\resource\\filter\\web.png')
mask = np.zeros(image.shape[:2], np.uint8)  # 创建掩码
bgd_model = np.zeros((1, 65), np.float64)  # 背景模型
fgd_model = np.zeros((1, 65), np.float64)  # 前景模型
 
# 2. 设定用户提供的矩形框 (x, y, width, height)
rect = (220, 20, 200, 150)
 
# 3. 执行 GrabCut 算法
cv2.grabCut(image, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
 
# 4. 更新掩码：前景=1，背景=0，不确定区域=2
mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
 
# 5. 提取前景
result = image * mask2[:, :, np.newaxis]
 
# 6. 显示结果
cv2.imshow('GrabCut Result', result)
cv2.waitKey(0)

```

<img src="https://i-blog.csdnimg.cn/direct/5a0ffd8c694a41e382e6d7ec77b543b1.png" alt="img" style="zoom: 50%;" />



<img src="https://i-blog.csdnimg.cn/direct/bbe1e964e4794720b453d1d91a64d92e.png" alt="img" style="zoom:50%;" />







