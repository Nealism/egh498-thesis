#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      "sg1/r26EGC7"
                      "sg1/r27EGC7"
                      "sg1/r28EGC6"
                      "sg1/r29EGC6"
                      "sg1/r30EGC6"
                      "sg1/r31EGC9"
                      "sg1/r32EGC9"
                      "sg1/r33EGC9"
                      "sg1/r34EGC6"
                      "sg1/r35EGC9"
                      
                      "sg1/r26C7E"
                      "sg1/r27C7E"
                      "sg1/r28C6E"
                      "sg1/r29C6E"
                      "sg1/r30C6E"
                      "sg1/r31C9E"
                      "sg1/r32C9E"
                      "sg1/r33C9E"
                      "sg1/r34C6E"
                      "sg1/r35C9E"
                      
                      "sg1/r26C7"
                      "sg1/r27C7"
                      "sg1/r28C6"
                      "sg1/r29C6"
                      "sg1/r30C6"
                      "sg1/r31C9"
                      "sg1/r32C9"
                      "sg1/r33C9"
                      "sg1/r34C6"
                      "sg1/r35C9"
                      # "s12/r6C3E"
                      # "s12/r7C3E"
                      # "s12/r8C3E"
                      # "s12/r9C3E"
                      # "s12/r10C3E"
                      # "s12/r11C3E"
                      # "s12/r12C3E"
                      # "s12/r13C3E"
                      # "s12/r14C3E"
                      # "s12/r15C6E"

          

                      # "s12/r16C7E"
                      # "s12/r17C7E"
                      # "s12/r18C7E"
                      # "s12/r19C5E"
                      # "s12/r20C5E"
                      # "s12/r21C3E"
                      # "s12/r22C3E"
                      # "s12/r23C4E"
                      # "s12/r24C8E"
                      # "s12/r25C7E"

      
                      
                      # "m1/m20"
                      # "m1/m20_3456"
                      # "m1/m20_4556"
                      # "m1/m20_5656"
                      # "m1/m20_6756"
                      
                      
                      
                      

                        )
