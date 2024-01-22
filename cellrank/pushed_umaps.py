import scanpy as sc
import cloudpickle
import numpy as np
import pandas as pd
import jax.numpy as jnp

from ott.tools import sinkhorn_divergence
from ott.geometry import pointcloud

import sys

if sys.argv[4]=='weighted':
    end = '_w'
else:
    end = ''
    
with open(f'/home/icb/jonas.flor/gast_atlas_clean/otfm/1M_{sys.argv[2]}/{sys.argv[3]}_cond_model{end}.pt', mode='rb') as file:
       fm = cloudpickle.load(file)

adata = sc.read_h5ad(f'/home/icb/jonas.flor/gast_atlas_clean/scarches/1M_{sys.argv[2]}/{sys.argv[1]}/{sys.argv[1]}_adata.h5ad')


divergence_ref = sinkhorn_divergence.sinkhorn_divergence(
            pointcloud.PointCloud, adata.obsm['X_emb'], adata.obsm['X_emb']
        ).divergence

adata_concat = sc.concat({'unpushed': adata, 'pushed': adata},label='pushed')
adata_concat.obsm["X_new"] = np.concatenate(
    (adata.obsm['X_emb'],
        np.array(fm.transport(jnp.array(adata.obsm['X_emb']), 
                            condition=np.expand_dims(adata.obs.day.values, axis=1), 
                            forward=True))
        ),
    axis=0
)
    
pd.DataFrame(
    data={'dataset': [sys.argv[1]], 'n_genes': [sys.argv[2]], 'time': ['cond'], 'integrated': [True if sys.argv[2]=="integrated" else False], 
          'weighted': [sys.argv[3]],
          'divergence': [sinkhorn_divergence.sinkhorn_divergence(
              pointcloud.PointCloud,
              adata_concat[adata_concat.obs.pushed=='unpushed'].obsm['X_new'],
              adata_concat[adata_concat.obs.pushed=='pushed'].obsm['X_new']
          ).divergence],
          'divergence_ref': [divergence_ref]
         }
).to_csv(f'/home/icb/jonas.flor/gast_atlas_clean/cellrank/{sys.argv[1]}/{sys.argv[2]}/{sys.argv[3]}/{sys.argv[4]}/divergences.csv')

del adata_concat.obsm['X_diffmap']
sc.pp.neighbors(adata_concat)
sc.tl.umap(adata_concat)

sc.pl.umap(adata_concat, color='cellcluster_moscot', save=f'_{sys.argv[1]}_{sys.argv[2]}_{sys.argv[3]}_{sys.argv[4]}_celltypes.png')
sc.pl.umap(adata_concat, color='day', save=f'_{sys.argv[1]}_{sys.argv[2]}_{sys.argv[3]}_{sys.argv[4]}_day.png')
sc.pl.umap(adata_concat, color='batch', save=f'_{sys.argv[1]}_{sys.argv[2]}_{sys.argv[3]}_{sys.argv[4]}_batch.png')
sc.pl.umap(adata_concat, color='pushed', save=f'_{sys.argv[1]}_{sys.argv[2]}_{sys.argv[3]}_{sys.argv[4]}_pushed.png')

# arg 1: dataset
# arg 2: genes
# arg 3: integrated
# arg 4: weighted (_w)
