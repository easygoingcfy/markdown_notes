# 指令

## command_monitor(c++)

### GetCommandType(command_monitor_util.cc)

* 判断rc_msg为空
  
  * true: return

* 比较时间param_obj->stat.timestamp - rc_time  kMaxMsgDelay(3.0)
  
  * 小于3.0（远程控制消息没有延迟（delay））
    * 判断RCmsgBelongPreFinishTask
      * true：MOVE_TO_POSITION
        * false：GetCommandTypeFromRcmsg(*rc_msg);
  * 大于等于3.0      有延迟
    * 判断TaskOverDetermine(*param_obj)          任务是否结束
      * true：MOVE_TO_POSITION
      * false: 使用chassis_msg 和 taskstate_msg辅助判断
        * chassis_msg 和 taskstate_msg不为空且chassis_msg->driving_mode() == Chassis::COMPLETE_AUTO_DRIVE)
          * taskstate_msg->task_mode() ： **FINISH**  && command_id 一致（rc_msg） && rc_time < tt_time    
            * 类型为GetCommandTypeFromRcmsg(*rc_msg)中状态的下一个阶段：
              * MOVE_VIA_CRANE_CPS  : WAIT_CRANE_OFF
              * MOVE_VIA_GANTRY_CPS : WAIT_GANTRY_OFF
              * MOVE_TO_GANTRY : WAIT_GANTRY_COME
              * MOVE_TO_CRANE : WAIT_CRANE_OFF
          * taskstate_msg->task_mode() : **RUNNING** && command_id 一致（rc_msg） && rc_time < tt_time
            * 判断GetCommandTypeFromRcmsg(*rc_msg)：
              * WAIT_GANTRY_OFF || WAIT_CRANE_OFF ： MOVE_TO_POSITION

### CommandSummary（command_monitor_processor.cc）

* 判断(param_obj_pre_.stat.timestamp > 0) 
  
  * HasTosIdChanged() || param_obj 与param_obj_pre的**command_type**不相同
    
    * 设置vehicle_name、command_type、command_end_time、command_duration
    
    * 判断is_test:
      
      * true：对所有错误类型执行GET_ERROR_TYPE
      * false：对所有错误类型执行UpdateRecordStr，如果采集到错误信息，执行AppendDrivingRecord

### TaskSummary（command_monitor_processor.cc）

* 判断(param_obj_pre_.stat.timestamp > 0) 
  * HasTosIdChanged() || param_obj 与param_obj_pre的**command_type**不相同
    * 判断ShouldAddCommand()
      * 加入command_summary_ `*task_summary_.add_command_summary() = command_summary_`
      * 清理储存的mutable_command_summary(不确定是前一个还是唯一的一个)
      * 设置桥吊id
    * 判断HasTosIdChanged() 
      * 设置vehicle_name  crane_id  mutable_command_context()    
      * task_summary_.mutable_command_context()->clear_type()
      * 检测异常
      * task_summary_.Clear();_
    * _command_summary_.Clear();

### StatUpdate()

#### ParamObjStatUpdate()        未标注_pre的全是对param_obj操作

* 判断param_obj_pre_.stat.timestamp < 0 && param_obj_.stat.command_type ： MOVE_TO_POSITION
  * param_obj_pre_.stat.command_type = param_obj_.stat.command_type
* command_type不相同
  * 设置param_obj_.stat
* 判断task_summary_.command_summary_size() == 0
  * 判断param_obj_.stat状态是否为二次对位：MOVE_VIA_GANTRY_CPS || MOVE_VIA_CRANE_CPS
    * true：判断rc_msg->tos_command_context().has_container_size()
      * true：设置param_obj_.stat.adjust_con_size
* GetCommandBeginWithTakeover();
  * 根据状态（command_type）执行函数
    * 前往吊具（MOVE_TO_CRANE || MOVE_TO_GANTRY）
      * GetVehicleIsStatic();
    * 等待龙门吊（WAIT_GANTRY_COME）
      * GetLocErrorBeginTime();
      * GetGantryOfflineBeginTime();
    * 等待作业完成（WAIT_GANTRY_OFF  ||  WAIT_CRANE_OFF ）
      * GetSecondAdjustEndPoint();

#### SummaryStatUpdate();

* 判断command_type 不相同
  
  * command_summary_.set_command_begin_time(param_obj_.stat.timestamp);
  * mutable_command_stat()->set_has_take_over(false)

* // tos_command_context update

