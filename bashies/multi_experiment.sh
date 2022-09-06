#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                        "first_franka_ball"
                        "first_franka_reach"
                        )
declare -a Arguments=(
                      "--cpu 64 --ident $USER --env franka_ball_mj"
                      "--cpu 64 --ident $USER --env franka_reach_mj"
                      )

for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "12:00:00"
done
