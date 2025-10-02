svn集中式版本控制

分布式版本控制



## 基本操作

### 初始化仓库

#### `git init`

在目标目录处使用`git init`来初始化仓库，目录下会生成`.git`文件夹

也可以指定参数：`git init my-res`,它会在当前目录下创建一个`my-res`文件夹作为，这个文件夹是git仓库

#### `git clone`

从网络中克隆一个仓库到当前目录

**需要明确的是：**

所有的版本控制系统，都只能跟踪文本的改动，比如txt、代码等，比如第五行删除了一个单词'linux',第七行添加了一个单词'Windows'。而对于图片、视频这些二进制文件，只能跟踪像文件大小之类的变化。

### 添加修改到暂存区

`git add 文件名/通配符`

注意

> git add的作用是将工作区文件的添加、修改、`删除`操作提交到`暂存区`

### 将修改提交到仓库

`git commit -m "说明"`

git commit命令，`-m`后面输入的是本次提交的说明，

**注意：**

> git add 可以一次add多个文件，git add file1.txt file2.txt
>
> git commit可以把add的文件一次性全部提交

### git status

查看状态

### 查看提交日志

#### git log [option]



- options:
    - --all:显示所有分支
    - --pretty=oneline 将提交信息显示为一行
    - --abbrev-commit 使得输出的commitid更简短
    - --graph 以图的形式显示

记录的是**提交历史**，即项目中所有被永久保存的提交（commit）记录。

**我们可以在/.bashrc中用起别名:alias git-log='git log --pretty=oneline --all --graph --abbrev-commit'让git-log可以直接达到：git log --pretty=oneline --all --graph --abbrev-commit的效果**

> 注意：
>
> `git log` 只会显示当前分支的提交历史以及与其他分支合并的历史，而其他分支（比如 `dev`）的新提交不会出现在当前视图中，**它默认不显示其他分支的提交**。
>
> - `git log 分支名`：直接查看指定分支的提交历史（无论当前在哪个分支）
> - `git log --all`：显示所有分支的提交历史
> - `git log --graph --all`：以图形化方式展示所有分支的提交关系

#### git refolg 

记录的是**本地仓库中引用（ref）的移动历史**，包括 `HEAD` 指针和分支的所有变动（如切换分支、提交、重置、合并、删除分支等操作）。

### 版本回退

`git reset --hard/soft/mixed 版本号`

| 参数    | 本地仓库（提交历史）       | 暂存区（Staging Area） | 工作区（Working Directory） | 典型场景                       |
| ------- | -------------------------- | ---------------------- | --------------------------- | ------------------------------ |
| `soft`  | 重置到目标提交（移动指针） | 不变（保留原暂存内容） | 不变（保留所有修改）        | 合并多个提交（重新提交）       |
| `mixed` | 重置到目标提交（移动指针） | 重置（与目标提交一致） | 不变（保留所有修改）        | 取消暂存，重新整理修改         |
| `hard`  | 重置到目标提交（移动指针） | 重置（与目标提交一致） | 重置（与目标提交一致）      | 彻底丢弃后续修改，回到历史版本 |

### 撤销修改

#### 撤销工作区修改

`git checkout -- filename`

使用该命令可以将文件恢复到**最近一次提交（commit）或暂存（add）的状态**,**其实就是用暂存区或者版本库中的版本来替换工作区的版本**。

1. 当该文件没有放到暂存区，撤销修改会回到和版本库一样的状态
2. 如果已添加到暂存区，但现在又做了修改，那么撤销修改会回到暂存区的状态

> 注意：
>
> `--`很重要，没有`--`就变成了"切换到另一个分支"的命令

#### 撤销暂存区

`git reset HEAD <file>`

它可以把暂存区的修改撤销掉，`重新放回工作区`

`git reset`既可以回退版本，也可以把暂存区修改回退到工作区。当使用`HEAD`时表示使用最新版本

该命令表示把<u>暂存区的文件file从暂存区放回到工作区，然后让暂存区状态和HEAD指向的版本的状态一致。</u>如果想要再把工作区修改撤销，参考1.7.1

### 删除文件

当我们在在工作区删除文件之后，可以通过`git add <file>`将修改提交到暂存区

也可以通过`git rm <file>`，它的操作可分为两 步：

1. 删除工作区文件(如果文件还没被删)
2. 将'删除文件'的修改添加到暂存区

通过以上两种方式删除工作区文件并添加到暂存区后，可以使用git commit提交

