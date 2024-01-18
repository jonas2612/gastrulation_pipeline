import scanpy as sc
import pandas as pd

adata = sc.read("basis/gastrulation.h5ad")
names = adata.var_names.to_frame(name='gene_short_name')
db = pd.read_csv('/home/icb/jonas.flor/gast_atlas_clean/data/basis/mouse.v12.geneID.txt', sep='\t')[['gene_ID', 'gene_short_name']]

new_names = adata.var_names.to_frame(name='gene_short_name').merge(db, on='gene_short_name', how='inner')
new_names.drop_duplicates(subset='gene_short_name', inplace=True)

adata = adata[:, adata.var_names.isin(list(new_names['gene_short_name']))]

adata.var_names = new_names['gene_ID']
adata.obs['day'] = [float(x[1:]) for x in adata.obs['stage']]
adata.obs['batch'] = adata.obs['sequencing.batch']
adata.obs.batch = [str(x) for x in adata.obs.batch]

sc.pl.umap(adata, color='celltype', save='_gastrulation_celltype.png')
sc.pl.umap(adata, color='batch', save='_gastrulation_batch.png')
sc.pl.umap(adata, color='day', save='_gastrulation_day.png')

sc.pp.neighbors(adata)
adata.uns['iroot'] = adata.obs.index.get_loc(
    adata[(adata.obs.stage == 6.5) & (adata.obs.celltype == 'Primitive Streak')]
    .obs.first_valid_index()
)
sc.tl.dpt(adata)

adata.write('/home/icb/jonas.flor/gast_atlas_clean/data/gastrulation.h5ad')