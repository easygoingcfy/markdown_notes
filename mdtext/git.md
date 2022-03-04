# 常用操作  

## 代理

### 重置代理

```
git config --global  --unset https.https://github.com.proxy 
git config --global  --unset http.https://github.com.proxy 
```

### 设置代理

```text
# http
git config --global http.https://github.com.proxy http://127.0.0.1:8080
git config --global https.https://github.com.proxy https://127.0.0.1:8080

# socket
git config --global http.proxy 'socks5://127.0.0.1:8080'
git config --global https.proxy 'socks5://127.0.0.1:8080'
```

- - -
## git init  
初始化当前目录为仓库，并将当前仓库设置为master
- - -
## git add 、 git commit -m  
### add 将文件添加到缓存区
git add --all 将所有改动文件提交到暂存区
git add .     提交所有改动，除了删除操作
commit 提交到本地仓库  -m表示注释  
改写提交：git commit --amend

## git 查看改动

### 查看未暂存的修改

```
git diff
此时比较的是 已暂存（staged）和已追踪未暂存（modified）之间的修改部分。
```



### 查看已暂存的修改

```
git diff --catched
此时比较的是 提交至仓库的版本 和 暂存区文件（staged）之间的修改部分
```

### 查看已提交的修改

```
git log -p 
此时比较的是每次提交到仓库的版本 与 上一次提交到仓库的版本之间的变化
```



# git 提交

## 合并提交

```
git rebase -i xxx
git rebase -i HEAD~2 
```



## 格式

```text
<type>(<scope>): <subject>
```

### **type(必须)**

用于说明git commit的类别，只允许使用下面的标识。

feat：新功能（feature）。

fix/to：修复bug，可以是QA发现的BUG，也可以是研发自己发现的BUG。

- fix：产生diff并自动修复此问题。适合于一次提交直接修复问题
- to：只产生diff不自动修复此问题。适合于多次提交。最终修复问题提交时使用fix

docs：文档（documentation）。

style：格式（不影响代码运行的变动）。

refactor：重构（即不是新增功能，也不是修改bug的代码变动）。

perf：优化相关，比如提升性能、体验。

test：增加测试。

chore：构建过程或辅助工具的变动。

revert：回滚到上一个版本。

merge：代码合并。

sync：同步主线或分支的Bug。

### **scope(可选)**

scope用于说明 commit 影响的范围，比如数据层、控制层、视图层等等，视项目不同而不同。

例如在Angular，可以是location，browser，compile，compile，rootScope， ngHref，ngClick，ngView等。如果你的修改影响了不止一个scope，你可以使用*代替。

### **subject(必须)**

subject是commit目的的简短描述，不超过50个字符。

建议使用中文（感觉中国人用中文描述问题能更清楚一些）。

---

# 远程仓库

## 公钥

### 查看公钥

一般名字是id_dsa,id_rsa

```
ls ~/.ssh
```

### 生成

```
ssh-keygen
如果想要添加密码
ssh-keygen -o 
保密性更高
```



## 查看远程仓库

```
git remote (-v)
```

使用-v会显示需要读写远程仓库使用的Git保存的简写与其对应的URL

## 添加远程仓库

```
git remote add <shortname> <url>
```

添加一个新的远程仓库，同时指定一个简写

## 从远程仓库中抓取与拉取

```
git fetch <remote>
```

访问远程仓库，从中拉取所有本地仓库还没有的数据。执行完成后，本地会拥有远程仓库中所有分支的引用，可以随时合并或查看。

```
git pull <远程主机名> <远程分支名> : <本地分支名>
```

如果分支设置了跟踪远程分支，可以用git pull 命令自动抓取后合并该远程分支到当前分支。

默认情况下，git clone命令会自动设置本地master分支跟踪克隆的远程仓库的master分支。

```
git push origin master
git push <远程主机名> <本地分支>:<远程分支>
```

推送到远程仓库。

如果本地分支与远程分支名字相同，冒号及后面的部分可以省略

## 查看远程仓库

```
git remote show <remote>
```

列出远程仓库的URL与跟踪分支的信息。

## 重命名与移除

```
git remote rename 
git remote remove 
git remote rm
```

## 标签

### 列出标签

```
git tag (-l --list)
git tag -l "v1.8.5*"
```

使用-l --list 按照通配符列出标签

### 附注标签

