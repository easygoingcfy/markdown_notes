## 字典dict

哈希表

### 字典的构造

格式：` d = {key1 : value1, key2:value2.....}`

``` 
items = [('name','Gumby'),('age',42)]
d = dict(items)
d = dict(name='Gumby',age=42,height=1.76)
```



### 遍历

#### 遍历key

```
for key in dict:
for key in dict.keys():
```

#### 遍历value

```
for value in d.values():
```

#### 遍历项

```
for key,values in d.items():
```

### 删除元素



```
del tinydict['Name']  # 删除键是'Name'的条目
tinydict.clear()      # 清空字典所有条目
del tinydict          # 删除字典
```



## 字符串

### strip()

Python strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。

当rm为空时，默认删除空白符（包括'\n', '\r',  '\t',  ' ')

```
strip(rm)
lstrip(rm)
rstrip(rm)
```

## json

```
json.dumps()  将python对象编码成Json字符串
json.loads()  将Json字符串解码成python对象
json.dump()   将python中的对象转化成json储存到文件中
json.load()   将文件中的json的格式转化成python对象提取
```

注意，此处python对象不包括自定义的数据结构（类，消息）

使用json处理Protobuf消息时，仍然需要使用PythonApi ( json_format.Parse()  json_format.MessageToJson() ) 来完成消息与json字符串的转换。

## 函数

```
def func(paras):
	balabala
	return xx	#如果有
```

### eval()

执行一个字符串表达式，并返回表达式的值

### exec()

exec 执行储存在字符串或文件中的Python语句，相比于 eval，exec可以执行更复杂的 Python 代码

### \_\_name\_\_:预定义全局变量

模块内部用来标识模块名称。如果模块被导入，则\_\_name\_\_的值为模块名称，如果主动执行，则为字符串“\_\_main\_\_”

因此就可以理解

if \_\_name\_\_ == '\_\_mian\_\_' : 

​		func()

### repr()

返回一个对象的string格式

### replace()

把字符串中的old替换成new，返回替换后的新字符串，如果指定max，则替换不超过max次

`str.replace(old, new[, max])`

### decode（）

以encoding指定的编码格式解码字符串。默认编码为字符串编码。

**返回值** 返回解码后的字符串

`str.decode(encoding='UTF-8',errors='strict')`

##### 参数

- encoding -- 要使用的编码，如"UTF-8"。
- errors -- 设置不同错误的处理方案。默认为 'strict',意为编码错误引起一个UnicodeError。 其他可能得值有 'ignore', 'replace', 'xmlcharrefreplace', 'backslashreplace' 以及通过 codecs.register_error() 注册的任何值。



## 列表

### 删除元素

#### del 

```
del listname[index]
del listname[start : end]
```

#### pop

如果不写 index 参数，默认会删除列表中的最后一个元素

```
listname.pop(index)
```

#### remove

除了 del 关键字，Python 还提供了 remove() 方法，该方法会根据元素本身的值来进行删除操作。

需要注意的是，remove() 方法只会删除第一个和指定值相同的元素，而且必须保证该元素是存在的，否则会引发 ValueError 错误。

```
list.remove(value)
```

#### clear()

Python clear() 用来删除列表的所有元素，也即清空列表

# 库

## import json

```
json.dumps()    将 Python 对象编码成 JSON 字符串
json.dumps().encode("utf-8")    将 Python 对象编码成 JSON 字符串,以utf-8格式编码。
json.loads()    将已编码的 JSON 字符串解码为 Python 对象
```



## import argparse

对命令行参数进行操作

```
parser = argparse.ArgumentParser()

parser.add_argument(
	'-i','--in',action='store',type=str,required=True,
	help="help instruction")
	
args = parser.parse_args()
```



## import struck

用来处理C结构数据，使用`struck.pack`将数据转化成C结构数据，使用`struck.unpack`将C结构数据解析成元组

## import zlib

用来对字符串进行压缩

```
zlib.compress(string)
zlib.decompress(string)
```

## import sys

命令行参数存在 sys.argv[]

## import time

### time.mktime()

```
time.mktime(t)
t -- 结构化的时间或者完整的9位元组元素。
返回用秒数来表示时间的浮点数
```

### time.time()

返回当前时间的时间戳

### time.strptime()

根据指定的格式把一个时间字符串解析为时间元组

```
time.strptime(string[, format])
```

- string -- 时间字符串。
- format -- 格式化字符串。

返回struct_time对象。

### time.strftime()

格式化时间，返回以可读字符串表示的当地时间，格式由参数 format 决定

