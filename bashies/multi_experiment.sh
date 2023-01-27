#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      "new_obs"
                      "one_wp_per_ep_and_new_obs"
                      "new_obs_and_2048_steps"
                      "new_obs_and_4096_steps"
                      
                        )
declare -a Arguments=(
                      "--cpu 32 --env anymal_cmd_mj --training_on_hpc --epochs 5000 --reward 1"
                      "--cpu 32 --env anymal_cmd_mj --training_on_hpc --epochs 5000 --reward 1 --one_wp_per_ep"
                      "--cpu 32 --env anymal_cmd_mj --training_on_hpc --epochs 5000 --reward 1 --max_ep_len 2048"
                      "--cpu 32 --env anymal_cmd_mj --training_on_hpc --epochs 5000 --reward 1 --max_ep_len 4096"
                      )
            
export SBATCH_ACCOUNT=OD-219033
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "24:00:00"
done