#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      "ME84_1/r21MGE103"
                      "ME84_1/1r21MGE103"
                      "ME84_1/2r21MGE103"
                      "ME84_1/3r21MGE103"
                      "ME84_1/4r21MGE103"
                      "ME84_1/5r21MGE103"
                      "ME84_1/6r21MGE103"
                      "ME84_1/7r21MGE103"
                      "ME84_1/8r21MGE103"
                      "ME84_1/9r21MGE103"
                      "ME84_1/10r21MGE103"
                      "ME84_1/11r21MGE103"
                      "ME84_1/12r21MGE103"
                      "ME84_1/13r21MGE103"
                      "ME84_1/14r21MGE103"
                      "ME84_1/15r21MGE103"
                      # "ME84/16r21MGE103"
                      # "ME84/17r21MGE103"
                      # "ME84/18r21MGE103"

                      # "ME84/19r21MGE103"
                      # "ME84/20r21MGE103"
                      
                      # "ME84/21r21MGE103"
                      # "ME84/22r21MGE103"
                      # "ME84/23r21MGE103"
                      # "ME84/24r21MGE103"
                      # "ME84/25r21MGE103"
                      # "ME84/26r21MGE103"
                      # "ME84/27r21MGE103"
                      # "ME84/28r21MGE103"

                      # "ME84/29r21MGE103"
                      # "ME84/30r21MGE103"
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
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2 --num_nodes 356"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2 --num_nodes 356"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2 --num_nodes 456"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2 --num_nodes 456"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2 --num_nodes 556"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2 --num_nodes 556"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2 --num_layers 3"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2 --num_layers 3"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2 --num_layers 3 --num_nodes 156"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2 --num_layers 3 --num_nodes 156"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2 --num_layers 3 --num_nodes 356"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2 --num_layers 3 --num_nodes 356"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2 --num_layers 3 --num_nodes 456"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2 --num_layers 3 --num_nodes 456"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 3 --final_gap_width 1.3 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2 --num_layers 4"
    
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