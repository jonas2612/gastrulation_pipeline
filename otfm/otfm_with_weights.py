from ott.neural.flows.models import VelocityField
from ott.neural.flows.flows import ConstantNoiseFlow
from ott.neural.flows.samplers import sample_uniformly
from ott.neural.flows.otfm import OTFlowMatching
from ott.solvers.linear import sinkhorn
from ott.neural.data.dataloaders import OTDataLoader, ConditionalDataLoader

import optax
import scanpy as sc

import numpy as np
import pandas as pd

import anndata as ad
from fractions import Fraction
import cloudpickle

import sys

def dataGeneration(data: ad.AnnData, weights: pd.DataFrame): #adjustment of data according to weights wrt to cellcluster_moscot
    weight = []
    mass_rel = []
    clusters = []
    for cluster in data.obs.cellcluster_moscot.values.unique():
        if cluster in weights['celltype'].values:
            weight.append(float(sum(Fraction(s) for s in weights.loc[weights['celltype']==cluster, 'weight'].values[0].split())))
        else:
            weight.append(1.)
        mass_rel.append(data[data.obs.cellcluster_moscot==cluster].n_obs)
        clusters.append(cluster)
    
    mass_rel = np.array(mass_rel)/data.n_obs
    weight = np.array(weight)

    mass = np.sum(mass_rel*weight)
    weight_adjusted = weight/mass

    weight_adjusted = pd.DataFrame(data={'cluster': clusters, 'weight': weight_adjusted})

    
    adata_collection = []

    for cluster in data.obs.cellcluster_moscot.values.unique(): #for each cluster get samples with replacement and sample according to these indices
        data_cluster = data[data.obs.cellcluster_moscot==cluster]
        old_n_obs = data_cluster.n_obs
        obs_indices = np.random.choice(
            old_n_obs,
            size=int(old_n_obs*weight_adjusted.loc[weight_adjusted['cluster']==cluster, 'weight'].values[0]),
            replace=True)
        adata_collection.append(data[obs_indices])

    return ad.concat(adata_collection) #concatenate all cluster

def dataGenerator(data: ad.AnnData, day_source: float, day_target: float, weights: pd.DataFrame): #prepare source and target for dataGeneration
    weights_time = weights[weights['timepoint']==day_source]
    weights_source = weights_time[weights_time['marginal']=='source_marginals']
    weights_target = weights_time[weights_time['marginal']=='target_marginals']
    
    data_source_prelim = data[data.obs.day==day_source]
    data_target_prelim = data[data.obs.day==day_target]

    data_source = dataGeneration(data_source_prelim, weights_source)
    data_target = dataGeneration(data_target_prelim, weights_target)

    return data_source, data_target


weights = pd.read_csv('/home/icb/jonas.flor/gastrulation_atlas/moscot/weights_together.csv')

adata = sc.read_h5ad(f'/home/icb/jonas.flor/gast_atlas_clean/scvi/{sys.argv[1]}_{sys.argv[2]}/{sys.argv[3]}_adata.h5ad')
day_sort=adata.obs.day.unique()
day_sort.sort()

dataloaders = {}
if sys.argv[3]=='integrated':
    for day_ind in range(day_sort.shape[0]-1):
        source, target = dataGenerator(adata, day_sort[day_ind], day_sort[day_ind+1], weights)
        
        dataloaders[day_sort[day_ind]] = OTDataLoader(
            1024, 
            source_lin=source.obsm['X_emb'], 
            target_lin=target.obsm['X_emb'], 
            source_conditions=np.expand_dims(source.obs.day.values, axis=1)
            )
elif sys.argv[3]=='unintegrated':
    for day_ind in range(day_sort.shape[0]-1):
        source, target = dataGenerator(adata, day_sort[day_ind], day_sort[day_ind+1], weights)
        
        dataloaders[day_sort[day_ind]] = OTDataLoader(
            1024, 
            source_lin=source.obsm['X_pca'], 
            target_lin=target.obsm['X_pca'], 
            source_conditions=np.expand_dims(source.obs.day.values, axis=1)
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
with open(f'/home/icb/jonas.flor/gast_atlas_clean/otfm/{sys.argv[1]}_{sys.argv[2]}/{sys.argv[3]}_cond_model_w.pt', mode='wb') as file:
   cloudpickle.dump(fm, file)
