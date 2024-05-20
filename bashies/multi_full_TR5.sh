#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      

                      # "ME35/r21TG1O"
                      # "ME35/r21TG1O"
                      # "ME35/r21TG1O"

                      # "ME35/r21TG1O"
                      # "ME35/r21TG1O"
                      # "ME35/r21TG1O"
                      # "ME35/r21TG1O"


                      # "ME35/r21TG1.5N"
                      # "ME35/r21TG1.3N"
                      # "ME35/r21TG1.3N"

                      # "ME35/r21TG1.3N"
                      # "ME35/r21TG1.3N"
                      # "ME35/r21TG1.3N"
                      # "ME35/r21TG1.3N"

                      # "ME35/r21TG1.3N"
                      # "ME35/r21TG1.3N"

                      "ME132/0r26G1E1"
                      "ME132/1r26G1E1"
                      "ME132/2r26G1E1"
                      "ME132/3r26G1E1"
                      "ME132/4r26G1E1"
                      
                      
                      "ME132/5r26G1E3"
                      "ME132/6r26G1E3"
                      "ME132/7r26G1E3"
                      "ME132/8r26G1E3"
                      "ME132/9r26G1E3"
                      
                      "ME132/10r27G1E1"
                      "ME132/11r27G1E1"
                      "ME132/12r27G1E1"
                      "ME132/13r27G1E1"
                      "ME132/14r27G1E1"
                      
                      "ME132/15r27G1E3"
                      "ME132/16r27G1E3"
                      "ME132/17r27G1E3"
                      "ME132/18r27G1E3"
                      "ME132/19r27G1E3"


                      "ME132/20r28G1E1"
                      "ME132/21r28G1E1"
                      "ME132/22r28G1E1"
                      "ME132/23r28G1E1"
                      "ME132/24r28G1E1"
                      
                      
                      "ME132/25r28G1E3"
                      "ME132/26r28G1E3"
                      "ME132/27r28G1E3"
                      "ME132/28r28G1E3"
                      "ME132/29r28G1E3"
                      
                      "ME132/30r29G1E1"
                      "ME132/31r29G1E1"
                      "ME132/32r29G1E1"
                      "ME132/33r29G1E1"
                      "ME132/34r29G1E1"
                      
                      "ME132/35r29G1E3"
                      "ME132/36r29G1E3"
                      "ME132/37r29G1E3"
                      "ME132/38r29G1E3"
                      "ME132/39r29G1E3"


                      "ME132/39r29G0.85E3"
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      # "ME66_4/16r21G1.5N"
                      # "ME66_4/17r21G1.5N"

                      # "ME66_4/18r21G1.5N"
                      # "ME66_4/19r21G1.5N"
                      # "ME66_4/20r21G1.5N"


                      # "ME66_4/21r21TG1.5N"
                      # "ME66_4/22r21TG1.5N"
                      # "ME66_4/23r21TG1.5N"
                      # "ME66_4/24r21TG1.5N"
                      # "ME66_4/25r21TG1.5N"
                      # "ME66_4/26r21TG1.5N"
                      # "ME66_4/27r21TG1.5N"

                      # "ME66_4/28r21TG1.5N"
                      # "ME66_4/29r21TG1.5N"
                      # "ME66_4/30r21TG1.5N"
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    
 
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_1  --ray_wall_type 1 --randomness 2"
    
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    





    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"



    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_1  --ray_wall_type 1 --randomness 2"
    
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    





    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    
    
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 0.85  --experiment_3  --ray_wall_type 1 --randomness 2"


    
    
    
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3.5 --final_gap_width 1.5  _3  --ray_wa1l_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  _3  --ray_wa1l_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  _3  --ray_wa1l_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  _3  --ray_wa1l_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  _3  --ray_wa1l_type 1 --randomness 2"



    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  _3  --ray_wa1l_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  _3  --ray_wa1l_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  _3  --ray_wa1l_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  _3  --ray_wa1l_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  _3  --ray_wa1l_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  _3  --ray_wa1l_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  _3  --ray_wa1l_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  _3  --ray_wa1l_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  _3  --ray_wa1l_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  _3  --ray_wa1l_type 1 --randomness 2"
    
    
    

    
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "120:00:00"
done