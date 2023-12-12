import numpy as np
import napari
from tifffile import imread
import zarr
from pathlib import Path

"""
结合stitching的结果，查看segmentation效果
"""
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

# load segmentation result
segmentation_dir = f"{output_dir}/{sample}/segmentation"
segmentation_dir_files = list(Path(segmentation_dir).glob("*.tif"))
assert len(segmentation_dir_files) == 1, "the number of segmentation results is not one"
segmentation_tif = segmentation_dir_files[0]
lb = imread(str(segmentation_tif))
print("label:")
print(lb.dtype, lb.shape, lb.min(), lb.max())

# load stitching result
stitching_dir = f"{output_dir}/{sample}/stitching/export.n5"
store = zarr.N5Store(stitching_dir)
im = zarr.open(store=store, mode="r")
img = im[f"{dapi}/{segmentation_scale}"][...]
print("image:")
print(img.dtype, img.shape, img.min(), img.max())
assert img.shape == lb.shape, "img.shape != lb.shape"

# show
viewer = napari.Viewer(ndisplay=2)
viewer.add_image(img, name="image", colormap="gray", blending="additive")
viewer.add_labels(lb, name="labels", blending="additive")
viewer.show(block=True)
