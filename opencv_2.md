# opencv

对于python的opencv来说，灰度图是二维数组，彩色是三维数组？

掩码的维度和图像维度，尺寸一致，但是掩码一般是单通道的





















## 特征检测和描述

### 定义

![img](https://docs.opencv.ac.cn/4.11.0/feature_building.jpg)

图像非常简单。在图像顶部，给出了六个小的图像块。问题是找到这些块在原始图像中的确切位置。你能找到多少个正确的结果？

A和B是平坦的表面，它们分布在一个很大的区域内。很难找到这些图像块的确切位置。

C和D要简单得多。它们是建筑物的边缘。你可以找到一个近似位置，但确切位置仍然很难。这是因为沿边缘的图案处处相同。然而，在边缘处，它是不一样的。因此，与平坦区域相比，边缘是更好的特征，但还不够好（在拼图游戏中，它对于比较边缘的连续性是好的）。

最后，E和F是建筑物的一些角点。它们很容易找到。因为在角点处，无论你移动这个图像块到哪里，它看起来都不同。所以它们可以被认为是良好的特征。所以现在我们转向更简单的（和广泛使用的图像）以便更好地理解。

![img](https://docs.opencv.ac.cn/4.11.0/feature_simple.png)

就像上面一样，蓝色图像块是平坦区域，难以找到和跟踪。无论你将蓝色图像块移动到哪里，它看起来都一样。黑色图像块有一个边缘。如果你在垂直方向（即沿梯度）移动它，它就会改变。沿着边缘（平行于边缘）移动，它看起来一样。对于红色图像块，它是一个角点。无论你将图像块移动到哪里，它看起来都不同，这意味着它是唯一的。因此，基本上，角点被认为是图像中的良好特征。

因此，寻找这些图像特征被称为**特征检测**。

我们在图像中找到了特征。一旦你找到了它，你应该能够在其他图像中找到相同的特征。们用我们自己的话来解释它，例如“上部是蓝天，下部是建筑物的一部分，建筑物上有玻璃等等”，同样，计算机也应该描述特征周围的区域，以便它可以在其他图像中找到它。这种所谓的描述被称为**特征描述**。

#### 角点的特征

角点还没有明确的数学定义，但普遍具有以下特征：

1. 局部小窗口沿各方向移动，窗口内的像素均产生明显变化的点。（比如有一个窗口，窗口中是蓝天，它的移动一般变化不大甚至没有，而如果是一个屋檐，窗口的移动会导致窗口内的像素产生明显变化）
2. 图像局部曲率(梯度)突变的点。
3. 对于同一场景，即使视角发生变化，其角点通常具备某些稳定不变性质的特征

### Harris角点检测

> **用于计算角点，不描述角点**

#### 函数

> cv.cornerHarris(src, blockSize, ksize, k[, dst[, borderType]]) ->dst
>
> - src - 输入**灰度图像**，**float32类型**
> - blockSize - 用于角点检测的**邻域大小**
> - ksize - 用于计算梯度图的Sobel算子的尺寸
> - k - 用于计算角点响应函数的参数k，取值范围常在0.04~0.06之间
> - dst-用于存储 Harris 计算后的值。它的类型为 CV_32FC1，尺寸与 src 相同

```python
filename = 'chessboard.png'
img = cv.imread(filename)
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
 
gray = np.float32(gray)
dst = cv.cornerHarris(gray,2,3,0.04)
 
#膨胀图像来标记角点
dst = cv.dilate(dst,None)
 
# 阈值用于最佳值，它可能因图像而异。
img[dst>0.01*dst.max()]=[0,0,255]
 
cv.imshow('dst',img)
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e224b8b80f944aed86402102dac65174.png#pic_center)

#### 返回值数值解释

假设输入图像`src`是3x3的float32图像：

> [[10.0, 20.0, 30.0],
>  [40.0, 50.0, 60.0],
>  [70.0, 80.0, 90.0]]

经过`cv.cornerHarris(src,2,3,0.04)`计算后，会得到类似的3x3矩阵：

> [[ -5.2,   3.8,  -2.1],
>  [ 12.5,  28.3,   9.7],
>  [ -1.3,   4.2,  -3.6]]

数值含义：

- **正值越大，表示该位置越可能是角点**
- 负值通常表示边缘或非角点区域
- 在实际图像中，**角点区域会出现明显的峰值**（如示例中的 28.3）



### 亚像素精确角点

有时，您可能需要以最大精度查找角点。OpenCV 提供了一个函数 **[cv.cornerSubPix()](https://docs.opencv.ac.cn/4.11.0/dd/d1a/group__imgproc__feature.html#ga354e0d7c86d0d9da75de9b9701a9a87e)**，它可以进一步细化检测到的角点，达到亚像素精度。

#### 函数

> cv.cornerSubPix(image, corners, winSize, zeroZone, criteria) ->corners
>
> | image    | 输入单通道，8 位或浮点图像。                                 |
> | -------- | ------------------------------------------------------------ |
> | corners  | 输入**角点的初始坐标**和**提供的精细输出坐标**。             |
> | winSize  | 搜索窗口边长的一半。例如，如果 winSize=[Size(5,5)](https://docs.opencv.ac.cn/4.11.0/dc/d84/group__core__basic.html#ga346f563897249351a34549137c8532a0)，则使用 (5x2+1) × (5x2+1) = 11 × 11 的搜索窗口。 |
> | zeroZone | 搜索区域中间的无效区域大小的一半，在此区域上不会进行以下公式中的求和运算。有时用于避免自相关矩阵可能的奇异性。(-1,-1) 值表示没有这样的尺寸。 |
> | criteria | 角点细化迭代过程终止的条件。换句话说，角点角度的细化过程要么在满足一组条件后结束（使用 CV_TERMCRIT_ITER 或 CV_TERMCRIT_EPS 或两者）。 |
>
> 输出：
>
> corners:存储的是经过亚像素级精炼后的角点坐标。这些坐标是浮点数





##### TermCriteria

`TermCriteria`是一种特殊的结构，用于指定算法的**终止条件**。这在许多需要迭代计算的算法中非常有用，如优化问题、梯度下降、角点检测的亚像素精度细化等。使用`TermCriteria`可以确保算法不会无限期地运行下去，而是在满足特定条件时停止，这些条件包括：

- 迭代次数（CV_TERMCRIT_ITER）：算法运行的迭代次数达到用户指定的迭代次数时终止。

- 误差精度（CV_TERMCRIT_EPS）：当连续迭代的解之间的差异小于用户指定的误差阈值时终止。

```python
// 只根据迭代次数终止
criteria = cv::TermCriteria(cv::TermCriteria::MAX_ITER, 100, 0.0);
// 只根据误差精度终止
criteria = cv::TermCriteria(cv::TermCriteria::EPS, 30, 0.01);
// 同时根据迭代次数和误差精度终止
criteria = cv::TermCriteria(cv::TermCriteria::MAX_ITER + cv::TermCriteria::EPS, 100, 0.01);

```

- `cv::TermCriteria::MAX_ITER`表示使用迭代次数作为终止条件。
- `cv::TermCriteria::EPS`表示使用误差精度作为终止条件。
- 第三个参数`100`和`30`分别是迭代次数和最大迭代次数。
- 第四个参数`0.01`是误差精度阈值。

#### 示例

我们首先需要找到 Harris 角点。然后，我们将这些角点的质心（角点处可能有一堆像素，我们取它们的质心）传递给函数以对其进行细化。

```python
filename = 'chessboard2.jpg'
img = cv.imread(filename)
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
 
# 查找 Harris 角点
gray = np.float32(gray)
dst = cv.cornerHarris(gray,2,3,0.04)
dst = cv.dilate(dst,None)
ret, dst = cv.threshold(dst,0.01*dst.max(),255,0)
dst = np.uint8(dst)
 
# 查找质心
ret, labels, stats, centroids = cv.connectedComponentsWithStats(dst)
 
# 定义停止和细化角点的标准
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.001)
corners = cv.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)
 
