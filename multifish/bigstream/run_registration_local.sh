#!/bin/bash

data_dir="/GPFS/yuezhifeng_lab_permanent/share/gong_lab/huanglinling/5gene_3round/inputs/"
work_dir="/GPFS/yuezhifeng_lab_permanent/share/gong_lab/zhuqj/hll/local2/"
rootlog_dir=${work_dir}/logs/
output_dir=${work_dir}/outputs

export TMPDIR=${work_dir}/tmp
export SINGULARITY_TMPDIR=${work_dir}/tmp/singularity

timenow=$(date +%Y.%m.%d-%H.%M.%S)
log_dir="${rootlog_dir}${timenow}_registration/"
spark_work_dir="${log_dir}spark"
nextflow_log="${log_dir}nextflow.log"
nextflow_work_dir="${log_dir}nextflow_work_dir"

mkdir $log_dir
echo logdir: $log_dir

export NXF_LOG_FILE=$nextflow_log

# copy this file to logdir
cp -rp $(pwd)/$0 $log_dir

module load multifish/multifish_nextflow_23.04.1_dev_Janelia
/usr/nzx-cluster/apps/multifish/pipeline/JaneliaSciComp_multifish/dev/main.nf \
        -w $nextflow_work_dir \
        --verify_md5 false \
        --runtime_opts "-B $work_dir -B $data_dir" \
        --spark_work_dir $spark_work_dir \
        --data_dir ${data_dir} \
        --output_dir $output_dir \
        --acq_names "r3_5genes,r2_5genes" \
	--ref_acq "r2_5genes" \
        --channels "c0,c1,c2,c3" \
        --dapi_channel "c0" \
        --skip stitching,segmentation,spot_extraction,warp_spots,measure_intensities,assign_spots \
        \
        --use_bigstream true \
        --use_existing_global_transform \
        --bigstream_global_cpus 2 \
        --bigstream_global_mem_gb 50 \
        --bigstream_local_cpus 8 \
        --bigstream_local_mem_gb 100 \
        --bigstream_global_steps "ransac,affine" \
        --bigstream_local_steps "ransac,deform" \
        --dask_workers 8 \
        --dask_worker_cores 4 \
        --dask_worker_threads 2 \
        --dask_worker_mem_gb_per_core 24 \
        --global_iterations 100 \
        --local_iterations 5 \
        --local_ransac_cc_radius 8 \
        --local_ransac_nspots 2000 \
        --local_ransac_diagonal_constraint 0.6 \
        --global_ransac_fix_spot_winsorize_limits "0,0.02" \
        --global_ransac_mov_spot_winsorize_limits "0,0.02" \
        --local_ransac_fix_spot_winsorize_limits "0,0.02" \
        --local_ransac_mov_spot_winsorize_limits "0,0.02"
