import scanpy as sc
from cellrank.kernels import VelocityKernel
from cellrank.estimators import GPCCA
import cellrank as cr
import scvelo as scv
import numpy as np
import pandas as pd
from pandas import DataFrame
import cloudpickle

import jax.numpy as jnp

import sys

#env cellrank_new

def preparation(adata, model, x_key, add_spliced):
    adata.obsm['velocity'] = np.array(fm.transport(jnp.array(adata.obsm[x_key]), 
                                   condition=np.expand_dims(adata.obs.day.values, axis=1), 
                                   forward=True)
                      )-adata.obsm[x_key]
    if add_spliced:
        adata.layers['spliced'] = np.ones((adata.n_obs, adata.n_vars))
        adata.layers['unspliced'] = np.ones((adata.n_obs, adata.n_vars))

    scv.pp.moments(adata)
    return None



if sys.argv[1]=='gastrulation':
    terminal_states = ['PGC', 'Mesenchyme', 'Surface ectoderm', 'Gut', 'Notochord', 'Somitic mesoderm', 'Endothelium', 'Forebrain/Midbrain/Hindbrain', 'Spinal cord', 'Cardiomyocytes', 'NMP', 'Erythroid3', 'Neural crest']
else:
    terminal_states = ['Amnion', 'Blood', 'Mid-Hind Gut', 'Foregut/Placodes', 'Mixed mesoderm', 'Extra-Embryonic ectoderm', 'Endothelial', 
                   'Cardiac', 'Endothelial/Mixed', 'Extra-Embryonic endoderm', 'Placodes/Extra-Embryonic mesoderm']


adata = sc.read_h5ad(f'/home/icb/jonas.flor/gast_atlas_clean/scarches/1M_{sys.argv[2]}/{sys.argv[1]}/{sys.argv[1]}_adata.h5ad')
cluster_key = 'celltype'
n_states = int(len(adata.obs.celltype.unique())*1.0)

if sys.argv[1]=='gastrulation':
    add_spliced=False
else:
    add_spliced=True

x_key = 'X_emb'

if sys.argv[4]=='weighted':
    end = '_w'
else:
    end = ''


with open(f'/home/icb/jonas.flor/gast_atlas_clean/otfm/1M_{sys.argv[2]}/{sys.argv[3]}_cond_model{end}.pt', mode='rb') as file:
       fm = cloudpickle.load(file)

preparation(adata, fm, x_key, add_spliced)

vk = VelocityKernel(adata, attr='obsm', xkey=x_key, vkey="velocity").compute_transition_matrix()
g = GPCCA(vk)

g.compute_macrostates(cluster_key=cluster_key, n_states=n_states)
g.predict_terminal_states(n_states=len(terminal_states), method='top_n')

terminal_states_contained = 0
for state in terminal_states:
    if any([terminal_state.startswith(state) for terminal_state in g.terminal_states.cat.categories.astype('string')]):
        terminal_states_contained = terminal_states_contained+1
terminal_states_found = terminal_states_contained/len(terminal_states)

corrcet_terminal_states = 0
for terminal_state in g.terminal_states.cat.categories.astype('string'):
    if any([terminal_state.startswith(state) for state in terminal_states]):
        corrcet_terminal_states = corrcet_terminal_states+1
corrcet_terminal_states = corrcet_terminal_states/len(g.terminal_states.cat.categories)

pd.DataFrame({'terminal_states_found': [terminal_states_found], 'correct_terminal_states': [corrcet_terminal_states]}).to_csv(f'/home/icb/jonas.flor/gast_atlas_clean/cellrank/{sys.argv[1]}/{sys.argv[2]}/{sys.argv[3]}/{sys.argv[4]}/terminal_cells.csv')

terminal_state_anno = []
for state in g.macrostates.cat.categories.astype('string'):
    if any([terminal_state.startswith(state) for state in terminal_states]):
        terminal_state_anno.append(state)
g.set_terminal_states(terminal_state_anno)

g.compute_fate_probabilities(tol=1e-20)
try:
    g.plot_fate_probabilities(same_plot=False, save=f'/home/icb/jonas.flor/gast_atlas_clean/cellrank/{sys.argv[1]}/{sys.argv[2]}/{sys.argv[3]}/{sys.argv[4]}/fate_probabilities.png')
except ValueError:
    g.plot_fate_probabilities(same_plot=True, save=f'/home/icb/jonas.flor/gast_atlas_clean/cellrank/{sys.argv[1]}/{sys.argv[2]}/{sys.argv[3]}/{sys.argv[4]}/fate_probabilities.png')
    

cr.pl.aggregate_fate_probabilities(
    adata,
    mode='heatmap',
    lineages=terminal_state_anno,
    cluster_key='celltype',
    clusters=list(adata.obs.celltype.unique()),
    title="",
    save=f'/home/icb/jonas.flor/gast_atlas_clean/cellrank/{sys.argv[1]}/{sys.argv[2]}/{sys.argv[3]}/{sys.argv[4]}/absorption_probability.png'
)

db = pd.read_csv('/home/icb/jonas.flor/gastrulation_atlas/data/mouse.v12.geneID.txt', sep='\t')[['gene_ID', 'gene_short_name']]
for t in g.terminal_states.cat.categories.astype('string'):
    try:
        driver_genes = g.compute_lineage_drivers(lineages = t, cluster_key=cluster_key)
        annotations = [db[db.gene_ID==x]['gene_short_name'].values[0] for x in driver_genes.index]
        driver_genes['gene_annotation'] = annotations
        driver_genes.to_csv(f'/home/icb/jonas.flor/gast_atlas_clean/cellrank/{sys.argv[1]}/{sys.argv[2]}/{sys.argv[3]}/{sys.argv[4]}/{t.replace("/","_")}_lineage_driver.csv')
    except RuntimeError:
        pd.DataFrame(data={'Terminal_States':g.terminal_states.cat.categories.astype('string')}).to_csv(f'/home/icb/jonas.flor/gast_atlas_clean/cellrank/{sys.argv[1]}/{sys.argv[2]}/{sys.argv[3]}/{sys.argv[4]}/no_lineage_drivers.csv')

# arg 1:dataset
# arg 2: genes
# arg 3: integrated
# arg 4: weighted (_w)






