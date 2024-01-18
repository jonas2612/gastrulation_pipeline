#!/bin/bash


#SBATCH -o /home/icb/jonas.flor/gast_atlas_clean/data/bash_messages/outputs_atlas_anno
#SBATCH -e /home/icb/jonas.flor/gast_atlas_clean/data/bash_messages/errors_atlas_anno
#SBATCH -J atlas_anno
#SBATCH -p cpu_p
#SBATCH --qos=cpu_long
#SBATCH --mem=300G
#SBATCH -t 1-00:00:00
#SBATCH --nice=10000


source $HOME/.bashrc

mamba activate atlas_pca
python /home/icb/jonas.flor/gast_atlas_clean/data/atlas_annotation.py

path="$(grep -i -E 'error|killed' /home/icb/jonas.flor/gast_atlas_clean/data/bash_messages/errors_atlas_anno)"
if [ -z "$path" ]
then
    sbatch /home/icb/jonas.flor/gast_atlas_clean/subsampling/subsampling_validation.cmd
    echo "Done!"
else
    echo "Error produced"
fi