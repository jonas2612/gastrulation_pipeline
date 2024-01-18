#!/bin/bash


#SBATCH -o /home/icb/jonas.flor/gast_atlas_clean/data/bash_messages/outputs_atlas_concat
#SBATCH -e /home/icb/jonas.flor/gast_atlas_clean/data/bash_messages/errors_atlas_concat
#SBATCH -J atlas_concat
#SBATCH -p cpu_p
#SBATCH --qos=cpu_long
#SBATCH --mem=300G
#SBATCH -t 0-12:00:00
#SBATCH --nice=10000


source $HOME/.bashrc

mamba activate atlas_pca
python /home/icb/jonas.flor/gast_atlas_clean/data/atlas_concat.py

path="$(grep -i -E 'error|killed' /home/icb/jonas.flor/gast_atlas_clean/data/bash_messages/errors_atlas_concat)"
if [ -z "$path" ]
then
    sbatch /home/icb/jonas.flor/gast_atlas_clean/data/02_atlas_annotation.cmd
else
    echo "Error produced"
fi