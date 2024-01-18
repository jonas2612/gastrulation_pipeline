import scib
import scanpy as sc
import pandas as pd
import sys

condition_key = 'batch'
label_key = 'celltype'

adata = sc.read_h5ad(f'/home/icb/jonas.flor/gast_atlas_clean/data/{sys.argv[1]}.h5ad')

scib_metrics = pd.DataFrame(
    data={'dataset': [sys.argv[1]], 'n_genes': [adata.n_vars], 'metric': ['ari_unintegrated']}
)
scib.me.cluster_optimal_resolution(adata, label_key=label_key, cluster_key='Leiden')

scib_metrics['value'] = scib.me.ari(adata, cluster_key='Leiden', label_key=label_key)

scib_metrics.to_csv(f'/home/icb/jonas.flor/gast_atlas_clean/scarches/results/{sys.argv[1]}_ari_unintegrated.csv')
