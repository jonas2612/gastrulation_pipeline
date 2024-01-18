#!/bin/bash


#SBATCH -o /home/icb/jonas.flor/gast_atlas_clean/scarches/bash_messages/outputs_spaces_1M_all_in
#SBATCH -e /home/icb/jonas.flor/gast_atlas_clean/scarches/bash_messages/errors_spaces_1M_all_in
#SBATCH -J spaces_1M_all_in
#SBATCH -p gpu_p
#SBATCH --qos=gpu_normal
#SBATCH --gres=gpu:1
#SBATCH --mem=150G # total memory in MB
#SBATCH --exclude supergpu[02-03,05-09]
#SBATCH -t 04:00:00 # format dd-hh:mm:ss
#SBATCH --nice=10000  # adjusts scheduling priority


source $HOME/.bashrc

mamba activate scvi
python /home/icb/jonas.flor/gast_atlas_clean/scarches/integration.py invitro 1M all_genes

path="$(grep -i 'error' /home/icb/jonas.flor/gast_atlas_clean/scarches/bash_messages/errors_spaces_1M_all_in)"
if [ -z "$path" ]
then
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scarches/preprocessing_1M_all_invitro.cmd
else
    echo "Error produced"
fi
 