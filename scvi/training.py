import scvi
import scanpy as sc
import numpy as np
import pandas as pd
import anndata as ad
import sys

condition_key = 'batch'
adata_path = f'/home/icb/jonas.flor/gast_atlas_clean/scvi/{sys.argv[1]}_{sys.argv[2]}'
metrics_path = f'/home/icb/jonas.flor/gast_atlas_clean/scvi/{sys.argv[1]}_{sys.argv[2]}/metrics'

if sys.argv[1]=='10k':
    n_obs=10000
elif sys.argv[1]=='100k':
    n_obs=100000
elif sys.argv[1]=='500k':
    n_obs=500000
elif sys.argv[1]=='1M':
    n_obs=1000000

adata = sc.read_h5ad(f'/lustre/groups/ml01/workspace/monge_velo/data/mouse_gastrulation_atlas/clean/adata_{sys.argv[1]}.h5ad')
obsp = adata.obsp
highly_variable = adata.var_names

if sys.argv[2]=='2k_genes':
    adata_copy = adata.copy()
    sc.pp.normalize_total(adata_copy)
    sc.pp.log1p(adata_copy)
    sc.pp.highly_variable_genes(
        adata_copy,
        n_top_genes=2000,
        batch_key=condition_key,
    )
    highly_variable = adata_copy.var["highly_variable"]
    del adata_copy
elif sys.argv[2]=='10k_genes':
    adata_copy = adata.copy()
    sc.pp.normalize_total(adata_copy)
    sc.pp.log1p(adata_copy)
    sc.pp.highly_variable_genes(
        adata_copy,
        n_top_genes=10000,
        batch_key=condition_key,
    )
    highly_variable = adata_copy.var["highly_variable"]
    del adata_copy

adata = ad.concat([
    sc.read_h5ad('/lustre/groups/ml01/workspace/monge_velo/data/mouse_gastrulation_atlas/clean/validation.h5ad'),
    adata
])
adata._inplace_subset_var(highly_variable)

var = adata.var #otherwise not subsetted to hgv genes

scvi.model.SCVI.setup_anndata(adata, batch_key=condition_key)
vae = scvi.model.SCVI(
    adata,
    n_layers=2,
    n_hidden=2048,
    n_latent=50
)
vae.train(max_epochs=500, early_stopping=True, check_val_every_n_epoch=1, train_size=n_obs/adata.n_obs, validation_size=None, shuffle_set_split=False, early_stopping_patience=30, early_stopping_monitor='reconstruction_loss_validation')
vae.save(adata_path, overwrite=True)

adata = adata[100000:]
adata.var = var
adata.obsp = obsp

adata.write(f'{adata_path}/unintegrated_adata.h5ad')
del adata

#training metrics
pd.DataFrame(
    np.concatenate([vae.history['train_loss_epoch'], vae.history['validation_loss']], axis=1), columns=['train_loss', 'val_loss']
).to_csv(
    f'{metrics_path}/loss.csv'
)

pd.DataFrame(
    np.concatenate([vae.history['elbo_train'], vae.history['elbo_validation']], axis=1), columns=['train_elbo', 'val_elbo']
).to_csv(
    f'{metrics_path}/elbo.csv'
)

pd.DataFrame(
    np.concatenate([vae.history['reconstruction_loss_train'], vae.history['reconstruction_loss_validation']], axis=1), columns=['train_recon_loss', 'val_recon_loss']
).to_csv(
    f'{metrics_path}/reconstr_loss.csv'
)
