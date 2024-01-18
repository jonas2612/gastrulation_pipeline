import scib
import scanpy as sc
import pandas as pd
import sys

condition_key = 'batch'
label_key = 'celltype'

adata_int = sc.read_h5ad(f'/home/icb/jonas.flor/gast_atlas_clean/scarches/1M_{sys.argv[2]}/{sys.argv[1]}/{sys.argv[1]}_adata.h5ad')

scib_metrics = pd.DataFrame(
    data={'dataset': [sys.argv[1]], 'n_genes': [sys.argv[2]], 'metric': ['ari_integrated']}
)
scib.me.cluster_optimal_resolution(adata_int, label_key=label_key, cluster_key='Leiden')

scib_metrics['value'] = scib.me.ari(adata_int, cluster_key='Leiden', label_key=label_key)

scib_metrics.to_csv(f'/home/icb/jonas.flor/gast_atlas_clean/scarches/results/{sys.argv[1]}_{sys.argv[2]}_ari_integrated.csv')


#arg 1: dataset
#arg 2: ..._genes