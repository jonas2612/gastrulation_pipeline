import scanpy as sc
import anndata as ad
import pandas as pd
import numpy as np

annotation = pd.read_csv('/home/icb/jonas.flor/gast_atlas_clean/data/basis/GSE208680_cell_annotation.txt', sep='\t')
data = pd.read_csv('/home/icb/jonas.flor/gast_atlas_clean/data/basis/GSE208680_raw_counts.csv', index_col='Name')
data_normalized = pd.read_csv('/home/icb/jonas.flor/gast_atlas_clean/data/basis/GSE208680_normalized_counts.csv', index_col=0)
db = pd.read_csv('/home/icb/jonas.flor/gast_atlas_clean/data/basis/mouse.v12.geneID.txt', sep='\t')[['gene_ID', 'gene_short_name']]

#create and save umap as in paper described
adata_norm = ad.AnnData(data_normalized.transpose())
adata_norm.obs['celltype'] = pd.Categorical([annotation.loc[annotation.Cell_barcode==x, 'cluster_annotation'].values[0] for x in adata_norm.obs_names])
adata_norm.obs['Nat_Synth'] = pd.Categorical([annotation.loc[annotation.Cell_barcode==x, 'Nat_Syn'].values[0] for x in adata_norm.obs_names])
adata_norm.obs['batch'] = pd.Categorical([annotation.loc[annotation.Cell_barcode==x, 'Sample_Name'].values[0] for x in adata_norm.obs_names])
adata_norm.obs['day'] = pd.Categorical([8.5 for x in range(adata_norm.n_obs)])

sc.pp.scale(adata_norm)
sc.pp.pca(adata_norm, n_comps=15)
sc.pp.neighbors(adata_norm)
sc.tl.umap(adata_norm)

#save umaps together
sc.pl.umap(adata_norm, color='celltype', save='_in+exvitro_celltype.png')
sc.pl.umap(adata_norm, color='batch', save='_in+exvitro_batch.png')
sc.pl.umap(adata_norm, color='day', save='_in+exvitro_day.png')

#compute neighbors and dpt in in- and exvitro for scIB
tmp = ad.AnnData(data_normalized.transpose())
tmp.obs['celltype'] = pd.Categorical([annotation.loc[annotation.Cell_barcode==x, 'cluster_annotation'].values[0] for x in tmp.obs_names])
tmp.obs['Nat_Synth'] = pd.Categorical([annotation.loc[annotation.Cell_barcode==x, 'Nat_Syn'].values[0] for x in tmp.obs_names])
tmp.obs['batch'] = pd.Categorical([annotation.loc[annotation.Cell_barcode==x, 'Sample_Name'].values[0] for x in tmp.obs_names])
tmp.obs['day'] = pd.Categorical([8.5 for x in range(tmp.n_obs)])

adata_synth_norm = tmp[tmp.obs.Nat_Synth=='Synthetic']
adata_nat_norm = tmp[tmp.obs.Nat_Synth=='Natural']

sc.pp.scale(adata_synth_norm)
sc.pp.scale(adata_nat_norm)

sc.pp.pca(adata_synth_norm)
sc.pp.pca(adata_nat_norm)

sc.pp.neighbors(adata_synth_norm)
sc.pp.neighbors(adata_nat_norm)

adata_synth_norm.uns['iroot'] = adata_synth_norm.obs.index.get_loc(
    adata_synth_norm[(adata_synth_norm.obs.day == 'E8.5') & (adata_synth_norm.obs.celltype == 'Mixed')]
    .obs.first_valid_index()
)
adata_nat_norm.uns['iroot'] = adata_nat_norm.obs.index.get_loc(
    adata_nat_norm[(adata_nat_norm.obs.day == 'E8.5') & (adata_nat_norm.obs.celltype == 'Mixed')]
    .obs.first_valid_index()
)

sc.tl.dpt(adata_synth_norm)
sc.tl.dpt(adata_nat_norm)

# finish dataset
adata = ad.AnnData(data.transpose().reindex(adata_norm.obs_names)) #ensure correct cell mapping
adata = adata[adata.obs_names.isin(list(annotation['Cell_barcode'])), :]

adata.obs['celltype'] = pd.Categorical([annotation.loc[annotation.Cell_barcode==x, 'cluster_annotation'].values[0] for x in adata.obs_names])
adata.obs['Nat_Synth'] = pd.Categorical([annotation.loc[annotation.Cell_barcode==x, 'Nat_Syn'].values[0] for x in adata.obs_names])
adata.obs['batch'] = pd.Categorical([annotation.loc[annotation.Cell_barcode==x, 'Sample_Name'].values[0] for x in adata.obs_names])
adata.obs['day'] = pd.Categorical([8.5 for x in range(adata.n_obs)])
adata.obsm['X_umap'] = adata_norm.obsm['X_umap']
adata.uns['batch_colors'] = adata_norm.uns['batch_colors']
adata.uns['day_colors'] = adata_norm.uns['day_colors']
adata.uns['celltype_colors'] = adata_norm.uns['celltype_colors']

new_names = adata.var_names.to_frame(name='gene_short_name').merge(db, on='gene_short_name', how='inner')
new_names.drop_duplicates(subset='gene_short_name', inplace=True)

adata = adata[:, adata.var_names.isin(list(new_names['gene_short_name']))]

adata.var_names = new_names['gene_ID']

adata_synth = adata[adata.obs.Nat_Synth=='Synthetic']
adata_nat = adata[adata.obs.Nat_Synth=='Natural']

adata_synth.obsm['X_pca'] = adata_synth_norm.obsm['X_pca']
adata_nat.obsm['X_pca'] = adata_nat_norm.obsm['X_pca']

adata_synth.uns['neighbors'] = adata_synth_norm.uns['neighbors']
adata_nat.uns['neighbors'] = adata_nat_norm.uns['neighbors']

adata_synth.obs['dpt_pseudotime'] = adata_synth_norm.obs['dpt_pseudotime']
adata_nat.obs['dpt_pseudotime'] = adata_nat_norm.obs['dpt_pseudotime']

adata_synth.obsp['distances'] = adata_synth_norm.obsp['distances']
adata_nat.obsp['distances'] = adata_nat_norm.obsp['distances']

adata_synth.obsp['connectivities'] = adata_synth_norm.obsp['connectivities']
adata_nat.obsp['connectivities'] = adata_nat_norm.obsp['connectivities']

#save data
adata_nat.write('/home/icb/jonas.flor/gast_atlas_clean/data/invitro.h5ad')
adata_synth.write('/home/icb/jonas.flor/gastrulation_atlas/data/exvitro.h5ad')

#save umaps
sc.pl.umap(adata_synth, color='celltype', save='_exvitro_celltype.png')
sc.pl.umap(adata_synth, color='batch', save='_exvitro_batch.png')
sc.pl.umap(adata_synth, color='day', save='_exvitro_day.png')
sc.pl.umap(adata_nat, color='celltype', save='_invitro_celltype.png')
sc.pl.umap(adata_nat, color='batch', save='_invitro_batch.png')
sc.pl.umap(adata_nat, color='day', save='_invitro_day.png')
