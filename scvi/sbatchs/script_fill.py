dict_bash = {'training': 'tr', 'preprocessing': 'prep', 'data_preparation': 'data_prep', 'metric_ari_integrated': 'metr_ari_in', 'metric_ari_unintegrated': 'metr_ari_un', 'metric_ASW_integrated': 'metr_ASW_in', 'metric_ASW_unintegrated': 'metr_ASW_un', 'metric_cLISI_integrated': 'metr_cLISI_in', 'metric_cLISI_unintegrated': 'metr_cLISI_un', 'metric_graph_connectivity_integrated': 'metr_gr_con_in', 'metric_graph_connectivity_unintegrated': 'metr_gr_con_un', 'metric_hgv_overlap': 'metr_hgv', 'metric_iLISI_integrated': 'metr_iLISI_in', 'metric_iLISI_unintegrated': 'metr_iLISI_un', 'metric_iso_labels_integrated': 'metr_iso_lab_in', 'metric_iso_labels_unintegrated': 'metr_iso_lab_un', 'metric_nmi_integrated': 'metr_nmi_in', 'metric_nmi_unintegrated': 'metr_nmi_un', 'metric_pcr_integrated': 'metr_pcr_in', 'metric_pcr_unintegrated': 'metr_pcr_un', 'metric_silhouette_batch_integrated': 'metr_sil_bat_in', 'metric_silhouette_batch_unintegrated': 'metr_sil_bat_un', 'metric_silhouette_integrated': 'metr_sil_in', 'metric_silhouette_unintegrated': 'metr_sil_un', 'metric_traject_conservation': 'metr_traj_con'}
next_mod = {'training': 'data_preparation', 'preprocessing': 'metric', 'data_preparation': 'preprocessing'}
time = {'training': '2-00:00:00',
        'preprocessing': '15:00:00',
        'data_preparation': '1-00:00:00',
        'metric_ari_integrated': '3-00:00:00',
        'metric_ari_unintegrated': '3-00:00:00',
        'metric_ASW_integrated': '1-12:00:00',
        'metric_ASW_unintegrated': '1-12:00:00',
        'metric_cLISI_integrated': '1-12:00:00',
        'metric_cLISI_unintegrated': '1-12:00:00',
        'metric_graph_connectivity_integrated': '1-12:00:00',
        'metric_graph_connectivity_unintegrated': '1-12:00:00',
        'metric_hgv_overlap': '1-12:00:00',
        'metric_iLISI_integrated': '1-12:00:00',
        'metric_iLISI_unintegrated': '1-12:00:00',
        'metric_iso_labels_integrated': '3-00:00:00',
        'metric_iso_labels_unintegrated': '3-00:00:00',
        'metric_nmi_integrated': '3-00:00:00',
        'metric_nmi_unintegrated': '3-00:00:00',
        'metric_pcr_integrated': '1-12:00:00',
        'metric_pcr_unintegrated': '1-12:00:00',
        'metric_silhouette_batch_integrated': '1-12:00:00',
        'metric_silhouette_batch_unintegrated': '1-12:00:00',
        'metric_silhouette_integrated': '1-12:00:00',
        'metric_silhouette_unintegrated': '1-12:00:00',
        'metric_traject_conservation': '1-12:00:00'
            }

for m in ['training', 'preprocessing', 'data_preparation', 'metric_ari_integrated', 'metric_ari_unintegrated', 'metric_ASW_integrated', 'metric_ASW_unintegrated', 'metric_cLISI_integrated', 'metric_cLISI_unintegrated', 'metric_graph_connectivity_integrated', 'metric_graph_connectivity_unintegrated', 'metric_hgv_overlap', 'metric_iLISI_integrated', 'metric_iLISI_unintegrated', 'metric_iso_labels_integrated', 'metric_iso_labels_unintegrated', 'metric_nmi_integrated', 'metric_nmi_unintegrated', 'metric_pcr_integrated', 'metric_pcr_unintegrated', 'metric_silhouette_batch_integrated', 'metric_silhouette_batch_unintegrated', 'metric_silhouette_integrated', 'metric_silhouette_unintegrated', 'metric_traject_conservation']:
    for o in ['1M']:
        for g in ['10k', 'all']:
            lr=''
            if m=="training":
                part = '''#SBATCH -p gpu_p
#SBATCH --qos=gpu_normal
#SBATCH --gres=gpu:1
#SBATCH --mem=150G
#SBATCH --exclude supergpu[02-03,05-09]'''
            else:
                part = '''#SBATCH -p cpu_p
#SBATCH --qos=cpu_normal
#SBATCH --mem=150G'''
            if "metr" in m:
                follow = 'echo "Done!"'
            elif m=='preprocessing':
                follow = f'''path="$(grep -iE 'killed' /home/icb/jonas.flor/gast_atlas_clean/scvi/bash_messages/errors_{dict_bash[m]}_{o}_{g})"
if [ -z "$path" ]
then                    
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_ari_integrated_{o}_{g}.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_ari_unintegrated_{o}_{g}.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_ASW_integrated_{o}_{g}.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_ASW_unintegrated_{o}_{g}.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_cLISI_integrated_{o}_{g}.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_cLISI_unintegrated_{o}_{g}.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_graph_connectivity_integrated_{o}_{g}.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_graph_connectivity_unintegrated_{o}_{g}.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_hgv_overlap_{o}_{g}.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_iLISI_integrated_{o}_{g}.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_iLISI_unintegrated_{o}_{g}.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_iso_labels_integrated_{o}_{g}.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_iso_labels_unintegrated_{o}_{g}.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_nmi_integrated_{o}_{g}.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_nmi_unintegrated_{o}_{g}.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_pcr_integrated_{o}_{g}.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_pcr_unintegrated_{o}_{g}.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_silhouette_batch_integrated_{o}_{g}.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_silhouette_batch_unintegrated_{o}_{g}.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_silhouette_integrated_{o}_{g}.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_silhouette_unintegrated_{o}_{g}.cmd
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/metric_traject_conservation_{o}_{g}.cmd
    echo "Done!"
else
    echo "Error produced"
fi
                        '''
            else:
                follow = f'''path="$(grep -iE 'killed' /home/icb/jonas.flor/gast_atlas_clean/scvi/bash_messages/errors_{dict_bash[m]}_{o}_{g})"
if [ -z "$path" ]
then
    sbatch /home/icb/jonas.flor/gast_atlas_clean/scvi/sbatchs/{next_mod[m]}_{o}_{g}.cmd
    echo "Done!"
else
    echo "Error produced"
fi
                        '''
                
            f = open(f'{m}_{o}_{g}.cmd', 'w+')
            f.write(f'''#!/bin/bash

#SBATCH -o /home/icb/jonas.flor/gast_atlas_clean/scvi/bash_messages/outputs_{dict_bash[m]}_{o}_{g}
#SBATCH -e /home/icb/jonas.flor/gast_atlas_clean/scvi/bash_messages/errors_{dict_bash[m]}_{o}_{g}
#SBATCH -J {dict_bash[m]}_{o}_{g}
{part}
#SBATCH -t {time[m]}
#SBATCH --nice=100000


source $HOME/.bashrc

mamba activate scvi
python /home/icb/jonas.flor/gast_atlas_clean/scvi/{m}.py {o} {g}_genes

{follow}
                        ''')
            f.close()
               