* 判断command_summary_和rc_msg __`!command_summary_.has_command_context() && rc_msg != nullptr`
  
  * 更新tos_command_context :`*command_summary_.mutable_command_context() = rc_msg->tos_command_context()`

* // crane_id for command_summary update

* 判断crane_id和cd_msg `!command_summary_.has_crane_id() && cd_msg != nullptr`
  
  * 判断状态（command_type）（确定是龙门吊还是桥吊）
    
    * MOVE_TO_CRANE || MOVE_VIA_CRANE_CPS || WAIT_CRANE_OFF 且target_crane有效（不为空且有id）
      
      * set_crane_id
    
    * MOVE_TO_GANTRY || WAIT_GANTRY_COME || WAIT_GANTRY_OFF 且 target_gantry有效（不为空且有id）
      
      * set_crane_id

* // has_take_over for command_summary update

* 判断 command_summary_.command_stat().has_take_over() == false &&

* !param_obj_.stat.cmd_begin_with_take_over && (chassis_msg != nullptr) && 

* (chassis_msg->driving_mode() == Chassis::EMERGENCY_MODE)
  
  * take_over = true `command_summary_.mutable_command_stat()->set_has_take_over(true);`

### AbnormalTypeDetermine(is_test)

异常大部分条件为 !CommandHasError() && abnormal_type_determine.HasSystemTimeError() 下面只给出具体错误名

* 实例化command_monitor::AbnormalTypeDetermine对象abnormal_type_determine
* 判断系统时间异常SYSTEM_TIME_ERROR
  * **CommandSummaryAddAbnormal**(CommandStat::SYSTEM_TIME_ERROR, &abnormal_value);
* 判断param_obj_.stat.command_type
  * MOVE_TO_CRANE || MOVE_TO_GANTRY ||  WAIT_GANTRY_COME || 
  * MOVE_VIA_CRANE_CPS || MOVE_VIA_GANTRY_CPS || WAIT_CRANE_OFF || WAIT_GANTRY_OFF
    * 判断tos 指令错误 TOS_COMMAND_ERROR
      * **CommandSummaryAddAbnormal**(CommandStat::TOS_COMMAND_ERROR,&abnormal_value);
  * MOVE_TO_CRANE) || MOVE_TO_GANTRY
    * 判断first adjust unfinished error  FIRST_ADJUST_UNFINISHED_ERROR    
      * **CommandSummaryAddAbnormal(**CommandStat::FIRST_ADJUST_UNFINISHED_ERROR,&abnormal_value);
  * WAIT_GANTRY_COME
    * 判断!param_obj_.stat.cmd_begin_with_take_over && 位置错误 LOCALIZATION_ERROR
      * **CommandSummaryAddAbnormal**(CommandStat::LOCALIZATION_ERROR,&abnormal_value);
    * 判断!param_obj_.stat.cmd_begin_with_take_over && 龙门吊离线错误 GANTRY_OFFLINE_ERROR
      * **CommandSummaryAddAbnormal**(CommandStat::GANTRY_OFFLINE_ERROR,&abnormal_value);
  * MOVE_VIA_CRANE_CPS || MOVE_VIA_GANTRY_CPS
    * 判断!param_obj_.stat.cmd_begin_with_take_over && EARLY_SPREADER_ERROR
      * **CommandSummaryAddAbnormal**(CommandStat::EARLY_SPREADER_ERROR, &abnormal_value);
* 类型不相同（param_obj_.stat.command_type != param_obj_pre_.stat.command_type） &&
* param_obj_.stat命令类型为：WAIT_CRANE_OFF || WAIT_GANTRY_OFF
  * 判断控制错误 CONTROL_ERROR
    * **CommandSummaryAddAbnormal**
* 判断param_obj_.stat.command_type
  * WAIT_CRANE_OFF || WAIT_GANTRY_OFF
    * !param_obj_.stat.cmd_begin_with_take_over && 桥吊移动错误CRANE_MOVE_ERROR
      * **CommandSummaryAddAbnormal**
  * MOVE_VIA_CRANE_CPS || MOVE_VIA_GANTRY_CPS || WAIT_CRANE_OFF || WAIT_GANTRY_OFF
    * 判断远程环境信息丢失错误REMOTE_ENV_MSG_LOST_ERROR
      * **CommandSummaryAddAbnormal**
* 打印信息(record_msg)

### abnormal_type_determine.cc

#### HasSystemTimeError(std::string *abnormal_value)

* 判断lidar_msg == nullptr || lidar_msg_pre == nullptr
  * true: return false
