#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                        "exp/terrain_only"
                        )
declare -a Arguments=(
                      "--cpu 64 --env anymal_cmd_mj --training_on_hpc --add_terrain"
                      )
            
export SBATCH_ACCOUNT=OD-227199
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "12:00:00"
  # sbatch -A OD-227199 ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "12:00:00"
  # sbatch -A OD-219033 ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "12:00:00"
done