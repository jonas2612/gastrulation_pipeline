import scib
import scanpy as sc
import pandas as pd
import sys

condition_key = 'batch'
label_key = 'celltype'

adata = sc.read_h5ad(f'/home/icb/jonas.flor/gast_atlas_clean/data/{sys.argv[1]}.h5ad')

scib_metrics = pd.DataFrame(
    data={'dataset': [sys.argv[1]], 'n_genes': [adata.n_vars], 'metric': ['pcr_unintegrated']}
)
scib_metrics['value'] = scib.me.pcr(adata, covariate=condition_key, recompute_pca=False)

scib_metrics.to_csv(f'/home/icb/jonas.flor/gast_atlas_clean/scarches/results/{sys.argv[1]}_pcr_unintegrated.csv')
