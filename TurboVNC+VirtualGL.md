## 通过TurboVNC+VirtuGL交互式使用计算节点



##### TurboVNC is a derivative of VNC (Virtual Network Computing) that is tuned to provide peak performance for 3D and video workloads

##### **TurboVNC, when used with [VirtualGL](https://www.virtualgl.org/), provides a highly performant and robust solution for remotely displaying 3D applications over all types of networks.**



1. ##### **登录集群vpn**

详见--集群用户手册第3-4页vpn登录
访问链接：https://cdsc.cibr.ac.cn/Public/Upload/File/20221114/北京脑中心高性能集群使用手册_v5.0%20-%20用户版.pdf

2. ##### **在你的电脑上使用终端ssh登录到集群**

终端以MobaXterm为例

下载链接：https://mobaxterm.mobatek.net/download-home-edition.html

```
ssh cluster_account@10.12.100.88
```

<img src=".image\turbovnc\image-20231129205129313.png" alt="image-20231129205129313" />



3. ##### 资源申请

  申请资源以gpu资源为例

```
 srun -p q_ai8 -c 4 --gres=gpu:1 --pty bash -i
```

<img src=".image\turbovnc\image-20231129205247673.png" alt="image-20231129205247673" />

- 已经跳转到申请的gpu节点的ai01上
  #-p  q_ai8  集群队列，其他队列可使用命令sinfo查看
- -c 申请的核心数    根据个人需求进行申请所需的核心数
- sinfo -O Partition,NodeHost,CPUsState,CPUsLoad,Memory,AllocMem,Gres 可查看节点核心数的使用情况
- --pty bash -i 为固定参数
- 集群硬件资源配置可查看集群用户手册第2页
  下载链接：https://hpc.cibr.ac.cn/Public/Upload/File/20221114/北京脑中心高性能集群使用手册_v5.0%20-%20用户版.pdf



4.  ##### **启动vncserver服务**

```
module load turbovnc/3.0.3
vncserver -list
vncserver
```

<img src=".image\turbovnc\image-20231129210721399.png" alt="image-20231129210721399" />

5. ##### **在MobaXterm终端重新打开一个窗口并创建ssh隧道**

<img src=".image\turbovnc\image-20231129211020283.png" alt="image-20231129211020283" />

```
ssh -L 5902:ai01:5902 wangyanmin@10.12.100.88
```

<img src=".image\turbovnc\image-20231129212650324.png" alt="image-20231129212650324" />

6. ##### vnc链接

```
打开Sessions—New session
```

<img src=".image\turbovnc\image-20231130123404361.png" alt="image-20231130123404361" />

```
点击VNC—IP address—Port—Start session in(可选)—OK
```

<img src=".image\turbovnc\image-20231129214048429.png" alt="image-20231129214048429" />

```
登陆时需要您输入密码是启动vncserver的时候创建的密码
```

<img src=".image\turbovnc\image-20231129214223491.png" alt="image-20231129214220947" />



```
点击Activities-Terminal
```

<img src=".image\turbovnc\image-20231129214405781.png" alt="image-20231129214405781" />

7. ##### 加载 turbovnc/3.0.3  virtualgl/3.1 环境

```
module load turbovnc/3.0.3 virtualgl/3.1
```

<img src=".image\turbovnc\image-20231129214739659.png" alt="image-20231129214739659" />

8. ##### 查看申请的GPU的编号

##### 

查看申请的GPU编号：
nvidia-smi -q | grep "Minor Number"

```
[wangyanmin@ai01 ~]$ nvidia-smi -q | grep "Minor Number"
    Minor Number                          : 5
```



9. ##### 运行

```
vglrun -d /dev/dri/card5 glxgears
```

-  vglrun 启用VirtualGL 
-  -d  /dev/dri/card5   5为申请的GPU卡的编号 
-  glxgears 运行的程序

##### 
