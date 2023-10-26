#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      "s10/EC1r1R3"
                      "s10/EC1r2R3"
                      "s10/EC1r3R3"
                      "s10/EC1r4R3"
                      "s10/EC1r5R3"

                      "s10/C1r1R3"
                      "s10/C1r2R3"
                      "s10/C1r3R3"
                      "s10/C1r4R3"
                      "s10/C1r5R3"

                      "s10/EC3r1R3"
                      "s10/EC3r2R3"
                      "s10/EC3r3R3"
                      "s10/EC3r4R3"
                      "s10/EC3r5R3"

                      "s10/C3r1R3"
                      "s10/C3r2R3"
                      "s10/C3r3R3"
                      "s10/C3r4R3"
                      "s10/C3r5R3"
                      
                      
                      # "m1/m20"
                      # "m1/m20_3456"
                      # "m1/m20_4556"
                      # "m1/m20_5656"
                      # "m1/m20_6756"
                      
                      
                      
                      

                        )
declare -a Arguments=(
    
    "--cpu 64 --env multi_robot_pb --reward_fn 1 --cur_succ 1 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --reward_fn 2 --cur_succ 1 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --reward_fn 3 --cur_succ 1 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --reward_fn 4 --cur_succ 1 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --reward_fn 5 --cur_succ 1 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    
    "--cpu 64 --env multi_robot_pb --reward_fn 1 --cur_succ 1 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --reward_fn 2 --cur_succ 1 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --reward_fn 3 --cur_succ 1 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --reward_fn 4 --cur_succ 1 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --reward_fn 5 --cur_succ 1 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    
    
    "--cpu 64 --env multi_robot_pb --reward_fn 1 --cur_succ 3 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --reward_fn 2 --cur_succ 3 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --reward_fn 3 --cur_succ 3 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --reward_fn 4 --cur_succ 3 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    "--cpu 64 --env multi_robot_pb --reward_fn 5 --cur_succ 3 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000 --expert_curr"
    
    "--cpu 64 --env multi_robot_pb --reward_fn 1 --cur_succ 3 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --reward_fn 2 --cur_succ 3 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --reward_fn 3 --cur_succ 3 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --reward_fn 4 --cur_succ 3 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    "--cpu 64 --env multi_robot_pb --reward_fn 5 --cur_succ 3 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 5000 --local_epoch_len 5000"
    
   


    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "48:00:00"
done