# 现在绘制它们
res = np.hstack((centroids,corners))
res = np.int0(res)
img[res[:,1],res[:,0]]=[0,0,255]
img[res[:,3],res[:,2]] = [0,255,0]
```

Harris 角点用红色像素标记，细化后的角点用绿色像素标记。

<img src="https://docs.opencv.ac.cn/4.11.0/subpixel3.png" alt="img" style="zoom:67%;" />

### Shi-Tomasi角点检测和良好特征跟踪

> **用于计算角点，不描述角点**

OpenCV 有一个函数，**[cv.goodFeaturesToTrack()](https://docs.opencv.ac.cn/4.11.0/dd/d1a/group__imgproc__feature.html#ga1d6bb77486c8f92d79c8793ad995d541)**。它使用 Shi-Tomasi 方法（也可以指定使用 Harris 角点检测）查找图像中 N 个最强的角点。

对Harris的改进

Shi-Tomasi角点检测原理与Harris角点检测相同，只是在最后判别式的选取上不同Shi-Tomasi角点检测选取特征中的最小的那个来判别。R=min(λ1,λ2)

> cv.goodFeaturesToTrack(image, maxCorners, qualityLevel, minDistance[, corners[, mask[, blockSize[,useHarrisDetector[, k]]]]]) ->corners
>
> cv.goodFeaturesToTrack(  image, maxCorners, qualityLevel, minDistance, mask, blockSize, gradientSize[, corners[, useHarrisDetector[, k]]]) ->corners
>
> image-输入 **8 位**或 32 位浮点的**单通道图像**。
>
> maxCorners-要返回的最大角点数。对于通过质量检测的角点，根据质量按降序对的角点进行排序，如果找到的角点多于指定的数量，则返回其中最强的N个的角点。`maxCorners <= 0` 表示没有设置最大数量限制，将返回所有检测到的角点。
>
> qualityLevel-**介于 0-1 之间的值**，是图像角点最小可接受质量。该参数值乘以最佳角点质量度量，该度量是最小特征值（参见 [cornerMinEigenVal](https://docs.opencv.ac.cn/4.11.0/dd/d1a/group__imgproc__feature.html#ga3dbce297c1feb859ee36707e1003e0a8)）或 Harris 函数响应（参见 [cornerHarris](https://docs.opencv.ac.cn/4.11.0/dd/d1a/group__imgproc__feature.html#gac1fc3598018010880e370e2f709b4345)）。质量度量小于该乘积的角点将被拒绝。例如，如果最佳角点的质量度量 = 1500，而 qualityLevel=0.01，则质量度量小于 15 的所有角点都将被拒绝。
>
> minDistance-两个角点之间的最小欧氏距离
>
> mask-可选的感兴趣区域。如果图像非空（需要具有 CV_8UC1 类型且大小与图像相同），则它指定检测角点的区域。
>
> blockSize-计算每个像素邻域的导数协方差矩阵的平均块大小。
>
> useHarrisDetector-指示是否使用 Harris 检测器
>
> 返回值：
>
> corners-**浮点型三维数组**，最内层存角点的x,y坐标

```python
img = cv.imread('blox.jpg')
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
corners = cv.goodFeaturesToTrack(gray,25,0.01,10)
corners = np.int0(corners)
for i in corners:
    x,y = i.ravel()
    cv.circle(img,(x,y),3,255,-1)
