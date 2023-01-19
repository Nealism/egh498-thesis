#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                        "no_terrain"
                        "0.01_terrain"
                        )
declare -a Arguments=(
                      "--cpu 64 --env anymal_cmd_mj --training_on_hpc --epochs 4000"
                      "--cpu 64 --env anymal_cmd_mj --training_on_hpc --epochs 4000 --add_terrain --rand_dz_mult 0.01"
                      )
            
export SBATCH_ACCOUNT=OD-219033
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "36:00:00"
done