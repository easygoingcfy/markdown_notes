#### 本地mount集群命令

```
sudo mount -t glusterfs storage1.fabu.ai:/onboard_data /onboard_data
```

## /private

```
sudo mount -t nfs 192.168.3.102:/private /private
```

## ssh

地址： 172.25.20.8

```
ssh caofangyu@172.25.20.8
```

流机：

```
ssh -p 31454 caofangyu@jumpserver.ssh.fabu.ai
```

## dev

192.168.3.50    

## arm3

```
192.168.11.203
```

自己的arm机器

```
nvidia@192.168.11.150
nvidia382764

nvidia@192.168.10.11
nvidia
```

### 数据存放

/fabudata

## 云控

云控访问地址：

```
http://nt-ecs.fabu.ai
http://pre.nt-ecs.fabu.ai    //预发
```

生产

```
http://192.168.3.100:8890/#/report
```

预发：

```
http://192.168.3.100:18890/#/report
```

```
s-public
fabu124
```



## 启动模块

```
启动prometheus加个参数--local-ip=127.0.0.1
```

## REMOTE_CONTROL

```
destination_id: "xxxx"
一共4个字符，前两个代表箱区，后两个代表泊位
堆场包括箱区 比如：6堆场包括所有6开头的箱区，从61 - 6M
JE:箱区 后面跟的数字代表贝位号，一共四个字符
CR:泊位
```

不规则箱区名：

![不规则厢区](/home/caofangyu/me/shared_folders_with_win10/不规则厢区.png)

6堆场箱区名：

![6堆场](/home/caofangyu/me/shared_folders_with_win10/6堆场.png)

## ThinkPad

fabu382764

## root_dir

/onboard_data/bags/meishangang/

## 公钥

文件地址： ~/.ssh/id_rsa.pub

## 消息

这里有所有消息的定义，可以直接用

```
http://git.fabu.ai/lihao/fabukit/blob/master/src/fabukit/message/topic_utils.py
```

## Fabupilot/quick starts

### 启动容器

$ sudo mount -t glusterfs storage1.fabu.ai:/onboard_data /onboard_data //挂载共享空间 具体见http://wiki.fabu.ai/wiki/doku.php?id=infrastructure:platform:nfs
$ ./deploy/dev_start.sh
$ ./deploy/dev_int.sh

### 拉取版本

拉取最新的开发版本(推荐)

$ bash deploy/common/update_release.sh master/HEAD

拉取指定版本

$ bash deploy/common/update_release.sh xxxx/xxxx

拉取版本是deploy版本不对的情况

```
进deploy切换版本后执行：
export LOCAL_DEPLOY_VERSION= commit_id
```

### 切换车号

$ cd /fabupilot
$ ./scripts/chcar.sh howo32 version

__monitor__

在docker外检查端口

$ ./deploy/check_port.sh

播包后可以在浏览器中查看monitor页面

### 播包

$ cd release 
$ ./scripts/message_service.sh play /onboard_data/bags/meishangang/howo21/20210515/1021/howo21_2021_05_15_10_36_18_15.msg

### 更新源

```
./deploy/common/update_resources.sh 
```

### DEV环境生成config

```
./scripts/generate_fabupilot_config.sh [--vehicle=howo1] [--use-local-config-online]
```

### 查看车上monitor

```
192.168.3.100:8(车名：ATXXX 不要AT)
```

不要经常开，会影响车上网络

### 模块

查看模块在车辆的哪台服务器上

```
在living modules里面看end_point
perception lidar在.2上，camera在.3上
```



#### 在后端*（不确定）启动模块

```
./scripts/planning_v3 start_fe
```

## openVpn

IPV4: 192.168.10.147

public IPv4 address / hostname exit

protocol : udp

port : 1194

DNS server for clients:Current system resolvers

name of first client : cilent 

## 配置

### dev下生成config

./scripts/generate_fabupilot_config.sh xxxx(vehicle_name)

## 配套工具

1、配套工具使用./scripts/message_service.sh启动

2、diagnose 查看模块中sender和receiver的连接状态。如查看monitor的连接状态：

```
./scripts/message_service.sh diagnose --module_name monitor --bag_only(show bag message only)
```

3、echo 查看当前正在发送的消息。如查看当前的LOCALIZATION消息：

```
./scripts/message_service.sh echo -type=LOCALIZATION
```

4、record 录包。bag 保存路径为 FLAGS_save_bag_path_时间.msg，例如：

```
./scripts/message_service.sh record -save_bag_path=/tmp/bag  #记录下的包为/tmp/bag_2019_03_19_13_38_36.msg
```

卡车数据采集

```
./scripts/record_bag.sh --ms   开始记录数据
```

## 编译

```
# Build without optimization
$ bash fabupilot.sh build
# Build with optimization
$ bash fabupilot.sh build_opt
# Build with GPU support
$ bash fabupilot.sh build_opt_gpu
```

## arcanist

![image-20220224165804550](/home/caofangyu/.config/Typora/typora-user-images/image-20220224165804550.png)
