#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      "s3/O20"
                      "s3/OE20"
                      "s3/O20LN"
                      "s3/OE20LN"
                      
                      

                        )
declare -a Arguments=(
    "--cpu 64 --env titan_pb_2 --training_on_hpc --epochs 5000 --max_ep_len 10000 --local_epoch_len 10000 --obstacle_avoidance"
    "--cpu 64 --env titan_pb_2 --training_on_hpc --epochs 5000 --max_ep_len 10000 --local_epoch_len 10000 --obstacle_avoidance --expert_curr "
    "--cpu 64 --env titan_pb_2 --training_on_hpc --epochs 5000 --max_ep_len 10000 --local_epoch_len 10000 --obstacle_avoidance --num_layers 3 --num_nodes 456"
    "--cpu 64 --env titan_pb_2 --training_on_hpc --epochs 5000 --max_ep_len 10000 --local_epoch_len 10000 --obstacle_avoidance --expert_curr --num_layers 3 --num_nodes 456"
   

    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "48:00:00"
done