import scanpy as sc
import cloudpickle
import numpy as np
import pandas as pd
import jax.numpy as jnp

from ott.tools import sinkhorn_divergence
from ott.geometry import pointcloud

import sys

if sys.argv[3]=='weighted':
    end = '_w'
else:
    end = ''
    
with open(f'/home/icb/jonas.flor/gast_atlas_clean/otfm/1M_{sys.argv[1]}/{sys.argv[2]}_cond_model{end}.pt', mode='rb') as file:
       fm = cloudpickle.load(file)
       
adata = sc.read_h5ad(f'/home/icb/jonas.flor/gast_atlas_clean/scvi/1M_{sys.argv[1]}/{sys.argv[2]}_adata.h5ad')

adata_concat = sc.concat({'unpushed': adata, 'pushed': adata},label='pushed')
if sys.argv[3]=='integrated':
    divergence_ref = sinkhorn_divergence.sinkhorn_divergence(
              pointcloud.PointCloud, adata.obsm['X_emb'], adata.obsm['X_emb']
          ).divergence
    adata_concat.obsm["X_new"] = np.concatenate(
        (adata.obsm['X_emb'],
         np.array(fm.transport(jnp.array(adata.obsm['X_emb']), 
                               condition=np.expand_dims(adata.obs.day.values, axis=1), 
                               forward=True))
         ),
        axis=0
    )
elif sys.argv[3]=='unintegrated':
    divergence_ref = sinkhorn_divergence.sinkhorn_divergence(
              pointcloud.PointCloud, adata.obsm['X_pca'], adata.obsm['X_pca']
          ).divergence
    adata_concat.obsm["X_new"] = np.concatenate(
        (adata.obsm['X_pca'],
         np.array(fm.transport(jnp.array(adata.obsm['X_pca']), 
                               condition=np.expand_dims(adata.obs.day.values, axis=1), 
                               forward=True))
         ),
        axis=0
    )
    
pd.DataFrame(
    data={'n_genes': [sys.argv[1]], 'weighted': [sys.argv[3]], 'time': ['cond'], 'integrated': [True if sys.argv[2]=="integrated" else False],
          'divergence': [sinkhorn_divergence.sinkhorn_divergence(
              pointcloud.PointCloud,
              adata_concat[adata_concat.obs.pushed=='unpushed'].obsm['X_new'],
              adata_concat[adata_concat.obs.pushed=='pushed'].obsm['X_new']
          ).divergence],
          'divergence_ref': [divergence_ref]
         }
).to_csv(f'/home/icb/jonas.flor/gast_atlas_clean/otfm/1M_{sys.argv[1]}/{sys.argv[2]}_{sys.argv[3]}_cond.csv')

sc.pp.neighbors(adata_concat)
sc.tl.umap(adata_concat)

sc.pl.umap(adata_concat, color='cellcluster_moscot', save=f'_atlas_{sys.argv[1]}_{sys.argv[2]}_{sys.argv[3]}_celltypes.png')
sc.pl.umap(adata_concat, color='day', save=f'_atlas_{sys.argv[1]}_{sys.argv[2]}_{sys.argv[3]}_day.png')
sc.pl.umap(adata_concat, color='batch', save=f'_atlas_{sys.argv[1]}_{sys.argv[2]}_{sys.argv[3]}_batch.png')
sc.pl.umap(adata_concat, color='pushed', save=f'_atlas_{sys.argv[1]}_{sys.argv[2]}_{sys.argv[3]}_push.png')

# argv1: genes
# argv2: integrated
# argv3: weighted