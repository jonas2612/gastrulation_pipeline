import scib
import scanpy as sc
import pandas as pd
import sys

condition_key = 'batch'
label_key = 'celltype'
adata_int = sc.read_h5ad(f'/home/icb/jonas.flor/gast_atlas_clean/scarches/1M_{sys.argv[2]}/{sys.argv[1]}/{sys.argv[1]}_adata.h5ad')

scib_metrics = pd.DataFrame(
    data={'dataset': [sys.argv[1]], 'n_genes': [sys.argv[2]], 'metric': ['cLISI_integrated']}
)
scib_metrics['value'] = scib.me.clisi_graph(adata_int, label_key=label_key, type_='embed')

scib_metrics.to_csv(f'/home/icb/jonas.flor/gast_atlas_clean/scarches/results/{sys.argv[1]}_{sys.argv[2]}_cLISI_integrated.csv')
