#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      "e5/pb3_t1"
                      "e5/pb3_t1_cur"
                      "e5/pb3_t2"
                      "e5/pb3_t2_cur"
                      "e5/pb3_3356"
                      "e5/pb3_3356_cur"
                      "e5/t2_4456"
                      "e5/t2_4456_cur"
                      "e5/t2_3456"
                      "e5/t2_3456_cur"
                      "e5/t2_3356"
                      "e5/t2_3356_cur"
                      "e5/pb2_cur"
                      "e5/pb4_R2"
                      "e5/pb4_4450"

                        )
declare -a Arguments=(
    "--cpu 64 --env titan_pb_3 --training_on_hpc --epochs 5000 --max_ep_len 2048 --local_epoch_len 2048"
    "--cpu 64 --env titan_pb_3 --training_on_hpc --cur --epochs 5000 --max_ep_len 2048 --local_epoch_len 2048"
    "--cpu 64 --env titan_pb_3 --training_on_hpc --epochs 5000 --max_ep_len 2048 --local_epoch_len 2048 --num_robots 2"
    "--cpu 64 --env titan_pb_3 --training_on_hpc --epochs 5000 --max_ep_len 2048 --local_epoch_len 2048 --num_robots 2 --cur"
    "--cpu 64 --env titan_pb_3 --training_on_hpc --epochs 5000 --max_ep_len 2048 --local_epoch_len 2048 --num_robots 2 --num_layers 3 --num_nodes 356"
    "--cpu 64 --env titan_pb_3 --training_on_hpc --epochs 5000 --max_ep_len 2048 --local_epoch_len 2048 --num_robots 2 --cur --num_layers 3 --num_nodes 356"
    "--cpu 64 --env titan_pb_2 --training_on_hpc --epochs 5000 --max_ep_len 2048 --local_epoch_len 2048 --num_robots 2 --num_nodes 456 --num_layers 4"
    "--cpu 64 --env titan_pb_1 --training_on_hpc --epochs 5000 --max_ep_len 2048 --local_epoch_len 2048 --num_robots 2 --cur --num_nodes 456 --num_layers 4"
    "--cpu 64 --env titan_pb_2 --training_on_hpc --epochs 5000 --max_ep_len 2048 --local_epoch_len 2048 --num_robots 2 --num_layers 3 --num_nodes 456"
    "--cpu 64 --env titan_pb_1 --training_on_hpc --epochs 5000 --max_ep_len 2048 --local_epoch_len 2048 --num_robots 2 --cur --num_layers 3 --num_nodes 456"
    "--cpu 64 --env titan_pb_2 --training_on_hpc --epochs 5000 --max_ep_len 2048 --local_epoch_len 2048 --num_robots 2 --num_layers 3 --num_nodes 356"
    "--cpu 64 --env titan_pb_1 --training_on_hpc --epochs 5000 --max_ep_len 2048 --local_epoch_len 2048 --num_robots 2 --cur --num_layers 3 --num_nodes 356"
    "--cpu 64 --env titan_pb_2 --training_on_hpc --epochs 5000 --max_ep_len 2048 --local_epoch_len 2048 --num_robots 2 --num_layers 3 --num_nodes 356 --cur"
    "--cpu 64 --env titan_pb_4 --training_on_hpc --epochs 5000 --max_ep_len 2048 --local_epoch_len 2048 --num_robots 2 --num_layers 3 --num_nodes 356 --reward_fn 2"
    "--cpu 64 --env titan_pb_4 --training_on_hpc --epochs 5000 --max_ep_len 2048 --local_epoch_len 2048 --num_robots 2 --num_layers 4 --num_nodes 450 --reward_fn 2"
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "48:00:00"
done