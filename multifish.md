# **EASI-FISH Nextflow Pipeline**

**This pipeline analyzes imagery collected using the [EASI-FISH](https://github.com/multiFISH/EASI-FISH) (Expansion-Assisted Iterative Fluorescence *In Situ* Hybridization) method described in [this Cell paper](https://doi.org/10.1016/j.cell.2021.11.024). It includes automated image stitching, distributed multi-round image registration, cell segmentation, and distributed spot detection**

### **版本**

| Organizations                               | Branch        | commint                                  | 运行方式 |
| ------------------------------------------- | ------------- | ---------------------------------------- | -------- |
| [CIBRalgosw](https://github.com/CIBRalgosw) | master        | 7b3248a50ef6416dc0a77364c440ccfcf2a31a2c | pipeline |
| [CIBRalgosw](https://github.com/CIBRalgosw) | multifish_dev | ec4b1db3e8f1f72a1d2e22e831c24af6719724e4 | pipeline |



### **安装CIBRalgosw  master分支**

安装路径：

```
/usr/nzx-cluster/apps/multifish/pipeline/CIBRalgosw_multifish/master
```

Clone this repository with the following command:

```
 git clone --recursive  https://github.com/CIBRalgosw/multifish.git
```

Before running the pipeline for the first time, run setup to pull in external dependencies:

```
./setup.sh
```

以 demo_tiny测试数据为例

首先加载环境运行环境

```
 module load multifish/multifish_nextflow_21.04.0_master_CIBR  
```

加载的软件和对应版本

```
nextflow/21.04.0   

singularity/3.7.0

multifish的安装路径  cd $multifish 可以直接进入到安装的路径下
```

demo_tiny.json和 demo_tiny.sh文件 存放路径为

```
/home/yuezhifeng_lab/wangyanmin/scratch60/test_data/multifish_test2
```

data数据存放路径为

```
/home/yuezhifeng_lab/wangyanmin/scratch60/test_data/multifish_test2/data
```

demo_tiny.json文件  （根据数据类型和大小进行调整json文件里的参数）

配置参数

调整workers数量 ("workers":40,)

```
{
    "data_manifest":"demo_tiny",
    "acq_names":"LHA3_R3_tiny,LHA3_R5_tiny",
    "ref_acq":"LHA3_R3_tiny",
    "channels":"c0,c1",
    "dapi_channel":"c1",
    "stitching_czi_pattern":"_V%02d",
    "stitching_block_size":"1024,1024,256",
    "retile_z_size":"128",
    "workers":40,
    "worker_cores":4,
    "gb_per_core":12,
    "driver_memory":"1g",
    "segmentation_cpus":8,
    "segmentation_memory":"2 G",
    "aff_scale":"s1",
    "def_scale":"s2",
    "registration_xy_stride":512,
    "registration_z_stride":64,
    "ransac_cpus":8,
    "ransac_memory":"1 G",
    "aff_scale_transform_memory":"2 G",
    "def_scale_transform_memory":"2 G",
    "deform_memory":"2 G",
    "registration_stitch_memory":"2 G",
    "registration_transform_memory":"2 G",
    "airlocalize_xy_stride":512,
    "airlocalize_xy_overlap":32,
    "airlocalize_z_stride":128,
    "airlocalize_z_overlap":32,
    "airlocalize_cpus":1,
    "airlocalize_memory":"2 G",
    "warp_spots_cpus":4,
    "warp_spots_memory":"2 G",
    "use_rsfish":true,
    "rsfish_workers":1,
    "rsfish_worker_cores":4,
    "rsfish_gb_per_core":12
}
```

demo_tiny.sh文件

```
#!/bin/bash
#
# This script downloads all the necessary data and runs the end-to-end pipeline on a small demo data set.
# 
# It takes 20 minutes to run on a 40 core machine with 128 GB of RAM. 
#
# If your /tmp directory is on a filesystem with less than 10 GB of space, you can set the TMPDIR variable
# in your environment before calling this script, for example, to use your /opt for all file access:
#
#   TMPDIR=/opt/tmp ./examples/demo_tiny.sh /opt/demo
#

DIR=$(cd "$(dirname "$0")"; pwd)
BASEDIR=$(realpath $DIR/..)

# The temporary directory needs to have 10 GB to store large Docker images
export TMPDIR="${TMPDIR:-/home/yuezhifeng_lab/wangyanmin/scratch60/test_data/multifish_test2/tmp}"
export SINGULARITY_TMPDIR="${SINGULARITY_TMPDIR:-$TMPDIR}"
export SINGULARITY_CACHEDIR="${SINGULARITY_CACHEDIR:-$TMPDIR/singularity}"
export workDir=`date +%Y-%m-%d-%H-%M-%S`
export NXF_LOG_FILE="/home/yuezhifeng_lab/wangyanmin/scratch60/test_data/multifish_test2/$workDir/`date +%Y%m%H%M%S`.nextflow.log"

mkdir -p $TMPDIR
mkdir -p $SINGULARITY_TMPDIR
mkdir -p $SINGULARITY_CACHEDIR

if [[ "$#" -lt 1 ]]; then
    echo "Usage: $0 <data dir>"
    echo ""
    echo "This is a demonstration of the EASI-FISH analysis pipeline on a small sized cutout of the LHA3 data set. "
    echo "The data dir will be created, data will be downloaded there based on the manifest, and the "
    echo "full end-to-end pipeline will run on these data, producing output in the specified data dir."
    echo ""
    exit 1
fi

datadir=$(realpath $1)
shift # eat the first argument so that $@ works later

#
# Memory Considerations
# =====================
# 
# The value of workers*worker_cores*gb_per_core determines the total Spark memory for each acquisition registration. 
# For the demo, two of these need to fit in main memory. The settings below work for a 40 core machine with 128 GB RAM.
#
# Reducing the gb_per_core to 2 reduces total memory consumption but doubles processing time.
#

/usr/nzx-cluster/apps/multifish/pipeline/CIBRalgosw_multifish/master/main.nf \
    -profile cibr --cibr_opts '-p q_cn' \
    -w "/home/yuezhifeng_lab/wangyanmin/scratch60/test_data/multifish_test2/$workDir" \
    -params-file "/home/yuezhifeng_lab/wangyanmin/scratch60/test_data/multifish_test2/demo_tiny.json" \
    --runtime_opts "-B $datadir -B $TMPDIR" \
    --shared_work_dir "$datadir" "$@"

```



文件第17行tmp路径指定

```
修改前：export TMPDIR="${TMPDIR:-/tmp}"

修改后:export TMPDIR="${TMPDIR:-/home/yuezhifeng_lab/wangyanmin/scratch60/test_data/multifish_test2/tmp}" 
```

增加环境变量

```
export workDir=`date +%Y-%m-%d-%H-%M-%S`

export NXF_LOG_FILE="/home/yuezhifeng_lab/wangyanmin/scratch60/test_data/multifish_test2/`date +%Y%m%H%M%S`.nextflow.log"
```

./main.nf 命令修改

```
修改前：

./main.nf \
    -params-file "./examples/demo_tiny.json" \
    --runtime_opts "-B $datadir -B $TMPDIR" \
    --shared_work_dir "$datadir" "$@"
    
修改后:
/usr/nzx-cluster/apps/multifish/pipeline/CIBRalgosw_multifish/master/main.nf \
    -profile cibr --cibr_opts '-p q_cn' \
    -w "/home/yuezhifeng_lab/wangyanmin/scratch60/test_data/multifish_test2/$workDir" \
    -params-file "/home/yuezhifeng_lab/wangyanmin/scratch60/test_data/multifish_test2/demo_tiny.json" \
    --runtime_opts "-B $datadir -B $TMPDIR" \
    --shared_work_dir "$datadir" "$@"
```

 



运行命令 :

```
/home/yuezhifeng_lab/wangyanmin/scratch60/test_data/multifish_test2/CIBR_master_demo_tiny.sh /home/yuezhifeng_lab/wangyanmin/scratch60/test_data/multifish_test2/data
```



### **安装CIBRalgosw  dev分支**

安装路径：

```
/usr/nzx-cluster/apps/multifish/pipeline/CIBRalgosw_multifish/dev
```

Clone this repository with the following command:

```
git clone --recursive  https://github.com/CIBRalgosw/multifish.git
git checkout multifish_dev
git pull; git submodule sync; git submodule update --init --recursive
```

Before running the pipeline for the first time, run setup to pull in external dependencies:

```
./setup.sh
```

以 demo_tiny测试数据为例

首先加载环境运行环境

```
 module load multifish/multifish_nextflow_23.04.1_dev_CIBR  
```

加载的软件和对应版本

```
nextflow/23.04.1

singularity/3.7.0

multifish的安装路径  cd $multifish 可以直接进入到安装的路径下
```

demo_tiny.json和 demo_tiny.sh文件 存放路径为

```
/home/yuezhifeng_lab/wangyanmin/scratch60/test_data/multifish_test2
```

data数据存放路径为

```
/home/yuezhifeng_lab/wangyanmin/scratch60/test_data/multifish_test2/data
```

demo_tiny.json文件  （根据数据类型和大小进行调整json文件里的参数）

默认配置参数

调整workers数量 ("workers":40,)

```
{
    "data_manifest":"demo_tiny",
    "acq_names":"LHA3_R3_tiny,LHA3_R5_tiny",
    "ref_acq":"LHA3_R3_tiny",
    "channels":"c0,c1",
    "dapi_channel":"c1",
    "stitching_czi_pattern":"_V%02d",
    "stitching_block_size":"1024,1024,256",
    "retile_z_size":"128",
    "workers":40,
    "worker_cores":4,
    "gb_per_core":12,
    "driver_memory":"1g",
    "segmentation_cpus":8,
    "segmentation_memory":"2 G",
    "aff_scale":"s1",
    "def_scale":"s2",
    "registration_xy_stride":512,
    "registration_z_stride":64,
    "ransac_cpus":8,
    "ransac_memory":"1 G",
    "aff_scale_transform_memory":"2 G",
    "def_scale_transform_memory":"2 G",
    "deform_memory":"2 G",
    "registration_stitch_memory":"2 G",
    "registration_transform_memory":"2 G",
    "airlocalize_xy_stride":512,
    "airlocalize_xy_overlap":32,
    "airlocalize_z_stride":128,
    "airlocalize_z_overlap":32,
    "airlocalize_cpus":1,
    "airlocalize_memory":"2 G",
    "warp_spots_cpus":4,
    "warp_spots_memory":"2 G",
    "use_rsfish":true,
    "rsfish_workers":1,
    "rsfish_worker_cores":4,
    "rsfish_gb_per_core":12
}
```

demo_tiny.sh文件

```
#!/bin/bash
# This script downloads all the necessary data and runs the end-to-end pipeline on a small demo data set. 
# It takes 20 minutes to run on a 40 core machine with 128 GB of RAM. 
# If your /tmp directory is on a filesystem with less than 10 GB of space, you can set the TMPDIR variable
# in your environment before calling this script, for example, to use your /opt for all file access:
#   TMPDIR=/opt/tmp ./examples/demo_tiny.sh /opt/demo

DIR=$(cd "$(dirname "$0")"; pwd)
BASEDIR=$(realpath $DIR/..)

# The temporary directory needs to have 10 GB to store large Docker images
export TMPDIR="${TMPDIR:-/home/yuezhifeng_lab/wangyanmin/scratch60/test_data/multifish_test2/tmp}"
export SINGULARITY_TMPDIR="${SINGULARITY_TMPDIR:-$TMPDIR}"
export SINGULARITY_CACHEDIR="${SINGULARITY_CACHEDIR:-$TMPDIR/singularity}"
export workDir=`date +%Y-%m-%d-%H-%M-%S`
export NXF_LOG_FILE="/home/yuezhifeng_lab/wangyanmin/scratch60/test_data/multifish_test2/$workDir/`date +%Y%m%H%M%S`.nextflow.log"

mkdir -p $TMPDIR
mkdir -p $SINGULARITY_TMPDIR
mkdir -p $SINGULARITY_CACHEDIR

if [[ "$#" -lt 1 ]]; then
    echo "Usage: $0 <data dir>"
    echo ""
    echo "This is a demonstration of the EASI-FISH analysis pipeline on a small sized cutout of the LHA3 data set. "
    echo "The data dir will be created, data will be downloaded there based on the manifest, and the "
    echo "full end-to-end pipeline will run on these data, producing output in the specified data dir."
    echo ""
    exit 1
fi

datadir=$(realpath $1)
shift # eat the first argument so that $@ works later
#
# Memory Considerations
# =====================
# 
# The value of workers*worker_cores*gb_per_core determines the total Spark memory for each acquisition registration. 
# For the demo, two of these need to fit in main memory. The settings below work for a 40 core machine with 128 GB RAM.
#
# Reducing the gb_per_core to 2 reduces total memory consumption but doubles processing time.

/usr/nzx-cluster/apps/multifish/pipeline/CIBRalgosw_multifish/dev/main.nf \
    -profile cibr --cibr_opts '-p q_cn' \
    -w "/home/yuezhifeng_lab/wangyanmin/scratch60/test_data/multifish_test2/$workDir" \
    -params-file "/home/yuezhifeng_lab/wangyanmin/scratch60/test_data/multifish_test2/demo_tiny.json" \
    --runtime_opts "-B $datadir -B $TMPDIR -B /GPFS/yuezhifeng_lab_temp/wangyanmin/test_data/multifish_test2" \
    --shared_work_dir "$datadir" "$@"

```

文件第17行tmp路径指定

```
修改前：export TMPDIR="${TMPDIR:-/tmp}"

修改后:export TMPDIR="${TMPDIR:-/home/yuezhifeng_lab/wangyanmin/scratch60/test_data/multifish_test2/tmp}" 
```

增加环境变量

```
export workDir=`date +%Y-%m-%d-%H-%M-%S`

export NXF_LOG_FILE="/home/yuezhifeng_lab/wangyanmin/scratch60/test_data/multifish_test2/`date +%Y%m%H%M%S`.nextflow.log"
```

./main.nf 命令修改

```
修改前：

./main.nf \
    -params-file "./examples/demo_tiny.json" \
    --runtime_opts "-B $datadir -B $TMPDIR" \
    --shared_work_dir "$datadir" "$@"
    
修改后:
/usr/nzx-cluster/apps/multifish/pipeline/CIBRalgosw_multifish/dev/main.nf \
    -profile cibr --cibr_opts '-p q_cn' \
    -w "/home/yuezhifeng_lab/wangyanmin/scratch60/test_data/multifish_test2/$workDir" \
    -params-file "/home/yuezhifeng_lab/wangyanmin/scratch60/test_data/multifish_test2/demo_tiny.json" \
    --runtime_opts "-B $datadir -B $TMPDIR -B /GPFS/yuezhifeng_lab_temp/wangyanmin/test_data/multifish_test2" \
    --shared_work_dir "$datadir" "$@"
```

 



运行命令 :

```
/home/yuezhifeng_lab/wangyanmin/scratch60/test_data/multifish_test2/demo_tiny.sh /home/yuezhifeng_lab/wangyanmin/scratch60/test_data/multifish_test2/data
```



