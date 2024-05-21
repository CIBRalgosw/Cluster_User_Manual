#                                        vscode

#### VS Code（Visual Studio Code）是一个免费且开源的代码编辑器，由微软开发。它提供了丰富的功能和扩展性，使开发人员能够更高效地编写和调试代码.



##### 主要特点：

- ##### 多语言支持

- ##### 内置终端

- ##### 调试支持

- ##### 版本控制集成

- ##### 扩展生态系统

  

### 使用前准备：

- 本地环境：Windows 11
- 远端环境：集群linux(centos7.6)

VSCode经过配置，可以远程连接到集群，在本地进行远程的开发部署工作



> ### 连接集群登录节点



**1. 本地安装 VS Code 及插件**

下载本地操作系统对应的 VSCode安装包并根据步骤安装 [VS code download](https://code.visualstudio.com/download) 

打开VSCode软件， 安装 Remote SSH插件

<img src=".image\vscode\image-20231120201143795.png" alt="image-20231120201143795" />

**2. SSH密钥配置**

在Windows上生成SSH密钥，然后部署到集群中，这样每次重启VSCode之后，使用Remote-SSH访问集群中的文件时，不需要手动输入密码了

在Windows系统上执行下述命令生成SSH密钥：

```
按键盘Win+R 然后输入cmd
输入命令ssh-keygen
```

输入上述命令之后，遇到等待时，直接按ENTER键保持默认，需要敲击3次ENTER键，然后就会在 `C:\Users\it_12\.ssh 目录中产生SSH密钥文件：`id_rsa` 和 `id_rsa.pub

<img src=".image\vscode\image-20231120201618434.png" alt="image-20231120201618434" />



**3. 部署密钥文件到集群**

首先，确保当前用户的用户目录下是否存在 `.ssh` 目录（我这里的完整路径为：`/home/yuezhifeng_lab/wangyanmin/.ssh` ）

如果没有此目录需要创建.ssh目录

```
mkdir ~/.ssh
```

通过SFTP等方式将windows电脑生成的 `id_rsa.pub` 文件传输到集群的 `/home/yuezhifeng_lab/wangyanmin/.ssh` 目录中

```
[wangyanmin@login02 .ssh]$ cat id_rsa.pub >> authorized_keys
```



**4. Remote-SSH配置**

配置Remote-SSH，完成Remote-SSH的配置之后，就可以通过Remote-SSH访问集群的文件或者文件夹，就像在本地电脑开发一样。

打开VSCode，然后点击左侧的 “远程资源管理器” 图标，接着点击右上角的小齿轮（设置）：

<img src=".image\vscode\image-20231120202535978.png" alt="image-20231120202535978" />

在弹出来的窗口中，选择第一项，打开 config 文件，然后填写配置信息：

<img src=".image\vscode\image-20231120202637154.png" alt="image-20231120202637154" />

```
# Read more about SSH config files: https://linux.die.net/man/5/ssh_config
Host login02
    HostName 10.12.100.6
    User wangyanmin
    IdentityFile C:\Users\it_12\.ssh\id_rsa
```

 集群登录节点为login01（10.12.100.5）和login02 （10.12.100.6）

在完成上述配置之后，进入 “远程资源管理器” 选项，右键点击主机名，然后选择“Connect to Host in Current Window”或者“Connect to Host in New Window”：

![image-20240521131921826](.image\vscode\image-20240521131921826.png)

![image-20240521132042945](.image\vscode\image-20240521132042945.png)

点击“打开文件夹”可以打开集群中的文件夹，我这里打开集群里的DATA文件夹，此时我们就可以在Windows系统中，利用VSCode的Remote-SSH插件阅读集群的数据了，是不是很酷：

![image-20240521132055643](.image\vscode\image-20240521132055643.png)



> ### 连接集群计算节点

登录集群申请资源，申请的计算节点为（c02b03n02）

```
[wangyanmin@login01 ~]$ salloc -p q_cn -c 10  
[wangyanmin@login01 ~]$ job
     JOBID PARTITION     NAME            USER ST       TIME  NODES   CPUS  MIN_M   NODELIST
   7686552      q_cn     bash      wangyanmin  R       0:13      1     10  4900M  c02b03n02
```

![image-20240521132413454](.image\vscode\vscode.md)

![image-20240521132433375](.image\vscode\image-20240521132433375.png)

更新配置文件C:\Users\it_12\.ssh\config

![image-20240521135143334](.image\vscode\image-20240521135143334.png)

刷新配置



![image-20240521135202995](.image\vscode\image-20240521135202995.png)

先连接登录节点

![image-20240521135247124](.image\vscode\image-20240521135247124.png)

![image-20240521135313961](.image\vscode\image-20240521135313961.png)

连接计算节点

![image-20240521135333301](.image\vscode\image-20240521135333301.png)



![image-20240521135422126](.image\vscode\image-20240521135422126.png)
