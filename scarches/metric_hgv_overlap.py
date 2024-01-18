import scib
import scanpy as sc
import pandas as pd
import sys

condition_key = 'batch'
label_key = 'celltype'

adata = sc.read_h5ad(f'/home/icb/jonas.flor/gast_atlas_clean/data/{sys.argv[1]}.h5ad')
adata_int = sc.read_h5ad(f'/home/icb/jonas.flor/gast_atlas_clean/scarches/1M_{sys.argv[2]}/{sys.argv[1]}/{sys.argv[1]}_adata.h5ad')

scib_metrics = pd.DataFrame(
    data={'dataset': [sys.argv[1]], 'n_genes': [sys.argv[2]], 'metric': ['hgv_overlap']}
)
scib_metrics['value'] = scib.me.hvg_overlap(adata, adata_int, batch_key=condition_key)

scib_metrics.to_csv(f'/home/icb/jonas.flor/gast_atlas_clean/scarches/results/{sys.argv[1]}_{sys.argv[2]}_hgv_overlap.csv')
