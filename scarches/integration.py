from typing import Dict

import scvi
import scanpy as sc
import anndata as ad
from scipy.sparse import csr_matrix

import sys

def query_and_subsetting(query_vars: Dict, ref_model: str) -> ad.AnnData:
    query = sc.read_h5ad(query_vars['path'])
    cells = query.uns['celltype_colors']
    batch = query.uns['batch_colors']
    del query.varm
    
    scvi.model.SCVI.prepare_query_anndata(query, ref_model)
    model = scvi.model.SCVI.load_query_data(
        query,
        ref_model,
        freeze_dropout = True,
        inplace_subset_query_vars=True
    )
    model.train(max_epochs=200, plan_kwargs=dict(weight_decay=0.0))
    model.save(query_vars['surgery_path'], overwrite=True)
    
    query_adata = ad.AnnData(model.get_normalized_expression())
    query_adata.obsm['X_emb'] = model.get_latent_representation()
    query_adata.obsm['X_umap'] = query.obsm['X_umap']
    
    query_adata.obs['day'] = query.obs.day
    query_adata.obs['celltype'] = query.obs.celltype
    query_adata.obs['batch'] = query.obs['batch']
    query_adata.uns['celltype_colors'] = cells
    query_adata.uns['batch_colors'] = batch
    return query_adata


dataset = sys.argv[1]
ref_path = f'/home/icb/jonas.flor/gast_atlas_clean/scvi/{sys.argv[2]}_{sys.argv[3]}'

paths = {
        'path': f'/home/icb/jonas.flor/gast_atlas_clean/data/{sys.argv[1]}.h5ad',
        'save_path': f'/home/icb/jonas.flor/gast_atlas_clean/scarches/{sys.argv[2]}_{sys.argv[3]}/{sys.argv[1]}/{sys.argv[1]}_adata.h5ad',
        'surgery_path': f'/home/icb/jonas.flor/gast_atlas_clean/scarches/{sys.argv[2]}_{sys.argv[3]}/{sys.argv[1]}'
    }
query = query_and_subsetting(paths, ref_path)
query.X = csr_matrix(query.X)
query.write(paths['save_path'])
    

