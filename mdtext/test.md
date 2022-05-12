

# arm3测试sqlite性能影响

test_sql:

22.7% - 24%

![image-20220511161227050](/home/caofangyu/.config/Typora/typora-user-images/image-20220511161227050.png)

只存储localization:

19.6%左右，存在向下跳变，有时候降到9%，play_bag也一起降

不存sqlite：（使用master：5f15268321fd005650b79e357dd8e3566a30b96c）

18%-20% 性能与只存储localization时接近

## 添加配置文件后：

### 存储的数据类型1

（REMOTE_CONTROL, DRIVING_RECORD,  TAKE_OVER_DRIVING_RECORD , PLANNING_INFO, LOCALIZATION,  MONITOR）

#### 结果

18%-20%左右。

![image-20220512104904893](/home/caofangyu/.config/Typora/typora-user-images/image-20220512104904893.png)

### 删除一些数据量大的数据

环境：arm3 使用bag: data/bag/howo38_2022_04_22_08_50_11_13.msg

删除的数据类型：COMPRESSED_CAMERA_HEAD_LEFT_PROTO, COMPRESSED_CAMERA_HEAD_RIGHT_PROTO,LIDAR_PACKET_MAIN, LIDAR_PACKET_HEAD_MID,LIDAR_PACKET_HEAD_RIGHT,LIDAR_PACKET_TAIL_MID,LIDAR_PACKET_TOP_MID

依据：

![image-20220512105624706](/home/caofangyu/.config/Typora/typora-user-images/image-20220512105624706.png)



#### 结果

22%-24%

![image-20220512110924560](/home/caofangyu/.config/Typora/typora-user-images/image-20220512110924560.png)

### 存储的数据类型2

保存的数据类型： (1的基础上增加event_info)

（REMOTE_CONTROL, DRIVING_RECORD,  TAKE_OVER_DRIVING_RECORD , PLANNING_INFO, LOCALIZATION,  MONITOR，EVENT_INFO）

#### 结果

18%-20%左右，增加一个event_info影响不大。

![image-20220512112427648](/home/caofangyu/.config/Typora/typora-user-images/image-20220512112427648.png)

### 删除一些数据数量多的数据

环境：arm3 使用bag: data/bag/howo38_2022_04_22_08_50_11_13.msg

删除的数据类型：所有次数大于1000的数据

CHASSIS,  CHASSIS_DETAIL, CONTROL_COMMAND, CONTROL_DEBUG, CONTROL_STATUS, GNSS_INS, MESSAGE_SERVICE_STATUS, TRAILER_DETECTION,PROCESS_STATUS, MONITOR_RESULT,COMMUNICATION_DETECT,COMMUNICATION_DETECT_RESULT,RAW_IMU

![image-20220512113154001](/home/caofangyu/.config/Typora/typora-user-images/image-20220512113154001.png)

#### 结果

18%-22%

![image-20220512113920315](/home/caofangyu/.config/Typora/typora-user-images/image-20220512113920315.png)

### 提交的配置

环境：arm3 使用bag: data/bag/howo38_2022_04_22_08_50_11_13.msg（此bag没有TAKE_OVER_DRIVING_RECORD消息，其他的都有）

保存的数据类型：第二行为2的基础上新增的数据类型

REMOTE_CONTROL, DRIVING_RECORD,  TAKE_OVER_DRIVING_RECORD , PLANNING_INFO, LOCALIZATION,  MONITOR，EVENT_INFO，

TRAILER_DETECTION， FUSION_MAP，REMOTE_ENVIRONMENT， TOS_COMMAND

#### 结果

18%-20%

![image-20220512142127642](/home/caofangyu/.config/Typora/typora-user-images/image-20220512142127642.png)

# 