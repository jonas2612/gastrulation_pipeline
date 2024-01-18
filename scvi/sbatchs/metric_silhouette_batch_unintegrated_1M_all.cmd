#!/bin/bash

#SBATCH -o /home/icb/jonas.flor/gast_atlas_clean/scvi/bash_messages/outputs_metr_sil_bat_un_1M_all
#SBATCH -e /home/icb/jonas.flor/gast_atlas_clean/scvi/bash_messages/errors_metr_sil_bat_un_1M_all
#SBATCH -J metr_sil_bat_un_1M_all
#SBATCH -p cpu_p
#SBATCH --qos=cpu_normal
#SBATCH --mem=150G
#SBATCH -t 1-12:00:00
#SBATCH --nice=100000


source $HOME/.bashrc

mamba activate scvi
python /home/icb/jonas.flor/gast_atlas_clean/scvi/metric_silhouette_batch_unintegrated.py 1M all_genes

echo "Done!"
                        