* 用SystemTimeDetermine判断各模块（lane,radar,chassis,gnss,rc）时间是否正确：
* SystemTimeDetermine(lane_msg, lane_msg_pre, abnormal_value) || ......
  * true: return true

#### HasTosCommandError()

## remote_control

RemoteControl：antenna发给planning的消息

RemoteControl不会一直发送，只有在车辆动的时候才发（大概？），tos_command会一直发，但是信息少很多。

planning应该是车端的自动驾驶

大致流程是tos(码头)会发指令给到antenna（tos_command），antenna会做一个处理（细化或者...），发送给到planning

```
syntax = "proto2";
package fabupilot.antenna;

import "modules/common/proto/header.proto";
import "modules/common/proto/geometry.proto";
import "modules/msgs/routing/proto/routing.proto";

message RemoteControl {
  optional fabupilot.common.Header header = 1;

  // One control command per message. Multiple commands should be delivered  in
  // multiple messages
  oneof command {
    StopVehicleCommand stop_vehicle_command = 2;
    TuningTerminalCommand tuning_terminal_command = 10;
  }

  message TosCommandContext {
    enum ActionType {
      UNKNOWN = 0;
      LOAD = 1;
      UNLOAD = 2;
      MOVE = 3;
      CHARGE = 4;
    };
    //指令ID，此指令ID（不确定是不是这个）与planning返回给antenna的ID是匹配的
    optional int32 tos_command_id = 5;
    optional ActionType action_type = 1;
    enum WiType {
      WI_UNKNOWN = 0;
      WI_LOAD = 1;
      WI_DSCH = 2;
      WI_YARD = 3;
      WI_GOTO = 4;
    };
    这个是tos发到antenna的指令类型
    optional WiType wi_type = 11 [default = WI_UNKNOWN];
    //CommandType包含了一般的作业流程，同时应该也是需要判断的车辆状态
    enum CommandType {
      STOP = 1;
      //1.前往龙门吊（桥吊）
      MOVE_TO_GANTRY = 2;
      MOVE_TO_CRANE = 3;
      MOVE_TO_POSITION = 5;
      MOVE_VIA_CRANE_CPS = 6;
      //2.等待龙门吊（桥吊）到达 ： 可以用这个判断是车先到还是吊具先到，如果是吊具先到也会进入这个状态，但是会很快结束（应该）
      WAIT_GANTRY_COME = 7;
      //3.进行二次对位
      MOVE_VIA_GANTRY_CPS = 8;
      MOVE_TO_STACKER = 9;
      WAIT_STACKER_BIND = 10;
      MOVE_VIA_STACKER = 11;
      MOVE_TO_CHARGE = 15;
      //前往锁亭装锁 码头面作业可能用到
      MOVE_TO_LOCK = 17;
      MOVE_TO_UNLOCK = 18;
      MOVE_TO_CASC = 19;
      MOVE_TO_NEXT_LOC = 20;
      MOVE_TO_STS = 21;
      MOVE_TO_REPOSITION = 22;
      MOVE_TO_FIRST_NEXT_LOC = 23;
      //4.进行装卸箱：包含几个过程：
      //4.1.车辆检测是否满足3个条件：吊具高度，锁状态，车自身箱子状态（？记不清了）
      //4.2.满足条件后会等待（可能一段时间），是否antenna发新的指令，如果有，会结束这个状态，执行新的指令
      //4.3.如果没有收到新的指令，会自己去最近的休息区（不确定）
      WAIT_GANTRY_OFF = 101;
      WAIT_CRANE_OFF = 102;
      STOP_CRANE_DETECTION = 103;
      WAIT_STACKER_OFF = 104;
      WAIT_CHARGE_OFF = 105;
      //前往锁亭卸锁，码头面作业可能用到
      WAIT_LOCK_OFF = 106;
      WAIT_UNLOCK_OFF = 107;
      MANUAL_CHECK = 201;
      CANCEL = 4;
      RESET = 202;
      WAIT_PAUSE = 203;
    };
    optional CommandType type = 8;
    enum DeviceType {
      UNKNOWN_DEVICE = 0;
      CRANE = 1;
      GANTRY = 2;
      STACKER = 3;
    };
    optional DeviceType device_type = 9 [default = UNKNOWN_DEVICE];
    optional string destination_id = 2;
    optional string container_id = 3;
    enum ContainerSize {
      SIZE_UNKNOWN = 0;
      SIZE_20_FEET = 1;
      SIZE_40_FEET = 2;
      SIZE_45_FEET = 3;
      SIZE_BINDED_TWIN = 4;
    };
    optional ContainerSize container_size = 6;
    optional int32 container_weight = 10;
    enum ContainerPosition {
      UNKNOWN_POSITION = 0;
      FRONT = 1;
      MIDDLE = 2;
      BEHIND = 3;
    };
    optional ContainerPosition container_position = 7;
    //可能是双箱相关，车辆装集装箱的方式
    enum TwinType {
      ALONE = 0;   // This command is a stand-alone command
      FIRST = 1;   // First command in a pair
      SECOND = 2;  // Second command in a pair
    }
    optional TwinType twin_type = 12;
    enum Priority {
      UNSET = 0;
      LOW = 1;
      NORMAL = 2;
      HIGH = 3;
      URGENT = 4;
    }
    //优先级，码头面作业判断：低优先级时先去引桥排队，高优先级时直接去桥吊
    optional Priority priority = 4;
    enum DestType {
      DEST_UNKNOWN = 0;
      DEST_DOCK = 1;
      DEST_YARD = 2;
      DEST_TEST = 3;
    };
    optional DestType dest_type = 13 [default = DEST_UNKNOWN];
  };
  optional TosCommandContext tos_command_context = 5;
  optional int32 command_id = 7;
}
//目前在用的两种指令之一：停车，一般是使用1，2
message StopVehicleCommand {
  enum StopPosition {
    UNKNOWN = 0;
    //自行去最近的停车场停车
    NEAREST_SAFE_POSITION = 1;
    //马上停车
    IMMEDIATE = 2;
    ROUTE_POSITION = 3;
  };
  optional StopPosition stop_position = 1;
}

//目前在用的两种指令之一：移动
message TuningTerminalCommand {
  //停车精度
  optional double stop_accuracy = 1;
  /* destionation: GOTO+point/id

  * rest area:NEAREST+ poi_tpye=rest
  * queue point:PASSBY + CR point + poi_tpye=queue
    */
      optional fabupilot.routing.LaneWayPoint lane_way_point = 2;
      message OffsetPoint {
    //offset:对位用到，1是二次对位，2是三次对位（好像还没用到）
    enum OffsetType {
      UNKNOWN = 0;
      BAR = 1;       // crane or gantry dist for second adjust
      SPREADER = 2;  // spreader dist for third adjust
    }
    optional OffsetType offset_type = 1 [default = UNKNOWN];
    optional double target_offset = 2;
    optional double offset_timestamp = 3;
      }
      optional OffsetPoint offset_point = 3;
    }
```

