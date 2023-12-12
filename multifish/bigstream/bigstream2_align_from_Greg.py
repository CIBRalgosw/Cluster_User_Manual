########################## inputs ##########################
import numpy as np, zarr, nrrd

fix_path = "/GPFS/yuezhifeng_lab_permanent/share/gong_lab/huanglinling/bigstitch/s2/fused/fused.n5/setup0"
mov_path = "/GPFS/yuezhifeng_lab_permanent/share/gong_lab/huanglinling/bigstitch/r4s2/fused/fused.n5/setup0"
exp_factor = 1  # replace this with the known expansion factor for your sample to use pre-expansion units

# load fix data and spacing
fix_zarr = zarr.open(store=zarr.N5Store(fix_path), path="timepoint0", mode="r")
fix_spacing = np.array([0.42, 0.23, 0.23])
fix_spacing_s1 = fix_spacing * [1, 2, 2]
fix_spacing_s3 = fix_spacing * [4, 8, 8]

# load mov data and spacing
mov_zarr = zarr.open(store=zarr.N5Store(mov_path), path="timepoint0", mode="r")
mov_spacing = np.array([0.42, 0.23, 0.23])
mov_spacing_s1 = mov_spacing * [1, 2, 2]
mov_spacing_s3 = mov_spacing * [4, 8, 8]


########################## global ##########################
# alignment functions
from bigstream.align import alignment_pipeline
from bigstream.transform import apply_transform
from scipy.ndimage import zoom

# output_dir
output_dir = (
    "/GPFS/yuezhifeng_lab_permanent/share/gong_lab/zhuqj/hll/debug_bigstream/outipynb"
)

# get global alignment channels
fix = fix_zarr["s3"][...]
mov = mov_zarr["s3"][...]
print(fix.dtype, fix.shape)
print(mov.dtype, mov.shape)

# resample in xy to save room
fix_custom = zoom(fix, (1, 0.5, 0.5), order=1)
mov_custom = zoom(mov, (1, 0.5, 0.5), order=1)
fix_spacing_custom = fix_spacing_s3 * (1, 2, 2)
mov_spacing_custom = mov_spacing_s3 * (1, 2, 2)

# define alignment steps
ransac_kwargs = {
    "blob_sizes": [2, 8],
    "cc_radius": 12,
    "match_threshold": 0.6,
    "nspots": 10000,
    "fix_spot_detection_kwargs": {
        "threshold": 0,
        "threshold_rel": 0.05,
    },
    "mov_spot_detection_kwargs": {
        "threshold": 0,
        "threshold_rel": 0.01,
    },
}

steps = [
    (
        "ransac",
        ransac_kwargs,
    ),
]

# align
affine = alignment_pipeline(
    fix_custom,
    mov_custom,
    fix_spacing_custom,
    mov_spacing_custom,
    steps,
)

# apply affine only
affine_aligned = apply_transform(
    fix_zarr["s3"],
    mov_zarr["s3"],
    fix_spacing_s3,
    mov_spacing_s3,
    transform_list=[
        affine,
    ],
)

# # write results
np.savetxt(f"{output_dir}/affine.mat", affine)
nrrd.write(
    f"{output_dir}/affine.nrrd", affine_aligned.transpose(2, 1, 0), compression_level=2
)

# load precomputed results
# affine = np.loadtxt('{output_dir}/affine.mat')


########################## local ##########################
from bigstream.piecewise_align import distributed_piecewise_alignment_pipeline

output_dir = (
    "/GPFS/yuezhifeng_lab_permanent/share/gong_lab/zhuqj/hll/debug_bigstream/outipynb"
)

# load affine
affine_result_path = f"{output_dir}/affine.mat"
affine = np.loadtxt(affine_result_path)

# get global alignment channels
fix = fix_zarr["s3"][...]
mov = mov_zarr["s3"][...]

# resample in xy to save room
fix_custom = zoom(fix, (1, 0.5, 0.5), order=1)
mov_custom = zoom(mov, (1, 0.5, 0.5), order=1)
fix_spacing_custom = fix_spacing_s3 * (1, 2, 2)
mov_spacing_custom = mov_spacing_s3 * (1, 2, 2)

# define alignment steps
ransac_kwargs = {
    "blob_sizes": [2, 8],
    "cc_radius": 12,
    "match_threshold": 0.6,
    "nspots": 10000,
    "fix_spot_detection_kwargs": {
        "threshold": 0,
        "threshold_rel": 0.05,
    },
    "mov_spot_detection_kwargs": {
        "threshold": 0,
        "threshold_rel": 0.01,
    },
}

affine_kwargs = {
    "shrink_factors": (1,),
    "smooth_sigmas": (1.0,),
    "optimizer_args": {
        "learningRate": 0.25,
        "minStep": 0.0,
        "numberOfIterations": 400,
    },
}

deform_kwargs = {
    "shrink_factors": (2,),
    "smooth_sigmas": (2.0,),
    "control_point_spacing": 200.0,
    "control_point_levels": (1,),
    "optimizer_args": {
        "learningRate": 2.5,
        "minStep": 0.07,
        "numberOfIterations": 100,
    },
}

steps = [
    (
        "ransac",
        ransac_kwargs,
    ),
    (
        "affine",
        affine_kwargs,
    ),
    (
        "deform",
        deform_kwargs,
    ),
]

blocksize = [152, 128, 128]

# cluster params
cluster_kwargs = {
    "queue": "q_cn,q_fat,q_fat_l,q_fat_c,q_fat_z",
    "job_cpu": 12,  # 每个worker的cpu数量
    "memory": "30GB",  # 每个worker的内存
    "threads": 1,
    "min_workers": 90,
    "max_workers":90,
}

# align
deform = distributed_piecewise_alignment_pipeline(
    fix_custom,
    mov_custom,
    fix_spacing_custom,
    mov_spacing_custom,
    steps,
    blocksize,
    static_transform_list=[
        affine,
    ],
    cluster_kwargs=cluster_kwargs,
)

# apply affine only
deform_aligned = apply_transform(
    fix_zarr["s3"],
    mov_zarr["s3"],
    fix_spacing_s3,
    mov_spacing_s3,
    transform_list=[affine, deform],
    transform_spacing=fix_spacing_custom,
)

# write results
nrrd.write(f"{output_dir}/deform.nrrd", deform, compression_level=2)
nrrd.write(
    f"{output_dir}/deformed.nrrd",
    deform_aligned.transpose(2, 1, 0),
    compression_level=2,
)

# load precomputed results
# deform, _ = nrrd.read(f'{output_dir}/deform.nrrd')
