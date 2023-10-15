#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      "mO6/2E"
                      "mO6/2E_3456"
                      "mO6/2E_4556"
                      "mO6/2E_5656"
                      "mO6/2E_6756"

                      "mO6/3E"
                      "mO6/3E_3456"
                      "mO6/3E_4556"
                      "mO6/3E_5656"
                      "mO6/3E_6756"
                      
                      "mO6/2"
                      "mO6/2_3456"
                      "mO6/2_4556"
                      "mO6/2_5656"
                      "mO6/2_6756"

                      "mO6/3"
                      "mO6/3_3456"
                      "mO6/3_4556"
                      "mO6/3_5656"
                      "mO6/3_6756"
                      
                      # "m1/m20"
                      # "m1/m20_3456"
                      # "m1/m20_4556"
                      # "m1/m20_5656"
                      # "m1/m20_6756"
                      
                      
                      
                      

                        )
declare -a Arguments=(
    "--cpu 64 --env multi_robot_pb --num_robots 2 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 3048 --local_epoch_len 3048 --expert_curr"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 3048 --local_epoch_len 3048 --expert_curr --num_layers 3 --num_nodes 456"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 3048 --local_epoch_len 3048 --expert_curr --num_layers 4 --num_nodes 556"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 3048 --local_epoch_len 3048 --expert_curr --num_layers 5 --num_nodes 656"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 3048 --local_epoch_len 3048 --expert_curr --num_layers 6 --num_nodes 656"
   

    "--cpu 64 --env multi_robot_pb --num_robots 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 3048 --local_epoch_len 3048 --expert_curr"
    "--cpu 64 --env multi_robot_pb --num_robots 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 3048 --local_epoch_len 3048 --expert_curr --num_layers 3 --num_nodes 456"
    "--cpu 64 --env multi_robot_pb --num_robots 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 3048 --local_epoch_len 3048 --expert_curr --num_layers 4 --num_nodes 556"
    "--cpu 64 --env multi_robot_pb --num_robots 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 3048 --local_epoch_len 3048 --expert_curr --num_layers 5 --num_nodes 656"
    "--cpu 64 --env multi_robot_pb --num_robots 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 3048 --local_epoch_len 3048 --expert_curr --num_layers 6 --num_nodes 656"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 3048 --local_epoch_len 3048"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 3048 --local_epoch_len 3048 --num_layers 3 --num_nodes 456"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 3048 --local_epoch_len 3048 --num_layers 4 --num_nodes 556"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 3048 --local_epoch_len 3048 --num_layers 5 --num_nodes 656"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 3048 --local_epoch_len 3048 --num_layers 6 --num_nodes 656"
   

    "--cpu 64 --env multi_robot_pb --num_robots 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 3048 --local_epoch_len 3048"
    "--cpu 64 --env multi_robot_pb --num_robots 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 3048 --local_epoch_len 3048 --num_layers 3 --num_nodes 456"
    "--cpu 64 --env multi_robot_pb --num_robots 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 3048 --local_epoch_len 3048 --num_layers 4 --num_nodes 556"
    "--cpu 64 --env multi_robot_pb --num_robots 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 3048 --local_epoch_len 3048 --num_layers 5 --num_nodes 656"
    "--cpu 64 --env multi_robot_pb --num_robots 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 3048 --local_epoch_len 3048 --num_layers 6 --num_nodes 656"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --training_on_hpc --epochs 5000 --max_ep_len 2040 --local_epoch_len 3048"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --training_on_hpc --epochs 5000 --max_ep_len 2048 --local_epoch_len 2048 --num_layers 3 --num_nodes 456"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --training_on_hpc --epochs 5000 --max_ep_len 2048 --local_epoch_len 2048 --num_layers 4 --num_nodes 556"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --training_on_hpc --epochs 5000 --max_ep_len 2048 --local_epoch_len 2048 --num_layers 5 --num_nodes 656"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --training_on_hpc --epochs 5000 --max_ep_len 2048 --local_epoch_len 2048 --num_layers 6 --num_nodes 656"


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "48:00:00"
done