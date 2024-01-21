#!/bin/bash


#SBATCH -o /home/icb/jonas.flor/gast_atlas_clean/scarches/bash_messages/outputs_prep_1M_10k_ex
#SBATCH -e /home/icb/jonas.flor/gast_atlas_clean/scarches/bash_messages/errors_prep_1M_10k_ex
#SBATCH -J prep_1M_10k_ex
#SBATCH -p cpu_p
#SBATCH --qos=cpu_long
#SBATCH --mem=100G # total memory in MB
#SBATCH -t 04:00:00 # format dd-hh:mm:ss
#SBATCH --nice=10000  # adjusts scheduling priority


source $HOME/.bashrc

mamba activate scvi
python /home/icb/jonas.flor/gast_atlas_clean/scarches/preprocessing.py exvitro 1M 10k_genes


sbatch /home/icb/jonas.flor/gast_atlas_clean/cellrank/analysis_exvitro_10k_integrated.cmd
sbatch /home/icb/jonas.flor/gast_atlas_clean/cellrank/analysis_exvitro_10k_integrated_w.cmd
sbatch /home/icb/jonas.flor/gast_atlas_clean/cellrank/analysis_exvitro_10k_unintegrated.cmd
sbatch /home/icb/jonas.flor/gast_atlas_clean/cellrank/analysis_exvitro_10k_unintegrated_w.cmd

sbatch /home/icb/jonas.flor/gast_atlas_clean/cellrank/umaps_push_exvitro_10k_integrated.cmd
sbatch /home/icb/jonas.flor/gast_atlas_clean/cellrank/umaps_push_exvitro_10k_integrated_w.cmd
sbatch /home/icb/jonas.flor/gast_atlas_clean/cellrank/umaps_push_exvitro_10k_unintegrated.cmd
sbatch /home/icb/jonas.flor/gast_atlas_clean/cellrank/umaps_push_exvitro_10k_unintegrated_w.cmd

for m in metric_ari_integrated metric_ASW_integrated metric_cLISI_integrated metric_graph_connectivity_integrated metric_hgv_overlap metric_iLISI_integrated metric_iso_labels_integrated metric_nmi_integrated metric_pcr_integrated metric_silhouette_batch_integrated  metric_silhouette_integrated metric_traject_conservation
do
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scarches/${m}_exvitro_10k.cmd
done
