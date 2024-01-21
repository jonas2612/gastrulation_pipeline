import scanpy as sc
import anndata as ad
import numpy as np
import pandas as pd
import sys

path = f'/home/icb/jonas.flor/gast_atlas_clean/scarches/{sys.argv[2]}_{sys.argv[3]}/{sys.argv[1]}/{sys.argv[1]}_adata.h5ad'
ref = sc.read(path)

day_dict = {'exvitro': 8.5, 'invitro': 8.5, 'gastrulation': 6.5}
celltype_dict = {'exvitro': 'Mixed', 'invitro': 'Mixed', 'gastrulation': 'Primitive Streak'}

sc.pp.normalize_total(ref)
sc.pp.log1p(ref)

sc.pp.neighbors(ref, use_rep='X_emb')
ref.uns['iroot'] = ref.obs.index.get_loc(
    ref[(ref.obs.day == day_dict[sys.argv[1]]) & (ref.obs.celltype == celltype_dict[sys.argv[1]])]
    .obs.first_valid_index()
)
sc.tl.dpt(ref)

ref.write(path)

sc.tl.umap(ref)
sc.pl.umap(ref, color='celltype', save=f'_{sys.argv[1]}_{sys.argv[3]}_celltypes.png')
sc.pl.umap(ref, color='day', save=f'_{sys.argv[1]}_{sys.argv[3]}_day.png')
sc.pl.umap(ref, color='batch', save=f'_{sys.argv[1]}_{sys.argv[3]}_batch.png')

atlas = sc.read_h5ad(f'/home/icb/jonas.flor/gast_atlas_clean/scvi/{sys.argv[2]}_{sys.argv[3]}/integrated_adata.h5ad', backed='r')

adata = ad.AnnData(np.empty((atlas.n_obs+ref.n_obs, 10000)))
adata.obs['celltype'] = pd.concat([atlas.obs.cellcluster_moscot, ref.obs.celltype]).values
adata.obs['batch'] = pd.concat([atlas.obs.embryo_id, ref.obs.batch]).values
adata.obs['day'] = pd.concat([atlas.obs.day, ref.obs.day]).values
adata.obs['dataset'] = pd.Categorical(np.array((['atlas'] * atlas.n_obs) + (['query'] * ref.n_obs)))
adata.obsm['X_emb'] = np.concatenate((atlas.obsm['X_emb'], ref.obsm['X_emb']), axis=0)
sc.pp.neighbors(adata, use_rep='X_emb')
sc.tl.umap(adata)

sc.pl.umap(adata, color='celltype', save=f'_{sys.argv[1]}_{sys.argv[3]}_joint_celltypes.png')
sc.pl.umap(adata, color='day', save=f'_{sys.argv[1]}_{sys.argv[3]}_joint_day.png')
sc.pl.umap(adata, color='batch', save=f'_{sys.argv[1]}_{sys.argv[3]}_joint_batch.png')
sc.pl.umap(adata, color='dataset', save=f'_{sys.argv[1]}_{sys.argv[3]}_joint_dataset.png')