## git的四个区域

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c923b8c5b57c9cf5b5ddd73df1b9e055.png)

![image-20250921221627355](C:\Users\dundundun\Desktop\Desktop(1)\assets\image-20250921221627355.png)

工作区:`.git`文件夹所在的区域

暂存区:`git add`

本地仓库：`git commit`

> 通过git status查看
>
> 红色表明它们在工作区，是在工作区中修改、添加、删除的文件
>
> 绿色表示在暂存区

## git远程仓库

### 添加远程仓库

`git remote add <远端名称> <仓库路径>`

- 远端名称:我们写`origin`，一般都这么写
- 仓库路径：远端服务器的url

### 查看远程仓库

`git remote`

### 推送到远程仓库

`git push [-f] [--set-upstream] [远端名称] [本地分支名][：远端分支名]`

例:git push origin master:master

- 如果远端分支名和本地分支名相同，可以只写本地分支名
    - git push origin master

#### -f 

表示强制覆盖，如果本地代码和云端代码冲突，那么可以使用-f强制覆盖

#### --set-upstream  (-u)

如果我们想要只写`git push`，我们需要`指定本地分支与远端分支的对应关系`，可以使用`git push --set-upstream origin master:master`，意思是我要把本地分支master推到远程master中去，同时绑定分支对应关系,也可以简写为`git push -u origin master:master`

> 如果当前分支已经和远端分支关联，则可以省略**[远端名称] [本地分支名] [:远端分支名]**,直接使用**git push**

### 查看分支对应关系

`git branch -vv`

查看本地分支和远程分支的对应关系

### 查看远程库信息

`git remote -v`

### 删除远程库

`git remote rm 远程库名称`

> 注意：
>
> 这里所说的删除远程库只是**解除本地与远程的绑定关系**，远程库本身**没有任何改动**

## 分支管理





### 分支指针和HEAD

#### **分支指针**

指向**所在分支的最新提交对象上**，例如`master`是分支指针，它指向master分支的最新提交对象

#### **HEAD指针**：

指向**当前分支**的**最新提交对象**，当我们进行提交操作时，HEAD 会自动指向最新提交

假设我们当前在分支 `master` 上，我们进行了一次提交，那么这次提交将会成为最新的提交，并且 HEAD 将指向这个最新的提交。如果我们切换到另一个分支 `feature` ，那么 HEAD 也会随之指向 `feature` 分支上的最新提交。

- HEAD 指向当前分支最新的提交。
- HEAD~ 等同于 HEAD^，表示当前提交的父提交。
- HEAD^ 表示当前提交的第一个父提交。
- HEAD~n 表示当前提交的第 n 代祖先提交。

#### **HEAD 和分离的 HEAD**



> **......待写**















`HEAD`指向的是**当前分支**的一个提交点(HEAD表示了当前在哪个分支)



```
                  HEAD
                    │
                    ▼
                 master
                    │
                    ▼
┌───┐    ┌───┐    ┌───┐
│   │───▶│   │───▶│   │
└───┘    └───┘    └───┘
```



当我们创建新的分支，例如`dev`时，Git新建了一个指针叫`dev`，指向`master`相同的提交，再把`HEAD`指向`dev`，就表示当前分支在`dev`上：

```
                 master
                    │
                    ▼
┌───┐    ┌───┐    ┌───┐
│   │───▶│   │───▶│   │
└───┘    └───┘    └───┘
                    ▲
                    │
                   dev
                    ▲
                    │
                  HEAD
```



假如我们在`dev`上的工作完成了，就可以把`dev`合并到`master`上。Git怎么合并呢？最简单的方法，就是直接把`master`指向`dev`的当前提交，就完成了合并：

```
                           HEAD
                             │
                             ▼
                          master
                             │
                             ▼
┌───┐    ┌───┐    ┌───┐    ┌───┐
│   │───▶│   │───▶│   │───▶│   │
└───┘    └───┘    └───┘    └───┘
                             ▲
                             │
                            dev
```



### 分支

#### 创建分支

##### 创建本地分支

`git branch 分支名`

##### 创建与远程分支关联的本地分支

`git branch --set-upstream-to=origin/dev  dev  `

设置了与远程分支origin/dev与本地分支dev的对应关系。

> 注意：它只负责对应关系，不会创建分支

#### 切换分支

`git checkout 分支名`

##### 创建并切换分支名

`git checkout -b 分支名`

