
该文档主要说：
* 怎样使用pipeline的中间结果，脱离pipeline把一个点坐标文件根据变形场做一个转换，eg:
  spots_c1.txt --> spots_c1_warped.txt


### 步骤

#### 加载环境进入workdir

1. 首先进入账户zqj00at00grlab
```commandline
ssh zqj00at00grlab@10.12.100.6
```
已登录其他账户的情况下也可以这样：
```commandline
su - zqj00at00grlab
```
2. 进入到workdir
```commandline
cd scratch60/IMAGES_codes/bigstream
```
3. 激活python环境
```commandline
source ~/py38ac
```

#### 修改参数

打开文件zqj_apply_transform_coords.py，参数设置在_run_apply_transform函数里开头地方，参数说明如下：
```python
# ************* params *************
dir = "/GPFS/gongrong_lab_temp/zqj00at00grlab/s2r6/outputs/s2_r6"  # 文件夹路径
input_coords_p = f"{dir}/spots/spots_c2.txt"  # 输入点坐标文件
output_coords_p = f"{dir}/spots/spots_c2_warped.txt"  # 输出点坐标文件
affine_transformations = [  # 全局变形场
    f"{dir}/registration/s2_r6-to-s2_r2/inv-affine-transform.mat"
]
local_transform = f"{dir}/registration/s2_r6-to-s2_r2/invtransform"  # 局部变形场
local_transform_subpath = "s3"  # 局部变形场scale
pixel_resolution = [0.23, 0.23, 0.42]  # 数据s0时的分辨率
scales = [  # scale信息
    [1, 1, 1],  # s0
    [2, 2, 1],  # s1
    [4, 4, 2],  # s2
    [8, 8, 4],  # s3
]
downsampling_factors = scales[3]  # 选择哪个scale，变形场对应的scale
# ************* params *************
```

#### 执行

修改完参数可通过下面两种方式（任选其一）来执行：
1. 申请资源+执行
```commandline
srun -p q_cn -c 18 --mem 100G -J apply_transform python zqj_apply_transform_coords.py
```
2. 独占节点然后进去执行
```commandline
# 独占节点
salloc -p q_cn -c 36 --mem 150G -J apply_transform
# 查看申请的哪个节点
job
# 进入
ssh name_of_node
# 进入独占节点后需要再次激活python环境
source ~/py38ac
# 执行脚本
python zqj_apply_transform_coords.py
```

如果担心节点被别人占用，建议以独占方式执行。

等待大概10分钟左右即可执行完毕。

