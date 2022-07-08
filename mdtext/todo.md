无人化车辆: 520/521/522/526/527/530/533/539/519

​              howo20  howo21 howo22 howo23 howo27 howo28 howo31 howo34 howo40

更新5g_delay的车（混线）：howo24 howo26 howo29 howo30 howo25      howo14，15，16，29，30

AT523 AT524 AT525 AT528 AT529



判断文件夹是否可写入，不可写入时db存放到/tmp中

新接受消息task_state，查看对cpu影响

## 撰写文档：

阐述driving_event模块的功能和用途

 异常处理策略

安全策略

```
11.2.8. 异常处理模块
11.2.8.1. 能统计、收集、查询自动驾驶水平运输设备的所有故障信息。监控界面上显示具体异常信息及影响范围，采用醒目颜色预警或其他方式通知相关人员。
11.2.8.2. 记录异常原因，对处理过程和影响范围提供追溯。

自动驾驶系统能够根据提前设计分级管理及异常处理流程，通过复位，重发指令等方式，让自动驾驶水平运输设备继续作业，或者进入自动驾驶水平运输设备缓冲区域，减少人工接管次数。
```



# 20220706

测试bag.py：

有错误，sqlalchemy报类型错误，未解决

# 20220705

```
1. data_analyzer 合并最基础的部分 db数据收集，collect先注释不做。 
2. 5g delay部分合并到master
3. fabupilot config合并+测试
```



# 20220704

0704南通测试的数据回传好了检查log，观察是否有 MONITOR_TOPIC_DELAY事件

data_analyzer:重构bag.py，将与db有关的操作放在另外一个类中

bag类目前用于管理多个bag, 新类用来对单个bag进行操作



# 20220701

调整从egoInfo找scene逻辑，扩大时间范围，返回完整列表。

修改comment里内容

离线更新场景：一车一天大概一个小时左右？

![image-20220704094530685](/home/caofangyu/.config/Typora/typora-user-images/image-20220704094530685.png)

场景更新步骤：拿到未更新场景的PingData数据， 根据时间从EgoInfo找scene，更新

# 20220630

1. doc整理好，排查下混线场景数据，有没有问题
2.  改comment上内容
3. 做完之后看下data_collect内容，要准备合并了

# 20220629

无人化延时数据 输出docx

线上优化ｄｂ，读ｂａｇ＿ｉｎｄｅｘ的时候存ｄｂ。db

无人化和混线在一个doc里分开统计。 先显示无人化的数据，再显示混线的数据。

doc里面的图片删掉

检查混线数据（场景数据很少）

# 20220627 

1. 新发版本本地测试，实车测试
2. 数据回传check脚本，检查recordF和recordB,固定执行，发送到微信群
   1. 无人化路径：/onboard_data/bags/meishangang_driverless_v2
   2. 从/fabudata读取recordB recordF中无人化数据scp到本地，再与/onboard_data上数据对比，检查回传漏包情况
3. ~~5G延时统计，输出到html中~~放弃，改为使用reportlib生成pdf

# 20220624

1. 无人化超时数据输出脚本化，输出到data3上某个目录，按时期给出划分（前天做的，1辆车一个直方图和表格数据）

   直方图：场景延时分布 表格数据形式如下：

   1. 从ecs log读文件保存到db数据中
   2. 根据db输出对应的直方图与表格数据，有空改下函数，支持显示的下标自定义？
   
1. 输出按场景分类后的直方图分布。

目前是三个场景，泊位，引桥，箱区

输出各场景的时间占比

文件储存在data3指定目录

# 20220623

1. ~~无人化场景数据解析，先尽快实现一个版本放着跑，直接利用bag.py就行，数据更新写到db里面。~~
2. 读bag index，写入db文件，然后基于db文件查找 和 1 对比下时间
3. 混线场景数据分析。
3. 写从db中读取index解析消息更新场景的脚本

无人化车辆: 520/521/522/526/527/530/533/539/519

# 20220621

写监控cpu的脚本
使用

```
ps -aux | grep data_analyzer/main.py
```



# 20220620

~~绘图函数，支持一次绘制多个车辆的数据~~

统计车辆运行时间（分段统计，间隔超过五分钟以上为一段，统计总时间）

~~查看5g_delay更新~~

陈彦冰-修改回传检查脚本

### 重构

需要的数据：

时间分布

场景分布

延迟

总时间

# 20220616

#### 5g_delay分支： 重写update_scene函数

现在直接在线上把scene_type存到了数据库中，重写update_scene函数来更新PingData

# 20220615

1. ~~改图（5G超时），梅山再跑一天，目前来看引桥分布最多，可以跑几天确认下~~ 
2. ~~跑1天南通数据（5G超时）~~
3. 测试情况跟踪（cpu），确认有没有退出自动驾驶事件以及退出后的分析。 
   1. 目前拿不到数据，延后

4. ~~5G数据集成到data_analyzer~~
5. 优化bag.py 

## data_analyzer：

### 5G超时统计整合到data-analyzer

放在data_collect.py里，collect()函数中

### 优化读bag_index（存到db里面）



