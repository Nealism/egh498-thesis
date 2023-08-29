#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      "s3/S40"
                      "s3/SE40"
                      "s3/SRE40"
                      "s3/SR40"
                      "s3/SRE40LN"
                      "s3/SR40LN"
                      "s3/S40LN"
                      "s3/SE40LN"
                      
                      

                        )
declare -a Arguments=(
    "--cpu 64 --env titan_pb_2 --training_on_hpc --epochs 5000 --max_ep_len 6000 --local_epoch_len 6000"
    "--cpu 64 --env titan_pb_2 --training_on_hpc --epochs 5000 --max_ep_len 6000 --local_epoch_len 6000 --expert_curr"
    "--cpu 64 --env titan_pb_2 --training_on_hpc --epochs 5000 --max_ep_len 6000 --local_epoch_len 6000 --expert_curr --region_curr"
    "--cpu 64 --env titan_pb_2 --training_on_hpc --epochs 5000 --max_ep_len 6000 --local_epoch_len 6000 --region_curr"
    "--cpu 64 --env titan_pb_2 --training_on_hpc --epochs 5000 --max_ep_len 6000 --local_epoch_len 6000 --expert_curr --region_curr --num_layers 3 --num_nodes 456"
    "--cpu 64 --env titan_pb_2 --training_on_hpc --epochs 5000 --max_ep_len 6000 --local_epoch_len 6000 --region_curr --num_layers 3 --num_nodes 456"
    "--cpu 64 --env titan_pb_2 --training_on_hpc --epochs 5000 --max_ep_len 6000 --local_epoch_len 6000 --num_layers 3 --num_nodes 456"
    "--cpu 64 --env titan_pb_2 --training_on_hpc --epochs 5000 --max_ep_len 6000 --local_epoch_len 6000 --expert_curr --num_layers 3 --num_nodes 456"
   

    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "48:00:00"
done