#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      "35_0.03_patches_and_per"
                      "0.03_patches_and_per"
                      "0.04_patches_and_per"
                      "0.03_whole_terr_and_perc"
                      "0.04_whole_terr_and_perc"
                        )
declare -a Arguments=(
    "--cpu 32 --env anymal_cmd_mj --training_on_hpc --epochs 3000 --max_ep_len 256 --local_epoch_len 1024 --add_terrain --rand_dz_mult 0.03 --undul_patches 35 --use_perception"
    "--cpu 32 --env anymal_cmd_mj --training_on_hpc --epochs 3000 --max_ep_len 256 --local_epoch_len 1024 --add_terrain --rand_dz_mult 0.03 --undul_patches 25 --use_perception"
    "--cpu 32 --env anymal_cmd_mj --training_on_hpc --epochs 3000 --max_ep_len 256 --local_epoch_len 1024 --add_terrain --rand_dz_mult 0.04 --undul_patches 25 --use_perception"
    "--cpu 32 --env anymal_cmd_mj --training_on_hpc --epochs 3000 --max_ep_len 256 --local_epoch_len 1024 --add_terrain --rand_dz_mult 0.03"
    "--cpu 32 --env anymal_cmd_mj --training_on_hpc --epochs 3000 --max_ep_len 256 --local_epoch_len 1024 --add_terrain --rand_dz_mult 0.04"
)
            
export SBATCH_ACCOUNT=OD-219033
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "23:59:59"
done