## 5G超时空间分布（scene）

1. log中的信息储存在sqlite3数据库中（ecs_network）
2. 根据车以及时间，从bag找scene数据（data_analyzer：common/bag.py）
3. 更新数据库
4. 根据数据绘图
   1. 绘图时空数据修改为无场景
   2. 针对单车运行进行修改

### log路径

```
梅山
root = /fabudata or /onboard_data/logs
/fabudata:  /fabudata/howo8/2022-06-02/ecs...
/onboard_data: /onboard_data/logs/howo8/2022-06-02/ecs...
南通
root = /onboard_data/logs
```



5G超时信息统计

1. 统计一个周期内的信息
2. 数据存储到db中



网络延时任务流程

1. 使用active_safety_reporter-master中的log_querier.py脚本生成指定日期的data.json数据（需要/private,需要在当前目录建立data文件夹软连接到/private/active_safety_reporter/d）

data.json数据格式：

{date:{vehicle:[{}, {}, {}, ... ]}}

2. 使用brake(data storage中）中脚本main.py 读取data.json更新max_vel  scene字段生成active_emer.json文件
3. 使用仓库data_parser中脚本parse_csv.py从csv文件读数据，结果保存在planning_emer.json中(需要/private)
4. 使用data_parser中脚本process_json.py合并json文件，并输出分析结果图片，保存在image目录中。

# 0606

http://jira.fabu.ai/browse/ATRUCK-2359?filter=-1

## 根据接管记录找接管包

1. 从云控拿接管记录
2. 根据接管记录的时间，车找接管包，统计缺失数
3. 根据接管记录（或者接管包找前后五分钟的包），统计丢失个数

## data_collecter



## data_analzyer问题

![image-20220530144449444](/home/caofangyu/.config/Typora/typora-user-images/image-20220530144449444.png)

![image-20220530171112518](/home/caofangyu/.config/Typora/typora-user-images/image-20220530171112518.png)



![image-20220530173014515](/home/caofangyu/.config/Typora/typora-user-images/image-20220530173014515.png)

del函数出错：

AttributeError: 'EventRecord' object has no attribute 'insert_cursor'

新接口

### 统计对位指标

# 先做

录接管数据，通过回调函数

处理 remote_control读数据

## 新建一个模块 data_analyzer

### 添加文件逻辑

- 存所有事件
  - 存储需要记录的状态（如时间，对应的时间名等）到DB文件中
    - db文件在什么时候创建
- 存分析结果

### analyzer.py

#### 接管时分析，自动驾驶过程中需要记录数据吗？

#### 在自动驾驶中

有哪些状态需要关注，分别需要干嘛

#### 退出自动驾驶

做的分析

对位误差：perception：crane_detection.proto   -->CraneObject(可以通过is_target_crane判断)   GantryObject

位置:  modules/tools/data_analyzer

先拉一个分支实现

* 写配置文件
  
  * xxx.conf

* 配置Living modules
  
  * ```
    config/modules/common/module_conf/conf/living_modules.pb.txt
    ```

1 往前搜包

## python脚本完成数据分析

根据企业微信文档 《对位数据指标》的说明，通过回调函数实现：

* 判断车辆状态（自动驾驶，脱离自动驾驶）
  * http://git.fabu.ai/fabupilot/fabupilot/blob/master/modules/common/driving_event/conf/driving_event_conf.pb.txt#L815
  * http://git.fabu.ai/fabupilot/fabupilot/blob/master/modules/common/driving_event/conf/driving_event_conf.pb.txt#L1087
  * 进入自动驾驶：VEHICLE_START
  * 脱离自动驾驶：VEHICLE_INTO_EMERGENCY
  * 通过解析数据来完成
* 脱离自动驾驶后进行实时分析，（数据为记录的db文件以及msg文件）
  * 确定分析的数据范围（时间或者状态决定）
  * 统计重要参数（见企业微信文档）

TOPIC:

msg_type : message_type

timestamp : data_header.send_time_ns

offset : 

length:

## 问题：

数据保存路径的问题，线上存的时候也是保存在data/bag里吗，相对路径一致吗

### 接管时需要的参数

接管时间

### 通过bag_index的内容解析数据，拿到数据队列

### 静态接管中怎么定位到车辆停止的时刻。

像bag_parser一样单独搜索？

#### 搜索数据的顺序

从前往后遍历比

在本地fabupilot上build时每次都会有个

```
Downloading LFS objects:
```

卡很久，但是在dev上没有，为什么

# TODO

## 播包，记录monitor数据，完成 对位配合作业次数统计

判断依据为两个指令状态之间无接管，是否发生接管可以通过event_tracking_type.proto拿到。

~~在modules/common/messsage/python里同时保存支持python2和python3的代码~~

## 1.将视频文件（数据）存到bag里面

## 2. 从bag中解析视频，播放，并能根据视频输出图片（给感知？）

## message_service

视频录到包里，message_service要做的事

1. 从bag里解析出视频数据（文件）
2. 播放视频，需要增加-s选项，用来定位时间。
   1. 设置帧率
   2. 设置waitkey（例子中用的1000/fps, 教程中建议25左右）。waitkey影响播放速度
3. 视频输出重定向？

## cache

用 numpy把已经发送过的record数据存储好，每次发送之前对照一次，已经发送过的数据就不再发送了。

### record_list转成np支持的格式（np数组？）

### 数据按时间存储，并且有检测时间的机制（将一周之前存储的数据删除）

暂时用json做了，先测试

## 停车点字符串

### 增加-s

提前3s

测试，暂定从停车时间点开始。

### record脚本补发逻辑？

有时候存在某几天服务器维护，无法上传数据的问题，能否设计一个补发逻辑。

从request里入手

## record log搜索问题，找时间验证一下是否都搜到静止点的log了

还有Log的显示方式要不要变化一下。

# 

# 辅助分析

先做最最简单的。

* 判断消息频率
  * 从msg_queue拿到时间段内的所有log消息。遍历消息，能拿到消息的event_code，用字典统计出现次数？
  * 不如统计标签的出现次数，这样如果出现多个标签，也能根据次数来确定百分比。
    * dict{'tag_name' : count}
  * 统计标签次数好还是统计event_code次数好？
* 分配标签
  * 存在同样的event_code对应多个标签的情况，用re匹配content，确定具体标签。content也需要有个列表或者字典。
    * dict{'tag_name': 're_patten'}

| monitor错误日志                                                          | EventCode                | 附加判断条件 | planning刹停规则 | 问题标签             |
| -------------------------------------------------------------------- | ------------------------ | ------ | ------------ | ---------------- |
|                                                                      | INPUT_GNSS_UNSTABLE      | 横纵路上   |              | 驱动-组合导航-组合导航信号异常 |
| 定位接收的GNSS不稳定,将触发规划停车                                                 | INPUT_GNSS_UNSTABLE      | 非横纵路上  |              | 定位-定位错误刹停        |
| 系统错误: 处于紧急阶段-无变道空间                                                   | PLANNING_SYSTEM_ERROR    | 无      |              | 规划--决策--无变道空间    |
| 系统错误: 地图路线搜索失败                                                       | PLANNING_SYSTEM_ERROR    | 无      |              | 规划--决策--路径搜索失败   |
| 模块消息延时:antenna [REMOTE_ENVIRONMENT] has delay                        | MODULE_TOPIC_DELAY       | 无      |              | 缺少合适的问题标签        |
| 系统错误: 处于紧急阶段-收到紧急停车指令 底盘参数异常，紧急停车                                    | PLANNING_SYSTEM_ERROR    | 无      |              | 车辆-底盘硬件错误        |
| 转向控制异常,将触发规划紧急停车                                                     | EPS_ANGLE_EXCEPTION      | 无      |              | 车辆-底盘硬件错误        |
| 定位接收的车道线错误,将触发规划停车                                                   | INPUT_VISION_LANE_ERROR  | 无      |              | 定位-定位错误刹停        |
| 双机时间同步异常,请求主动安全停车                                                    | COMPUTER_TIME_SYNC_ERROR | 无      |              | 普罗米修斯-双机同步异常     |
| perception_lidar has error: [NEED_EMERGENCY_FATAL]-106021-[激光雷达遮挡错误] |                          | 无      |              | 驱动-激光雷达-激光雷达帧率异常 |

* 从云控拿到的数据可以转成字典，字典格式如下：

* ```
  {
  vehicleEvents: list
  totalElements: int
  totalPages:int
  }
  ```

* 看错误判断的原理

形如HasSystemTimeError()。在abnormal_type_determine.cc里面

## 录包

连接失败。record_bag启动之后没有连接成功。

### 溯源

- message::MessageService::Init(module_name,callback,1)
  
  - MessageService::InitImpl(module_name,callback)
  - 

- fabupilot::common::adapter::AdapterManager::Init(configs)    
  
  - configs: config/modules/planning_v3/conf/adapter.conf
    
    - config形式：
      
      ```
      config {
           type: LOCALIZATION
           mode: RECEIVE_ONLY
           message_history_limit: 50
        }
      ```
  
  - 对config.type: EnableLocalization

# handler

新增一个handler，暂定名NotepadHandler

自己先写一个Notepad的Proto。放在modules/msgs/notepad/proto/notepad_log.proto里。

自己先测试。

dev0执行arc diff --preview 报错：No space left on device

### NotepadHandler

主要用于向Notepad端发送数据（司机），基本内容应该与MonitorHandler一致，需要ParseContent

* driving_event.cc 进行注册（RegisterFactory)    

