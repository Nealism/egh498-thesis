#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                        "exp7/pos"
                        "exp7/pos2"
                        "exp7/pos_cur"
                        "exp7/pos_cur2"
                        "exp7/tor"
                        "exp7/tor2"
                        "exp7/tor_cur"
                        "exp7/tor_cur2"
                        )
declare -a Arguments=(
                      # --training_on_hpc argument is required for mujoco environments 
                      "--cpu 64 --ident $USER --env franka_reach_dm_mj --control_type position --training_on_hpc --seed 42"
                      "--cpu 64 --ident $USER --env franka_reach_dm_mj --control_type position --training_on_hpc --seed 84"
                      "--cpu 64 --ident $USER --env franka_reach_dm_mj --control_type position --training_on_hpc --cur --seed 42"
                      "--cpu 64 --ident $USER --env franka_reach_dm_mj --control_type position --training_on_hpc --cur --seed 84"
                      "--cpu 64 --ident $USER --env franka_reach_dm_mj --control_type torque --training_on_hpc --seed 42"
                      "--cpu 64 --ident $USER --env franka_reach_dm_mj --control_type torque --training_on_hpc --seed 84"
                      "--cpu 64 --ident $USER --env franka_reach_dm_mj --control_type torque --training_on_hpc --cur --seed 42"
                      "--cpu 64 --ident $USER --env franka_reach_dm_mj --control_type torque --training_on_hpc --cur --seed 84"
                      )

for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "12:00:00"
done
