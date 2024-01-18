import scanpy as sc
import sys

path = f'/home/icb/jonas.flor/gast_atlas_clean/scarches/{sys.argv[2]}_{sys.argv[3]}/{sys.argv[1]}/{sys.argv[1]}_adata.h5ad'
ref = sc.read(path)

day_dict = {'exvito': 8.5, 'invito': 8.5, 'gastrulation': 6.5}
celltype_dict = {'exvito': 'Mixed', 'invito': 'Mixed', 'gastrulation': 'Primitive Streak'}

sc.pp.normalize_total(ref)
sc.pp.log1p(ref)

sc.pp.neighbors(ref, use_rep='X_emb')
ref.uns['iroot'] = ref.obs.index.get_loc(
    ref[(ref.obs.day == day_dict[sys.argv[1]]) & (ref.obs.celltype == celltype_dict[sys.argv[1]])]
    .obs.first_valid_index()
)
sc.tl.dpt(ref)

ref.write(path)

sc.tl.umap(ref)
sc.pl.umap(ref, color='celltype', save=f'_{sys.argv[1]}_{sys.argv[3]}_celltypes.png')
sc.pl.umap(ref, color='day', save=f'_{sys.argv[1]}_{sys.argv[3]}_day.png')
sc.pl.umap(ref, color='batch', save=f'_{sys.argv[1]}_{sys.argv[3]}_batch.png')