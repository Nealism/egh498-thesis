#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                        "terrain_first_disturb4"
                        "terrain_first_no_disturb4"
                        # "disturb4"
                        # "no_disturb4"
                        )
declare -a Arguments=(
                      "--cpu 64 --final_terrain_difficulty 0.4 --add_terrain --terrain_first --cur --apply_disturbances"
                      "--cpu 64 --final_terrain_difficulty 0.4 --add_terrain --terrain_first --cur"
                      # "--cpu 64 --final_terrain_difficulty 0.4 --add_terrain --cur --apply_disturbances"
                      # "--cpu 64 --final_terrain_difficulty 0.4 --add_terrain --cur"
                      )

for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "12:00:00"
done
