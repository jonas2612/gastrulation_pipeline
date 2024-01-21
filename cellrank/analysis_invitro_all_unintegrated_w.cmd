#!/bin/bash

#SBATCH -o /home/icb/jonas.flor/gast_atlas_clean/cellrank/bash_messages/outputs_analysis_in_all_unintegrated_w
#SBATCH -e /home/icb/jonas.flor/gast_atlas_clean/cellrank/bash_messages/errors_analysis_in_all_unintegrated_w
#SBATCH -J analysis_in_all_unintegrated_w
#SBATCH -p cpu_p
#SBATCH --qos=cpu_normal
#SBATCH --mem=100G
#SBATCH -t 1-00:00:00
#SBATCH --nice=100000


source $HOME/.bashrc

mamba activate cellrank_new
python /home/icb/jonas.flor/gast_atlas_clean/cellrank/analysis.py invitro all_genes unintegrated weighted
                