import scanpy as sc
import sys

adata_path = f'/home/icb/jonas.flor/gast_atlas_clean/scvi/{sys.argv[1]}_{sys.argv[2]}'

#unintegrated adata preprocessing
adata = sc.read_h5ad(f'{adata_path}/unintegrated_adata.h5ad')

sc.pp.normalize_total(adata)
sc.pp.log1p(adata)

adata.obs.day[adata.obs.day == 0.] = 19

sc.pp.neighbors(adata, use_rep='X_pca')
adata.uns['iroot'] = adata.obs.index.get_loc(
    adata[(adata.obs.day == 8.5) & (adata.obs.celltype == 'Lateral plate and intermediate mesoderm')]
    .obs.first_valid_index()
)
sc.tl.dpt(adata)

adata.write(f'{adata_path}/unintegrated_adata.h5ad')

sc.tl.umap(adata)
sc.pl.umap(adata, color='cellcluster_moscot', save=f'_atlas_{sys.argv[2]}_celltype_pca.png')
sc.pl.umap(adata, color='batch', save=f'_atlas_{sys.argv[2]}_batch_pca.png')
sc.pl.umap(adata, color='day', save=f'_atlas_{sys.argv[2]}_day_pca.png')
del adata


#integrated adata preprocessing
adata = sc.read_h5ad(f'{adata_path}/integrated_adata.h5ad')

sc.pp.normalize_total(adata)
sc.pp.log1p(adata)

adata.obs.day[adata.obs.day == 0.] = 19

sc.pp.neighbors(adata, use_rep='X_emb')
adata.uns['iroot'] = adata.obs.index.get_loc(
    adata[(adata.obs.day == 8.5) & (adata.obs.celltype == 'Lateral plate and intermediate mesoderm')]
    .obs.first_valid_index()
)
sc.tl.dpt(adata)

adata.write(f'{adata_path}/integrated_adata.h5ad')

sc.tl.umap(adata)
sc.pl.umap(adata, color='cellcluster_moscot', save=f'_atlas_{sys.argv[2]}_celltype_emb.png')
sc.pl.umap(adata, color='batch', save=f'_atlas_{sys.argv[2]}_batch_emb.png')
sc.pl.umap(adata, color='day', save=f'_atlas_{sys.argv[2]}_day_emb.png')
