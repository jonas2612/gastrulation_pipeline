#!/bin/bash


#SBATCH -o /home/icb/jonas.flor/gast_atlas_clean/data/bash_messages/outputs_gastrulation_prep
#SBATCH -e /home/icb/jonas.flor/gast_atlas_clean/data/bash_messages/errors_gastrulation_prep
#SBATCH -J gastrulation_prep
#SBATCH -p cpu_p
#SBATCH --qos=cpu_long
#SBATCH --mem=150G
#SBATCH -t 06:00:00
#SBATCH --nice=10000


source $HOME/.bashrc

mamba activate atlas_pca
python /home/icb/jonas.flor/gast_atlas_clean/data/gastrulation_prep.py

path="$(grep -i -E 'error|killed' /home/icb/jonas.flor/gast_atlas_clean/data/bash_messages/errors_gastrulation_prep)"
if [ -z "$path" ]
then
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scarches/integration_1M_10k_gast.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scarches/integration_1M_all_gast.cmd

    for m in metric_ari metric_ASW metric_cLISI metric_graph_connectivity metric_iLISI metric_iso_labels metric_nmi metric_pcr metric_silhouette_batch metric_silhouette
    do
        sbatch /home/icb/jonas.flor/gast_atlas_clean/scarches/{m}_unintegrated_gastrulation.cmd
    done
    echo "Done!"
else
    echo "Error produced"
fi