* handler.h 同monitor_log

* handler.cc同monitor_log,之后根据proto进行修改。

* driving_event_test.cc  使用测试代码（沿用之前的）

* 修改driving_event_conf.pb.txt  在事件中加入EmergencyHandler和NotepadHandler，用message_service查看发送内容

* driving_event_conf.pb.txt新加的事件需要在modules/common/proto/event_code.proto中登记

* 需要修改配置
  
  * modules/common/adapters/proto/adapter_config.proto  主要是新的message_type，目前应该是使用NOTEPAD或者新加NOTEPAD_LOG
  
  * modules/common/adapters/message_adapters.h 需要包含的proto消息的C++编译文件头文件（xxx.pb.h），类型Python中的xxx_pb2.py，并在adapter命名空间中声明该消息的Adapter：
    
    * ```
      using LocalizationAdapter = Adapter<::fabupilot::localization::Localization>;
      ```

* modules/common/adapters/adapter_manager.h 需要使用REGISTER_ADAPTER注册新增的proto消息，看起来只需要消息的类名就行

自己播包，学一下怎么分析接管原因。

结合monitor_command代码

## 看看c++代码规范（Google style）

## handle

需要增加一个handle，在某种情况下发消息给planning，让planning紧急停车

在driving_event里面看。包括conf里面的配置文件