plt.imshow(img),plt.show()
```

![shitomasi_block1.jpg](https://apachecn.github.io/opencv-doc-zh/docs/4.0.0/img/930d9178c2c86314c092c8fcad111ac6.jpg)

### SIFT算法(尺度不变特征变换)

#### 原理



#### 函数

> **cv2.SIFT.create()**创建sift对象
>
> sift = cv2.SIFT_create(nfeatures=0, nOctaveLayers=3, contrastThreshold=0.04, edgeThreshold=10, sigma=1.6)
>
> nfeatures-需要保留的特征点的个数，特征按分数排序（分数取决于局部对比度） nOctaveLayers-每一组高斯差分金字塔的层数，sift论文中用的3。高斯金字塔的组数通过图片分辨率计算得到 
>
> contrastThreshold- 对比度阈值，用于过滤低对比度区域中的特征点。阈值越大，检测器产生的特征越少。 (sift论文用的0.03，nOctaveLayers若为3， 设置参数为0.09，实际值为：contrastThreshold/nOctaveLayers) edgeThreshold-用于过滤掉类似图片边界处特征的阈值(边缘效应产生的特征)，注意其含义与contrastThreshold不同，即edgeThreshold越大，检测器产生的特征越多(过滤掉的特征越少)；sift论文中用的10；
>
> sigma-第一组高斯金字塔高斯核的sigma值，sift论文中用的1.6。 （图片较模糊，或者光线较暗的图片，降低这个参数） 
>
> descriptorType-特征描述符的数据类型，支持CV_32F和CV_8U 
>
> 返回值：sift对象(cv2.Feature2D对象)

> **cv2.Feature2D.detect()**检测特征关键点
>
> keypoints = cv2.Feature2D.detect(image, mask) 
>
> image-需要检测关键点的图片 
>
> mask-掩膜，为0的区域表示不需要检测关键点，大于0的区域检测 返回值： keypoints-检测到的关键点列表

> **cv2.Feature2D.compute()**生成特征关键点的描述符
>
> keypoints, descriptors = cv.Feature2D.compute(image, keypoints) 
>
> image-需要生成描述子的图片
>
> keypoints-需要生成描述子的关键点 
>
> 返回值： 
>
> keypoints-关键点列表（原始关键点中，不能生成描述子的关键点会被移除；） 
>
> descriptors-关键点对应的描述子

> **cv2.Feature2D.detectAndCompute()**
>
> 检测关键点，并生成描述符，是上面detect()和compute()的综合
>
> keypoints, descriptors = cv.Feature2D.detectAndCompute(image, mask)

> **cv2.drawKeypoints()**绘制检测到的关键点
>
> outImage = cv2.drawKeypoints(image, keypoints, outImage, color, flags)
>
> image：检测关键点的原始图像 
>
> keypoints：检测到的关键点列表
>
> outImage：绘制关键点后的图像，其内容取决于falgs的设置 
>
> color：绘制关键点采用的颜色 
>
> flags： 	
>
> - cv2.DRAW_MATCHES_FLAGS_DEFAULT:默认值，匹配了的关键点和单独的关键点都会被绘制 	
> - cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS: 绘制关键点，且每个关键点都绘制圆圈和方向
> - cv2.DRAW_MATCHES_FLAGS_DRAW_OVER_OUTIMG
> - cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS：只绘制匹配的关键点，单独的关键点不绘制

#### 返回值

keypoint，在opencv中是一个类对象，其具有如下几个属性：

> angle: 特征点的方向，值在0-360 
>
> class_id: 用于聚类id,没有进行聚类时为-1 
>
> octave: 特征点所在的高斯金差分字塔组 
>
> pt: 特征点坐标 
>
> response: 特征点响应强度，代表了该点时特征点的程度（特征点分数排序时，会根据特征点强度） 
>
> size:特征点领域直径

keypoints

> keypoint的列表

**descriptor**

> 检测点对应的descriptor，是一个128维的向量。

**descriptors**

> 是描述符（descriptor）的矩阵，形状为`(N, 128)`，其中`N`是关键点的数量。
>
> - 每个关键点对应一个 128 维的向量，这个向量量化地描述了该关键点周围的图像区域特征。
> - 描述符对旋转、尺度变化具有一定的不变性，是实现图像匹配的核心数据。

#### 应用

```python
img = cv.imread('home.jpg')
gray= cv.cvtColor(img,cv.COLOR_BGR2GRAY)
 
