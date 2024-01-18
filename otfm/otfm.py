from ott.neural.flows.models import VelocityField
from ott.neural.flows.flows import ConstantNoiseFlow
from ott.neural.flows.samplers import sample_uniformly
from ott.neural.flows.otfm import OTFlowMatching
from ott.solvers.linear import sinkhorn
from ott.neural.data.dataloaders import OTDataLoader, ConditionalDataLoader

import optax
import scanpy as sc
import numpy as np

import cloudpickle

import sys

adata = sc.read_h5ad(f'/home/icb/jonas.flor/gast_atlas_clean/scvi/{sys.argv[1]}_{sys.argv[2]}/{sys.argv[3]}_adata.h5ad')
day_sort=adata.obs.day.unique()
day_sort.sort()

dataloaders = {}
if sys.argv[3]=='integrated':
    for day_ind in range(day_sort.shape[0]-1):
        dataloaders[day_sort[day_ind]] = OTDataLoader(
            1024, 
            source_lin=adata[adata.obs.day==day_sort[day_ind]].obsm['X_emb'], 
            target_lin=adata[adata.obs.day==day_sort[day_ind+1]].obsm['X_emb'], 
            source_conditions=np.expand_dims(adata[adata.obs.day==day_sort[day_ind]].obs.day.values, axis=1)
            )
elif sys.argv[3]=='unintegrated':
    for day_ind in range(day_sort.shape[0]-1):
        dataloaders[day_sort[day_ind]] = OTDataLoader(
            1024, 
            source_lin=adata[adata.obs.day==day_sort[day_ind]].obsm['X_pca'], 
            target_lin=adata[adata.obs.day==day_sort[day_ind+1]].obsm['X_pca'], 
            source_conditions=np.expand_dims(adata[adata.obs.day==day_sort[day_ind]].obs.day.values, axis=1)
            )
else:
    raise NotImplementedError

cond_prob = np.ones(day_sort.shape[0]-1)/(day_sort.shape[0]-1)
cond_prob[0] = 1-sum(cond_prob[1:])
adata_loader = ConditionalDataLoader(dataloaders, cond_prob)

neural_vf = VelocityField(
    output_dim=50,
    condition_dim=1,
    latent_embed_dim=256,
    n_frequencies=128
)
ot_solver = sinkhorn.Sinkhorn()
time_sampler = sample_uniformly
optimizer = optax.adam(learning_rate=1e-4)
fm = OTFlowMatching(
    neural_vf,
    input_dim=50,
    cond_dim=1,
    iterations=100000,
    valid_freq=1000,
    ot_solver=ot_solver,
    flow=ConstantNoiseFlow(0.0),
    time_sampler=time_sampler,
    optimizer=optimizer
)
fm(adata_loader, adata_loader)
with open(f'/home/icb/jonas.flor/gast_atlas_clean/otfm/{sys.argv[1]}_{sys.argv[2]}/{sys.argv[3]}_cond_model.pt', mode='wb') as file:
   cloudpickle.dump(fm, file)