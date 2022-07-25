#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                        "orig"
                        "orig_frozen"
                        "best_emitter"
                        "best_emitter_frozen"
                        "ucb_test"
                        "ucb_test_frozen"
                        )
declare -a Arguments=(
                      "--cpu 16"
                      "--cpu 16 --frozen_walker"
                      "--cpu 16 --best_emitter"
                      "--cpu 16 --best_emitter --frozen_walker"
                      "--cpu 16 --ucb_test"
                      "--cpu 16 --ucb_test --frozen_walker"
                      )

for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro.sh "main_multiemitter_parallel.py" ${Experiments[$i]} "${Arguments[$i]}" "04:00:00"
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
