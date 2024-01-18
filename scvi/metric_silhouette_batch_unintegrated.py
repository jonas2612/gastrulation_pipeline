import scib
import scanpy as sc
import pandas as pd
import sys

condition_key = 'batch'
label_key = 'celltype'
adata_path = f'/home/icb/jonas.flor/gast_atlas_clean/scvi/{sys.argv[1]}_{sys.argv[2]}'

adata = sc.read_h5ad(f'{adata_path}/unintegrated_adata.h5ad')

scib_metrics = pd.DataFrame(
    data={'n_obs': [adata.n_obs], 'n_cells': [sys.argv[1]], 'n_genes': [sys.argv[2]], 'n_layers': [sys.argv[3]], 'n_hidden': [sys.argv[4]], 'metric': ['silhouette_batch_unintegrated']}
)
scib_metrics['value'] = scib.me.silhouette_batch(adata, batch_key=condition_key, label_key=label_key, embed='X_pca', return_all=True)[0]

scib_metrics.to_csv(f'{adata_path}/metrics/metrics_silhouette_batch_unintegrated.csv')
