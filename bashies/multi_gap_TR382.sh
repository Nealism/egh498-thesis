#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      "ME83_3/r21MGE103"
                      "ME83_3/1r21MGE103"
                      "ME83_3/2r21MGE103"
                      "ME83_3/3r21MGE103"
                      "ME83_3/4r21MGE103"
                      "ME83_3/5r21MGE103"
                      "ME83_3/6r21MGE103"
                      "ME83_3/7r21MGE103"
                      "ME83_3/8r21MGE103"
                      "ME83_3/9r21MGE103"
                      "ME83_3/10r21MGE103"
                      "ME83_3/11r21MGE103"
                      "ME83_3/12r21MGE103"
                      "ME83_3/13r21MGE103"
                      "ME83_3/14r21MGE103"
                      "ME83_3/15r21MGE103"
                      # "ME83/16r21MGE103"
                      # "ME83/17r21MGE103"
                      # "ME83/18r21MGE103"

                      # "ME83/19r21MGE103"
                      # "ME83/20r21MGE103"
                      
                      # "ME83/21r21MGE103"
                      # "ME83/22r21MGE103"
                      # "ME83/23r21MGE103"
                      # "ME83/24r21MGE103"
                      # "ME83/25r21MGE103"
                      # "ME83/26r21MGE103"
                      # "ME83/27r21MGE103"
                      # "ME83/28r21MGE103"

                      # "ME83/29r21MGE103"
                      # "ME83/30r21MGE103"
                      # "ME61/r21MGE103"
                      # "ME61/r21MGE103"
                      # "ME61/r21MGE103"
                      # "ME61/r21MGE103"
                      # "ME61/r21MGE103"
                      # "ME61/r21MGE103"
                      # "ME61/r21MGE103"


                    


                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"
    
    
    
    
    
    
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"

    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"


    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"

    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"

    
    
    
    
    
    
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.3 --MA_bootstrap_extreme --experiment_3  --ray_wall_type 1 --randomness 2"
    



    

    
    
    
    

    
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "168:00:00"
done