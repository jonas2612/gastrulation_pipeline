import scanpy as sc

adata = sc.read_h5ad('/lustre/groups/ml01/workspace/monge_velo/data/mouse_gastrulation_atlas/clean/gastrulation_atlas.h5ad', backed='r')

adata = sc.pp.subsample(adata, n_obs=100000, copy=True)

adata.write('/lustre/groups/ml01/workspace/monge_velo/data/mouse_gastrulation_atlas/clean/validation.h5ad')