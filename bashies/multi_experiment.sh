#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      "clip_r1_no_terrain"
                        )
declare -a Arguments=(
                      "--cpu 32 --env anymal_cmd_mj --training_on_hpc --epochs 2000 --reward 1 --clip"
                      )
            
export SBATCH_ACCOUNT=OD-219033
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "12:00:00"
done