首先，我们创建一个叫`dev`的分支，然后切换到`dev`分支，在`dev`分支上正常提交，此时如下图



```
                  HEAD
                    │
                    ▼
                 master
                    │
                    ▼
┌───┐    ┌───┐    ┌───┐    ┌───┐
│   │───▶│   │───▶│   │───▶│   │
└───┘    └───┘    └───┘    └───┘
                             ▲
                             │
                            dev
```

##### 基于远程分支创建并切换分支

`git checkout -b dev origin/dev `

基于远程origin仓库的dev分支在本地创建一个名为dev的分支,立即切换到dev分支并创建本地与远程的对应关系。

#### 查看分支

`git branch`



```plain
$ git branch
* dev
  master
```



`git branch`命令会列出所有分支，当前分支前面会标一个`*`号。



#### 合并分支

##### 快速合并

`git merge 分支名`

一般是把其他分支合并到master(main)分支上，所以一般在master分支执行该操作

如把`dev`分支的工作成果合并到`master`分支上：

`````
                           HEAD
                             │
                             ▼
                          master
                             │
                             ▼
┌───┐    ┌───┐    ┌───┐    ┌───┐
│   │───▶│   │───▶│   │───▶│   │
└───┘    └───┘    └───┘    └───┘
                             ▲
                             │
                            dev
`````





```plain
$ git merge dev
Updating d46f35e..b17d20e
Fast-forward
 readme.txt | 1 +
 1 file changed, 1 insertion(+)
```



注意到上面的`Fast-forward`信息，Git告诉我们，这次合并是“快进模式”，也就是直接把`master`指向`dev`的当前提交，所以合并速度非常快。

##### 不使用Fast forward

通常，合并分支时，如果可能，Git会用`Fast forward`模式，但这种模式下，**我们使用git log图像化是看不到分支合并的。**

在git merge 时加上`--no-ff`参数，Git就会在**merge时生成一个新的commit**

如：

```plain
$ git merge --no-ff -m "merge with no-ff" dev
Merge made by the 'recursive' strategy.
 readme.txt | 1 +
 1 file changed, 1 insertion(+)
```

**因为本次合并要创建一个新的commit，所以加上`-m`参数，把commit描述写进去**。



合并后，我们用`git log`看看分支历史,**此时我们可以看到合并记录**：

```plain
$ git log --graph --pretty=oneline --abbrev-commit
*   e1e9c68 (HEAD -> master) merge with no-ff
|\  
| * f52c633 (dev) add merge
|/  
*   cf810e4 conflict fixed
...
```



可以看到，不使用`Fast forward`模式，merge后就像这样：

```
                                 HEAD
                                  │
                                  ▼
                                master
                                  │
                                  ▼
                                ┌───┐
                         ┌─────▶│   │
┌───┐    ┌───┐    ┌───┐  │      └───┘
│   │───▶│   │───▶│   │──┤        ▲
└───┘    └───┘    └───┘  │  ┌───┐ │
                         └─▶│   │─┘
                            └───┘
                              ▲
                              │
                             dev
```







#### 删除分支

`git branch -d 分支名`删除分支时，需要做各种检查

`git branch -D 分支名`不做任何检查，强制删除



#### 解决冲突



现在有新的`feature1`分支，修改`readme.txt`最后一行，改为：

```plain
Creating a new branch is quick AND simple.
```

切换到`master`分支，在`master`分支上把`readme.txt`文件的最后一行改为：

```plain
Creating a new branch is quick & simple.
```





这种情况下，Git无法执行“快速合并”，只能试图把各自的修改合并起来，但这种合并就可能会有冲突，我们试试看：

```plain
$ git merge feature1
Auto-merging readme.txt
CONFLICT (content): Merge conflict in readme.txt
Automatic merge failed; fix conflicts and then commit the result.
```



Git告诉我们，`readme.txt`文件存在冲突，必须手动解决冲突后再提交。

我们可以直接查看readme.txt的内容：

```plain
Git tracks changes of files.
<<<<<<< HEAD
Creating a new branch is quick & simple.
=======
Creating a new branch is quick AND simple.
>>>>>>> feature1
```

以下是head的所在分支的修改

`````
<<<<<<< HEAD
Creating a new branch is quick & simple.
=======
`````



以下是feature1的修改

`````
=======
Creating a new branch is quick AND simple.
>>>>>>> feature1
`````

**我们要做的是把它们两个删一个**,如下：

