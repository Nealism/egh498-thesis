#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      "ME109/r22MGE315"
                      "ME109/1r22MGE315"
                      "ME109/2r22MGE315"
                      "ME109/3r22MGE315"
                      "ME109/4r22MGE315"
                      "ME109/5r23MGE315"
                      "ME109/6r23MGE315"
                      "ME109/7r23MGE315"
                      "ME109/8r23MGE315"
                      "ME109/9r23MGE315"
                      "ME109/10r24MGE315"
                      "ME109/11r24MGE315"
                      "ME109/12r24MGE315"
                      "ME109/13r24MGE315"
                      "ME109/14r24MGE315"
                      "ME109/15r24MGE315"
                      
                      
                      
                      
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
    

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    
    
    
    
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1000 --local_epoch_len 200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1000 --local_epoch_len 200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"


    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    
    
    
    #_____________________________________________________________________________________________
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200 --expert_curr --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5 --MA_bootstrap --experiment_3  --ray_wall_type 1 --randomness 2"
    



    

    
    
    
    

    
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "168:00:00"
done