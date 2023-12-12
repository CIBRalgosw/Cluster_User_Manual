### Note

该说明文档是脱离multifish pipeline单独跑bigstrem2的使用说明。

### 使用基础

* 有一定python基础

* 会在集群使用jupyter notebook

### 使用说明

可以参考下面这个jupyter notebook来运行自己的数据

[bigstream2_align_from_Greg.ipynb](https://github.com/CIBRalgosw/Cluster_User_Manual/blob/cv/bigstream/bigstream2_align_from_Greg.ipynb)

下载下来之后，还需要加载环境、修改参数，然后才能运行。

对应的也有py文件，也可以直接使用python运行：[bigstream2_align_from_Greg.py](https://github.com/CIBRalgosw/Cluster_User_Manual/blob/cv/bigstream/bigstream2_align_from_Greg.py)

### 环境加载

```commandline
module load bigstream/ca7e77
```
### 参数设置

#### 分布式计算参数 

算法先进行global alignment，这一步没有使用分布式计算。

然后进行local alignment，这一步使用了分布式计算，这里所说的分布式参数主要针对这一步。

这一步设置在notebook中local这个cell里面，主要涉及以下几个参数：

```python
cluster_kwargs = {
    'queue':'q_cn,q_fat,q_fat_l,q_fat_c,q_fat_z',
    'job_cpu':12,   # 每个worker的cpu数量
    'memory':'30GB', # 每个worker的内存
    'threads':1,   
    'min_workers':90,   
    'max_workers':90,   
}
```

上面是建议参数值，适用于资源充足的情况，具体还要根据实际情况来做出最合适的修改。

主要建议修改的参数有三个：
```python
min_workers,max_workers # 设置多少worker
job_cpu # 每个worker分配多少cpu
memory  # 每个worker分配多少内存
```
job_cpu和memory直接在上述参数里面设置，workers数量可以通过使min_workers和max_workers相等的方式来设置。

设置这些参数之前可以通过下面命令查看集群资源使用情况：
```commandline
sinfo
```
或者结果更详细的这个命令：
```commandline
sinfo -O Partition,NodeHost,CPUsLoad,CPUsState,Memory,AllocMem,Gres
```
根据上述结果可以大概估计出一个合适的参数设置方案。

刚开始运行时，可以使用```job```命令查看申请的资源是不是在排队，若在排队，说明申请的资源太多了，空余资源不够用，可以减少workers的数量再重新运行尝试。

#### 算法参数

待更新...

### 关键包版本信息

#### Bigstream2
* Github: https://github.com/CIBRalgosw/bigstream
* Branch: master
* Commit: 7ca7e7707ce159461821bb0e5de2f02e33d02885
#### ClusterWarp
* Github: https://github.com/CIBRalgosw/ClusterWrap
* Branch: feature_expose_memory_option
* Commit: 4e932fe264102ffe0ab39fa58add7cbe387689d9