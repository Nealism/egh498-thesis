#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      "no_commands_obs"
                      # "yaw_diff_obs"
                      # "clip"
                      "r3_no_terr"
                        )
declare -a Arguments=(
                      "--cpu 32 --env anymal_cmd_mj --training_on_hpc --epochs 2000 --wp_time_scalar 2.5 --obs_fn 2"
                      # "--cpu 32 --env anymal_cmd_mj --training_on_hpc --epochs 2500 --wp_time_scalar 2.5 --obs_fn 3"
                      # "--cpu 32 --env anymal_cmd_mj --training_on_hpc --epochs 2500 --wp_time_scalar 2.5 --clip"
                      "--cpu 32 --env anymal_cmd_mj --training_on_hpc --epochs 2000 --wp_time_scalar 2.5 --reward_fn 3"
                      )
            
export SBATCH_ACCOUNT=OD-219033
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "10:00:00"
done