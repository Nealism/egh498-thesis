#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      "ME82_2/r21MGE103"
                      "ME82_2/1r21MGE103"
                      "ME82_2/2r21MGE103"
                      "ME82_2/3r21MGE103"
                      "ME82_2/4r21MGE103"
                      "ME82_2/5r21MGE103"
                      "ME82_2/6r21MGE103"
                      "ME82_2/7r21MGE103"
                      "ME82_2/8r21MGE103"
                      "ME82_2/9r21MGE103"
                      "ME82_2/10r21MGE103"
                      "ME82_2/11r21MGE103"
                      "ME82_2/12r21MGE103"
                      "ME82_2/13r21MGE103"
                      "ME82_2/14r21MGE103"
                      "ME82_2/15r21MGE103"
                      
                      
                      
                      # "ME82/16r21MGE103"
                      # "ME82/17r21MGE103"
                      # "ME82/18r21MGE103"

                      # "ME82/19r21MGE103"
                      # "ME82/20r21MGE103"
                      
                      # "ME82/21r21MGE103"
                      # "ME82/22r21MGE103"
                      # "ME82/23r21MGE103"
                      # "ME82/24r21MGE103"
                      # "ME82/25r21MGE103"
                      # "ME82/26r21MGE103"
                      # "ME82/27r21MGE103"
                      # "ME82/28r21MGE103"

                      # "ME82/29r21MGE103"
                      # "ME82/30r21MGE103"
                      # "ME61/r21MGE103"
                      # "ME61/r21MGE103"
                      # "ME61/r21MGE103"
                      # "ME61/r21MGE103"
                      # "ME61/r21MGE103"
                      # "ME61/r21MGE103"
                      # "ME61/r21MGE103"


                    


                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    
    
    
    
    
    
    
    
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"


    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"






















    #_______________________________________________________________________________________

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    



    

    
    
    
    

    
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "168:00:00"
done