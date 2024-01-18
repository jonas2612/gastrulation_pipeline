#!/bin/bash


#SBATCH -o /home/icb/jonas.flor/gast_atlas_clean/otfm/bash_messages/outputs_otfm_1M_all_un
#SBATCH -e /home/icb/jonas.flor/gast_atlas_clean/otfm/bash_messages/errors_otfm_1M_all_un
#SBATCH -J otfm_1M_all_un
#SBATCH -p gpu_p
#SBATCH --qos=gpu_normal
#SBATCH --gres=gpu:1
#SBATCH --mem=120G # total memory in MB
#SBATCH --exclude supergpu[02-03,05-09]
#SBATCH -t 2-00:00:00 # format dd-hh:mm:ss
#SBATCH --nice=100000  # adjusts scheduling priority


source $HOME/.bashrc

mamba activate moscot_flow
python /home/icb/jonas.flor/gast_atlas_clean/otfm/otfm.py 1M all_genes unintegrated

path="$(grep -i 'error' /home/icb/jonas.flor/gast_atlas_clean/otfm/bash_messages/errors_otfm_1M_all_un)"
if [ -z "$path" ]
then
    sbatch /home/icb/jonas.flor/gast_atlas_clean/otfm/otfm_umaps_all_un.cmd
    echo "Done!"
else
    echo "Error produced"
fi