附注标签是储存在Git数据库中的一个完整对象，包含打标签者的名字、电子邮件地址、日期时间和标签信息，并且可以使用GNU Privacy Guard(GPG)签名并验证。通常会建议创建附注标签。

```
git tag -a v1.4 -m "my version 1.4"
```

### 轻量标签

```
git tag v1.4-lw
```

### 后期打标签

需要在命令的末尾指定条件的校验和（或者部分）

```
git tag -a v1.2 xxxxxx
```

### 共享标签

```
git push origin <tagname> 推送一个标签
git push origin --tags	  推送所有不在远程仓库服务器的标签（不会区分轻量标签和附注标签）
```

### 删除标签

```
git tag -d <tagname>
git push origin --delete <tagname>
```

## GIT别名

```
git config --global alias.<name> commend
ex:
git config --global alias.co checkout
```

## git ignore

在主目录添加.gitignore文件，使用git ignore

- 空白行或以 开头`#`的行将被忽略。
- 标准 glob 模式有效，并将在整个工作树中递归应用。
- 您可以使用正斜杠 ( `/`) 开始模式以避免递归。
- 您可以使用正斜杠 ( `/`) 结束模式以指定目录。
- 您可以通过以感叹号 ( `!`) 开头来否定模式。

### 使.gitignore生效

```
git rm -r --cached .			#清除缓存
git add .						#重新trace file
```



# git分支

Git保存的不是文件的变化或者差异，而是一系列不同时刻的 快照 

在进行提交操作时，Git会保存一个提交对象（commit object）。

提交对象会包含一个指向暂存内容的指针，作者的姓名、邮箱、提交时输入的信息以及指向父对象的指针。

更具体的，Git会使用blob对象保存当前版本的文件快照，并将校验和加入到暂存区等待提交

当使用git commit进行提交操作时，Git会先计算每一个子目录的校验和，然后在Git仓库中将这些校验和保存为树对象（记录着目录结构和blob对象索引）。

随后，Git会创建一个提交对象，它除了上面提到的那些信息外，还包含指向这个树对象（项目根目录）的指针。如此一来，Git就可以在需要的时候重现此次保存的快照。



Git的分支，本质上仅仅是指向提交对象的可变指针。

## HEAD指针

HEAD指向当前所在的本地分支。

## 创建分支

```
git branch branch_name
```

创建分支并切换过去

```
git checkout -b <newbranchname>
```



## 查看各分支当前所指的对象

```
git log --online --decorate
```

## 切换分支

```
git checkout branch_name
```

## 删除分支

```
git branch -d branch_name
```



- - -
## git log 查看历史提交日志
git log filename 查看单个文件的历史日志
- - -
## git reset --opt  回滚代码仓库
### --soft
只恢复头指针
### --mixed  
恢复头指针，已经add的暂存区丢掉,工作空间不变
### --hard  
一切恢复(并不理解)
- - -
## git status 查看状态  
## git config 用户操作

`git config user.name` 

`git config --global user.name "new_name"`	修改用户名

`git config user.password`

`git config user.email`

`git config --list`		查看配置信息

## git checkout
切换分支
git checkout -b dev 创建一个分支，并切换过去
--file 将文件切换到最近一次的状态（不能迭代）
- - -
## git rm 删除文件
使用git rm删除文件需要使用commit提交
- - -
## git reflog 查看提交历史
- - -
## git branch
查看分支
git branch branch_name 创建一个分支,但不会切换
git branch -m branch_name_old brancn_name_new 修改分支名
git branch -D 强制删除分支
- - -
## git merge 合并分支
常用来在master中合并其他分支（开发中建议使用分支）
- - -
## git stash
保存当前工作状态。(当工作区修改了文件或其他功能时，不能切换分区，使用git stash)
使用git stash pop恢复
- - -
## git diff 
查看不同分支的文件差异
- - -


# 一些经验
## git分支开发步骤  



在不饶乱master代码的情况下进行开发
拉取分支（分支名简洁，commit中简单描述）
完成后合并到master，合并后删除分支

## 拒绝合并无关历史

git pull origin master --allow-unrelated-histories

默认情况下，git合并命令拒绝合并没有共同祖先的历史。当两个项目的历史独立地开始时，这个选项可以被用来覆盖这个安全。由于这是一个非常少见的情况，因此没有默认存在的配置变量，也不会添加。（有道翻译）
