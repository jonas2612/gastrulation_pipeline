import scvi
import scanpy as sc
import anndata as ad
import sys

adata_path = f'/home/icb/jonas.flor/gast_atlas_clean/scvi/{sys.argv[1]}_{sys.argv[2]}'

adata = sc.read_h5ad(f'{adata_path}/unintegrated_adata.h5ad')
vae = scvi.model.SCVI.load(dir_path=adata_path, adata=adata)

#data preparation
adata_int = ad.AnnData(vae.posterior_predictive_sample().to_scipy_sparse())
adata_int.obs = adata.obs
adata_int.var = adata.var
adata_int.obsm["X_emb"] = vae.get_latent_representation()
del vae


#write adata_int
adata_int.write(f'{adata_path}/integrated_adata.h5ad')