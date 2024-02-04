
该说明包含两个部分：
* 转换变形场格式（把外部跑bigstream2的结果转换成pipeline里面可以使用的格式）
* 应用warp_spots

把外部跑bigstream2的结果转换成pipeline里面可以使用的格式。需要的文件，两个变形场，eg：

AFFINE_S4.mat, DEFORM_S3.nrrd

应用warp_spots需要有pipeline spot extraction的结果。

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

打开文件cvt_format_to_pipeline.py，参数在main那一行（if __ name__ == "__ main__"）下面，参数说明如下：
```python
# 输入变形场文件所在文件夹
input_dir = "/GPFS/yuezhifeng_lab_permanent/share/gong_lab/huanglinling/registration_s2/r7_to_r2"
# 全局变形场文件名
aff_p = f"{input_dir}/AFFINE_S4.mat"
# 局部变形场文件名
deform_p = f"{input_dir}/DEFORM_S3.nrrd"
# 输出路径，为避免再次拷贝，建议选择pipeline里registration的输出路径，若文件夹不存在则手动创建
out_dir = "/GPFS/gongrong_lab_temp/zqj00at00grlab/s2r7/outputs/s2_r7/registration"
# acq名字，跟pipeline run.sh里面acq_names参数值对应，主要为了创建文件夹命名而用。
fix_acq = "s2_r2"
mov_acq = "s2_r7"
# fix图像n5路径
fix_path = "/GPFS/yuezhifeng_lab_permanent/share/gong_lab/zhuqj/hll/run_231119/outputs/s2_r2/stitching/export.n5"
# 上面的deform用的s几做的这里就写多少
n5_subpath = "s3" 
# 并行处理使用多少核心
cores = 70
```
耗时情况举例说明：

数据s2r7，使用一个fat节点，cores设置70，需要内存大概500G，运行时间86分钟。

#### 转换变形场格式

修改完参数可通过下面两种方式（任选其一）来执行：
1. 申请资源+执行
```commandline
srun -p q_fat -c 72 --mem 1000G -J cvt_fmt python cvt_format_to_pipeline.py
```
2. 独占节点然后进去执行
```commandline
# 独占节点
salloc -p q_fat -c 72 --mem 1500G -J cvt_fmt
# 查看申请的哪个节点
job
# 进入
ssh name_of_node
# 进入独占节点后需要再次激活python环境
source ~/py38ac
# 执行脚本
python cvt_format_to_pipeline.py
```

如果担心fat节点被别人占用，建议以独占方式执行。

等待一个半小时，上述命令执行完，output目录结构如下：
```commandline
.
└── s2_r7-to-s2_r2
    ├── aff
    │   └── ransac_affine.mat
    ├── inv-affine-transform.mat
    ├── invtransform
    │   ├── attributes.json
    │   └── s3
    ├── transform
    │   ├── attributes.json
    │   └── s3
    └── warped
```
需要说明的是，上述方式不能生成完整结果，warped文件夹下缺少内容(warped结果仅仅是为了可视化查看需要，没有该结果也不影响后续spot_warped的执行)，warped文件夹内容通过执行下面命令来生成：
```commandline
python main_apply_local_transform.py \
--fixed /GPFS/yuezhifeng_lab_permanent/share/gong_lab/zhuqj/hll/run_231119/outputs/s2_r2/stitching/export.n5 \
--fixed-subpath c0/s3 \
\
--moving /GPFS/gongrong_lab_temp/zqj00at00grlab/s2r7/outputs/s2_r7/stitching/export.n5 \
--moving-subpath c3/s3 \
\
--output /GPFS/gongrong_lab_temp/zqj00at00grlab/s2r7/outputs/s2_r7/registration/s2_r7-to-s2_r2/warped \
--output-subpath c3/s3 \
\
--affine-transformations /GPFS/gongrong_lab_temp/zqj00at00grlab/s2r7/outputs/s2_r7/registration/s2_r7-to-s2_r2/aff/ransac_affine.mat \
--local-transform /GPFS/gongrong_lab_temp/zqj00at00grlab/s2r7/outputs/s2_r7/registration/s2_r7-to-s2_r2/transform \
--local-transform-subpath s3 \
\
--output-blocksize 256,256,256 \
--blocks-overlap-factor 0.125
```
上面命令为示例命令，参数值需要修改，参数说明如下：
* --fixed： fix图像路径
* --fixed-subpath subpath： 通道/scale
* --moving： mov图像路径
* --moving-subpath： subpath
* --output： 输出路径，一定要设置为上面的那个warped文件夹
* --output-subpath： subpath
* --affine-transformations： 全局变形场路径
* --local-transform： 局部变形场路径
* --local-transform-subpath： 局部变形场subpath
* --output-blocksize： 跟输出保存形式有关，使用上述默认，不建议更改
* --blocks-overlap-factor： 跟输出保存形式有关，使用上述默认，不建议更改

如果不是独占节点方式，上述命令前面需要加上srun命令, eg:
```commandline
srun -c 36 --mem 150G -J apply_transform
```

注意：
* local-transform-subpath只能设置为s3，因为咱们的数据只有s3的
* moving-subpath和output-subpath需要完全设置一致
* moving-subpath、output-subpath和fixed-subpath的scale需要设置一致
* fixed-subpath的通道设置为c0即可，不用跟另外两个保持一致
* 修改通道和scale，多次执行得到自己想要的结果

warped结果仅仅是为了可视化查看需要，没有该结果也不影响后续spot_warped的执行。

#### 应用warp_spots

转换变形场之后可以使用转换后的变形场进行warp_spots操作，示例命令如下：
```commandline
python \
main_apply_transform_coords.py \
--input-coords /GPFS/gongrong_lab_temp/zqj00at00grlab/s2r7/outputs/s2_r7/spots/spots_c1.txt \
--output-coords /GPFS/gongrong_lab_temp/zqj00at00grlab/s2r7/outputs/s2_r7/spots/spots_c1_warped.txt \
--input-volume /GPFS/gongrong_lab_temp/zqj00at00grlab/s2r7/outputs/s2_r7/stitching/export.n5 \
--input-dataset /c0/s3 \
--vector-field-transform /GPFS/gongrong_lab_temp/zqj00at00grlab/s2r7/outputs/s2_r7/registration/s2_r7-to-s2_r2/invtransform \
--vector-field-transform-subpath s3
```
参数说明：
* --input-coords：spot extraction结果坐标文件路径
* --output-coords：输出路径
* --input-volume：对应图像的路径，即mov image路径
* --input-dataset：对应图像subpath
* --vector-field-transform：选择上述生成的变形场里面的invtransform文件夹的路径
* --vector-field-transform-subpath：设置为s3

如果不是独占节点方式，上述命令前面需要加上srun命令, eg:
```commandline
srun -c 10 --mem 50G -J apply_transform_coords
```

执行完即可生成spots_c1_warped.txt文件，多个通道需要多次执行。
