

使用bigstitcher配准的结果，使其适配到pipeline，需要修改的信息。

该方法免复制，以软链接的形式，方便快速。

### 步骤

#### 创建输出目录

确定pipeline里stitching的outputs目录，比如 outputs/s2_r6/stitching/export.n5，如果stitching以及export.n5文件夹不存在，则手动创建。


#### 创建json文件

在export.n5文件夹里创建文件attributes.json，把下面信息复制到attributes.json里：
```json
{
    "n5": "2.5.1",
    "pixelResolution": {
        "dimensions": [
            0.23,
            0.23,
            0.42
        ],
        "unit": "um"
    },
    "scales": [
        [
            1,
            1,
            1
        ],
        [
            2,
            2,
            1
        ],
        [
            4,
            4,
            2
        ],
        [
            8,
            8,
            4
        ],
        [
            16,
            16,
            8
        ]
    ]
}
```

但是，需要核查pixelResolution以及scales两个信息是否正确，scales信息需要跟bigstitcher结果setup0/attributes.json里的downsamplingFactors保持一致。

#### 链接文件

在export.n5文件夹下创建软链接，链接名为c0，链接到bigstitcher结果里的setup0/timepoint0：

```commandline
ln -s bigstitcher_result_dir/setup0/timepoint0 c0
```

如果有多个通道，则同理：

```commandline
ln -s bigstitcher_result_dir/setup1/timepoint0 c1
ln -s bigstitcher_result_dir/setup2/timepoint0 c2
ln -s bigstitcher_result_dir/setup3/timepoint0 c3
```

至此，完成了所有文件的创建，文件结构如下：

```commandline
├── attributes.json
├── c0 -> bigstitcher_result_dir/setup0/timepoint0
├── c1 -> bigstitcher_result_dir/setup1/timepoint0
├── c2 -> bigstitcher_result_dir/setup2/timepoint0
└── c3 -> bigstitcher_result_dir/setup3/timepoint0
```

### 最关键的一点请注意

上述多处使用了软链接，要使其能在pipeline里work，一定要把链接的原始路径挂载进去。

比如上面多个地方都链接到了bigstitcher_result_dir里的某个路径，那么只需把bigstitcher_result_dir挂载一下就可以了。

具体操作，在pipeline sh文件里面的runtime_opts参数里加入相关路径即可（格式：-B bigstitcher_result_dir）：

```commandline
--runtime_opts "-B $work_dir -B bigstitcher_result_dir"
```