## remote_environment

主要包括header，gantry_status,crane_status

```
spreader_height_cm 吊具高度
bool is_target_crane 车对应的作业吊具为true，其他为false，可以用来定位吊具，但好像没什么用

spreader_horizonal_position_mm 龙门吊的水平偏移量，有港口（吊具）的PLC给出，精度可能有误差，一般云端（感知或者咱的啥）拿到会处理一下，补偿啥的。这个值基于龙门吊自己的一维坐标系
```

## task_state

planning回传给antenna的数据，主要包括header, task_mode,command_id

# fabu开发流程

1. 进入容器后，拉最新版本,拉最新版本，或者拉需要的版本（bash deploy/common/update_release.sh master/HEAD）
2. 写代码，自测
3. 提交的时候要保证工作区没有变动*大概是这个意思把。
4. 先提交到自己的分支，拿到版本号
5. 在master合并分支，写CR，同时JR上提交需求，禅道链接要放到CR summary中
6. 在custom.fabu.ai上生成版本，并进行测试（会转到jenkins）
7. build成功(./scripts/update_release.sh custom_builds/xxxxxx)后，进行自测，自测成功将版本和需求（怎么测，测什么之类的）发给测试，让测试测一测
8. 使用arc_land命令，会提交到Jenkins（Pipeline fabupilot-check-before-land）

### arc_land

```
./scripts/arc_land.sh 
-m modules_name  一个模块时
不确定模块名时自己查看帮助
```

## CR

使用命令arc diff --preview生成  *我也不懂

CR需要在summary中加上禅道（目前）的链接，否则会挂掉

主要也是编辑summary，然后选择Reviewers。

### cr出错

检查是否更新resources:

```
cd resources 
git pull
```

检查是否更新子模块

```
git submodule update
```

bazel clean

```
bazel clean
```

### login

每次使用arc diff --preview时会需要权限：执行arc install-certificate 生成一个API Token

可以自己执行

