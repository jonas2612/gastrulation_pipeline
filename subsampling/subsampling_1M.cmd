#!/bin/bash


#SBATCH -o /home/icb/jonas.flor/gast_atlas_clean/subsampling/bash_messages/outputs_subsampling_1M
#SBATCH -e /home/icb/jonas.flor/gast_atlas_clean/subsampling/bash_messages/errors_subsampling_1M
#SBATCH -J 1M_subsampling
#SBATCH -p cpu_p
#SBATCH --qos=cpu_long
#SBATCH --mem=300G # total memory in MB
#SBATCH -t 01-00:00:00 # format dd-hh:mm:ss
#SBATCH --nice=100000  # adjusts scheduling priority


source $HOME/.bashrc

mamba activate subsampling
python /home/icb/jonas.flor/gast_atlas_clean/subsampling/subsampling.py 1M

path="$(grep -i 'error|killed' /home/icb/jonas.flor/gast_atlas_clean/subsampling/bash_messages/errors_subsampling_1M)"
if [ -z "$path" ]
then
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/training_1M_10k.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/training_1M_all.cmd
    echo "Done!"
else
    echo "Error produced"
fi