### 大概步骤

1. **driving_event_conf.pb.txt**中加入driving_event_msg，在对应模块下 分配对应的event_code、level 、和handler
2. handler.h中加入新的handler类（从base集成,EmergencyHandler），写构造函数 和 Execute函数声明
3. handler.cc中写Execute函数，主要内容为生成对应的数据类型（），设置该数据的参数，然后调用AdapterManager中FillxxxHeader和PublishXxx
4. 如果AdapterManager中没有上述函数，自己写
5. driving_event.cc 里，RegisterFactory增加自己的handler类。

### 问题：

#### 目前的改动

driving_event_conf.pb.txt: 加了模板，具体内容没写

handler.h : copy MonitorLogHandler的构造函数，设置时间间隔为1，做了ParseFreq

handler.cc : 写了EmergencyHandler::Execute,设置module,error_code,event_level

driving_event.cc ： RegisterFactory增加EMERGENCY

# 作业流程

# 接管

**3.4** 好几个msg解析失败，没有找到原因，错误全是解析bag_index的时候失败。

参考 ： modules/common/message/tools/message_bag.cc

常见接管类型，判断的方法，数据在哪（那个字段）

应该看看播包的脚本 以及 接管分析的PPT

可能更关心车发出去（本身）的数据，而不是接收到的？

## 压线

车的信息（车道），速度，状态等。

## 吊具在作业

吊具高度？如何匹配吊具

# 数据

git@git.fabu.ai:caofangyu/event_parser.git

## RemoteControl

频率：1/s  每个bag60个

一般包括3个部分

header

command

tos_command_text

## TosCommand

频率 1/s

header

tos_commands_info

## TaskState

频率：10/s  584个

header

task_mode

command_id

## RemoteEnvironment

频率 10/s 558

### header

### gantry_status

cps_guide_cm

spreader_horizonal_position_mm

spreader_size

### crane_status

* spreader_lane
* is_working
* spreader_size
* spreader_lane_old
* spreader_speed
* netload

# 指令

阅读antenna中相关proto，了解指令类型与作业流程

## 通过解析msg包了解流程

找一段时间的msg解析观察 指令 状态 和一些需要关注的值，最好能找出来统计一下

最少对整个流程得有大概的认识

# 目前的目的

能够通过解析接管时的信息知道接管发生时所处的状态（阶段）

![f06be0c1-1d07-47f5-a8ae-44cd9b0b373f](/home/caofangyu/me/f06be0c1-1d07-47f5-a8ae-44cd9b0b373f.jpg)

————————————————————————————————————————————————————————————

# 最终的目标

能够通过数据分析出接管发生的原因（可能是出于替代（减少）人工的想法）

### 我的问题

怎么在Jenkins中找到自己的构建

## 数据可视化

### 在容器外运行容器内指令？

关联pick_bag.py

了解docker exec

### 另一种方式：通过在数据平台页直接运行？（传入日期等信息）

—————————————————————————————————————————————————————————————————————

—————————————————————————————————————————————————————————————————————

# 消息提示

如果检测虚拟机里面的企业微信消息

然后在Linux中给个弹窗

--------------------------------------------***---------------------------------------------------------------------------------------------------

-------------------------------朴素的手动分割线--------------------------------------------------------------------------------------------

--------------------------------------------***---------------------------------------------------------------------------------------------------数据平台

### 目前网页上统计数据以 当前时间 为分界线

## 必要字段

record_list：

* timestamp_sec

* text

* take_over

* take_over_reason

--------------------------------------------***---------------------------------------------------------------------------------------------------

-------------------------------朴素的手动分割线--------------------------------------------------------------------------------------------

--------------------------------------------***---------------------------------------------------------------------------------------------------

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

（message文件格式应该是分段的，每段开头是8位的unsignedlong，记录本段数据长度    ）

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

​                        车辆

​                            |

​                         data

​                            |

​            record_list + loc[]

​    record_list采用字典形式存放每辆车的batch_record

   message_list同样

#### 如何减少判断？

# 2020/1/25

影响时间复杂度的好像更多是对字典的增删元素以及判断

判断可以通过预设列表消除。

## 两种方法的效率比较

设文件数为m,record_list数目为n

### 第一种

将数据全部读出来，最后再去比较

