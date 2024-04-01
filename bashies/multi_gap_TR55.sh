#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      "ME75/r21MGE103"
                      "ME75/1r21MGE103"
                      "ME75/2r21MGE103"
                      "ME75/3r21MGE103"
                      "ME75/4r21MGE103"
                      "ME75/5r21MGE103"
                      "ME75/6r21MGE103"
                      "ME75/7r21MGE103"
                      "ME75/8r21MGE103"
                      "ME75/9r21MGE103"
                      "ME75/10r21MGE103"
                      "ME75/11r21MGE103"
                      "ME75/12r21MGE103"
                      "ME75/13r21MGE103"
                      "ME75/14r21MGE103"
                      "ME75/15r21MGE103"
                      "ME75/16r21MGE103"
                      "ME75/17r21MGE103"
                      "ME75/18r21MGE103"

                      "ME75/19r21MGE103"
                      "ME75/20r21MGE103"
                      
                      "ME75/21r21MGE103"
                      "ME75/22r21MGE103"
                      "ME75/23r21MGE103"
                      "ME75/24r21MGE103"
                      "ME75/25r21MGE103"
                      "ME75/26r21MGE103"
                      "ME75/27r21MGE103"
                      "ME75/28r21MGE103"

                      "ME75/29r21MGE103"
                      "ME75/30r21MGE103"
                      # "ME61/r21MGE103"
                      # "ME61/r21MGE103"
                      # "ME61/r21MGE103"
                      # "ME61/r21MGE103"
                      # "ME61/r21MGE103"
                      # "ME61/r21MGE103"
                      # "ME61/r21MGE103"


                    


                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"


    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 10 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"
    



    

    
    
    
    

    
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "168:00:00"
done