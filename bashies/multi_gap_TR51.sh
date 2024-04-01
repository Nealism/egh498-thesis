#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      "ME71_2/r21MGE103"
                      "ME71_2/1r21MGE103"
                      "ME71_2/2r21MGE103"
                      "ME71_2/3r21MGE103"
                      "ME71_2/4r21MGE103"
                      "ME71_2/5r21MGE103"
                      "ME71_2/6r21MGE103"
                      "ME71_2/7r21MGE103"
                      "ME71_2/8r21MGE103"
                      "ME71_2/9r21MGE103"
                      "ME71_2/10r21MGE103"
                      "ME71_2/11r21MGE103"
                      "ME71_2/12r21MGE103"
                      "ME71_2/13r21MGE103"
                      "ME71_2/14r21MGE103"
                      "ME71_2/15r21MGE103"
                      
                      
                      
                      # "ME71_2/16r21MGE103"
                      # "ME71_1/17r21MGE103"
                      # "ME71_1/18r21MGE103"

                      # "ME71_1/19r21MGE103"
                      # "ME71_1/20r21MGE103"
                      
                      # "ME71_1/21r21MGE103"
                      # "ME71_1/22r21MGE103"
                      # "ME71_1/23r21MGE103"
                      # "ME71_1/24r21MGE103"
                      # "ME71_1/25r21MGE103"
                      # "ME71_1/26r21MGE103"
                      # "ME71_1/27r21MGE103"
                      # "ME71_1/28r21MGE103"

                      # "ME71_1/29r21MGE103"
                      # "ME71_1/30r21MGE103"
                      # "ME61/r21MGE103"
                      # "ME61/r21MGE103"
                      # "ME61/r21MGE103"
                      # "ME61/r21MGE103"
                      # "ME61/r21MGE103"
                      # "ME61/r21MGE103"
                      # "ME61/r21MGE103"


                    


                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"


    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"













    #________________________________________________________________________________

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0 --starting_gap_width 1.3 --final_gap_width 1.3  --experiment_3  --ray_wall_type 1 --randomness 2"
    



    

    
    
    
    

    
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "168:00:00"
done