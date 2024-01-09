### Note

该说明文档是使用multifish pipeline Janelia dev以local方式跑bigstrem2的使用说明。

### 步骤

#### 下载模板sh文件

[run_registration_local.sh](https://github.com/CIBRalgosw/Cluster_User_Manual/blob/cv/bigstream/run_registration_local.sh)

#### 修改参数，主要是数据路径、算法参数等

#### 独占方式申请一个胖节点，然后运行脚本

为了便于查看实时的处理进度，建议独占方式申请一个节点，再ssh进去运行脚本。

```commandline
salloc -p q_fat,q_fat_l,q_fat_c,q_fat_z -c 72 --mem 1400G -J local
```

ssh进去刚才申请的节点，比如：

```commandline
ssh fat01
```

然后直接执行脚本：

```commandline
./run_registration_local.sh
```

### 其他说明

* 该说明有很多地方待进一步完善，有不明白的地方随时联系。