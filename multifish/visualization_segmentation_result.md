### Note

该文档是查看multifish pipeline里的segmentation模块效果的使用说明。

### 使用基础

* 有一定python基础

* 会以VNC的方式使用集群

### 环境

可以使用已有的python环境，也可以自己创建新的，需要满足该环境下有下面几个包：
* numpy
* tifffile
* zarr
* napari

若缺少某个包，对应的安装命令如下：
```commandline
pip install numpy
pip install tifffile
pip install zarr
pip install "napari[all]"
```

起VNC注意事项：
* [参考教程](https://github.com/CIBRalgosw/Cluster_User_Manual/blob/main/%E5%8F%AF%E8%A7%86%E5%8C%96%E5%B9%B3%E5%8F%B0/%E9%80%9A%E8%BF%87VNC%E4%BA%A4%E4%BA%92%E5%BC%8F%E4%BD%BF%E7%94%A8%E8%AE%A1%E7%AE%97%E8%8A%82%E7%82%B9.md)
* VNC要起在计算节点
* 该计算节点至少申请内存50G
* 该计算节点至少申请核心10个(核心越多使用napari操作起来(比如旋转3D图像、放大缩小等)越流畅)

### 代码与参数

可以参考下面这个python代码来运行自己的数据:

[visualization_segmentation_result.py](https://github.com/CIBRalgosw/Cluster_User_Manual/blob/cv/multifish/visualization_segmentation_result.py)

主要参数如下：
```python
###################### params ##########################
# pipeline的output目录
output_dir = (
    "/GPFS/yuezhifeng_lab_permanent/share/gong_lab/zhuqj/hll/run_231116/outputs"
)
# 样本
sample = "s1"
dapi = "c0"
segmentation_scale = "s2"

###################### params ##########################
```
output_dir为pipeline对应的输出路径，sample为分割的样本或者round，dapi为dapi通道，segmentation_scale为分割使用的scale，默认是s2。
这些参数设置好之后会自动计算相应的segmentation路径以及stitching路径。

修改好参数，在VNC里面执行改代码：
```commandline
python visualization_segmentation_result.py
```

### napari使用

设置正确参数然后运行代码后，等一会，会启动napari界面，其中有两个图层，一个是image，一个是分割的label，修改label透明度或者隐藏某个图层即可对比查看分割效果。