#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      "s9/EC1R1"
                      "s9/EC1R2"
                      "s9/EC1R3"
                      "s9/EC1R4"
                      "s9/EC1R5"

                      "s9/C1R1"
                      "s9/C1R2"
                      "s9/C1R3"
                      "s9/C1R4"
                      "s9/C1R5"

                      "s9/EC2R1"
                      "s9/EC2R2"
                      "s9/EC2R3"
                      "s9/EC2R4"
                      "s9/EC2R5"

                      "s9/C2R1"
                      "s9/C2R2"
                      "s9/C2R3"
                      "s9/C2R4"
                      "s9/C2R5"

                      "s9/EC3R1"
                      "s9/EC3R2"
                      "s9/EC3R3"
                      "s9/EC3R4"
                      "s9/EC3R5"

                      "s9/C3R1"
                      "s9/C3R2"
                      "s9/C3R3"
                      "s9/C3R4"
                      "s9/C3R5"

                      "s9/EC4R1"
                      "s9/EC4R2"
                      "s9/EC4R3"
                      "s9/EC4R4"
                      "s9/EC4R5"

                      "s9/C4R1"
                      "s9/C4R2"
                      "s9/C4R3"
                      "s9/C4R4"
                      "s9/C4R5"

                      "s9/EC5R1"
                      "s9/EC5R2"
                      "s9/EC5R3"
                      "s9/EC5R4"
                      "s9/EC5R5"

                      "s9/C5R1"
                      "s9/C5R2"
                      "s9/C5R3"
                      "s9/C5R4"
                      "s9/C5R5"

                      "s9/EC6R1"
                      "s9/EC6R2"
                      "s9/EC6R3"
                      "s9/EC6R4"
                      "s9/EC6R5"

                      "s9/C6R1"
                      "s9/C6R2"
                      "s9/C6R3"
                      "s9/C6R4"
                      "s9/C6R5"
                      
                      
                      # "m1/m20"
                      # "m1/m20_3456"
                      # "m1/m20_4556"
                      # "m1/m20_5656"
                      # "m1/m20_6756"
                      
                      
                      
                      

                        )
declare -a Arguments=(
    "--cpu 64 --env multi_robot_pb --cur_succ 1 --return_fn 1 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --cur_succ 1 --return_fn 2 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --cur_succ 1 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --cur_succ 1 --return_fn 4 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --cur_succ 1 --return_fn 5 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
   

    

    "--cpu 64 --env multi_robot_pb --cur_succ 1 --return_fn 1 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --cur_succ 1 --return_fn 2 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --cur_succ 1 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --cur_succ 1 --return_fn 4 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --cur_succ 1 --return_fn 5 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
   


    "--cpu 64 --env multi_robot_pb --cur_succ 2 --return_fn 1 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --cur_succ 2 --return_fn 2 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --cur_succ 2 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --cur_succ 2 --return_fn 4 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --cur_succ 2 --return_fn 5 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"


    "--cpu 64 --env multi_robot_pb --cur_succ 2 --return_fn 1 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --cur_succ 2 --return_fn 2 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --cur_succ 2 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --cur_succ 2 --return_fn 4 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --cur_succ 2 --return_fn 5 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"

    "--cpu 64 --env multi_robot_pb --cur_succ 3 --return_fn 1 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --cur_succ 3 --return_fn 2 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --cur_succ 3 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --cur_succ 3 --return_fn 4 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --cur_succ 3 --return_fn 5 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"

    
    "--cpu 64 --env multi_robot_pb --cur_succ 3 --return_fn 1 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --cur_succ 3 --return_fn 2 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --cur_succ 3 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --cur_succ 3 --return_fn 4 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --cur_succ 3 --return_fn 5 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"

    "--cpu 64 --env multi_robot_pb --cur_succ 4 --return_fn 1 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --cur_succ 4 --return_fn 2 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --cur_succ 4 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --cur_succ 4 --return_fn 4 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --cur_succ 4 --return_fn 5 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"

    
    "--cpu 64 --env multi_robot_pb --cur_succ 4 --return_fn 1 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --cur_succ 4 --return_fn 2 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --cur_succ 4 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --cur_succ 4 --return_fn 4 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --cur_succ 4 --return_fn 5 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"

    "--cpu 64 --env multi_robot_pb --cur_succ 5 --return_fn 1 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --cur_succ 5 --return_fn 2 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --cur_succ 5 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --cur_succ 5 --return_fn 4 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --cur_succ 5 --return_fn 5 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"

    
    "--cpu 64 --env multi_robot_pb --cur_succ 5 --return_fn 1 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --cur_succ 5 --return_fn 2 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --cur_succ 5 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --cur_succ 5 --return_fn 4 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --cur_succ 5 --return_fn 5 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"

    "--cpu 64 --env multi_robot_pb --cur_succ 6 --return_fn 1 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --cur_succ 6 --return_fn 2 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --cur_succ 6 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --cur_succ 6 --return_fn 4 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --cur_succ 6 --return_fn 5 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"

    
    "--cpu 64 --env multi_robot_pb --cur_succ 6 --return_fn 1 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --cur_succ 6 --return_fn 2 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --cur_succ 6 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --cur_succ 6 --return_fn 4 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --cur_succ 6 --return_fn 5 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --training_on_hpc --epochs 5000 --max_ep_len 2040 --local_epoch_len 3048"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --training_on_hpc --epochs 5000 --max_ep_len 2048 --local_epoch_len 2048"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --training_on_hpc --epochs 5000 --max_ep_len 2048 --local_epoch_len 2048 --num_layers 4 --num_nodes 556"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --training_on_hpc --epochs 5000 --max_ep_len 2048 --local_epoch_len 2048 --num_layers 5 --num_nodes 656"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --training_on_hpc --epochs 5000 --max_ep_len 2048 --local_epoch_len 2048 --num_layers 6 --num_nodes 656"


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "48:00:00"
done