#### 测试用recordB文件地址

/onboard_data/bags/meishangang/howo9/20211123/0854/recordB

#### 本地mount集群命令

```
sudo mount -t glusterfs storage1.fabu.ai:/onboard_data /onboard_data
```

## ssh 

地址： 172.25.20.8

````
ssh caofangyu@172.25.20.8
````

### 数据存放

/fabudata

## root_dir

/onboard_data/bags/meishangang/

## 命令

python main.py -p /onboard_data/bags/meishangang/ -d 20220101

## 公钥

文件地址： ~/.ssh/id_rsa.pub



## Fabupilot/quick starts

### 启动容器

$ sudo mount -t glusterfs storage1.fabu.ai:/onboard_data /onboard_data //挂载共享空间 具体见http://wiki.fabu.ai/wiki/doku.php?id=infrastructure:platform:nfs
$ ./deploy/dev_start.sh 
$ ./deploy/dev_int.sh  

### 拉取版本

拉取最新的开发版本(推荐)

$ bash deploy/common/update_release.sh candidate/HEAD

拉取指定版本

$ bash deploy/common/update_release.sh candidate/********

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



## openVpn

IPV4: 192.168.10.147

public IPv4 address / hostname exit

protocol : udp

port : 1194

DNS server for clients:Current system resolvers

name of first client : cilent 

## 配置

主要配置文件在release/.config里面，每次更新或启动会把本地的与这个.config同步。更改的话需要改.config

如果运行不了，可以先在release里面跑

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
