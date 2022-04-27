## 接管分析

## 对位有偏差

对面有偏差应该是司机主动接管的情况

- 在装箱或者卸箱时对位有问题（司机判断的？），司机主动踩刹车接管，装卸完成后又回到自动驾驶状态。

- > 可以观察车辆指令状态（装卸箱过程中），速度0，吊具高度变化，一般是二次对位失败时接管，此时吊具高度有一个范围。

  - ./scripts/message_service.sh play /fabudata/howo15/20220310/0828/howo15_2022_03_10_14_49_46_381.msg
  - ./scripts/message_service.sh play /fabudata/howo19/20220310/0828/howo19_2022_03_10_14_42_02_373.msg
  - ./scripts/message_service.sh play /fabudata/howo38/20220310/0825/howo38_2022_03_10_12_14_53_229.msg
  - ./scripts/message_service.sh play /fabudata/howo23/20220310/0823/howo23_2022_03_10_15_43_26_440.msg
    - 可以看到司机接管后主动倒车了。
    - ./scripts/message_service.sh play /fabudata/howo20/20220310/0811/howo20_2022_03_10_15_50_13_458.msg
  - ./scripts/message_service.sh play /fabudata/howo16/20220310/1103/howo16_2022_03_10_15_49_49_286.msg
    - 装第一个箱子时是自动驾驶，装第二个箱子的时候位置有问题，司机主动接管，倒车了，可以看到坐标变化。

- 到达装卸箱位置时，司机接管（不确定是车辆定位不准确或者司机个人原因）

  - ./scripts/message_service.sh play /fabudata/howo23/20220310/0823/howo23_2022_03_10_14_57_26_394.msg

## 交互不避让

> 有没有可能拿到其他车的planning（路径规划？）感觉要么是v2v的问题，要么是不在系统内的车辆。
>
> 所以本身planning也有问题（感知？ 测距不准确，有延迟      通信：信息传递不及时？planning没有及时更改规划）

有车开过来，planning没有控制减速或者停车的样子，司机直接踩刹车了。

- ./scripts/message_service.sh play /fabudata/howo15/20220310/0828/howo15_2022_03_10_10_13_46_105.msg
  - 从右边高速（相对）开过来一脸车，完全没减速直接过来的
  - 分析：引桥口自车前方有小车驶过，自车轨迹避让不及时
- ./scripts/message_service.sh play /fabudata/howo24/20220310/0928/howo24_2022_03_10_09_53_16_25.msg
  - 右拐时左侧车辆加速超过，车辆没减速
  - 分析：外集卡外道超车到自车前面

## 前端未响应

- ./scripts/message_service.sh play /fabudata/howo8/20220310/0854/howo8_2022_03_10_16_15_23_441.msg
  - 货物装箱之后，接管了，如果能看到龙门吊状态应该会好很多。
  - 分析：龙门吊未接入
- ./scripts/message_service.sh play /fabudata/howo14/20220310/0826/howo14_2022_03_10_16_00_29_454.msg
  - 应该是在卸箱子？龙门吊没有动静，司机自己开走了？
  - 分析：龙门吊未接入
- ./scripts/message_service.sh play /fabudata/howo25/20220311/0824/howo25_2022_03_11_17_10_35_526.msg
  - 桥吊作业结束，车辆行驶中接管，接管8s前有【drivers】惯导设备:INS570D: 未知异常状态, 请等待几分钟;感觉是司机接到消息去其他地方了？
  - 分析： 前端未响应

- ./scripts/message_service.sh play /fabudata/howo38/20220311/0831/howo38_2022_03_11_09_34_08_62.msg
  - 【control】紧急停车
  - 分析：左转进入7A箱区报远控停车

- ./scripts/message_service.sh play /fabudata/howo14/20220311/0825/howo14_2022_03_11_09_27_33_62.msg
  - 桥吊作业结束 - 【planning】规划正常：PLANNING_TASK_REMOTE_ASK_TO_STOP - 【planning】系统错误 - 【active_safe】紧急刹车
  - -【control】按规划要求紧急停车 - 接管
  - 分析：前端未响应


## 变道、转向、掉头

- ./scripts/message_service.sh play /fabudata/howo8/20220310/0854/howo8_2022_03_10_10_39_23_105.msg
  - 规划路径上有车，planning没有变车道，停车了，停了快10s，司机接管了
  - 分析：纵路左转横一路，自车路径上有集卡阻挡



## 异常刹停

有没有必要将Log的读取时间延长，从异常刹停看，车道线错误造成异常刹停这种原因能直接从log读取，并且确定问题。但常有时间是在接管前半分钟左右。

基本可以分为：

* 各种原因被怼停（包括 全局路径不合理 障碍物框误检  变道失败）
* 误检误报（包括 主动安全误报）
* 模块问题
  * planning:地图路线搜索失败 
  * vehicle：底盘问题（硬件，参数）  转向控制异常
  * antenna：网络超时 
  * localization：车道线错误





