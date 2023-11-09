### AFsample - AlphaFold with aggressive sampling



This package provides an implementation of the `Wallner` method that was the best method in multimer prediction in CASP15.

It is based on the AlphaFold system developed by DeepMind https://github.com/deepmind/alphafold/



###### **版本**

| version | build | squeue  | Organizations | Branch | commint                                  |
| ------- | ----- | ------- | ------------- | ------ | ---------------------------------------- |
| 2.2.0   | conda | gpu/cpu | bjornwallner  | main   | 9f76c2adf55403fd80b9079052716857d77a0396 |



###### 软件安装路径：

```
/usr/nzx-cluster/apps/afsample
```

###### 数据库路径：

```
/GPFS/PUB/afsample/alphafold_data
```

###### 使用前准备

- 新建文件夹，如afsample 
- 在文件夹里放置一个fasta文件，例如test.fasta文件



Say we have a monomer with the sequence `<SEQUENCE>`. The input fasta should be:

```fasta
>sequence_name
<SEQUENCE>
```

Say we have a homomer with 3 copies of the same sequence `<SEQUENCE>`. The input fasta should be:

```fasta
>sequence_1
<SEQUENCE>
>sequence_2
<SEQUENCE>
>sequence_3
<SEQUENCE>
```





###### AFsample  monomer运行示例：

```
#!/bin/bash 
#SBATCH --job-name=afsample
#SBATCH -p q_ai8,q_ai4  
#SBATCH -n 1
#SBATCH  -c 8
#SBATCH --gres=gpu:1    #use 1 GPU
#SBATCH --output=%j.out
#SBATCH --error=%j.err

module load afsample/2.2.0

python /usr/nzx-cluster/apps/afsample/alphafoldv2.2.0/run_alphafold.py \
--fasta_paths=/home/yuezhifeng_lab/wangyanmin/scratch60/test_data/afsample/ENSFCAP00000052000_Fcat.fasta
--uniref90_database_path=$DOWNLOAD_DIR/uniref90/uniref90.fasta  \
--mgnify_database_path=$DOWNLOAD_DIR/mgnify/mgy_clusters.fa \
--template_mmcif_dir=/GPFS/PUB/afsample/alphafold_data/pdb_mmcif/mmcif_files \
--obsolete_pdbs_path=/GPFS/PUB/afsample/alphafold_data/pdb_mmcif/obsolete.dat \
--small_bfd_database_path=$DOWNLOAD_DIR/small_bfd/bfd-first_non_consensus_sequences.fasta \
--pdb70_database_path=/GPFS/PUB/afsample/alphafold_data/pdb70/pdb70 \
--output_dir=/home/yuezhifeng_lab/wangyanmin/scratch60/test_data/afsample \
--max_template_date=2020-05-14 \
--model_preset=monomer \
--db_preset=reduced_dbs
```





###### AFsample  multimer运行示例：

```
#!/bin/bash 
#SBATCH --job-name=afsample
#SBATCH -p q_ai8,q_ai4  
#SBATCH -n 1
#SBATCH  -c 8
#SBATCH --gres=gpu:1       # use 1 GPU
#SBATCH --output=%j.out
#SBATCH --error=%j.err

module load afsample/2.2.0

python /usr/nzx-cluster/apps/afsample/alphafoldv2.2.0/run_alphafold.py \
--fasta_paths=/home/yuezhifeng_lab/wangyanmin/scratch60/test_data/afsample/ENSHHUP00000061568_Hhuc.fasta \
--uniref90_database_path=$DOWNLOAD_DIR/uniref90/uniref90.fasta \
--mgnify_database_path=$DOWNLOAD_DIR/mgnify/mgy_clusters.fa \
--template_mmcif_dir=$DOWNLOAD_DIR/pdb_mmcif/mmcif_files \
--obsolete_pdbs_path=$DOWNLOAD_DIR/pdb_mmcif/obsolete.dat \
--small_bfd_database_path=$DOWNLOAD_DIR/small_bfd/bfd-first_non_consensus_sequences.fasta \
--pdb_seqres_database_path=$DOWNLOAD_DIR/pdb_seqres/pdb_seqres.txt \
--uniprot_database_path=$DOWNLOAD_DIR/uniref90/uniref90.fasta \
--output_dir=/home/yuezhifeng_lab/wangyanmin/scratch60/test_data/afsample \
--max_template_date=2020-05-14 \
--model_preset=multimer \
--db_preset=reduced_dbs
```



#### 参考：

github 网址：https://github.com/bjornwallner/alphafoldv2.2.0





