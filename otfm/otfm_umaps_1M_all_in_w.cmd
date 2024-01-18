#!/bin/bash


#SBATCH -o /home/icb/jonas.flor/gast_atlas_clean/otfm/bash_messages/outputs_otfm_umaps_all_in_w
#SBATCH -e /home/icb/jonas.flor/gast_atlas_clean/otfm/bash_messages/errors_otfm_umaps_all_in_w
#SBATCH -J otfm_umaps_all_in_w
#SBATCH -p cpu_p
#SBATCH --qos=cpu_normal
#SBATCH --mem=250G # total memory in MB
#SBATCH -t 1-00:00:00 # format dd-hh:mm:ss
#SBATCH --nice=100000  # adjusts scheduling priority


source $HOME/.bashrc

mamba activate moscot_flow
python /home/icb/jonas.flor/gast_atlas_clean/otfm/otfm_umaps.py all_genes integrated weighted