```
time.strftime(format[, t])
```

- format -- 格式字符串。
- t -- 可选的参数 t 是一个 struct_time 对象。

返回以可读字符串表示的当地时间

## import numpy



## import pandas

Pandas 的主要数据结构是 Series （一维数据）与 DataFrame（二维数据），这两种数据结构足以处理金融、统计、社会科学、工程等领域里的大多数典型用例。

### Series

https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html

Pandas Series 类似表格中的一个列（column），类似于一维数组，可以保存任何数据类型。

Series 由索引（index）和列组成，函数如下：

```
pandas.Series( data, index, dtype, name, copy)
```

- **data**：一组数据(ndarray 类型)。
- **index**：数据索引标签，如果不指定，默认从 0 开始。
- **dtype**：数据类型，默认会自己判断。
- **name**：设置名称。
- **copy**：拷贝数据，默认为 False。

#### 判断元素是否为空

```
pandas.isna()
pandas.notna()
```

### DataFrame

DataFrame 是一个表格型的数据结构，它含有一组有序的列，每列可以是不同的值类型（数值、字符串、布尔型值）。DataFrame 既有行索引也有列索引，它可以被看做由 Series 组成的字典（共同用一个索引）。

DataFrame 构造方法如下：

```
pandas.DataFrame( data, index, columns, dtype, copy)
```

参数说明：

- **data**：一组数据(ndarray、series, map, lists, dict 等类型)。
- **index**：索引值，或者可以称为行标签。
- **columns**：列标签，默认为 RangeIndex (0, 1, 2, …, n) 。
- **dtype**：数据类型。
- **copy**：拷贝数据，默认为 False。

Pandas DataFrame 是一个二维的数组结构，类似二维数组。

#### 转换Excel

https://pandas.pydata.org/pandas-docs/version/0.22/generated/pandas.DataFrame.to_excel.html

```
DataFrame.to_excel()
DataFrame.to_excel(excel_writer, sheet_name='Sheet1', na_rep='', float_format=None, columns=None, header=True, index=True, index_label=None, startrow=0, startcol=0, engine=None, merge_cells=True, encoding=None, inf_rep='inf', verbose=True, freeze_panes=None)
```

参数：

**excel_writer** : 字符串或 ExcelWriter 对象

> 文件路径或现有 ExcelWriter

**sheet_name** : 字符串，默认为 'Sheet1'

> 将包含 DataFrame 的工作表名称

**na_rep** : 字符串，默认 ''

> 缺少数据表示

**float_format** : 字符串，默认无

> 浮点数的格式字符串

**列**：序列，可选

> 要写的列

**header** : 布尔值或字符串列表，默认为 True

> 写出列名。如果给出字符串列表，则假定它是列名的别名

**index** : 布尔值，默认为 True

> 写行名（索引）

**index_label** : 字符串或序列，默认无

> 如果需要，索引列的列标签。如果给出 None，并且 header和index为 True，则使用索引名称。如果 DataFrame 使用 MultiIndex，则应给出一个序列。

**开始行：**

> 左上角单元格行转储数据帧

**起始点：**

> 左上角单元格列转储数据框

**引擎**：字符串，默认无

> 编写要使用的引擎 - 您也可以通过选项 `io.excel.xlsx.writer`、`io.excel.xls.writer`和 `io.excel.xlsm.writer`.

**merge_cells**：布尔值，默认为 True

> 将 MultiIndex 和 Hierarchical Rows 写入合并单元格。

**编码：字符串，默认无**

> 生成的excel文件的编码。只有 xlwt 需要，其他编写器原生支持 unicode。

**inf_rep** : 字符串，默认 'inf'

> 无穷大的表示（Excel 中没有无穷大的本地表示）

**freeze_panes**：整数元组（长度为 2），默认无

> 指定要冻结的从 1 开始的最底行和最右列
>
> *0.20.0 版中的新功能。*



## import psutil





## os.system()

运行系统命令

## file 文件IO

### with

Python 中的 **with** 语句用于异常处理，封装了 **try…except…finally** 编码范式，提高了易用性。

**with** 语句使代码更清晰、更具可读性， 它简化了文件流等公共资源的管理。

在处理文件对象时使用 with 关键字是一种很好的做法

使用 **with** 关键字系统会自动调用 f.close() 方法， with 的作用等效于 try/finally 语句是一样的。

```
with open(file_name,'rb') as f:

```

#### 原理

with 语句实现原理建立在上下文管理器之上。

