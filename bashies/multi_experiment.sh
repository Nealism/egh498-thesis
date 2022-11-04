#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                        "exp1/pos_py311"
                        "exp1/tor_py311"
                        "exp1/tor_grass_py311"
                        "exp1/tor_tree_py311"
                        "exp1/titan_grass_py311"
                        "exp1/any_cur_py311"
                        "exp1/any_py311"
                        )
declare -a Arguments=(
                      # --training_on_hpc argument is required for mujoco environments 
                      "--cpu 64 --ident $USER --env franka_reach_dm_mj --cur --control_type position --training_on_hpc"
                      "--cpu 64 --ident $USER --env franka_reach_dm_mj --cur --control_type torque --training_on_hpc"
                      "--cpu 64 --ident $USER --env franka_reach_dm_mj --cur --tree_type grass --control_type torque --training_on_hpc"
                      "--cpu 64 --ident $USER --env franka_reach_dm_mj --cur --tree_type tree --control_type torque --training_on_hpc"
                      "--cpu 64 --ident $USER --env titan_mj --training_on_hpc --tree_type grass"
                      "--cpu 64 --ident $USER --env anymal_mj --cur --training_on_hpc"
                      "--cpu 64 --ident $USER --env anymal_mj --training_on_hpc"
                      )

for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet3_11.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "12:00:00"
done
