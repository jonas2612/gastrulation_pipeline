#!/bin/bash

#SBATCH -o /home/icb/jonas.flor/gast_atlas_clean/scvi/bash_messages/outputs_metr_pcr_in_1M_all
#SBATCH -e /home/icb/jonas.flor/gast_atlas_clean/scvi/bash_messages/errors_metr_pcr_in_1M_all
#SBATCH -J metr_pcr_in_1M_all
#SBATCH -p cpu_p
#SBATCH --qos=cpu_normal
#SBATCH --mem=150G
#SBATCH -t 1-12:00:00
#SBATCH --nice=100000


source $HOME/.bashrc

mamba activate scvi
python /home/icb/jonas.flor/gast_atlas_clean/scvi/metric_pcr_integrated.py 1M all_genes

echo "Done!"
                        