上下文管理器是一个实现 **__enter__** 和 **__exit__** 方法的类。

使用 with 语句确保在嵌套块的末尾调用 __exit__ 方法。

这个概念类似于 try...finally 块的使用。

### 创建新文件

```
os.mknod(filename)
os.open()
```

### file.open()

```
open(file, mode='r')
```

| r    | 以只读方式打开文件。文件的指针将会放在文件的开头。这是默认模式。 |
| ---- | :----------------------------------------------------------- |
| rb   | 以二进制格式打开一个文件用于只读。文件指针将会放在文件的开头。这是默认模式。一般用于非文本文件如图片等。 |
| r+   | 打开一个文件用于读写。文件指针将会放在文件的开头。           |
| w    | 打开一个文件只用于写入。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。 |
| wb   | 以二进制格式打开一个文件只用于写入。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。一般用于非文本文件如图片等。 |
| w+   | 打开一个文件用于读写。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。 |
| a    | 打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。 |
| ab   | 以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。 |
| a+   | 打开一个文件用于读写。如果该文件已存在，文件指针将会放在文件的结尾。文件打开时会是追加模式。如果该文件不存在，创建新文件用于读写。 |
|      |                                                              |

### file.read ()

read（）方法从一个打开的文件中读取一个字符串。需要重点注意的是，Python字符串可以是二进制数据，而不是仅仅是文字。

`f.read([count])` count : 读取字节数

read()默认会读取整个文件，将文件内容存放到一个字符变量中

### f.readlines()

按列读取文件，返回由列组成的列表（list）

### f.readline()

每次读取一列，没怎么用过，效率较低。

### file.write([str])

str : 要写入文件的字符串

返回写入的字符长度

### file.tell()

定位文件读写指针

### file.seek(offset)

设置文件读写指针位置

## shell

### 退出

ctrl d 或者输入`exit()`

## urllib

### `urllib.request` 打开和读取URL

`urllib.request.urlopen(url, data=None, [timeout, ]*, cafile=None, capath=None, cadefault=False, context=None)`

- **url**：url 地址。
- **data**：发送到服务器的其他数据对象，默认为 None。
- **timeout**：设置访问超时时间。
- **cafile 和 capath**：cafile 为 CA 证书， capath 为 CA 证书的路径，使用 HTTPS 需要用到。
- **cadefault**：已经被弃用。
- **context**：ssl.SSLContext类型，用来指定 SSL 设置。  

---

#### urllib.request.Request类：模拟头部信息

`class urllib.request.Request(url, data=None, headers={}, origin_req_host=None, unverifiable=False, method=None)`

- **url**：url 地址。
- **data**：发送到服务器的其他数据对象，默认为 None。
- **headers**：HTTP 请求的头部信息，字典格式。
- **origin_req_host**：请求的主机地址，IP 或域名。
- **unverifiable**：很少用这个参数，用于设置网页是否需要验证，默认是False。
- **method**：请求方法， 如 GET、POST、DELETE、PUT等。







### `urlib.error`异常信息

包含两个方法

URLError:

OSError的一个子类，处理程序出错时引发，包含的属性reason异常原因

HTTPError:

URLError的一个子类，处理特殊HTTP错误

属性： code -状态码    reason异常原因	headers -http响应头

### `urllib.parse`解析URL

`urllib.parse.urlparse(urlstring, scheme='', allow_fragments=True)`

- **urlstring** : url地址
- **scheme**   :  协议类型
- **allow_fragment**   :  参数为 false，则无法识别片段标识符。相反，它们被解析为路径，参数或查询组件的一部分，并 fragment 在返回值中设置为空字符串。

`urllib.parse.encode` 对参数进行编码

`urllib.prase.decode` 对参数进行解码

###  `urllib.robotparser`解析robots.txt文件



## dir

**dir()** 函数不带参数时，返回当前范围内的变量、方法和定义的类型列表；

带参数时，返回参数的属性、方法列表。如果参数包含方法\_\_dir\_\_()，该方法将被调用。如果参数不包含\_\_dir\_\_()，该方法将最大限度地收集参数信息。

`dir([object])`

## 正则表达式 RE

匹配数字

```
\d
```



```
re.match(pattern,string)
match要求完全匹配

re.search(pattern,string)
rearch只需要存在即可，类似 in

re.sub(pattern,repl,string)
将string中匹配的部分用repl替换

re.findall(pattern,string,flags=0)
查找字符串中所有和模式匹配的子串放入列表
```









## 格式化输出

### 缩进:\t

### 换行:\n

### 设置字符串的颜色

