import scib
import scanpy as sc
import pandas as pd
import sys

condition_key = 'batch'
label_key = 'celltype'
adata_path = f'/home/icb/jonas.flor/gast_atlas_clean/scvi/{sys.argv[1]}_{sys.argv[2]}'

adata_int = sc.read_h5ad(f'{adata_path}/integrated_adata.h5ad')

scib_metrics = pd.DataFrame(
    data={'n_obs': [adata_int.n_obs], 'n_genes': [sys.argv[2]], 'metric': ['silhouette_integrated']}
)
scib_metrics['value'] = scib.me.silhouette(adata_int, label_key=label_key, embed='X_emb')

scib_metrics.to_csv(f'{adata_path}/metrics/metrics_silhouette_integrated.csv')
