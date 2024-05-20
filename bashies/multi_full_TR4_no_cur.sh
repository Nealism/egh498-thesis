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

                      "ME131/0r26G1NE1"
                      "ME131/1r26G1NE1"
                      "ME131/2r26G1NE1"
                      "ME131/3r26G1NE1"
                      "ME131/4r26G1NE1"
                      
                      
                      "ME131/5r26G1NE3"
                      "ME131/6r26G1NE3"
                      "ME131/7r26G1NE3"
                      "ME131/8r26G1NE3"
                      "ME131/9r26G1NE3"
                      
                      "ME131/10r27G1NE1"
                      "ME131/11r27G1NE1"
                      "ME131/12r27G1NE1"
                      "ME131/13r27G1NE1"
                      "ME131/14r27G1NE1"
                      
                      "ME131/15r27G1NE3"
                      "ME131/16r27G1NE3"
                      "ME131/17r27G1NE3"
                      "ME131/18r27G1NE3"
                      "ME131/19r27G1NE3"


                      "ME131/20r28G1NE1"
                      "ME131/21r28G1NE1"
                      "ME131/22r28G1NE1"
                      "ME131/23r28G1NE1"
                      "ME131/24r28G1NE1"
                      
                      
                      "ME131/25r28G1NE3"
                      "ME131/26r28G1NE3"
                      "ME131/27r28G1NE3"
                      "ME131/28r28G1NE3"
                      "ME131/29r28G1NE3"
                      
                      "ME131/30r29G1NE1"
                      "ME131/31r29G1NE1"
                      "ME131/32r29G1NE1"
                      "ME131/33r29G1NE1"
                      "ME131/34r29G1NE1"
                      
                      "ME131/35r29G1NE3"
                      "ME131/36r29G1NE3"
                      "ME131/37r29G1NE3"
                      "ME131/38r29G1NE3"
                      "ME131/39r29G1NE3"
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
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
    
   
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1   --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1   --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1   --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1   --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1   --experiment_1  --ray_wall_type 1 --randomness 2"
    
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    





    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"



    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1   --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1   --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1   --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1   --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1   --experiment_1  --ray_wall_type 1 --randomness 2"
    
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    





    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"


    
    
    
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 3.1 --final_gap_width 1.5  _3  --ray_wa1l_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1.5  _3  --ray_wa1l_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1.5  _3  --ray_wa1l_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1.5  _3  --ray_wa1l_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1.5  _3  --ray_wa1l_type 1 --randomness 2"



    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1.5  _3  --ray_wa1l_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1.5  _3  --ray_wa1l_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1.5  _3  --ray_wa1l_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1.5  _3  --ray_wa1l_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1.5  _3  --ray_wa1l_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1.5  _3  --ray_wa1l_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1.5  _3  --ray_wa1l_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1.5  _3  --ray_wa1l_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1.5  _3  --ray_wa1l_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1.5  _3  --ray_wa1l_type 1 --randomness 2"
    
    
    

    
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "72:00:00"
done