import scib
import scanpy as sc
import pandas as pd
import sys

condition_key = 'batch'
label_key = 'celltype'
adata_path = f'/home/icb/jonas.flor/gast_atlas_clean/scvi/{sys.argv[1]}_{sys.argv[2]}'

adata = sc.read_h5ad(f'{adata_path}/unintegrated_adata.h5ad')

scib_metrics = pd.DataFrame(
    data={'n_obs': [adata.n_obs], 'n_genes': [sys.argv[2]], 'metric': ['pcr_unintegrated']}
)
scib_metrics['value'] = scib.me.pcr(adata, covariate=condition_key, recompute_pca=False)

scib_metrics.to_csv(f'{adata_path}/metrics/metrics_pcr_unintegrated.csv')