sift = cv.SIFT_create()
kp = sift.detect(gray,None)
 
img=cv.drawKeypoints(gray,kp,img)
```

`sift.detect`用来查找图像的关键点，如果只搜索图像的一部分，可以输入掩码。每个关键点都是一个特殊的结构，具有许多属性，例如其 (x,y) 坐标、有意义的邻域的大小、指定其方向的角度、指定关键点强度的响应等。

**cv.drawKeyPoints()** 函数，该函数在关键点的位置绘制小圆圈。如果传入标志**cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS**，它将绘制一个与关键点大小相同的圆圈，甚至会显示其方向。

```python
img=cv.drawKeypoints(gray,kp,img,flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv.imwrite('sift_keypoints.jpg',img)
```

<img src="https://docs.opencv.ac.cn/4.11.0/sift_keypoints.jpg" alt="img" style="zoom: 80%;" />

现在要计算描述符，有两种方法

1. 如果已经找到了关键点，您可以调用**sift.compute()**，它将根据我们找到的关键点计算描述符。例如：kp,des = sift.compute(gray,kp)
2. 如果还未找到关键点，请使用函数**sift.detectAndCompute()**一步直接查找关键点和描述符。

```python
sift = cv.SIFT_create()
kp, des = sift.detectAndCompute(gray,None)
```

#### 关于旋转不变性

具有旋转不变性

### SURF(加速稳健特征)

SIFT的加速版本，它和SIFT的使用基本相同，还有一些可选条件：

1. 64维或128维描述符(**描述符的维度**，由参数`Extended(布尔值)`控制)
    - 64:`False,默认值`
    - 128:`True`
    - 参数控制：`surf.getExtended()`和`surf.setExtended(布尔值)`
2. Normal SURF/Upright(**特征点的方向**，由参数`Upright(布尔值)`控制)
    - Normal SURF(**带方向的,False,默认值**):
        - 会计算每个特征点的**主方向**（基于特征点邻域内的梯度方向分布）。
        - 特征描述子会**根据主方向进行旋转归一化**，使描述子具备旋转不变性。
        - 适用于需要处理图像旋转的场景（例如物体旋转后仍需匹配）。
        - 计算量稍大（因为多了方向计算步骤）。
    - Upright SURF(**不带方向，True**):
        - **不计算特征点的方向**
        - 特征描述子不进行旋转归一化，因此**不具备旋转不变性**。
        - 计算速度更快（省去了方向估计步骤）。
        - 适用于已知图像不会发生旋转的场景（例如文档扫描、正视拍摄的图像）。
    - Normal SURF 对旋转更鲁棒，Upright SURF 在图像旋转时匹配性能会下降。
    - **速度**：Upright SURF 比 Normal SURF 快约 30%（因省去方向计算）。
    - 参数控制: `surf.getUpright()`和`surf.setUpright(布尔值)`
    
    #### API
    
    > cv.xfeatures2d.SURF_create(hessianThreshold=100, nOctaves=4, nOctaveLayers=3, extended=False, upright=False)
    >
    > **hessianThreshold**-设定 Hessian 矩阵的阈值，越大检测到的特征点越少，但更稳定。
    >
    > nOctaves-金字塔尺度层数，值越大能检测更多的特征点，但计算更慢。
    >
    > nOctaveLayers-每层的图像层数，影响特征点检测的精度。
    >
    > **extended**-False 生成 64 维特征描述子，True 生成 128 维特征描述子。
    >
    > **upright**-False计算旋转不变性(即计算方向)，True不计算方向，计算速度更快但旋转不变性较差。
    
    #### 应用
    
    ```python
    img = cv.imread('fly.png', cv.IMREAD_GRAYSCALE)
    
    surf = cv.xfeatures2d.SURF_create(50000)
    kp, des = surf.detectAndCompute(img,None)
    img2 = cv.drawKeypoints(img,kp,None,(255,0,0),4)
    ```
    
    <img src="https://docs.opencv.ac.cn/4.11.0/surf_kp1.jpg" alt="img" style="zoom:67%;" />
    
    使用U-SURF(不计算方向)
    
    ```python
    surf.setUpright(True)
    kp = surf.detect(img,None)
    img2 = cv.drawKeypoints(img,kp,None,(255,0,0),4)
    ```
    
    <img src="https://docs.opencv.ac.cn/4.11.0/surf_kp2.jpg" alt="img" style="zoom:67%;" />

描述符维度

```python
>>> print(surf.descriptorSize())
64

＃因此，我们将其设置为True以获得128维描述符。
>>> surf.setExtended(True)
>>> kp, des = surf.detectAndCompute(img,None)
>>> print(surf.descriptorSize())
128
```

#### 关于旋转不变性

具有旋转不变性

### FAST算法

FAST比其他现有的角点检测器快几倍。但它对高噪声不鲁棒，也**不具备旋转不变性**。

> **因为FAST和Harris、Shi-Tomasi都是计算角点的，但并不描述它。**

它像OpenCV中的任何其他特征检测器一样被调用。如果需要，可以指定**阈值**、**是否应用非最大值抑制**、**使用的邻域**等。

对于邻域，定义了三个标志，cv.FAST_FEATURE_DETECTOR_TYPE_5_8、cv.FAST_FEATURE_DETECTOR_TYPE_7_12和cv.FAST_FEATURE_DETECTOR_TYPE_9_16。

#### API

实例化fast（FastFeatureDetector_create函数 ）

> static Ptr<FastFeatureDetector)>cv::FastFeatureDetector::create
>
> (int *threshold*=10,
>
> bool *nonmaxSuppression*=true,
>
> FastFeatureDetector::DetectorType type=FastFeatureDetector::TYPE_9_16 )
>
> fast = cv.FastFeatureDetector.create( [, threshold[, nonmaxSuppression[, type]]])
>
> 参数：
>
> threshold：**阈值t**，有默认值10
> **nonmaxSuppression**：**是否进行非极大值抑制**，默认值**True**
>
> 返回：
>
> 创建的**FastFeatureDetector对象**

利用**fast.detect**检测关键点（fast.detect函数）

> kp = fast.detect(Img,Mask)
>
> **参数**：
> Img：进行关键点检测的图像
>
> Mask:掩码
>
> **返回**：
> **kp**：关键点列表

#### 应用

```python
 
img = cv.imread('blox.jpg', cv.IMREAD_GRAYSCALE)
 
# 使用默认值初始化FAST对象
fast = cv.FastFeatureDetector_create()
 
# 查找并绘制关键点
kp = fast.detect(img,None)
img2 = cv.drawKeypoints(img, kp, None, color=(255,0,0))

# 禁用非极大值抑制
fast.setNonmaxSuppression(0)
kp = fast.detect(img, None)
img3 = cv.drawKeypoints(img, kp, None, color=(255,0,0))
```

第一张图显示了使用非极大值抑制的FAST算法，第二张图则没有使用非极大值抑制。

![img](https://docs.opencv.ac.cn/4.11.0/fast_kp.jpg)

### BRIEF特征点描述算法(二进制鲁棒独立基本特征)

BRIEF对**已检测到的特征点进行描述**，它是一种**二进制**编码的描述子，摈弃了利用区域灰度直方图描述特征点的传统方法，大大的加快了特征描述符建立的速度。

#### 原理

 由于BRIEF仅仅是特征描述子，所以事先要得到特征点的位置，接下来看BRIEF算法建立特征描述符过程。

1. 为减少噪声干扰，先对图像进行高斯滤波(方差为2，高斯窗口为9x9)
2. 以特征点为中心，取SxS的邻域窗口。在窗口内随机选取一对（两个）点，比较二者像素的大小，进行如下二进制赋值。![img](https://img-blog.csdn.net/20150716132835182)其中，p(x)，p(y)分别是随机点x=(u1,v1),y=(u2,v2)的像素值
3. 在窗口中随机选取N对随机点，重复步骤2的二进制赋值，形成一个二进制编码，这个编码就是对特征点的描述，即特征描述子。（可以是128、256或512，一般N=256）

经过上面的特征提取算法，对于一幅图中的每一个特征点，都得到了一个256bit(32字节)的二进制编码。

```python
img = cv.imread('simple.jpg', cv.IMREAD_GRAYSCALE)
 
# 初始化FAST检测器
star = cv.xfeatures2d.StarDetector_create()
 
# 初始化BRIEF提取器
brief = cv.xfeatures2d.BriefDescriptorExtractor_create()
 
# 使用STAR查找关键点
kp = star.detect(img,None)
 
# 使用BRIEF计算描述符
kp, des = brief.compute(img, kp)
 
print( brief.descriptorSize() )
print( des.shape )
```

brief.getDescriptorSize()给出以字节为单位的大小，默认值32

#### 关于旋转不变性

BRIEF 描述符本身不具备旋转不变性。

BRIEF 描述符的工作原理是：在关键点周围的固定区域内，随机选择若干对像素点，通过比较每对像素的亮度值（如果第一个像素比第二个亮则记为 1，否则记为 0），生成一个二进制串作为描述符。

这种机制的问题在于：当图像发生旋转时，关键点周围的像素分布会发生旋转，而 BRIEF 中用于比较的像素对坐标是固定的（相对于关键点的原始方向），这会导致同一特征在旋转前后生成的二进制描述符差异很大，从而失去匹配能力。

### ORB(定向FAST和旋转BRIEF)

因为SIFT 和 SURF 有专利，ORB是他们的替代方案

ORB 基本上是 **FAST 关键点检测器和 BRIEF 描述符的融合**（`所以说它的描述符是像BRIEF一样的二进制的`），并进行了许多改进以增强性能。它首先使用 FAST 查找关键点，然后应用 Harris 角点测量来找到其中排名前 N 的点。它还使用金字塔来生成多尺度特征。

#### API

> cv.ORB.create([,nfeatures[,scaleFactor[,nlevels[,edgeThreshold[,firstLevel[,WTA_K[,scoreType[,patchSize[,fastThreshold]]]]]]]]])->retval
>
> nfeatures- 要保留的最大特征数量，默认500
>
> WTA_K-决定产生定向 BRIEF 描述符的每个元素的点数。默认为 2，即一次选择两个点。在这种情况下，对于匹配，使用 NORM_HAMMING 距离。如果 WTA_K 为 3 或 4，则需要 3 或 4 个点来生成 BRIEF 描述符，则匹配距离由 NORM_HAMMING2 定义。
>
> scoreType-默认的`HARRIS_SCORE`表示使用`Harris算法`对特征进行排序（分数写入KeyPoint::score并用于保留最佳nfeatures特征）；FAST_SCORE是该参数的替代值，它产生的关键点略微不稳定，但计算速度稍快。

#### 示例

```python
img = cv.imread('simple.jpg', cv.IMREAD_GRAYSCALE)
 
# 初始化 ORB 检测器
orb = cv.ORB_create()
 
# 使用 ORB 查找关键点
kp = orb.detect(img,None)
 
# 使用 ORB 计算描述符
kp, des = orb.compute(img, kp)
 
# 只绘制关键点位置，不绘制大小和方向
img2 = cv.drawKeypoints(img, kp, None, color=(0,255,0), flags=0)
```

<img src="https://docs.opencv.ac.cn/4.11.0/orb_kp.jpg" alt="img" style="zoom:67%;" />



#### 关于选择不变性

ORB 的描述符是类似于 BRIEF 的二进制描述符。

具体来说，ORB 采用了 BRIEF 描述符的核心思想 —— 通过比较关键点周围特定像素对的亮度值，生成由 0 和 1 组成的二进制串。不过，ORB 对 BRIEF 进行了重要改进：引入了**旋转不变性**。它会基于 FAST 关键点的方向（通过灰度矩计算），对 BRIEF 中使用的像素对坐标进行旋转，确保生成的二进制描述符在图像旋转时仍能保持一致性。

因此，ORB 的描述符本质上是具有旋转不变性的二进制描述符，继承了 BRIEF 二进制特性（计算快、存储效率高）的同时，提升了对几何变换的鲁棒性。

### 特征匹配

#### 暴力匹配

现在有两个图片的描述符，暴力匹配器取第一组中的一个描述符于第二组中所有特征描述符匹配，返回距离最近的那个匹配。

##### API

> static Ptr< BFMatcher > cv::BFMatcher::create（int *normType* = NORM_L2,bool *crossCheck*=false )
>
> **Python**
>
> cv.BFMatcher.create([, normType[, crossCheck]])->返回值
>
> **normType**-NORM_L1、`NORM_L2(默认值)`、NORM_HAMMING、NORM_HAMMING2 之一。
>
> - 对于 SIFT 和 SURF 描述符，L1 和 L2 范数是更好的选择；
> - 对于ORB、BRISK 和 BRIEF，应使用 NORM_HAMMING；当 WTA_K==3 或 4 时（参见 ORB::ORB 构造函数说明），应与 ORB一起使用 NORM_HAMMING2。
>
> **crossCheck**
>
> - `默认为false`，只要特征点 A 在特征点集 B 中找到了最佳匹配，就会保留该匹配对，不考虑反向是否匹配。
> - 如果为true，只有当特征点 A 在特征点集 B 中匹配到特征点 B，且特征点 B 在特征点集 A 中也恰好匹配到特征点 A 时，才会保留这个匹配对。这相当于进行了双向验证。当有足够多的匹配项时，这种技术通常会产生具有最少异常值的最佳结果。

match:返回最佳匹配

> void cv::DescriptorMatcher::match ( 
>
> InputArray  queryDescriptors,
>
> InputArray    trainDescriptors,
>
> **std::vector< DMatch > & matches,**
>
> InputArray     mask = noArray()
>
> )const
> 
>
> **Python**
>
> cv.DescriptorMatcher.match(queryDescriptors,trainDescriptors[, mask])->matches
>
> cv.DescriptorMatcher.match(queryDescriptors[, masks]) ->matches
>
> - queryDescriptors:查询描述子集合
> - trainDescriptors: 训练描述子集合
> - matches:两个集合描述子匹配结果
> - mask:描述子匹配时的掩码矩阵，用于指定匹配哪些描述子
>
> 返回值：
>
> `matches:一维列表，存储DMatch对象的列表`,如[dmatch1,dmatch2]

knnMatch():返回指定的k个最佳匹配

> void cv::DescriptorMatcher::knnMatch ( 
>
> InputArray   queryDescriptors,
>
> InputArray   trainDescriptors,
>
> **std::vector< std::vector< DMatch > > & matches,**
>
> int     k,
>
> InputArray   mask = noArray(),
>
> bool    compactResult = false
>
> )const
> k:每个查询描述子在训练描述子集合中寻找的最优匹配结果的数目
>
> 返回值：
>
> `matches:二维列表，每个元素都是有k个DMatch对象的列表`,如[[dmatch1...]]

DMatch

> | 公共属性 |                                                              |
> | -------- | ------------------------------------------------------------ |
> | float    | distance 距离： `**两个描述符之间的差异程度（用orm的话就是两个描述符的汉明距离），距离越小，则两个描述符的相似度越高**` |
> | int      | imgIdx 训练图像索引                                          |
> | int      | queryIdx 查询图像的特征点的索引                              |
> | int      | trainIdx 训练图像的特征点的索引                              |

drawMatches

> void drawMatches( const Mat& img1, const vector<KeyPoint>& keypoints1,
>                   const Mat& img2, const vector<KeyPoint>& keypoints2,
>                   const vector<vector<DMatch> >& matches1to2, Mat& outImg,
>                   const Scalar& matchColor=Scalar::all(-1), 		const Scalar& singlePointColor=Scalar::all(-1),
>                   const vector<vector<char> >& matchesMask=vector<vector<char> >(),
>
>  int flags=DrawMatchesFlags::DEFAULT );
>
> python:
>
>  cv.drawMatches(img1, keypoints1, img2, keypoints2,matches1to2, outImg[, matchColor[, singlePointColor[, matchesMask[,flags]]]])->outImg
>
> | img1             | 第一个源图像。                                               |
> | ---------------- | ------------------------------------------------------------ |
> | keypoints1       | 来自第一个源图像的特征点。                                   |
> | img2             | 第二个源图像。                                               |
> | keypoints2       | 来自第二个源图像的特征点。                                   |
> | matches1to2      | 从第一个图像到第二个图像的匹配，这意味着 keypoints1[i] 在 keypoints2[matches[i]] 中有一个对应的点。 |
> | outImg           | 输出图像。其内容取决于定义在输出图像中绘制内容的标志值。请参见下面的可能的标志位值。 |
> | matchColor       | 匹配的颜色（线条和连接的特征点）。如果 matchColor == [Scalar::all](https://docs.opencv.ac.cn/4.11.0/d1/da0/classcv_1_1Scalar__.html#a9c7b78a3333aa12198cc332ca352d1dc)(-1)，则颜色随机生成。 |
> | singlePointColor | 单个特征点的颜色（圆圈），这意味着特征点没有匹配。如果 singlePointColor == [Scalar::all](https://docs.opencv.ac.cn/4.11.0/d1/da0/classcv_1_1Scalar__.html#a9c7b78a3333aa12198cc332ca352d1dc)(-1)，则颜色随机生成。 |
> | matchesMask      | 确定绘制哪些匹配的掩码。如果掩码为空，则绘制所有匹配。       |
> | flags            | 设置绘图功能的标志。可能的标志位值由 DrawMatchesFlags 定义。 |

 cv::DrawMatchesFlags

| DEFAULT                | `默认值`，将创建输出图像矩阵（[Mat::create](https://docs.opencv.ac.cn/4.11.0/d3/d63/classcv_1_1Mat.html#a55ced2c8d844d683ea9a725c60037ad0)），即可以重用输出图像的现有内存。将绘制两个源图像、匹配和单个关键点。对于每个关键点，只绘制中心点（不绘制关键点大小和方向的圆圈）。 |
| ---------------------- | ------------------------------------------------------------ |
| DRAW_OVER_OUTIMG       | 不会创建输出图像矩阵（[Mat::create](https://docs.opencv.ac.cn/4.11.0/d3/d63/classcv_1_1Mat.html#a55ced2c8d844d683ea9a725c60037ad0)）。匹配将绘制在输出图像的现有内容上。 |
| NOT_DRAW_SINGLE_POINTS | 不会绘制单个关键点。                                         |
| DRAW_RICH_KEYPOINTS    | 将绘制每个关键点周围具有关键点大小和方向的圆圈。             |

##### 示例

```python
img1 = cv.imread('box.png',cv.IMREAD_GRAYSCALE) # queryImage
img2 = cv.imread('box_in_scene.png',cv.IMREAD_GRAYSCALE) # trainImage
 
# 初始化ORB检测器
orb = cv.ORB_create()
 
# 使用ORB查找关键点和描述符
kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)
# 创建BFMatcher对象,使用cv.NORM_HAMMING,因为我们用的是ORM
bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
 