declare -a Arguments=(
    
    "--cpu 64 --env multi_robot_pb --reward_fn 26 --cur_succ 7 --return_fn 3 --training_on_hpc --gap_avoidance --epochs 7000 --max_ep_len 2150 --local_epoch_len 4500 --expert_curr --gap_curr"
    "--cpu 64 --env multi_robot_pb --reward_fn 27 --cur_succ 7 --return_fn 3 --training_on_hpc --gap_avoidance --epochs 7000 --max_ep_len 2150 --local_epoch_len 4500 --expert_curr --gap_curr"
    "--cpu 64 --env multi_robot_pb --reward_fn 28 --cur_succ 6 --return_fn 3 --training_on_hpc --gap_avoidance --epochs 7000 --max_ep_len 2150 --local_epoch_len 4500 --expert_curr --gap_curr"
    "--cpu 64 --env multi_robot_pb --reward_fn 29 --cur_succ 6 --return_fn 3 --training_on_hpc --gap_avoidance --epochs 7000 --max_ep_len 2150 --local_epoch_len 4500 --expert_curr --gap_curr"
    "--cpu 64 --env multi_robot_pb --reward_fn 30 --cur_succ 6 --return_fn 3 --training_on_hpc --gap_avoidance --epochs 7000 --max_ep_len 2150 --local_epoch_len 4500 --expert_curr --gap_curr"
    "--cpu 64 --env multi_robot_pb --reward_fn 31 --cur_succ 9 --return_fn 3 --training_on_hpc --gap_avoidance --epochs 7000 --max_ep_len 2150 --local_epoch_len 4500 --expert_curr --gap_curr"
    "--cpu 64 --env multi_robot_pb --reward_fn 32 --cur_succ 9 --return_fn 3 --training_on_hpc --gap_avoidance --epochs 7000 --max_ep_len 2150 --local_epoch_len 4500 --expert_curr --gap_curr"
    "--cpu 64 --env multi_robot_pb --reward_fn 33 --cur_succ 9 --return_fn 3 --training_on_hpc --gap_avoidance --epochs 7000 --max_ep_len 2150 --local_epoch_len 4500 --expert_curr --gap_curr"
    "--cpu 64 --env multi_robot_pb --reward_fn 34 --cur_succ 9 --return_fn 3 --training_on_hpc --gap_avoidance --epochs 7000 --max_ep_len 2150 --local_epoch_len 4500 --expert_curr --gap_curr"
    "--cpu 64 --env multi_robot_pb --reward_fn 35 --cur_succ 9 --return_fn 3 --training_on_hpc --gap_avoidance --epochs 7000 --max_ep_len 2150 --local_epoch_len 4500 --expert_curr --gap_curr"


    "--cpu 64 --env multi_robot_pb --reward_fn 26 --cur_succ 7 --return_fn 3 --training_on_hpc --gap_avoidance --epochs 7000 --max_ep_len 2150 --local_epoch_len 4500 --expert_curr"
    "--cpu 64 --env multi_robot_pb --reward_fn 27 --cur_succ 7 --return_fn 3 --training_on_hpc --gap_avoidance --epochs 7000 --max_ep_len 2150 --local_epoch_len 4500 --expert_curr"
    "--cpu 64 --env multi_robot_pb --reward_fn 28 --cur_succ 6 --return_fn 3 --training_on_hpc --gap_avoidance --epochs 7000 --max_ep_len 2150 --local_epoch_len 4500 --expert_curr"
    "--cpu 64 --env multi_robot_pb --reward_fn 29 --cur_succ 6 --return_fn 3 --training_on_hpc --gap_avoidance --epochs 7000 --max_ep_len 2150 --local_epoch_len 4500 --expert_curr"
    "--cpu 64 --env multi_robot_pb --reward_fn 30 --cur_succ 6 --return_fn 3 --training_on_hpc --gap_avoidance --epochs 7000 --max_ep_len 2150 --local_epoch_len 4500 --expert_curr"
    "--cpu 64 --env multi_robot_pb --reward_fn 31 --cur_succ 9 --return_fn 3 --training_on_hpc --gap_avoidance --epochs 7000 --max_ep_len 2150 --local_epoch_len 4500 --expert_curr"
    "--cpu 64 --env multi_robot_pb --reward_fn 32 --cur_succ 9 --return_fn 3 --training_on_hpc --gap_avoidance --epochs 7000 --max_ep_len 2150 --local_epoch_len 4500 --expert_curr"
    "--cpu 64 --env multi_robot_pb --reward_fn 33 --cur_succ 9 --return_fn 3 --training_on_hpc --gap_avoidance --epochs 7000 --max_ep_len 2150 --local_epoch_len 4500 --expert_curr"
    "--cpu 64 --env multi_robot_pb --reward_fn 34 --cur_succ 9 --return_fn 3 --training_on_hpc --gap_avoidance --epochs 7000 --max_ep_len 2150 --local_epoch_len 4500 --expert_curr"
    "--cpu 64 --env multi_robot_pb --reward_fn 35 --cur_succ 9 --return_fn 3 --training_on_hpc --gap_avoidance --epochs 7000 --max_ep_len 2150 --local_epoch_len 4500 --expert_curr"

    "--cpu 64 --env multi_robot_pb --reward_fn 26 --cur_succ 7 --return_fn 3 --training_on_hpc --gap_avoidance --epochs 7000 --max_ep_len 2150 --local_epoch_len 4500"
    "--cpu 64 --env multi_robot_pb --reward_fn 27 --cur_succ 7 --return_fn 3 --training_on_hpc --gap_avoidance --epochs 7000 --max_ep_len 2150 --local_epoch_len 4500"
    "--cpu 64 --env multi_robot_pb --reward_fn 28 --cur_succ 6 --return_fn 3 --training_on_hpc --gap_avoidance --epochs 7000 --max_ep_len 2150 --local_epoch_len 4500"
    "--cpu 64 --env multi_robot_pb --reward_fn 29 --cur_succ 6 --return_fn 3 --training_on_hpc --gap_avoidance --epochs 7000 --max_ep_len 2150 --local_epoch_len 4500"
    "--cpu 64 --env multi_robot_pb --reward_fn 30 --cur_succ 6 --return_fn 3 --training_on_hpc --gap_avoidance --epochs 7000 --max_ep_len 2150 --local_epoch_len 4500"
    "--cpu 64 --env multi_robot_pb --reward_fn 31 --cur_succ 9 --return_fn 3 --training_on_hpc --gap_avoidance --epochs 7000 --max_ep_len 2150 --local_epoch_len 4500"
    "--cpu 64 --env multi_robot_pb --reward_fn 32 --cur_succ 9 --return_fn 3 --training_on_hpc --gap_avoidance --epochs 7000 --max_ep_len 2150 --local_epoch_len 4500"
    "--cpu 64 --env multi_robot_pb --reward_fn 33 --cur_succ 9 --return_fn 3 --training_on_hpc --gap_avoidance --epochs 7000 --max_ep_len 2150 --local_epoch_len 4500"
    "--cpu 64 --env multi_robot_pb --reward_fn 34 --cur_succ 9 --return_fn 3 --training_on_hpc --gap_avoidance --epochs 7000 --max_ep_len 2150 --local_epoch_len 4500"
    "--cpu 64 --env multi_robot_pb --reward_fn 35 --cur_succ 9 --return_fn 3 --training_on_hpc --gap_avoidance --epochs 7000 --max_ep_len 2150 --local_epoch_len 4500"

    # "--cpu 64 --env multi_robot_pb --reward_fn 6 --cur_succ 3 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr"
    # "--cpu 64 --env multi_robot_pb --reward_fn 7 --cur_succ 3 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr"
    # "--cpu 64 --env multi_robot_pb --reward_fn 8 --cur_succ 3 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr"
    # "--cpu 64 --env multi_robot_pb --reward_fn 9 --cur_succ 3 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr"
    # "--cpu 64 --env multi_robot_pb --reward_fn 10 --cur_succ 3 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr"
    # "--cpu 64 --env multi_robot_pb --reward_fn 11 --cur_succ 3 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr"
    # "--cpu 64 --env multi_robot_pb --reward_fn 12 --cur_succ 3 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr"
    # "--cpu 64 --env multi_robot_pb --reward_fn 13 --cur_succ 3 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr"
    # "--cpu 64 --env multi_robot_pb --reward_fn 14 --cur_succ 3 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr"
    # "--cpu 64 --env multi_robot_pb --reward_fn 15 --cur_succ 6 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr"

    # "--cpu 64 --env multi_robot_pb --reward_fn 16 --cur_succ 7 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr"
    # "--cpu 64 --env multi_robot_pb --reward_fn 17 --cur_succ 7 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr"
    # "--cpu 64 --env multi_robot_pb --reward_fn 18 --cur_succ 7 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr"
    # "--cpu 64 --env multi_robot_pb --reward_fn 19 --cur_succ 5 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr"
    # "--cpu 64 --env multi_robot_pb --reward_fn 20 --cur_succ 5 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr"
    # "--cpu 64 --env multi_robot_pb --reward_fn 21 --cur_succ 3 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr"
    # "--cpu 64 --env multi_robot_pb --reward_fn 22 --cur_succ 3 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr"
    # "--cpu 64 --env multi_robot_pb --reward_fn 23 --cur_succ 4 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr"
    # "--cpu 64 --env multi_robot_pb --reward_fn 24 --cur_succ 8 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr"
    # "--cpu 64 --env multi_robot_pb --reward_fn 25 --cur_succ 7 --return_fn 3 --training_on_hpc --obstacle_avoidance --epochs 5000 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr"
    
    
    
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "48:00:00"
done