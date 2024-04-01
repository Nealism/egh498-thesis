#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      "ME65_5/r21MGE103"
                      "ME65_5/1r21MGE103"
                      "ME65_5/2r21MGE103"
                      "ME65_5/3r21MGE103"
                      "ME65_5/4r21MGE103"
                      "ME65_5/5r21MGE103"
                      "ME65_5/6r21MGE103"
                      "ME65_5/7r21MGE103"
                      "ME65_5/8r21MGE103"
                      "ME65_5/9r21MGE103"
                      "ME65_5/10r21MGE103"
                      "ME65_5/11r21MGE103"
                      "ME65_5/12r21MGE103"
                      "ME65_5/13r21MGE103"
                      "ME65_5/14r21MGE103"
                      "ME65_5/15r21MGE103"
                      
                      
                      
                      
                      # "ME65_4/16r21MGE103"
                      # "ME65_4/17r21MGE103"
                      # "ME65_4/18r21MGE103"

                      # "ME65_4/19r21MGE103"
                      # "ME65_4/20r21MGE103"
                      
                      # "ME65_4/21r21MGE103"
                      # "ME65_4/22r21MGE103"
                      # "ME65_4/23r21MGE103"
                      # "ME65_4/24r21MGE103"
                      # "ME65_4/25r21MGE103"
                      # "ME65_4/26r21MGE103"
                      # "ME65_4/27r21MGE103"
                      # "ME65_4/28r21MGE103"

                      # "ME65_4/29r21MGE103"
                      # "ME65_4/30r21MGE103"
                      # "ME61/r21MGE103"
                      # "ME61/r21MGE103"
                      # "ME61/r21MGE103"
                      # "ME61/r21MGE103"
                      # "ME61/r21MGE103"
                      # "ME61/r21MGE103"
                      # "ME61/r21MGE103"


                    


                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    
    
    
    
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"


    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    
    
    
    #_____________________________________________________________________________________________
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    



    

    
    
    
    

    
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "168:00:00"
done