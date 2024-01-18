import anndata as ad

ad.experimental.concat_on_disk(in_files={'ds1': "/lustre/groups/ml01/workspace/monge_velo/data/mouse_gastrulation_atlas/adata_JAX_dataset_12.h5ad",
                                         'ds2': "/lustre/groups/ml01/workspace/monge_velo/data/mouse_gastrulation_atlas/adata_JAX_dataset_34.h5ad"},
                               out_file='/lustre/groups/ml01/workspace/monge_velo/data/mouse_gastrulation_atlas/clean/gastrulation_atlas.h5ad')