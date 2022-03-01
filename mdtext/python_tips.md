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



## 函数

```
def func(paras):
	balabala
	return xx	#如果有
```

### eval()

执行一个字符串表达式，并返回表达式的值

## exec()

exec 执行储存在字符串或文件中的Python语句，相比于 eval，exec可以执行更复杂的 Python 代码

## main函数

main函数只有该python脚本直接作为执行程序时才会执行（<u>目前不懂</u>）

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

```
re.match(pattern,string)
match要求完全匹配
re.search(pattern,string)
rearch只需要存在即可，类似 in
re.sub(pattern,repl,string)
将string中匹配的部分用repl替换
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



