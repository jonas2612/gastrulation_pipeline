#!/bin/bash

#SBATCH -o /home/icb/jonas.flor/gast_atlas_clean/scvi/bash_messages/outputs_prep_1M_10k
#SBATCH -e /home/icb/jonas.flor/gast_atlas_clean/scvi/bash_messages/errors_prep_1M_10k
#SBATCH -J prep_1M_10k
#SBATCH -p cpu_p
#SBATCH --qos=cpu_long
#SBATCH --mem=150G
#SBATCH -t 15:00:00
#SBATCH --nice=100000


source $HOME/.bashrc

mamba activate scvi
python /home/icb/jonas.flor/gast_atlas_clean/scvi/preprocessing.py 1M 10k_genes

path="$(grep -iE 'killed' /home/icb/jonas.flor/gast_atlas_clean/scvi/bash_messages/errors_prep_1M_10k)"
if [ -z "$path" ]
then         
    sbatch /home/icb/jonas.flor/gast_atlas_clean/otfm/otfm_1M_10k_in_w.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/otfm/otfm_1M_10k_un_w.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/otfm/otfm_1M_10k_in.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/otfm/otfm_1M_10k_un.cmd
    
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_ari_integrated_1M_10k.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_ari_unintegrated_1M_10k.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_ASW_integrated_1M_10k.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_ASW_unintegrated_1M_10k.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_cLISI_integrated_1M_10k.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_cLISI_unintegrated_1M_10k.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_graph_connectivity_integrated_1M_10k.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_graph_connectivity_unintegrated_1M_10k.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_hgv_overlap_1M_10k.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_iLISI_integrated_1M_10k.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_iLISI_unintegrated_1M_10k.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_iso_labels_integrated_1M_10k.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_iso_labels_unintegrated_1M_10k.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_nmi_integrated_1M_10k.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_nmi_unintegrated_1M_10k.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_pcr_integrated_1M_10k.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_pcr_unintegrated_1M_10k.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_silhouette_batch_integrated_1M_10k.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_silhouette_batch_unintegrated_1M_10k.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_silhouette_integrated_1M_10k.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_silhouette_unintegrated_1M_10k.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_traject_conservation_1M_10k.cmd
    echo "Done!"
else
    echo "Error produced"
fi
                        
                        