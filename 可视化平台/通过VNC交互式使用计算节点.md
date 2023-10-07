## 通过VNC交互式使用计算节点



##### VNC是一款优秀的远程控制工具软件，由著名的 AT&T 的欧洲研究实验室开发的。VNC 是在基于 UNIX 和 Linux 操作系统的免费的开源软件，远程控制能力强大，高效实用。

1. **登录集群vpn**

    详见--集群用户手册第3-4页vpn登录
    访问链接：https://.cibr.ac.cn/Public/Upload/File/20221114/北京脑中心高性能集群使用手册_v5.0%20-%20用户版.pdf

2. **在你的电脑上使用终端ssh登录到集群**

    终端以MobaXterm为例
    下载链接：https://mobaxterm.mobatek.net/download-home-edition.html

> ​        `ssh cluster_account@10.12.100.88`
>

<img src="..\.image\vnc\1.png" alt="Image [1]" style="zoom: 80%;" />

3. **资源申请**

  申请资源以cpu资源为例

> ​       `srun -p q_cn -c 10 --pty bash -i`
>

<img src="..\.image\vnc\Image.png" alt="Image [1]" style="zoom: 80%;" />

- 已经跳转到申请的计算节点c03b06n04上
  #-p  q_cn  集群队列，其他队列可使用命令sinfo查看，需要GPU的程序可申请q_ai8/q_ai4队列
- -c 申请的核心数    根据个人需求进行申请所需的核心数
- sinfo -O Partition,NodeHost,CPUsState,CPUsLoad,Memory,AllocMem,Gres 可查看节点核心数的使用情况
- --pty bash -i 为固定参数
- 集群硬件资源配置可查看集群用户手册第2页
  下载链接：https://hpc.cibr.ac.cn/Public/Upload/File/20221114/北京脑中心高性能集群使用手册_v5.0%20-%20用户版.pdf

4. **启动vncserver服务**

  > `vncserver -ist`
  > `vncserver`

<img src="..\.image\vnc\Image [1].png" alt="Image [1]" style="zoom: 80%;" />

5. **在MobaXterm终端重新打开一个窗口并创建ssh隧道**

<img src="..\.image\vnc\Image [2].png" alt="Image [2]" style="zoom:80%;" />

>  ssh -L 5902:c03b06n04:5902 wangyanmin@10.12.100.88

<img src="..\.image\vnc\Image [3].png" alt="Image [1]" style="zoom: 80%;" />

**6.vnc链接**

> `打开Sessions—New session`



<img src="..\.image\vnc\Image [4].png" alt="Image [1]" style="zoom: 80%;" />

> `点击VNC—IP address—Port—Start session in(可选)—OK`

<img src="..\.image\vnc\Image [5].png" alt="Image [5]" style="zoom:80%;" />

> `登陆时需要您输入密码是启动vncserver的时候创建的密码`

<img src="..\.image\vnc\Image [6].png" alt="Image [6]" style="zoom: 67%;" />

> `右击鼠标-Open Terminal`

<img src="..\.image\vnc\Image [7].png" alt="Image [7]" style="zoom:67%;" />

以deeplabcut程序为例

> 环境加载： module load singularity_deeplabcut/2.2.3
> 程序运行命令: singularity $IMG python3 -m deeplabcut

<img src="..\.image\vnc\Image [8].png" alt="Image [8]" style="zoom:67%;" />

<img src="..\.image\vnc\Image [9].png" alt="Image [9]" style="zoom:67%;" />


7. **关闭vnc远程桌面服务**

  > `vncserver -kill :[screen]`

​       例如：我本次启动vncserver的会话编号为2

<img src="..\.image\vnc\Image [10].png" alt="Image [1]" style="zoom: 80%;" />

##### 常见问题：

1. 我的图形界面显示不全
   这样在启动vncserver服务的时候需要指定屏幕分辨率，比如我的电脑分辨率是1920x1080就可以设置为

> ​        `vnserver -geometry 1920x1080`

<img src="..\.image\vnc\Image [11].png" alt="Image [1]" style="zoom: 80%;" />

2. vnc登录密码忘记
   vnc忘记之前设置的密码，可通过使用vncpasswd 命令修改密码，之后就可以使用新密码登录

3. 2天之后我的任务为什么中断了
   目前集群单次任务运行最长为2天，如果需要更长的运行时间可在离任务结束提前3小时左右联系管理员进行延长



------



> **计算与数据科学中心网站：cdsc.cibr.ac.cn**
>
> **有问题可直接发送邮箱：cdsc@cibr.ac.cn**

