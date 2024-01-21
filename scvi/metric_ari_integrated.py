import scib
import scanpy as sc
import pandas as pd
import sys

condition_key = 'batch'
label_key = 'celltype'
adata_path = f'/home/icb/jonas.flor/gast_atlas_clean/scvi/{sys.argv[1]}_{sys.argv[2]}'

adata_int = sc.read_h5ad(f'{adata_path}/integrated_adata.h5ad')

scib_metrics = pd.DataFrame(
    data={'n_obs': [adata_int.n_obs], 'n_genes': [sys.argv[2]], 'metric': ['ari_integrated']}
)
scib.me.cluster_optimal_resolution(adata_int, label_key=label_key, cluster_key='Leiden')

scib_metrics['value'] = scib.me.ari(adata_int, cluster_key='Leiden', label_key=label_key)

scib_metrics.to_csv(f'{adata_path}/metrics/metrics_ari_integrated.csv')
