### Note
For yanmin.

该说明文档是脱离multifish pipeline单独跑bigstrem的部署说明。

思路是通过anaconda安装环境，通过module load的方式开放给大家使用。

### 使用Anaconda安装方式

1. 创建python环境并激活

```commandline
conda create --name bigstream_cibr_slurm python=3.10
source activate bigstream_cibr_slurm
```

2. 安装Bigstream和ClusterWrap包

找一个合适的路径，把这两个包clone到本地（后续不要删除）：
```commandline
git clone https://github.com/CIBRalgosw/bigstream.git
git clone https://github.com/CIBRalgosw/ClusterWrap.git -b feature_expose_memory_option
```
进入两个仓库分别执行：
```commandline
git pull; git submodule sync; git submodule update --init --recursive
```
使用pip的方式安装这两个python包到当前环境（先安装ClustreWrap再安装Bigstream）：
```commandline
pip install -e [ClusterWrap本地仓库路径]
pip install -e [bigstream本地仓库路径]
```

