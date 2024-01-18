#!/bin/bash

#SBATCH -o /home/icb/jonas.flor/gast_atlas_clean/scarches/bash_messages/outputs_metr_iLISI_in_inv_10k
#SBATCH -e /home/icb/jonas.flor/gast_atlas_clean/scarches/bash_messages/errors_metr_iLISI_in_inv_10k
#SBATCH -J metr_iLISI_in_inv_10k
#SBATCH -p cpu_p
#SBATCH --qos=cpu_normal
#SBATCH --mem=150G
#SBATCH -t 1-12:00:00
#SBATCH --nice=100000


source $HOME/.bashrc

mamba activate scvi
python /home/icb/jonas.flor/gast_atlas_clean/scarches/metric_iLISI_integrated.py invitro 10k_genes

echo "Done!"
