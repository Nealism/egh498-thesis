#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      "e2/RG20"
                      "e2/RGE20"
                      "e2/RGRE20"
                      "e2/RGR20"
                      

                        )
declare -a Arguments=(
    "--cpu 64 --env titan_pb_2 --training_on_hpc --epochs 5000 --max_ep_len 3048 --local_epoch_len 5048"
    "--cpu 64 --env titan_pb_2 --training_on_hpc --cur --epochs 5000 --max_ep_len 3048 --local_epoch_len 5048 --just_expert"
    "--cpu 64 --env titan_pb_2 --training_on_hpc --epochs 5000 --max_ep_len 3048 --local_epoch_len 5048 --just_expert --region_curr"
    "--cpu 64 --env titan_pb_2 --training_on_hpc --cur --epochs 5000 --max_ep_len 3048 --local_epoch_len 5048 --region_curr"
    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "48:00:00"
done