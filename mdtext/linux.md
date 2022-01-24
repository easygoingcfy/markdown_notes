# 常用操作

## 终端

`ctrl + shift + t` 		 在当前终端窗口中新建一个终端，通过alt+数字键切换

`ctrl + alt + t `		  	新打开一个终端窗口

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

## mv

` mv  source_file dest_file` 	更改文件名

` mv source_file dest_directory`		移动文件

`mv source_dir dest_dir` 	如果dest_dir存在，则移动目录，否则更改目录名

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

## less

逐屏显示文件

## head与tail

显示文件的头部或尾部，默认选择 10 行，-n选项可以选择函数

## tee：三通

将从标准输入stdin得到的数据抄送到标准输出stdout显示，同时存入磁盘文件中

ex: `./myap | tee myap.log `

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

## grep

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

# 系统

## 环境变量

### 查看环境变量

`env` 

`env | grep XXX`

`echo $ENVNAME`

### 设置环境变量

`export ENVNAME = 'env_content'`

### 删除环境变量

`unset ENVNAME`