每个数据文件读一次，最后遍历一次，相当于每个文件遍历两次

读2m次文件

### 第二种

根据标题中的时间信息筛选文件，对于每个record_list，读一次文件。

需要读n次文件。

## 1补全字典初始化  done

## 2面向对象改造

先写好三个类，record，bag，bagParse

### Record

#### 成员：车辆名，日期，根据名字和日期所匹配的所有文件路径(按时间排序)

#### 方法：匹配路径   解析record文件

### Bag

#### 成员：车辆名，日期，根据名字和日期所匹配的所有文件路径（按照时间排序）

#### 方法：从文件名中提取时间信息 根据路径解析msg文件。

### BagParse

把我的SS代码面向对象一下，这个可能要花点时间

把一些常用的功能写成公共函数，可以增加参数使其适用性更广泛

## 3在recordItem中新增一个字段，字段信息从msg中提取（目前为是否动态接管，判断速度是否为0？）

需要根据时间匹配bags中的数据之后，读取信息，再将信息填到record中，发送出去

# 2021/1/26

查看文档，protobuf里面的message对象怎么复制或者删除。完善update_record函数

目前的程序执行完成用了大概一个多小时，好消息是没有报错，坏消息是好消息的补集。

## 1record 采用字典形式存放所有车辆数据

遍历目录来取得当前车辆的列表

## 2根目录改成可以配置的方法（参考ApolloAuto/apollo）

## 3对关心的参数配置一个列表（类似type_list），记录类型与关键值（如timestamp这种）

## 4 如何发送文件

## 面向对象的问题：

~~如何配置列表或者字典来维护需要关心的消息类型，没有好的想法，如果把类型名作为key，是否把类名作为value可以直接用dict[key]来实例化对象（没有理解msg_define中的字典）~~

---> 可以

## 我的问题

### 类和函数的命名有点丑

### 文件处理速度还是很慢，一直没有改善。

认真看下代码，不用从每个unit里获取时间，直接遍历更上层的时间列表。

### 代码虽然看起来面向对象了，但是函数的参数更多了，感觉函数的位置和参数并不是很合理，虚假的面向对象

# 2022/1/27

## 优化时间

1. 直接保存了需要读取的msg文件数据，省去了每次打开关闭文件的操作。
   
   时间从1个多小时减少到了半小时左右把

2. 目前的结构为从bag_index里面每次读一个chunk，从chunk中读文件类型，如果符合在建立对应类型的对象提取数据
   
   考虑：
   
   根据message_bag.proto文件，
   
   bag_index中的每个units中的data_header中包含message_type，同时units中也有message_data_offset和data_length
   
   所以：直接使用bag_index.units[index]判断类型并且读取数据。省去解析bag_chunk的过程。

​        用process_units代替了next_chunk和process_chunk函数。

​        时间~~大概是~~~依然是半个小时

         从bag_index中直接读取时间，然后先判断时间再判断类型，但是效率并没有显著提升。

3. 应该如何正确的面向对象

## 遇到问题时进行统计

对涉及到批量处理的地方，在测试的时候最好统计一下文件数目等比较重要的数量信息

进行时间效率的分析时，也尽可能把每一步的时间（间隔）打印出来，方便分析，找到重点。

# 2022/1/28

## 完善打印时间的程序

对于数值较小的时间，乘以一个倍率来打印

尽量细化到每一个步骤之间打印一次。

## 使用二分法来优化时间

bag_index中的时间数据应该是顺序排列的，尝试用二分法找到想到的数据区间。

如果不用二分，也可以根据实际情况来优化，一个bag_index大概是一分钟的时间数据，根据record_time与文件名的差值可以直接给index设置初值，再去遍历（or查找）

## *打印时间后发现占用时间最大的是读msg文件（get_msg_file）

重写之前的程序对比一下。

我超，不读完整msg，7s干掉

## 1 发送batch_record消息

### 1.1 测试post能否成功

所有record放在一个batch里面

如果将现在的record添加到batch_record里面

### 1.2 修改proto，添加关心的数据类型

目前测试是localization中的坐标数据(utm_x?)

### 1.3  面向对象一哈

## 2 添加消息队列

对每个消息，需要采集目标时间范围内的一个区间

再确认一下对不对。

## 3 二分法优化

## 1 解决一个时间点可能涉及到两个msg文件的问题

## 2 整理一下代码，每个类可以单独建立一个文件。

## 3 新加一个类，msg_analyzer,用于处理数据文件。

干嘛的：

我觉得是 用来处理并且存储一个record_list对应的所有数据的

考虑到一个record_list的时间区间可能会对应两个msg文件。

一个msg文件对应一个analyzer对象好还是一个record_list对应一个analyzer对象好

后者把。

### 修改BagParser类

done

### msg_analyzer

成员：字典{类型名：数据list}

#### 方法：

#### 处理unit：

参数： 文件路径 unit

输出：对应的类型对象（或者再处理，可以再写函数）

## 4 如何用字典把数据关联起来，方便管理

## 5 考虑建立一个配置文件，方便后续扩展和改动。

## 2022/2/11

