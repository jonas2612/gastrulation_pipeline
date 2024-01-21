#!/bin/bash

#SBATCH -o /home/icb/jonas.flor/gast_atlas_clean/cellrank/bash_messages/outputs_umaps_push_in_all_integrated
#SBATCH -e /home/icb/jonas.flor/gast_atlas_clean/cellrank/bash_messages/errors_umaps_push_in_all_integrated
#SBATCH -J umaps_push_in_all_integrated
#SBATCH -p cpu_p
#SBATCH --qos=cpu_normal
#SBATCH --mem=100G
#SBATCH -t 1-00:00:00
#SBATCH --nice=100000


source $HOME/.bashrc

mamba activate cellrank_new
python /home/icb/jonas.flor/gast_atlas_clean/cellrank/pushed_umaps.py invitro all_genes integrated unweighted
                