`````
Git tracks changes of files.
Creating a new branch is quick and simple.
`````

再提交：

```plain
$ git add readme.txt 
$ git commit -m "conflict fixed"
[master cf810e4] conflict fixed
```

现在，`master`分支和`feature1`分支合并



#### BUG分支

##### 重点

所有**未提交**的修改(即没有commit的修改)对于所有分支都是可见的，如你可以在main分支修改文件，然后切换到另一个分支dev后提交了这个修改，那么这会被算作是**dev分支的提交**。



##### git stash

如果有bug要修改，而现在的工作还没法提交，那么可以使用`git stash`把工作存储起来

```plain
$ git stash
Saved working directory and index state WIP on dev: f52c633 add merge
```

现在用`git status`查看工作区就是干净的。

> 我们之所以要这么做，是因为如4.2.7.1所说，**所有未提交的修改(即没有commit的修改)对于所有分支都是可见的**

##### 修改bug

完成上面的操作后，我们可以开始修改bug，假如要在`main`分支修改，就从main分支创建临时分支，修改完成后提交，然后我们要回到`dev`分支继续工作



##### 将修改复制到分支

因为`dev`是`main`分出来的。所以这个Bug在`dev`也存在。那么我们可以把main的提交复制到

dev。

`git cherry-pick 提交号`

首先切换到到`dev`分支，，然后使用git cherry-pick把main的修改复制到**当前分支**,**然后自动提交**

```plain
$ git branch
* dev
  master
$ git cherry-pick 4c805e2
[master 1d4b803] fix bug 101
 1 file changed, 1 insertion(+), 1 deletion(-)
```



##### 从stash恢复

用`git stash list`可以查看

```plain
$ git stash list
stash@{0}: WIP on dev: f52c633 add merge
```



1. `git stash apply`

    用`git stash apply`恢复后，stash的内容**不会被删除**，可以使用`git stash drop`来删除

    `````
    $ git stash list
    stash@{0}: WIP on dev01: 47bf059 dev01 commit 2
    
    $ git stash apply stash@{0}
    On branch dev01
    ...
    
    $ git stash drop stash@{0}
    Dropped stash@{0} (d6cfa2cfc79a76519ee13814e0e702ab4fc7825c)
    `````

    

2. git stash pop

    用git stash pop在恢复的同时也会把stash的内容删除

    `````
    $ git status
    On branch dev01
    nothing to commit, working tree clean
    
    $ git stash pop
    On branch dev01
    Changes not staged for commit:
      (use "git add <file>..." to update what will be committed)
      (use "git restore <file>..." to discard changes in working directory)
            modified:   a.txt
    
    no changes added to commit (use "git add" and/or "git commit -a")
    Dropped refs/stash@{0} (1827530c068642877520da6e83e576c867e179e2)
    
    $ git stash list
    
    `````

##### 推送到远程



1. 当同事已经push的修改和你的push冲突时，需要解决冲突

- 先使用`git branch --set-upstream-to=origin/dev  dev `创建与同事提交的分支对应的分支

`````
$ git branch --set-upstream-to=origin/dev  dev
Branch 'dev' set up to track remote branch 'dev' from 'origin'.
`````

- 切换到该分支，用`git pull`拉取同事的提交 

```plain
$ git pull
Auto-merging env.txt
CONFLICT (add/add): Merge conflict in env.txt
Automatic merge failed; fix conflicts and then commit the result.
```



- 然后手动解决冲突，和我们之前**解决本地冲突一样**，解决完后提交，再push



1. 当远程分支比你的分支新，需要git pull来合并

- 用git pull 拉取来合并
- 然后再push

#### git pull

`git pull `将远程分支的提交和本地提交merge，它可能会产生新的提交记录

**`git pull = git fetch + git merge`** 

1. 默认情况下

    - 如果本地分支与远程分支的提交历史是「线性的」（本地没有新提交，远程有新提交），会执行「快进合并（fast-forward）」，此时**不会产生新的提交记录**，只是将本地分支指针直接移动到远程分支的最新提交。
    - 如果本地分支有独立的新提交，远程分支也有新提交（历史出现分叉），合并时会生成一个**新的合并提交（merge commit）**，此时会产生一条新的提交记录。

2. 变基(`git pull --rebase`)

    这种情况下会执行「变基合并」，将本地的新提交「嫁接」到远程提交之后，**不会产生新的合并提交**，提交历史会保持线性。

    





