## scripts/compress_bag.py

对需要压缩的数据类型使用zlib进行压缩。不知道什么时候进行解压。

## 2022/2/16

尝试改的过程中 优化一下代，增加一点可读性。我现在看着自己的get_path都脑壳疼

## fabudata里面存在命名错误的数据

## 尝试发送单个小文件：

done

# 2022/2/17

应该把BagParser里面的updata整合到get_data里面，用dict统一处理

# 2022/2/22

需要检测 driverlesses == true 

之后去更改相应配置

参照fabupilot_config.py

![image-20220222145250582](/home/caofangyu/.config/Typora/typora-user-images/image-20220222145250582.png)

```
def common_setup():
    output("handle speicfic cases of common_setup"
           " onboard = {}".format(onboard))

    flag_path_base = 'modules/common/data/global_flagfile.txt'
    flag_path = flag_path_base
    if onboard or conf_without_custom_config:
        flag_path = os.path.join(".config", flag_path)
        output("flag_path = {} ".format(flag_path))
    # tensorrt version, based on machine arch: x86->7.0.0 aarch64->7.1.3

    trt_version = "7.0.0" if machine_arch == "x86_64" else "7.1.3"
    replace_and_append(
        src_path=flag_path,
        dst_path=os.path.join(CONFIG_TEMP_PATH, flag_path_base),
        criterias=["trt_version"],
        from_regexs=["\d\.\d\.\d$"],
        tos=[trt_version])

    if not onboard and Flags.config_for == "develop":
        src_path_base = os.path.join("modules", "common", "module_conf",
                                     "conf", "living_modules_conf.pb.txt")
        src_path = src_path_base
        if conf_without_custom_config:
            src_path = os.path.join('.config', src_path)
        dst_path = os.path.join(CONFIG_TEMP_PATH, src_path_base)
        # replace_and_append(
        #    src_path,
        #    dst_path=dst_path,
        #    criterias=["CAMERA"],
        #    from_regexs=["CAMERA"],
        #    tos=["COMPRESSED_CAMERA"])
        replace_and_append(
            src_path,
            dst_path=dst_path,
            criterias=["endpoint"],
            from_regexs=["\d+\.\d+\.\d+\.\d+"],
            tos=["127.0.0.1"])

def replace_and_append(src_path,
                       dst_path=None,
                       criterias=None,
                       from_regexs=None,
                       tos=None,
                       append=None,
                       insert=None,
                       node_regex=None,
                       node_start_line=None,
                       node_end_line=None,
                       node_replace_in_copy=False):
    if not os.path.isfile(src_path):
        output("replace_and_append return src_path \"{}\" doesn't"
               " exist.".format(src_path))
        return
    if not dst_path:
        dst_path = os.path.join(CONFIG_TEMP_PATH, src_path)
    if criterias is not None:
        if not (len(criterias) == len(from_regexs) == len(tos)):
            raise Exception(
                "Lens of criterias, from_regexs and tos must be equal: %s" %
                (dst_path))
    if (os.path.islink(dst_path)):
        os.unlink(dst_path)
        src_file = open(src_path, 'r')
        conf_file = open("%s.bak" % dst_path, 'w+')
    else:
        src_file = open(dst_path, 'r')
        conf_file = open("%s.bak" % dst_path, 'w+')
    if insert is not None:
        conf_file.write(insert)
    if node_regex is None:
        for line in src_file:
            origin = line
            line, show_info = edit_line_with_regex(dst_path, line, criterias,
                                                   from_regexs, tos)
            conf_file.write(line)
            if show_info and line != origin:
                # if show_info:
                output("{} : {} -> {}".format(dst_path,
                                              origin.strip(), line.strip()))
    else:
        assert(node_start_line is not None and node_end_line is not None)
        buffer = []
        is_in_node = False
        is_target = False
        for line in src_file:
            if not is_in_node:
                if re.match(node_start_line, line) is not None:
                    is_in_node = True
                    buffer.append(line)
                else:
                    conf_file.write(line)
                continue
            elif re.match(node_end_line, line) is not None:
                buffer.append(line)
                if is_target and node_replace_in_copy:
                    # dump buffer once first as original
                    for buf_line in buffer:
                        conf_file.write(buf_line)

                # dump buffer
                for buf_line in buffer:
                    origin = buf_line
                    if is_target:
                        buf_line, show_info =\
                            edit_line_with_regex(dst_path,
                                                 buf_line, criterias,
                                                 from_regexs, tos)
                        if show_info and buf_line != origin:
                            output("{} : {} -> {}".format(dst_path,
                                                          origin.strip(),
                                                          line.strip()))
                    conf_file.write(buf_line)
                is_in_node = False
                is_target = False
                buffer = []
                continue
            else:
                buffer.append(line)
                if re.search(node_regex, line) is not None:
                    is_target = True
                continue
    src_file.close()

    if append is not None:
        # print("%s : %s" % (dst_path, append))
        conf_file.write(append)
    conf_file.close()
    if os.path.isfile(dst_path):
        os.remove(dst_path)
    os.rename("%s.bak" % dst_path, dst_path)
```

