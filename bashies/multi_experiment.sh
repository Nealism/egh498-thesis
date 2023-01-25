#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      "no_terrain_r1_lin"
                      "no_terrain_r1_exp_cmd_ranges0"
                      "no_terrain_r1_exp_one_wp_per_ep"
                        )
declare -a Arguments=(
                      "--cpu 32 --env anymal_cmd_mj --training_on_hpc --epochs 5000 --reward 1"
                      "--cpu 32 --env anymal_cmd_mj --training_on_hpc --epochs 5000 --reward 2 --cmd_ranges (0,0,0)"
                      "--cpu 32 --env anymal_cmd_mj --training_on_hpc --epochs 5000 --reward 2 --one_wp_per_ep"
                      )
            
export SBATCH_ACCOUNT=OD-219033
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "24:00:00"
done