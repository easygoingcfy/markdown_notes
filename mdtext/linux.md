# 常用操作

## 通知

## 磁盘操作

### 显示硬盘以及所属分区情况

```
sudo fdisk -l
```

### 硬盘格式化

ubuntu下存储数据的格式为ext4

```
sudo mkfs -t ext4 /dev/sda
```

### 硬盘挂载

```
sudo mount -t ext4 硬盘名 挂载点
eg:
sudo mount -t ext4 /dev/sda /devdata
```

可以用df -l命令确认挂载情况

### 清理磁盘缓存*

```
echo 3 | sudo tee /proc/sys/vm/drop_caches
```

## 

### 给用户权限

```
sudo usermod -aG sudo username
```

## 终端

`ctrl + shift + t`          在当前终端窗口中新建一个终端，通过alt+数字键切换

`ctrl + alt + t `              新打开一个终端窗口

## 后台执行命令(nohup, & screen)

&: 在Linux命令或者脚本后面增加&符号，用户退出登录时命令会被自动终止

```
./my-shell-script.sh &
```

nohup：

```
nohup ./my-shell-script.sh &
```

screen：退出登录后可以重新连接到会话。（类似于tmux）

```
安装：
apt install screen -y
screen
```



## ctrl + r 查找历史命令

```
history
```

列出之前用过的所有命令

## sudo

sudo命令以系统管理者的身份执行指令

- -V 显示版本编号
- -h 会显示版本编号及指令的使用方式说明
- -l 显示出自己（执行 sudo 的使用者）的权限
- -v 因为 sudo 在第一次执行时或是在 N 分钟内没有执行（N 预设为五）会问密码，这个参数是重新做一次确认，如果超过 N 分钟，也会问密码
- -k 将会强迫使用者在下一次执行 sudo 时问密码（不论有没有超过 N 分钟）
- -b 将要执行的指令放在背景执行
- -p prompt 可以更改问密码的提示语，其中 %u 会代换为使用者的帐号名称， %h 会显示主机名称
- -u username/#uid 不加此参数，代表要以 root 的身份执行指令，而加了此参数，可以以 username 的身份执行指令（#uid 为该 username 的使用者号码）
- -s 执行环境变数中的 SHELL 所指定的 shell ，或是 /etc/passwd 里所指定的 shell
- -H 将环境变数中的 HOME （家目录）指定为要变更身份的使用者家目录（如不加 -u 参数就是系统管理者 root ）
- command 要以系统管理者身份（或以 -u 更改为其他人）执行的指令

## ping

