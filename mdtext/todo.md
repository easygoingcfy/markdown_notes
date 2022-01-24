# current 

~~换个字体吧~~~

使用wine安装新版微信

~~解析msg文件~~ ： one_msg.py

根据record里面的时间信息匹配localization，访问localization中的数据

## 分解

输入：时间

功能： 

- 根据时间检索所有需要解析的msg文件路径。
- 对msg文件解析，序列化后通过Json传到服务器上

## 用传来的proto解析recordB文件

### 实现read address book

#### 步骤

##### 安装protocol buffers编译器 

###### 先安装setuptools

我做的：

去官网下载了Source

解压缩后文件放到/opt/中

执行`python setup.py build`

执行`python setup.py test`进行测试

执行`python setup.py install`

可能：

`pip install setuptools` 官网写的

---

安装依赖项

`sudo apt-get install autoconf automake libtool curl make g++ unzip`

官网下载protobuf sorce，解压缩后移动到/opt/

进入protobuf目录执行(编译protobuf)：

```
./autogen.sh
./configure
make
make check
sudo make install
sudo ldconfig 
```

测试是否安装成功，进入protobuf下的python

```
python
import google.protobuf
```

不报错就算成功

编译.proto文件

## python post get

# 2022/1/18

- 查看protobuf对int64是怎么处理的（应该是解析的问题，考虑到json本身就是字符串格式）
- ~~同时看到json字符串把record_list中的driver_name也改了，观察解析后是否会还原~~：确认会正常解析

进度：

- 可以确定text_format.Parse没有改变int64的数据类型，但是在执行json_format.MessageToString的时候，将int64序列化成了string类型，导致最后解析的时候出错（并且在MessageToString的参数列表中没有相关的可选项）。所以要么直接在proto文件中修改driver_id的类型（改为string或其他），要么在序列化时使用其他函数。

解析问题：

德佳使用的JsonFormat.merge()  目前不知道具体怎么操作的

我用的是JsonFormat.Parser()，然后使用TextFormat.MessageToString()

# 2022/1/19

学习一下工程里面文件夹应该怎么整理，把自己的git整理一下。

# 2022/1/20

## 解析msg文件

1、从modules.common.message.python（as m）实例化一个BagReader对象（参数为待读取的msg文件列表）:

`reader = m.BagReader([raw_bag_file])`

类似的有

`writer = m.BagWriter(save_bag_file)`

new1、从modules.common.message.tools.proto.message_bag_pb2 as message_bag_pb2实例化对象对msg文件进行读取，分别读header和index：

`bag_header = message_bag_pb2.BagHeader()`

`bag_index = message_bag_pb2.BagIndex()`

其中读文件需要用到struct.unpack函数。

（message文件格式应该是分段的，每段开头是8位的unsignedlong，记录本段数据长度	）

2、 从modules.common.message.tools.proto import message_bag_pb2 as message_bag 实例化一个BagDataChunk对象:

`d = message_bag.BagDataChunk()`

3、使用BagReader.Next()函数一次读取一个msg文件:

`reader.Next(d)`

msg数据会存在d.message_data中，使用proto默认的ParseFromString解析

## to do 

先解析一个msg文件。

# 2022/1/21

## 分析：

record中的数据量远少于msg中数据量。

msg文件应该是按照时间顺序（按频率采样保存）存储，记录所有关心的参数，数据更密集。

record文件应该主要做索引，频率更低的共同只关心一些主要的状态，在出现意外（状态变化的时候）需要根据record中记录的关键时间去检索msg中的信息（目前是localization）

输入为时间，输出为时间匹配(或者差值在指定范围）的loc信息（单个或list）

先根据输入筛选需要读取的文件（msg文件名中包含时间信息，需要处理一下）

## 先梳理一下大致的框架（by read_log）：

### read_log

1. 清空list
2. read_log：更新list
3. 从list中读取时间（date）
4. 根据date读文件，更新list（读取take over之前一段时间的所有信息）
5. 保存，上传

### 大概思路

解析record得到message信息，从record中读时间。

根据时间从msg文件读数据，保存。

#### 方便扩展？

不会

#### 现在有的东西

解析record：solution.py

def get_path(输入：时间 输出：list): 检索目录，在列表（path_list）存放当天所有的recordB路径。

def post_message:对path_list中的所有recordB文件，每个文件用一个record对象进行解析，存放在batch_record中，然后转成json字符串，通过post发送到服务器。

解析msg：/test/one_msg.py  （输入：path）

利用message_bag对msg文件进行解析，能读到一个个的Localization数据

#### 输入输出

#### 类

Message：保存record 以及record对应的数据（包括但不限于Localization）

我觉得结构应该是record中一个record_list  + 这个record_list对应的数据。

record_list 

data_list = []

需要提取的信息：

​						车辆

​							|

​						 data

​							|

​			record_list + loc[]

​	record_list采用字典形式存放每辆车的batch_record

   message_list同样

