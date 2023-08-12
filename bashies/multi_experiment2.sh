#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      "e2/t1"
                      "e2/t1_cur"
                      "e2/ob1_1"
                      "e2/obs_cur"
                      "e2/ob1_1_3456"
                      "e2/obs_cur_3456"
                      

                        )
declare -a Arguments=(
    "--cpu 64 --env titan_pb_2 --training_on_hpc --epochs 5000 --max_ep_len 3048 --local_epoch_len 5048"
    "--cpu 64 --env titan_pb_2 --training_on_hpc --cur --epochs 5000 --max_ep_len 3048 --local_epoch_len 5048"
    "--cpu 64 --env titan_pb_2 --training_on_hpc --epochs 5000 --max_ep_len 6048 --local_epoch_len 10048 --obstacle_avoidance"
    "--cpu 64 --env titan_pb_2 --training_on_hpc --epochs 5000 --max_ep_len 6048 --local_epoch_len 10048 --obstacle_avoidance --cur"
    "--cpu 64 --env titan_pb_2 --training_on_hpc --epochs 5000 --max_ep_len 6048 --local_epoch_len 10048 --obstacle_avoidance --num_layers 3 --num_nodes 456"
    "--cpu 64 --env titan_pb_2 --training_on_hpc --epochs 5000 --max_ep_len 6048 --local_epoch_len 10048 --obstacle_avoidance --cur --num_layers 3 --num_nodes 456"
    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "48:00:00"
done