**p[ing命令](https://www.baidu.com/s?wd=ping命令&tn=24004469_oem_dg&rsv_dl=gh_pl_sl_csd)**用来测试主机之间网络的连通性。执行ping指令会使用ICMP传输协议，发出要求回应的信息，若远端主机的网络功能没有问题，就会回应该信息，因而得知该主机运作正常。

```
-d：使用Socket的SO_DEBUG功能；
-c<完成次数>：设置完成要求回应的次数；
-f：极限检测；
-i<间隔秒数>：指定收发信息的间隔时间；
-I<网络界面>：使用指定的网络界面送出数据包；
-l<前置载入>：设置在送出要求信息之前，先行发出的数据包；
-n：只输出数值；
-p<范本样式>：设置填满数据包的范本样式；
-q：不显示指令执行过程，开头和结尾的相关信息除外；
-r：忽略普通的Routing Table，直接将数据包送到远端主机上；
-R：记录路由过程；
-s<数据包大小>：设置数据包的大小；
-t<存活数值>：设置存活数值TTL的大小；
-v：详细显示指令的执行过程。
```

eg:

```
ping -i 0.3 -c 4 baidu.com
```



# 文件操作

## 文件属性与颜色

Linux不同颜色 文件类型 /权限 /属性
蓝色文件----------目录
白色文件----------一般性文件，如文本文件，配置文件，源码文件等
浅蓝色文件----------链接文件，主要是使用ln命令建立的文件
绿色文件----------可执行文件，可执行的程序
红色文件-----------压缩文件或者包文件

红色闪烁-------表示链接的文件有问题了

黄色------------设备文件
Linux下用字符表示的文件类型
-：普通文件
d：目录文件
l：链接文件
b：块设备文件
c：字符设备文件
p：管道文件



## mkdir

```
mkdir dir 创建文件夹
mkdir -p dir 递归创建文件夹
```

## mv

` mv  source_file dest_file`     更改文件名

` mv source_file dest_directory`        移动文件

`mv source_dir dest_dir`     如果dest_dir存在，则移动目录，否则更改目录名

## rsync

rsync 可以理解为 remote sync（远程同步）

```
rsync [OPTION] SRC DEST
```

参数

```
-a	这是归档模式，表示以递归方式传输文件，并保持所有属性，它等同于-r、-l、-p、-t、-g、-o、-D 选项。-a 选项后面可以跟一个 --no-OPTION，表示关闭 -r、-l、-p、-t、-g、-o、-D 中的某一个，比如-a --no-l 等同于 -r、-p、-t、-g、-o、-D 选项。
-r	表示以递归模式处理子目录，它主要是针对目录来说的，如果单独传一个文件不需要加 -r 选项，但是传输目录时必须加。
-v	表示打印一些信息，比如文件列表、文件数量等。
-l	表示保留软连接。
-L	表示像对待常规文件一样处理软连接。如果是 SRC 中有软连接文件，则加上该选项后，将会把软连接指向的目标文件复制到 DEST。
-p	表示保持文件权限。
-o	表示保持文件属主信息。
-g	表示保持文件属组信息。
-D	表示保持设备文件信息。
-t	表示保持文件时间信息。
--delete	表示删除 DEST 中 SRC 没有的文件。
--exclude=PATTERN	表示指定排除不需要传输的文件，等号后面跟文件名，可以是通配符模式（如 *.txt）。
--progress	表示在同步的过程中可以看到同步的过程状态，比如统计要同步的文件数量、 同步的文件传输速度等。
-u	表示把 DEST 中比 SRC 还新的文件排除掉，不会覆盖。
-z	加上该选项，将会在传输过程中压缩。
```

最常用的几个  -a、-v、-z、--delete 和 --exclude

## cp

复制文件，参数类似mv

### 参数列表

- -a：此选项通常在复制目录时使用，它保留链接、文件属性，并复制目录下的所有内容。其作用等于dpR参数组合。
- -d：复制时保留链接。这里所说的链接相当于 Windows 系统中的快捷方式。
- -f：覆盖已经存在的目标文件而不给出提示。
- -i：与 **-f** 选项相反，在覆盖目标文件之前给出提示，要求用户确认是否覆盖，回答 **y** 时目标文件将被覆盖。
- -p：除复制文件的内容外，还把修改时间和访问权限也复制到新文件中。
- **-r**：若给出的源文件是一个目录文件，此时将复制该目录下所有的子目录和文件。
- -l：不复制文件，只是生成链接文件。

复制文件夹时使用-r

## cat

连接文件并打印到标注输出设备上

```
cat [-AbeEnstTuv] [--help] [--version] fileName
```

**-n 或 --number**：由 1 开始对所有输出的行数编号。

**-b 或 --number-nonblank**：和 -n 相似，只不过对于空白行不编号。

**-s 或 --squeeze-blank**：当遇到有连续两行以上的空白行，就代换为一行的空白行。

**-v 或 --show-nonprinting**：使用 ^ 和 M- 符号，除了 LFD 和 TAB 之外。

**-E 或 --show-ends** : 在每行结束处显示 $。

**-T 或 --show-tabs**: 将 TAB 字符显示为 ^I。

**-A, --show-all**：等价于 -vET。

**-e：**等价于"-vE"选项；

**-t：**等价于"-vT"选项；

## 输出重定向

### >

直接把内容生成到指定文件，会覆盖源文件中的内容

### >>

尾部追加，不会覆盖掉文件中原有的内容，相当于append

### 2>&1

把标准错误重定向到标准输出并以后台的形式运行

```
/dev/null：表示空设备文件
0 表示stdin标准输入
1 表示stdout标准输出
2 表示stderr标准错误
&是把该命令以后台的job的形式运行
```

### ln 软链接

```
 ln [参数][源文件或目录][目标文件或目录]
 eg:
 ln -s log2013.log link2013
```

## less

逐屏显示文件

## bc : 计算器

scale:设置精度

## head与tail

显示文件的头部或尾部，默认选择 10 行，-n选项可以选择函数

## tee：三通

将从标准输入stdin得到的数据抄送到标准输出stdout显示，同时存入磁盘文件中

ex: `./myap | tee myap.log `

## ps 进程状态

用于显示当前进程的状态，类似于 windows 的任务管理器。

### 查找进程

```
ps -ef | grep 进程关键字
```

### 参数

ps 的参数非常多, 在此仅列出几个常用的参数并大略介绍含义    

- -A 列出所有的进程

- -w 显示加宽可以显示较多的资讯

- -au 显示较详细的资讯

- -aux 显示所有包含其他使用者的行程

- au(x) 输出格式 :
  
  ```
  USER PID %CPU %MEM VSZ RSS TTY STAT START TIME COMMAND
  ```
  
  - USER: 行程拥有者
  - PID: pid
  - %CPU: 占用的 CPU 使用率
  - %MEM: 占用的记忆体使用率
  - VSZ: 占用的虚拟记忆体大小
  - RSS: 占用的记忆体大小
  - TTY: 终端的次要装置号码 (minor device number of tty)
  - STAT: 该行程的状态:
    - D: 无法中断的休眠状态 (通常 IO 的进程)
    - R: 正在执行中
    - S: 静止状态
    - T: 暂停执行
    - Z: 不存在但暂时无法消除
    - W: 没有足够的记忆体分页可分配
    - <: 高优先序的行程
    - N: 低优先序的行程
    - L: 有记忆体分页分配并锁在记忆体内 (实时系统或捱A I/O)
  - START: 行程开始时间
  - TIME: 执行的时间
  - COMMAND:所执行的指令

## wc: 字计数

列出文件中有多少行，多少个单词，多少字符，文件数大于1时，列出合计

-l : 只列出行计数

## sort

-n： 对于数字按照算数值大小排序

## tr：翻译字符

tr string1 string2

把标准输入拷贝到标准输出，string1中出现的字符替换为string2中的对应字符

注意：tr默认是自动补齐  ex：

```
tr caofangyu sb
caofangyu 
sbbbbbbbb 
```

## tar.gz

```
tar -zxvf xxx.tar.gz  解压缩
```

## tar.xz

```
xz -d xxxx.tar.xz 解压缩
```

## dpkg

```
dpkg -i xxx.deb   安装软件
```

## grep 查找

查找文件中符合条件的字符串

ex : `cat telnos | tr UVX uvx `

## uniq : 筛选文件中的重复行

-u : 只保留没有重复的行

-d : 只保留有重复的行（只打印一次）

默认打印所有行（重复的只打印一次）

-c : 计算重复行行数

## mount

挂载文件系统。

`mount -t type [-o options] device dir`

device: 指定要挂载的设备，比如磁盘，光驱

dir： 指定把文件系统挂载到哪个目录

type：指定挂载的文件系统类型，一般不用指定，mount命令可以自行判断

options： 指定挂载参数，比如ro表示只读方式挂载文件系统

## dpkg

dpkg是Debian的一个底层包管理工具，主要用于对已下载到本地和已安装的软件包进行管理

`dpkg -i <.deb file name>`安装下载好的软件

## 磁盘，文件  df du

### df

df 以磁盘分区为单位查看文件系统，可以获取硬盘被占用了多少空间，目前还剩下多少空间等信息。

```
df -h  查看每个根路径的分区大小
df -hl 查看磁盘剩余空间
```

### du

**du** 的英文原义为 **disk usage**，含义为显示磁盘空间的使用情况，用于查看当前目录的总大小。

```
du -sh    查看当前目录的大小
du log2012.log     显示指定文件所占空间
```

- **-s**：对每个Names参数只给出占用的数据块总数。
- **-a**：递归地显示指定目录中各文件及子目录中各文件占用的数据块数。若既不指定-s，也不指定-a，则只显示Names中的每一个目录及其中的各子目录所占的磁盘块数。
- **-b**：以字节为单位列出磁盘空间使用情况（系统默认以k字节为单位）。
- **-k**：以1024字节为单位列出磁盘空间使用情况。
- **-c**：最后再加上一个总计（系统默认设置）。
- **-l**：计算所有的文件大小，对硬链接文件，则计算多次。
- **-x**：跳过在不同文件系统上的目录不予统计。
- **-h**：以K，M，G为单位，提高信息的可读性。

# 系统

## 进程

### ps

查看静态的进程统计信息

常见的选项：

- a：显示当前终端下的所有进程信息，包括其他用户的进程。
- u：使用以用户为主的格式输出进程信息。
- x：显示当前用户在所有终端下的进程。
- -e：显示系统内的所有进程信息。
- -l：使用长（long）格式显示进程信息。
- -f：使用完整的（full）格式显示进程信息。

```
ps -uf
```

## top

查看进程动态信息

以全屏交互式的界面显示进程排名，及时跟踪包括CPU、内存等系统资源占用情况，默认情况下每三秒刷新一次

## pstree

查看进程树，以树形结构列出进程信息

```
pstree -aup
pstree -ap username
```

## 环境变量

### 查看环境变量

`env` 

`env | grep XXX`

`echo $ENVNAME`

### 设置环境变量

#### 用于当前终端

`export ENVNAME = 'env_content'`

#### 用于当前用户

```
vim .bashrc
export PATH=<你的要加入的路径>:$PATH

加入多个路径（每个路径以冒号分离）
export PATH=<你要加入的路径1>:<你要加入的路径2>: ...... :$PATH

使配置生效
source ~/.bashrc 或者注销再次登录
```

#### 用于所有用户

```
sudo vim /etc/profile 
```



### 删除环境变量

`unset ENVNAME`

# shell

## 条件语句

```
if []; then
  command
fi
```

## 后台执行脚本

```
nohup command &
nohup 和 & 都需要
```

## grep -v 

```
grep -v grep
这样结果不会出现grep命令本身
-v 反选，排序grep -v后面的参数
```

## awk 显示指定列

AWK 是一种处理文本文件的语言，是一个强大的文本分析工具。

```
awk '{print $3, $4}'

```



# ssh

## server:172.25.20.8

## 文件传输

从服务器上下载文件：

`scp username@servername:/path/filename /var/www/local_dir`

上传本地文件到服务器：

`scp /path/filename username@servername:/path `

从服务器下载整个目录

`scp -r username@servername:/var/www/remote_dir/（远程目录） /var/www/local_dir（本地目录）`

上传目录到服务器：

`scp -r local_dir username@servername:remote_dir`

# 工具

## Tmux

终端复用器，常用开发工具

TMUX快捷键使用方法为：先按下前缀键，然后输入命令。如：先按下ctrl+b 松开，再按d

### 分屏

```
Ctrl+b % 竖直分屏
Ctrl+b " 水平分屏
Ctrl+b o 切换屏幕
Ctrl+b space 分屏模式切换
Ctrl+b x 关闭分屏
Ctrl+b q 分屏编号
```



### 安装

```bash
# Ubuntu 或 Debian
$ sudo apt-get install tmux
```

### 启动/退出

```
tmux
exit/Ctrl+d
```

### 前缀键

默认的前缀键是`Ctrl+b`

### 会话管理

#### 新建会话

第一个启动的 Tmux 窗口，编号是`0`，第二个窗口的编号是`1`，以此类推。这些窗口对应的会话，就是 0 号会话、1 号会话。

使用编号区分会话，不太直观，更好的方法是为会话起名

```bash
$ tmux new -s <session-name>
```

#### 分离会话

在 Tmux 窗口中，按下`Ctrl+b d`或者输入`tmux detach`命令，就会将当前会话与窗口分离

```bash
$ tmux detach
```

`tmux ls`命令可以查看当前所有的 Tmux 会话。

```bash
$ tmux ls
# or
$ tmux list-session
```

#### 接入会话

`tmux attach`命令用于重新接入某个已存在的会话。

> ```bash
> # 使用会话编号
> $ tmux attach -t 0
> 
> # 使用会话名称
> $ tmux attach -t <session-name>
> ```

#### 杀死会话

`tmux kill-session`命令用于杀死某个会话。

> ```bash
> # 使用会话编号
> $ tmux kill-session -t 0
> 
> # 使用会话名称
> $ tmux kill-session -t <session-name>
> ```

#### 切换会话

`tmux switch`命令用于切换会话。

> ```bash
> # 使用会话编号
> $ tmux switch -t 0
> 
> # 使用会话名称
> $ tmux switch -t <session-name>
> ```

#### 重命名会话

`tmux rename-session`命令用于重命名会话。

> ```bash
> $ tmux rename-session -t 0 <new-name>
> ```

#### 常用快捷键

下面是一些会话相关的快捷键。

> - `Ctrl+b d`：分离当前会话。
> - `Ctrl+b s`：列出所有会话。
> - `Ctrl+b $`：重命名当前会话。

## crontab

### 查看是否运行

```
pgrep cron
ps -ef | grep cron
```

## /var/log下没有cron日志

### 修改rsyslog

```
sudo vim /etc/rsyslog.d/50-default.conf
cron.*              /var/log/cron.log #将cron前面的注释符去掉
```

### 重启rsyslog

```
sudo service rsyslog restart
```

## python 脚本不运行

https://blog.csdn.net/weixin_36343850/article/details/79217611

https://www.runoob.com/linux/linux-comm-crontab.html

所有文件使用绝对路径，包括python(which python)

## 重启cron服务

```
使用crontab -e 编辑之后需要重启
service cron restart
0 */4 * * * python /home/caofangyu/caofangyu/event_parser/send_record_by_time
```