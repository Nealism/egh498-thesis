#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                        "exp9/tor_cur_jit_5"
                        "exp9/tor_cur_jit_10"
                        "exp9/tor_cur_jit_20"
                        "exp9/tor_cur_jit_50"
                        "exp9/tor_cur_grass"
                        "exp9/tor_cur_tree"
                        
                        # "exp1/titan_grass"
                        # "exp3/anymal_cur"
                        # "exp3/anymal"
                        )
declare -a Arguments=(
                      "--cpu 64 --ident $USER --env franka_reach_dm_mj --goal end_effector --cur --control_type torque --training_on_hpc --jitter_scalar 5"
                      "--cpu 64 --ident $USER --env franka_reach_dm_mj --goal end_effector --cur --control_type torque --training_on_hpc --jitter_scalar 10"
                      "--cpu 64 --ident $USER --env franka_reach_dm_mj --goal end_effector --cur --control_type torque --training_on_hpc --jitter_scalar 20"
                      "--cpu 64 --ident $USER --env franka_reach_dm_mj --goal end_effector --cur --control_type torque --training_on_hpc --jitter_scalar 50"
                      "--cpu 64 --ident $USER --env franka_reach_dm_mj --goal end_effector --cur --control_type torque --training_on_hpc --jitter_scalar 10 --tree_type grass"
                      "--cpu 64 --ident $USER --env franka_reach_dm_mj --goal end_effector --cur --control_type torque --training_on_hpc --jitter_scalar 10 --tree_type tree"

                      # "--cpu 64 --ident $USER --env titan_mj --training_on_hpc --tree_type grass"
                      # "--cpu 64 --ident $USER --env anymal_mj --cur --training_on_hpc"
                      # "--cpu 64 --ident $USER --env anymal_mj --training_on_hpc"
                      )
export SBATCH_ACCOUNT=OD-227199
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "12:00:00"
  # sbatch -A OD-227199 ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "12:00:00"
  # sbatch -A OD-219033 ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "12:00:00"
done