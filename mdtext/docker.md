## 获取应用程序

### 1.下载应用程序内容

可以直接拉取整个项目

可以下载并解压

## 构建应用的容器镜像 

使用Dockerfile创建容器镜像

1.在package.json同目录文件夹下建立Dockerfile文件

2.使用docker build命令构建容器镜像

```
docker build -t getting-started .		
```

## 启动容器

```
docker run -dp 3000:3000 getting-started
```

### 在浏览器中查看

```
heep://localhost:3000
```

## docker 容器

### 获取镜像

```
docker pull
```

### 启动容器

示例：使用Ubuntu镜像启动一个容器，参数为以命令行模式进入该容器

```
docker run -it ubuntu /bin/bash
-i 交互式操作
-t 终端
-v 挂载宿主机的一个目录
```

### 查看容器

```
docker ps 查看正在运行的容器
-a 查看所有容器
-l 查询最后一次创建的容器
docker port containerId 查看端口映射
docker start containerId 启动一个停止的容器
docker stop containerId 停止容器
docker restart containerId 重启容器
```

#### 后台运行

```
docker run -itd --name NAME ubuntu /bin/bash
-d:后台运行，使用-d后默认不会进入容器
```

### 进入容器

```
docker attach containerId 进入容器，退出后容器会停止运行
docker exec -it containerId /bin/bash 退出容器后，容器不会停止运行，建议使用exec
```

### 导出容器

```
docker export containerId > filename
```

### 导入容器

```
docker import
cat docker/ubuntu.tar | docker	import - test/ubuntu:v1
docker import http://example.com/exampleimage.tag example/imagerepo
```

### 删除容器

```
docker rm -f containerId	删除一个容器
docker container prune   	删除所有停止的容器
```

### 查看程序日志

```
docker logs -f containerId
-f : 像tail -f 一样打印容器内部的标准输出
```

### 查看容器进程

```
docker top containerId
```

### 查看Docker底层信息

```
docker inspect containerId
```

## docker 镜像

### 查看镜像

```
docker images
```

### 下载镜像

```
docker pull IMAGENAME
```

### 查找镜像

```
docker search NAME
```

### 删除镜像

```
docker rmi NAME
```

### 创建镜像

两种方式：

- 1、从已经创建的容器中更新镜像，并且提交这个镜像
- 2、使用 Dockerfile 指令来创建一个新的镜像

#### 更新镜像

先用镜像创建一个容器`docker run -t -i ubuntu:15.10 /bin/bash`

在运行的容器内使用apt-get update命令

使用docker commit提交容器副本

```
docker commit -m="has update" -a="runoob" e218edb10161 runoob/ubuntu:v2
```

- **-m:** 提交的描述信息
- **-a:** 指定镜像作者
- **e218edb10161：**容器 ID
- **runoob/ubuntu:v2:** 指定要创建的目标镜像名

### 构建镜像



## 拷贝文件

```
docker cp [OPTIONS] CONTAINER:SRC_PATH DEST_PATH|-
```

## 用户 usermod

### 查看用户组

```
sudo cat /etc/group | grep docker
```

### 添加用户

```
sudo usermod -aG docker ${usr}
sudo usermod -aG docker caofangyu
```

添加用户之后需要重新登录以使权限生效。
