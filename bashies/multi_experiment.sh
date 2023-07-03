#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      "exp2/titan"
                      "exp2/titan_cur"

                        )
declare -a Arguments=(
    "--cpu 64 --env titan_pb_2 --training_on_hpc --epochs 5000 --max_ep_len 2048 --local_epoch_len 2048"
    "--cpu 64 --env titan_pb_2 --training_on_hpc --cur --epochs 5000 --max_ep_len 2048 --local_epoch_len 2048"
)
            
export SBATCH_ACCOUNT=OD-219033
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "10:00:00"
done