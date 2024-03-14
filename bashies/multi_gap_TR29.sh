#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      "ME57/r13MGE102"
                      "ME57/r14MGE102"
                      "ME57/r15MGE102"
                      "ME57/r16MGE102"
                      "ME57/r17MGE102"
                      "ME57/r18MGE102"
                      "ME57/r19MGE102"
                      "ME57/r20MGE102"
                      "ME57/r21MGE102"
                      "ME57/r22MGE102"
                      "ME57/r23MGE102"
                      "ME57/r24MGE102"
                      "ME57/r25MGE102"
                      "ME57/r26MGE102"
                      "ME57/r27MGE102"
                      "ME57/r28MGE102"
                      "ME57/r29MGE102"
                      "ME57/r30MGE102"

                      "ME57/r31MGE102"
                      "ME57/r32MGE102"
                      "ME57/r33MGE102"
                      # "ME57/r40MGE102"
                      # "ME57/r35MGE102"
                      # "ME57/r36MGE102"
                      # "ME57/r37MGE102"
                      # "ME57/r38MGE102"
                      # "ME57/r39MGE102"
                      # "ME57/r40MGE102"


                    


                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 2 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 14 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 2 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 15 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 2 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 16 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 2 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 17 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 2 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 18 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 2 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 19 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 2 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 20 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 2 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 2 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 2 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 2 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 2 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 2 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 2 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 2 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 2 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 2 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 2 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 2 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 2 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 33 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 2 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 40 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 2 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 35 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 2 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 36 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 2 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 37 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 2 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 38 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 2 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 39 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 2 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 40 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 2 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"
    



    

    
    
    
    

    
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "96:00:00"
done