# 匹配描述符。
matches = bf.match(des1,des2)
 
# 按距离排序。
matches = sorted(matches, key = lambda x:x.distance)
 
# 绘制前10个匹配项。
img3 = cv.drawMatches(img1,kp1,img2,kp2,matches[:10],None,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
```

<img src="https://docs.opencv.ac.cn/4.11.0/matcher_result1.jpg" alt="img" style="zoom:67%;" />

#### FLANN匹配器

FLANN代表快速近似最近邻库。它包含一系列针对大型数据集和高维特征的快速最近邻搜索而优化的算法。对于大型数据集，它的速度比BFMatcher更快。

##### API

对于基于FLANN的匹配器，我们需要传递两个字典，它们指定要使用的算法、相关参数等。

第一个字典是IndexParams。

> 1. 对于SIFT、SURF等算法：
>
>     - FLANN_INDEX_KDTREE = 1
>     - index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
>
> 2. 使用ORB时(注释中的值是文档中推荐的值)：
>
>     - FLANN_INDEX_LSH = 6
>
>         index_params= dict(algorithm = FLANN_INDEX_LSH,
>
>         table_number = 6, `# 12`
>
>         key_size = 12, `# 20`
>
>         multi_probe_level = 1) `#2`

第二个字典是SearchParams。