# 2022/2/28

## write log

把write log整理一下。包括语句的格式，错误的类型。

统一一下方便查找，定位。

重要的信息：包的数量，各种错误信息。

把整个过程捋一捋⑧

# 2022/3/14

检查新脚本的运行时间。

### old:

[main]total_record_list:488 
[main]process use :5763.485047 s 

### new:

[main]total_record_list:488
[main]process use :1451.712782 s

**0312**

new

[__main__]total_record_list:638
[__main__]process use :4484.862074 s

old

[main]total_record_list:638
[main]process use :7649.830548 s

# 2022/5/9

## c++

std::funtion

# 2022/5/10

## c++

gflags库

```
无人化修改配置
文件：modules/active_safety/conf/active_safety_config.pb.txt
内容：
搜索 use_planning_v3，将false改成true
搜索 safe_dist_checker_config，把下边的enable: false修改为enable: true
搜索 vision_lane_checker_config，把下边的enable: false修改为enable: true

文件：modules/perception_v2/conf/crane/crane_process_config.pb.txt
内容：搜索tmp_test_correct_crane_status，true改为false

文件：modules/perception_v2/conf/perception_camera.conf
内容：搜索--dag_config_path，dag_port_camera.config改为dag_port_camera_object.config

文件：modules/perception_v2/conf/obstacle/lidar/cnnseg_v2_truck_hesai40_velo16_config.pb.txt
内容：config_file: 无人化使用 resources/perception/models/deep_lidar/mxnet_models/truck_rs32_velo16/lidar_fire_howo_tail-50_v1.5.1_config.conf

文件：modules/perception_v2/conf/obstacle/lidar/ray_segmentor_config.pb.txt
内容：enable_static_low_x_filter配置项 无人化为false

Test Plan:  测试

Reviewers: zhengtu, tangwenjian, xiezhongjian, qianwei, wangpeng

Reviewed By: xiezhongjian, qianwei, wangpeng
```

# 2022/5/11

## c++

static_cast<>

lambda表达式

# 工作记录

## 20220613 周一

### 完善统计5G超时分布的python脚本

主要内容：

1. 从指定日期的log中收集5G超时数据，保存在sqlite数据库中。
2. 更新数据库中的数据：根据时间从bag中读场景信息（scene)
3. 画出5G超时数据分布图，包括时间分布与场景分布

修复之前一个脚本的bug，该脚本用来统计数据回传丢包的情况

### data_analyzer：

合并data_collect分支

修改main函数和shell脚本，暂时不使用fire库，使用argparse进行命令行参数的解析

## 20220614 周二

### data_analyzer:

南通现场测试：

车辆：nbtyd1

问题：

modules/tools/data_analyzer/data_collector.py中引用了不需要的库

line7:  import tqdm  需要删除

模块不能自启，需要修改module_conf

目前的版本后台启动模块不需要使用start

内容：

统计5G超时数据，统计模块CPU占用率情况

使用takeover_message作为退出自动驾驶事件

修复现场测试发现的问题

### 5G超时统计脚本：

修复一些bug

增加log_root参数，现在支持对南通港口数据进行处理，默认为梅山港数据

整理上传南通港06.11，梅山港06.06，06.07统计数据到企业微信文档

重构数据处理及绘图代码，为并入data_analyzer做准备

## 20220615 周三

###  data_analyzer & 5G超时统计

合并5G超时统计到data_analyzer中。

5G超时统计增加绘制延迟分布柱状图

与陈彦冰讨论数据回传检查的细节，确定数据回传检查需求具体内容

## 20220616 周四

#### 5g_delay分支： 重写update_scene函数

现在直接在线上把scene_type存到了数据库中，重写update_scene函数来更新PingData

修复检测不到log文件时会直接挂掉的问题

解决绘图时注释文本位置不正确的问题

## 20220617 周五

### 5g_delay分支：

#### 重构超时数据处理代码

