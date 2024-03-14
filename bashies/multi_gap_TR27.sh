#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      "ME55/r13MGE1.3"
                      "ME55/r14MGE1.3"
                      "ME55/r15MGE1.3"
                      "ME55/r16MGE1.3"
                      "ME55/r17MGE1.3"
                      "ME55/r18MGE1.3"
                      "ME55/r19MGE1.3"
                      "ME55/r20MGE1.3"
                      "ME55/r21MGE1.3"
                      "ME55/r24MGE1.3"
                      "ME55/r23MGE1.3"
                      "ME55/r24MGE1.3"
                      "ME55/r25MGE1.3"
                      "ME55/r26MGE1.3"
                      "ME55/r27MGE1.3"
                      "ME55/r28MGE1.3"
                      "ME55/r29MGE1.3"
                      "ME55/r30MGE1.3"

                      "ME55/r31MGE1.3"
                      "ME55/r32MGE1.3"
                      "ME55/r33MGE1.3"
                      # "ME55/r40MGE1.3"
                      # "ME55/r35MGE1.3"
                      # "ME55/r36MGE1.3"
                      # "ME55/r37MGE1.3"
                      # "ME55/r38MGE1.3"
                      # "ME55/r39MGE1.3"
                      # "ME55/r40MGE1.3"


                    


                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 14 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 15 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 16 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 17 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 18 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 19 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 20 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 33 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 40 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 35 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 36 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 37 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 38 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 39 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 40 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 1"
    



    

    
    
    
    

    
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "96:00:00"
done