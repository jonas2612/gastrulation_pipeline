dict_ds = {'gastrulation': 'gast', 'invitro': 'in', 'exvitro': 'ex'}
dict_weight = {'weighted': '_w', 'unweighted':''}
dict_mem = {'gastrulation': '150G', 'invitro': '100G', 'exvitro': '100G'}

for d in ['gastrulation', 'invitro', 'exvitro']:
    for g in ['10k', 'all']:
        for i in ['integrated', 'unintegrated']:
            for w in ['weighted', 'unweighted']:
                f=open(f'analysis_{d}_{g}_{i}{dict_weight[w]}.cmd', 'w+')
                f.write(f'''#!/bin/bash

#SBATCH -o /home/icb/jonas.flor/gast_atlas_clean/cellrank/bash_messages/outputs_analysis_{dict_ds[d]}_{g}_{i}{dict_weight[w]}
#SBATCH -e /home/icb/jonas.flor/gast_atlas_clean/cellrank/bash_messages/errors_analysis_{dict_ds[d]}_{g}_{i}{dict_weight[w]}
#SBATCH -J analysis_{dict_ds[d]}_{g}_{i}{dict_weight[w]}
#SBATCH -p cpu_p
#SBATCH --qos=cpu_normal
#SBATCH --mem={dict_mem[d]}
#SBATCH -t 1-00:00:00
#SBATCH --nice=100000


source $HOME/.bashrc

mamba activate cellrank_new
python /home/icb/jonas.flor/gast_atlas_clean/cellrank/analysis.py {d} {g}_genes {i} {w}
                ''')
                f.close()

                f=open(f'umaps_push_{d}_{g}_{i}{dict_weight[w]}.cmd', 'w+')
                f.write(f'''#!/bin/bash

#SBATCH -o /home/icb/jonas.flor/gast_atlas_clean/cellrank/bash_messages/outputs_umaps_push_{dict_ds[d]}_{g}_{i}{dict_weight[w]}
#SBATCH -e /home/icb/jonas.flor/gast_atlas_clean/cellrank/bash_messages/errors_umaps_push_{dict_ds[d]}_{g}_{i}{dict_weight[w]}
#SBATCH -J umaps_push_{dict_ds[d]}_{g}_{i}{dict_weight[w]}
#SBATCH -p cpu_p
#SBATCH --qos=cpu_normal
#SBATCH --mem={dict_mem[d]}
#SBATCH -t 1-00:00:00
#SBATCH --nice=100000


source $HOME/.bashrc

mamba activate cellrank_new
python /home/icb/jonas.flor/gast_atlas_clean/cellrank/pushed_umaps.py {d} {g}_genes {i} {w}
                ''')
                f.close()