[修复检测不到日期文件夹会自动退出的bug，现在使用同一个db文件存储数据，所有对数据库的操作封装在event_db中](http://git.fabu.ai/fabupilot/fabupilot/commit/38cec03c137fe5fec8b95925ccdc2405d40d9c4a)

优化读超时log代码，每次读log文件时增量读取，每次最多处理1000条记录进行提交

#### 在车端服务器上测试版本，修复问题

## 20220620 monday

### 绘图函数：

增加绘制指定日期所有车辆数据的功能 使用-t date -f folder来执行。

小更新：

* 给文件名和图表标题增加车辆日期信息
* 增加logger,保存日志信息到ecs.log中
* 解决图标信息展示不全的问题，解决X轴标签过长重叠的问题

增加统计功能：统计每辆车每天运行的时间，统计每辆车平均每小时超时次数，发送到企业微信

## 20220621 tuesday

data_analyzer：

修改scene字段保存方式，不在存储时进行中英文转换，直接保存原内容

### 绘图

重构绘图代码，使用EcsData类处理并保存数据，使用Plotter类完成绘图和统计功能。

删除重复和无用代码，统一对单车数据与多车数据的处理，使用Plottr类完成全部功能

新增绘制延迟分布散点图，横轴为时间，纵轴为延迟

### 脚本

完成监控模块cpu占用的脚本，放在scripts中

## 20220622 Wednesday

### 绘图

优化绘图代码，增加分辨率，修改字体，调整颜色，让显示更清晰

修改延时统计直方图X轴下标，现在为`[0-30ms] [30-100ms][100ms-200ms] [200ms-300ms][300ms-500ms] [500ms-1s], 1s以上，接管`

延时统计改为每次Ping数据为一次记录，此前为4次统计为一条，修改相关的统计与绘图代码

按要求输出延时统计数据，内容包括 延时平均值，延时最大值，上述下标所占比例，丢包比例，支持单车、多车统计，多车时既输出单车数据，也输出总的统计数据。

统计单并输出一天记录中场景记录的数量

### data_analyzer

优化读ecs log文件逻辑，改成增量读取



## 20220623 Thursday

### data_analyzer

1. 无人化场景延迟数据解析与更新
   1. 解析
   
      从无人化车辆的ecs log中读取数据储存到db中
   
   2. 更新
   
      1. 解析bag数据存储index到数据库中，利用该数据库寻找并更新延迟数据的场景
      2. 根据时间找相应的bag，解析planning_info得到scene更新数据中场景字段

2. 修复没有使用lru_cache缓存的问题，修复新版本读ecs log文件会挂掉的问题

## 20220627 monday

### 5G超时检测&绘图

修复定时脚本运行失败的bug

统一db文件命名：现在所有存储ping_data的db文件名字为：howoxx-2022xxxx.db（日期为8位没有不用'-'连接格式）

1. 新发版本本地测试，实车测试
2. 数据回传check脚本，检查recordF和recordB,固定执行，发送到微信群
   1. 无人化路径：/onboard_data/bags/meishangang_driverless_v2
   2. 从/fabudata读取recordB recordF中无人化数据scp到本地，再与/onboard_data上数据对比，检查回传漏包情况
3. ~~5G延时统计，输出到html中~~放弃，改为使用reportlib生成pdf

## 20220628 tuesday

查到recordF文件存在重复上传的情况（eg /fabudata/howo31/20220617/0845/recordF，/fabudata/howo31/20220617/1546/recordF），输出recordF增加去重，recordF改为每天更新前三天的数据

### 5G超时检测&绘图

~~增加Pdf类，用于输出pdf文档。~~改成使用python-docx生成word文档

将场景延时分布改为用表示显示，调整图片大小让图表能在Word上完整显示

修改输出文档格式与内容，首先输出总的统计表格，之后按照表格-三场景延时分布图片的顺序排列

## 20220629 Wednesday

南通港现场测试：

fabupilot_config未配置living_modules

monitor不显示data_analyzer模块，重启无效，未查出原因

data_analyzer启动后log不刷新

问题疑似为版本生成失败/错误

### 5G超时检测&绘图

延时数据统计表格中加入总数据一栏，增加运行时长统计

修改 无人化场景延迟数据解析脚本，现在每天主动更新howo21车的场景数据，并发送doc文档到企业微信。

## data_analyzer

修改读bag方式：现在读bag时把数据索引存到sqlite数据库，一个bag对应一个db文件，直接使用sqlite查询数据。

## 20220630 Thursday

输出docx中不再放入图片

doc中将无人化数据与混线数据分开统计，先显示无人化数据，再显示混线数据	



优化bag.py：按要求修改bag.py代码，大致内容如下：

去掉tqdm,删除冗余的函数，对db文件操作统一使用utils中SqliteDB接口，将db文件存储在bag目录日期文件夹内，现在表名为MsgUnit

检查混线场景数据量少的问题：

对比db文件内场景数量一致，确认是场景数据没有存储下来





主要原因是发送的Planning_info消息中大部分没有scene字段

查看data_analyzer中消息的处理逻辑（message.py），认为没有问题

## 20220704

### 5g超时检测&doc

#### 离线场景更新脚本

离线更新混线场景数据

混线场景数据使用批量更新，处理一个db文件时间缩短到3分钟左右。

将存储无人化bag数据索引到db，以及使用存储的索引更新场景的函数也改为批量存储与更新



### 现场测试

南通现场测试，一切正常

## 20220705

混线测试车辆从howo24 howo26 howo29 howo30 howo25 更换成 howo14，15，16，29，30，修改拷贝log脚本车辆名以及对应的IP地址

1. data_analyzer 合并最基础的部分 db数据收集，collect先注释不做。 
2. 5g delay部分合并到master

## 20220706

### data_analyzer

重构bag.py，将所有对单个包的操作放到bag_manager类中，有bag_manager提供对外的接口

测试bag.py功能：

 修复没有检测db文件夹的问题，修复两个数据类型的错误

使用宁波现场测试的数据测试bag.py流程，能正常存储bag索引到db文件，并根据提供的时间搜索指定类型的数据。



判断文件夹是否可写入，不可写入时db存放到/tmp中

新接受消息task_state，查看对cpu影响
