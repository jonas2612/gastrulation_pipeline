#!/bin/bash


#SBATCH -o /home/icb/jonas.flor/gast_atlas_clean/scarches/bash_messages/outputs_integration_1M_all_ex
#SBATCH -e /home/icb/jonas.flor/gast_atlas_clean/scarches/bash_messages/errors_integration_1M_all_ex
#SBATCH -J integration_1M_all_ex
#SBATCH -p gpu_p
#SBATCH --qos=gpu_normal
#SBATCH --gres=gpu:1
#SBATCH --mem=150G # total memory in MB
#SBATCH --exclude supergpu[02-03,05-09]
#SBATCH -t 04:00:00 # format dd-hh:mm:ss
#SBATCH --nice=10000  # adjusts scheduling priority


source $HOME/.bashrc

mamba activate scvi
python /home/icb/jonas.flor/gast_atlas_clean/scarches/integration.py exvitro 1M all_genes

path="$(grep -i 'error' /home/icb/jonas.flor/gast_atlas_clean/scarches/bash_messages/errors_integration_1M_all_ex)"
if [ -z "$path" ]
then
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scarches/preprocessing_1M_all_exvitro.cmd
else
    echo "Error produced"
fi
 