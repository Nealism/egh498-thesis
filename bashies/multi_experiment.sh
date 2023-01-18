#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                        "exp/terrain_a_little_higher"
                        )
declare -a Arguments=(
                      "--cpu 64 --env anymal_cmd_mj --training_on_hpc --add_terrain --epochs 2000"
                      )
            
export SBATCH_ACCOUNT=OD-219033
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "36:00:00"
done