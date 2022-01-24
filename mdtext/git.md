# 常用操作  
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

---

## git push

`git push <远程主机名> <本地分支>:<远程分支>`

如果本地分支与远程分支名字相同，冒号及后面的部分可以省略

## git pull

` git pull <远程主机名> <远程分支名> : <本地分支名> `

省略情况同push，注意参数顺序

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
## git remote
查看当前仓库名称
git remote -v   详细信息

# 一些经验
## git分支开发步骤  



在不饶乱master代码的情况下进行开发
拉取分支（分支名简洁，commit中简单描述）
完成后合并到master，合并后删除分支

## 拒绝合并无关历史

git pull origin master --allow-unrelated-histories

默认情况下，git合并命令拒绝合并没有共同祖先的历史。当两个项目的历史独立地开始时，这个选项可以被用来覆盖这个安全。由于这是一个非常少见的情况，因此没有默认存在的配置变量，也不会添加。（有道翻译）