> 它指定应递归遍历索引中树的次数。较高的值可提供更高的精度，但也需要更多时间。可以使用search_params = dict(checks=100)来设置次数,也可以为空。

```python
img1 = cv.imread('box.png',cv.IMREAD_GRAYSCALE) # queryImage
img2 = cv.imread('box_in_scene.png',cv.IMREAD_GRAYSCALE) # trainImage
 
# 初始化SIFT检测器
sift = cv.SIFT_create()
 
# 使用SIFT查找关键点和描述符
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)
 
# FLANN参数
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50) # 或传入空字典
 
flann = cv.FlannBasedMatcher(index_params,search_params)
 
matches = flann.knnMatch(des1,des2,k=2)
 
# 只需绘制良好的匹配项，因此创建一个掩码
matchesMask = [[0,0] for i in range(len(matches))]
 
# 根据Lowe的论文进行比率测试
for i,(m,n) in enumerate(matches)
    if m.distance < 0.7*n.distance
matchesMask[i]=[1,0]
 
draw_params = dict(matchColor = (0,255,0),
singlePointColor = (255,0,0),
matchesMask = matchesMask,
flags = cv.DrawMatchesFlags_DEFAULT)
 
img3 = cv.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)
```

![img](https://docs.opencv.ac.cn/4.11.0/matcher_flann.jpg)



























