#                                                         Jupyter Notebook



#### Jupyter是一个非营利组织，旨在“为数十种编程语言的交互式计算开发开源软件，开放标准和服务”。2014年由Fernando Pérez从IPython中衍生出来，Jupyter支持几十种语言的执行环境。Jupyter项目开发并支持交互式计算产品Jupyter Notebook、JupyterHub和JupyterLab，这是Jupyter Notebook的下一代版本



**Jupyter相关组件的功能和用途主要区别：**

- Jupyter Notebook是最常用的Jupyter项目组件，用于创建和共享交互式文档。它使用内核来执行代码。

- Jupyter Kernels是用于在Jupyter Notebook中执行不同编程语言的插件，每个编程语言有一个对应的内核。

- JupyterHub是一个多用户的Jupyter Notebook服务器，允许多个用户同时访问和使用Jupyter Notebook。

- JupyterHub API是JupyterHub提供的一组RESTful API，用于管理和操作JupyterHub服务器。

- JupyterLab是Jupyter项目的下一代Web界面，提供了更丰富的交互式计算环境，支持多个Notebook和其他组件的同时显示。

  ### 版本

| version | build | squeue  |
| ------- | ----- | ------- |
| 3.6.3   | conda | cpu/gpu |

### 软件安装路径：

/usr/nzx-cluster/apps/jupyter/jupyter_notebook

### 使用前准备：

- 使用终端Terminal：MobaXterm
- 软件：jupyter-notebook

用户可以通过slurm运行jupyter-notebook、jupyter-lab，需要slurm提交作业至计算节点，并拥有足够的计算资源，将本地笔记本电脑的SSH端口转发到计算节点，必须创建隧道，因为您无法直接通过ssh登录到计算节点



**1.首先ssh登录到集群的登录节点**

```
ssh wangyanmin@10.12.100.88
```

**2.创建脚本jupyter-notebook.sh**

```
#!/bin/bash 
#SBATCH -J jupyter 
#SBATCH -p q_cn           #根据需求申请不同的队列
#SBATCH -o job.%j.out 
#SBATCH -c 10             #根据需求申请不同的资源
#SBATCH --mail-type=all 
#SBATCH --mail-user=wangyanmin@cibr.ac.cn 

module load jupyter/3.6.3    #加载公共的jupyter环境或者加载自己账户下的环境

jupyter-notebook --ip=0.0.0.0 --port=14780   #以14780端口为例，可申请不同的端口，具体以日志输出的端口为准
```



**3.提交作业**

```
sbatch   jupyter-notebook.sh
```

**4.查看作业分配状态，已分配到c03b06n04节点上**

```
[wangyanmin@login02 jupyter]$ job
     JOBID PARTITION     NAME            USER ST       TIME  NODES   CPUS  MIN_M   NODELIST
   6800568      q_cn  jupyter      wangyanmin  R       1:00      1     10  4900M  c03b06n04
```

**5.查看日志输出**

```
To access the notebook, open this file in a browser: 
    file:///home/yuezhifeng_lab/wangyanmin/.local/share/jupyter/runtime/nbserver-341619-open.html 
Or copy and paste one of these URLs: 
    http://c03b06n04:14780/?token=024538b3cd59f7006e0365c81da450eb0498188e399485ed 
 or **http://127.0.0.1:14780/?token=024538b3cd59f7006e0365c81da450eb0498188e399485ed** 
```

需要拷贝127.0.0.1这一个网址：

**http://127.0.0.1:14780/?token=024538b3cd59f7006e0365c81da450eb0498188e399485ed**

**6.在MobaXterm上打开一个新的窗口并创建ssh隧道:（第一个14780为本地端口,不能冲突，一个jupyter只能使用一个不同的端口，可随意设置） 第二个14780端口要和日志输出的端口为准，参考5日志输出信息）**

```
ssh -L 14780:c03b06n04:14780 wangyanmin@10.12.100.88
```

**7.在笔记本电脑上打开浏览器窗口，您就可以直接浏览**

**http://127.0.0.1:14780/?token=024538b3cd59f7006e0365c81da450eb0498188e399485ed**





