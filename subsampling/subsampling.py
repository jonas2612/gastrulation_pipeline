import scanpy as sc
import pandas as pd
import numpy as np
import sys

if sys.argv[1]=='10k':
    n_obs=10000
elif sys.argv[1]=='100k':
    n_obs=100000
elif sys.argv[1]=='500k':
    n_obs=500000
elif sys.argv[1]=='1M':
    n_obs=1000000

adata = sc.read('/lustre/groups/ml01/workspace/monge_velo/data/mouse_gastrulation_atlas/clean/gastrulation_atlas.h5ad', backed='r')
val = sc.read('/lustre/groups/ml01/workspace/monge_velo/data/mouse_gastrulation_atlas/clean/validation.h5ad', backed='r')

data = pd.DataFrame({'Index': list(range(adata.n_obs))}, index=adata.obs.index)
indices = data.drop(labels=val.obs.index).Index
obs_indices = np.random.choice(indices, size=n_obs, replace=False)
adata_tmp = adata[obs_indices].to_memory()

adata_tmp.write(f'/lustre/groups/ml01/workspace/monge_velo/data/mouse_gastrulation_atlas/clean/adata_{sys.argv[1]}.h5ad')