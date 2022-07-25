#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                        "orig"
                        )
declare -a Arguments=(
                      "--cpu 14"
                      )

for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_brace.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "12:00:00"
done

# # ==================================================================================
# # Experiment type
# # ==================================================================================
# Terrains=""
# declare -a Experiments=(
#                         "frozen"
#                         "not_frozen"
#                         )
# declare -a Arguments=(
#                       "--cpu 12 --frozen_walker"
#                       "--cpu 12"
#                       )

# for terrain in $Terrains; do 
#   for (( i=0; i<${#Arguments[@]}; i++ )); do 
#     sbatch ./base_csiro.sh "main_multiemitter.py" $terrain ${Experiments[$i]} "${Arguments[$i]}" "02:00:00"
#   done
# done