```
cp ~/.arcrc .   //这个好像没用
mv .arcrc ~  在本地执行
*******具体实现自己看deploy/dev_start.sh************
```

## JR

JR.fabu.ai

### 项目

DrivingEvent，属于集卡自动驾驶系统

### 模块

DrivingEvent，属于fabupilot

## custom.fabu.ai

代码初步完成后，

1. push到自己的分支（cfy），
2. 拿到自己的版本号，点击Reset
3. 会根据自己的版本好生成各个子模块的对应版本号，此时可以根据需要自己更改对应模块的版本号
4. 如果更改了子模块的版本号，点击update，没有-》5
5. 点击submit，会自动提交到jenkins（modules_name/custom_build）
6. 根据自己的版本号找到

## jenkins

i know ge p

大概是根据你的提交

按照指定的流程进行 检测 测试 构建版本 部署版本的

一个工具把

# DEV

遇到问题先确定有没有拉最新版本，有没有更新代码

## 更新子模块（不一定需要*）

遇到缺少文件的问题，如果生成配置，更新resources都没用，可能是没有更新子模块的问题。最好的办法是自己好好查看错误信息，跟着错误信息排查。

```
git submodule update
```

## 拉版本

```
./deploy/common/update_release.sh master/HEAD
```

## 模块

加载（目前使用的模块）注册在`config/modules/common/module_conf/conf/living_modules.pb.txt`里

如果里面不存在的模块引用了，就会出undefined modules:xxx的错误（在运行driving_event_test.cc时遇到）

### living_modules

message_service使用的，用来确认给哪些模块发消息。

```
config/modules/common/module_conf/conf/living_modules.pb.txt
```

# proto

在fabupilot项目中，根据proto文件生成了C和python文件是存放在/fabupilot/bazel-genfiles/modules中的，如果需要修改Proto文件也可以修改之后使用build生成相关配置

整个项目是基于bazel的，所以新增proto需要同时在bazel的配置文件（BUILD）中更新

## 新增proto文件

需要在BUILD中新增cc_proto_library (c++) 或者 Python的（百度一哈）

```
eg:
cc_proto_library(
    name = "notepad_log_proto",
    protos = ["notepad_log.proto"],
    deps = [
        "//modules/common/proto:header_proto",
        "//modules/common/proto:event_code_proto",
        "//modules/common/proto:module_proto",
    ],
)
```

需要修改配置

* modules/common/adapters/BUILD    cc_library中加入依赖

* modules/common/adapters/proto/adapter_config.proto  主要是新的message_type

* modules/common/adapters/message_adapters.h 需要包含的proto消息的C++编译文件头文件（xxx.pb.h），类型Python中的xxx_pb2.py，并在adapter命名空间中声明该消息的Adapter：
  
  * eg:
    
    ```
    #include "modules/msgs/notepad/proto/notepad_log.pb.h"
    
    using NotepadMessageAdapter = Adapter<fabupilot::notepad::NotepadMessage>;
    ```

* ```
  using LocalizationAdapter = Adapter<::fabupilot::localization::Localization>;
  ```

* 需要在BUILD中添加依赖，（modules/common/adapters/BUILD -> message_adapters.h）

* modules/common/adapters/adapter_manager.h 需要使用REGISTER_ADAPTER注册新增的proto消息，看起来只需要消息的类名就行
  
  * eg:
    
    ```
    (REGISTER_ADAPTER(NotepadMessage)
    ```

* modules/common/adapters/adapter_manager.cc 加入case(用来关联adapter.conf中定义的消息类型(NOTEPAD_LOG) 和proto消息类（NotepadMessage）)。
  
  * eg:
    
    ```
    case AdapterConfig::NOTEPAD_LOG:
    +        EnableNotepadMessage(config.type(), config.mode(),
    +                           config.message_history_limit());
    +        break;
    ```

* modules/common/driving_event/BUILD中添加新的依赖（handler）

### 问题

在adapter.conf里面定义的消息类型（比如MONITOR -> MonitorMessage， NOTEPAD_LOG -> NotepadMessage)是怎么通过adapter映射的?

 在modules/common/adapter/adapet_manager.cc里面，通过config.type（）进行配置。

## echo

记得编译，编译，编译

build build build

```
bazel build //modules/common/message/tools:echo_message
```

# 宁波出差事宜

1. # **流机网络访问**

- WiFi：DO NOT USE VPN；密码：fabu382764
- 浏览器访问：meishan.fabu.ai:1234
- 输入login账号，密码及otp码即可正常上网



