import scib
import scanpy as sc
import pandas as pd
import sys

condition_key = 'batch'
label_key = 'celltype'
adata_path = f'/home/icb/jonas.flor/gast_atlas_clean/scvi/{sys.argv[1]}_{sys.argv[2]}'

adata = sc.read_h5ad(f'{adata_path}/unintegrated_adata.h5ad')

scib_metrics = pd.DataFrame(
    data={'n_obs': [adata.n_obs], 'n_cells': [sys.argv[1]], 'n_genes': [sys.argv[2]], 'n_layers': [sys.argv[3]], 'n_hidden': [sys.argv[4]], 'metric': ['nmi_unintegrated']}
)
scib.me.cluster_optimal_resolution(adata, label_key=label_key, cluster_key='Leiden')

scib_metrics['value'] = scib.me.nmi(adata, cluster_key='Leiden', label_key=label_key)

scib_metrics.to_csv(f'{adata_path}/metrics/metrics_unintegrated.csv')