TRAJ_INPUT_ERROR_STATUS ACTIVE_SAFETY ERROR

```
[紧急刹车] 轨迹输入异常
```



 PLANNING_SYSTEM_ERROR PLANNING ERROR

```
系统错误: 目标点或自车位置非法，请求route异常-自车在路口范围内，不能请求route，请将集卡移到车道内 | cur lane is in junction.
```



被怼停(感知-障碍物感知-障碍物框误检)：

PLANNING_OBSTACLE_BLOCK PLANNING WARN

```
受xx方xxx米处栅格障碍物xxx障碍物影响, 停车等待
```



系统错误: 地图路线搜索失败- | （规划 / 决策 / 路径搜索失败）

PLANNING_SYSTEM_ERROR PLANNING ERROR:

```
系统错误: 地图路线搜索失败- | .
```



PLANNING_SEVERE_PASSES_BLOCK PLANNING WARN:

```
受前方17.989米处46号桥吊重关影响, 停车等待.
```



误检(主动安全-主动安全误报)：

TOO_CLOSE_TO_COASTLINE_STATUS ACTIVE_SAFETY ERROR

```
自车离海岸线MAP_PORT_EDGE过近，再过0.000000s，距离只有3.916179m
```

GRID_COLLISION_STATUS ACTIVE_SAFETY ERROR

```
[紧急刹车] 自车当前轨迹再过0.700000s,车头将与范围为0.003000的GRID碰撞
```



PLANNING_SET_EMERGENCY CONTROL ERROR



手刹异常(车辆-底盘硬件错误)

EPB_CONTROL_EXCEPTION VEHICLE ERROR

```
手刹控制异常,将触发规划紧急停车
```



底盘参数异常

PLANNING_SYSTEM_ERROR PLANNING ERROR：

```
系统错误: 处于紧急阶段-收到紧急停车指令 底盘参数异常，紧急停车
```



网络问题

ANTENNA_NET_EXCEPTION ANTENNA ERROR:

```
Antenna网络延时:可能失去连接，超时时间超过4000.000000 ms!!!, 请求主动安全停车
```



MODULE_TOPIC_DELAY ACTIVE_SAFETY ERROR:

```
[2022-04-11 18:28:58][当前人工驾驶] 模块消息延时:vehicle [CHASSIS] has delay 0.102442 with acceptable_delay 0.08
```



无变道空间

PLANNING_SYSTEM_ERROR PLANNING ERROR:

```
系统错误: 处于紧急阶段-无变道空间 
```





全局路径不合理（实际原因应该算 被怼停？司机主动接管）

PLANNING_LOW_SPREADER_BLOCK PLANNING WARN:



转向控制异常（）

EPS_ANGLE_EXCEPTION VEHICLE ERROR

```
转向控制异常,将触发规划紧急停车:
```



车道线错误（ 定位-定位纵向误差）

INPUT_VISION_LANE_ERROR LOCALIZATION ERROR

```
定位接收的车道线错误,将触发规划停车
```



信号异常（驱动 / 组合导航 / 组合导航信号异常）

INPUT_GNSS_UNSTABLE LOCALIZATION ERROR

```
定位接收的GNSS不稳定,将触发规划停车
```



PLANNING_SYSTEM_ERROR PLANNING ERROR:

```
系统错误: 车辆所在车道定位失败-沿当前路径无法定位自车车道 | Cannot locate ego lane along route,
```

 

- ./scripts/message_service.sh play /fabudata/howo37/20220311/0837/howo37_2022_03_11_16_05_08_447.msg
  - 【planning】受道路条件约束(PN051: 前方{1}米有路沿挡路)，等待通行，持续等待后司机接管
  - 分析: 横一路组合导航定位偏了导致被路沿怼停
- ./scripts/message_service.sh play /fabudata/howo30/20220311/0816/howo30_2022_03_11_13_42_13_325.msg
  - 【planning】受道路条件约束(PN060: 无安全轨迹)，等待通行
  - 分析：泊位直行被捆扎区域障碍物对停obs12758
- ./scripts/message_service.sh play /fabudata/howo37/20220311/0837/howo37_2022_03_11_13_04_08_266.msg
  - 【planning】受右前方inf米处阻塞影响，等待通行  - 接管 ，司机接管好自行开车前进
  - 分析：泊位直行被捆扎区域障碍物对停obs12816
- ./scripts/message_service.sh play /fabudata/howo30/20220311/0816/howo30_2022_03_11_10_37_13_140.msg
  - 【activeSafe】[紧急刹车] 规划轨迹延时
  - 分析：船头船尾设置planning 重启

- ./scripts/message_service.sh play /fabudata/howo32/20220311/0832/howo32_2022_03_11_10_18_53_106.msg
  - 【planning】[ STOP ]: 规划正常 ，车辆一直停止
  - 分析：路径规划失败，循环规划。（引桥远控停车，planning已经返回finish）