\033[3;

字体颜色

\033[4;

背景颜色



## 运算符

/ : 除法，结果是小数。即便能整除也是小数

% : 取模

// : 求商，结果是整数（往小取整）

** 求幂



## 字符串

单引号，双引号，三引号都可以，分行写时用\连接

# global

在函数内部对函数外的变量进行操作时，需要在函数内部声明为global

# OpenCv

## 图像

```
cv.imread(path, flag)
```

path:图像路径
flag:
**cv.IMREAD_COLOR**：加载彩色图像，任何图像的透明度都会被忽略，它是默认标志
**cv.IMREAD_GRAYSCALE**：以灰度模式加载图像
**cv.IMREAD_UNCHANGED**：加载图像，包括 alpha 通道

```
cv.imshow(name, image)
```

第一个参数是窗口名，它是一个字符串，第二个参数就是我们的图像。你可以根据需要创建任意数量的窗口，但是窗口名字要不同。

```
cv.waitkey()
```

一个键盘绑定函数，它的参数是以毫秒为单位的时间。该函数为任意键盘事件等待指定毫秒。如果你在这段时间内按下任意键，程序将继续。如果传的是 0，它会一直等待键盘按下

```
cv.destroyAllWindows()
```

简单的销毁我们创建的所有窗口。如果你想销毁任意指定窗口，应该使用函数 **[cv.destroyWindow()](https://docs.opencv.org/4.0.0/d7/dfc/group__highgui.html#ga851ccdd6961022d1d5b4c4f255dbab34)** 参数是确切的窗口名

```
cv.namedWindow(name, flag)
```

默认情况下，flag 是 **[cv.WINDOW_AUTOSIZE](https://docs.opencv.org/4.0.0/d7/dfc/group__highgui.html#ggabf7d2c5625bc59ac130287f925557ac3acf621ace7a54954cbac01df27e47228f)**。但如果你指定了 flag 为 **[cv.WINDOW_NORMAL](https://docs.opencv.org/4.0.0/d7/dfc/group__highgui.html#ggabf7d2c5625bc59ac130287f925557ac3a29e45c5af696f73ce5e153601e5ca0f1)**，你能调整窗口大小。当图像尺寸太大，在窗口中添加跟踪条是很有用的。

```
cv.imwrite(name, img)
```

第一个参数是文件名，第二个参数是你要保存的图像。

### 关于Matplotlib

Matplotlib 是一个 Python 的绘图库，提供了丰富多样的绘图函数。

彩色图像 OpenCV 用的 BGR 模式，但是 Matplotlib 显示用的 RGB 模式,使用Matplotlib显示opencv读取的彩色图像时需要进行转换：

```
1. img2 = img[:, :, ::-1]
2. img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
```

### cv.get()

```
enum cv::VideoCaptureProperties {
  cv::CAP_PROP_POS_MSEC =0,
  cv::CAP_PROP_POS_FRAMES =1,
  cv::CAP_PROP_POS_AVI_RATIO =2,
  cv::CAP_PROP_FRAME_WIDTH =3,
  cv::CAP_PROP_FRAME_HEIGHT =4,
  cv::CAP_PROP_FPS =5,
  cv::CAP_PROP_FOURCC =6,
  cv::CAP_PROP_FRAME_COUNT =7,
  cv::CAP_PROP_FORMAT =8,
  cv::CAP_PROP_MODE =9,
  cv::CAP_PROP_BRIGHTNESS =10,
  cv::CAP_PROP_CONTRAST =11,
  cv::CAP_PROP_SATURATION =12,
  cv::CAP_PROP_HUE =13,
  cv::CAP_PROP_GAIN =14,
  cv::CAP_PROP_EXPOSURE =15,
  cv::CAP_PROP_CONVERT_RGB =16,
  cv::CAP_PROP_WHITE_BALANCE_BLUE_U =17,
  cv::CAP_PROP_RECTIFICATION =18,
  cv::CAP_PROP_MONOCHROME =19,
  cv::CAP_PROP_SHARPNESS =20,
  cv::CAP_PROP_AUTO_EXPOSURE =21,
  cv::CAP_PROP_GAMMA =22,
  cv::CAP_PROP_TEMPERATURE =23,
  cv::CAP_PROP_TRIGGER =24,
  cv::CAP_PROP_TRIGGER_DELAY =25,
  cv::CAP_PROP_WHITE_BALANCE_RED_V =26,
  cv::CAP_PROP_ZOOM =27,
  cv::CAP_PROP_FOCUS =28,
  cv::CAP_PROP_GUID =29,
  cv::CAP_PROP_ISO_SPEED =30,
  cv::CAP_PROP_BACKLIGHT =32,
  cv::CAP_PROP_PAN =33,
  cv::CAP_PROP_TILT =34,
  cv::CAP_PROP_ROLL =35,
  cv::CAP_PROP_IRIS =36,
  cv::CAP_PROP_SETTINGS =37,
  cv::CAP_PROP_BUFFERSIZE =38,
  cv::CAP_PROP_AUTOFOCUS =39,
  cv::CAP_PROP_SAR_NUM =40,
  cv::CAP_PROP_SAR_DEN =41,
  cv::CAP_PROP_BACKEND =42,
  cv::CAP_PROP_CHANNEL =43,
  cv::CAP_PROP_AUTO_WB =44,
  cv::CAP_PROP_WB_TEMPERATURE =45
}
```



## 视频

### VideoCapture

去获取一个视频，你需要创建一个**VideoCapture**对象。它的参数可以是设备索引或者一个视频文件名。

```
cap = cv.VideoCapture(0)
```

#### cap.read()

**[cap.read()](https://docs.opencv.org/4.0.0/d2/d75/namespacecv.html#a9afba2f5b9bf298c62da8cf66184e41f)** 返回一个 bool 值(`True`/`False`)。如果加载成功，它会返回`True`。因此，你可以通过这个返回值判断视频是否结束。

有时，cap 可能没有初始化 capture。在这种情况下，此代码显示错误。你可以通过该方法 **cap.isOpened()** 检查它是否初始化。如果它是 True，那么是好的，否则用 **[cap.open()](https://docs.opencv.org/4.0.0/d6/dee/group__hdf5.html#ga243d7e303690af3c5c3686ca5785205e)** 打开在使用。



#### cap.get(propId)

你也可以通过使用 **cap.get(propId)** 函数获取一些视频的特征，这里的 propld 是一个 0-18 的数字，每个数字代表视频的一个特征 (如果这个视频有)，或者使用cv:VideoCapture:get()获取全部细节。它们中有些值可以使用 **cap.set(propId, value)** 修改。Value 就是你想要的新值



### 播放视频

#### cv.waitkey()

如果它太小，视频将非常快，如果太大，视频将很慢 (嗯，这就是如何显示慢动作)。正常情况下，25 毫秒就可以了。

### 保存视频

建一个 **VideoWriter** 对象。我们应该指定输出文件的名字 (例如：output.avi)。然后我们应该指定 **FourCC** 码 (下一段有介绍)。然后应该传递每秒帧数和帧大小。最后一个是 **isColor** flag。如果是 True，编码器期望彩色帧，否则它适用于灰度帧。

```
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('output.avi',fourcc, 20.0, (640,480))
```

**[FourCC](http://en.wikipedia.org/wiki/FourCC)** 是用于指定视频解码器的 4 字节代码。这里 **[fourcc.org](http://www.fourcc.org/codecs.php)** 是可用编码的列表。它取决于平台，下面编码就很好。

- In Fedora: DIVX, XVID, MJPG, X264, WMV1, WMV2. (XVID 是最合适的. MJPG 结果比较大. X264 结果比较小)
- In Windows: DIVX (还需要测试和添加跟多内容)
- In OSX: MJPG (.mp4), DIVX (.avi), X264 (.mkv).

#### 编码大小

尝试过XVID, MJPG,MP4V

```
XVID(.avi) 大小和MP4V接近，略高
MJEP(.avi) 极大
MP4V(mp4)目前最小的
```



#### **保存视频失败的问题

保存视频时设置的视频尺寸，必须要与读到的每帧图片大小一致，两种解决办法

```
1. 修改cv.VideoWriter中视频尺寸参数，可以通过cap.get()函数获取图片的宽和高
2. 修改图片大小，使用cv.resize(frame, (width, height))
```



# conda

## conda 不可用（以zsh客户端为例，如bash则是~/.bashrc）

添加conda环境变量

```
vim ~/.zshrc
export PATH=/home/caofangyu/anaconda3/bin:$PATH   ****此处需要根据自己实际情况输入
source ~/.zshrc					 在终端中运行
```

之后在zsh中运行

```
conda init zsh
运行conda init后需要重启shell才生效
```



## 查看环境

```
conda env list	
```

## 创建环境

```
conda create -n ENV python=x.x
```



## 激活环境

```
conda activate ENV
conda deactivate ENV
```



# 使用C或C++扩展Python

