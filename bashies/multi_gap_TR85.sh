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

                      "ME115/r24TG1.3N"
                      "ME115/1r24TG1.3N"
                      "ME115/2r24TG1.3N"
                      "ME115/3r24TG1.3N"
                      "ME115/4r24TG1.3N"
                      
                      
                      "ME115/5r24TG1N"
                      "ME115/6r24TG1N"
                      "ME115/7r24TG1N"
                      "ME115/8r24TG1N"
                      "ME115/9r24TG1N"
                      
                      "ME115/10r24TG0.85N"
                      "ME115/11r24TG0.85N"
                      "ME115/12r24TG0.85N"
                      "ME115/13r24TG0.85N"
                      "ME115/14r24TG0.85N"
                      
                      "ME115/15r24TG0.80N"
                      "ME115/16r24TG0.80N"
                      "ME115/17r24TG0.80N"
                      "ME115/18r24TG0.80N"
                      "ME115/19r24TG0.80N"
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      # "ME66_4/16r21TG1.5N"
                      # "ME66_4/17r21TG1.5N"

                      # "ME66_4/18r21TG1.5N"
                      # "ME66_4/19r21TG1.5N"
                      # "ME66_4/20r21TG1.5N"


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
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"




    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05.5 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05.5 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05.5 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05.5 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05.5 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05.5 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05.5 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"


    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.5 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.5 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"

    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/Control_Rate_10_Hz/13r24MGE315_ME109_Stepped/2024_04_23_23_34_50/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/Control_Rate_10_Hz/13r24MGE315_ME109_Stepped/2024_04_23_23_34_50/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/Control_Rate_10_Hz/13r24MGE315_ME109_Stepped/2024_04_23_23_34_50/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/Control_Rate_10_Hz/13r24MGE315_ME109_Stepped/2024_04_23_23_34_50/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/Control_Rate_10_Hz/13r24MGE315_ME109_Stepped/2024_04_23_23_34_50/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/Control_Rate_10_Hz/13r24MGE315_ME109_Stepped/2024_04_23_23_34_50/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/Control_Rate_10_Hz/13r24MGE315_ME109_Stepped/2024_04_23_23_34_50/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/Control_Rate_10_Hz/13r24MGE315_ME109_Stepped/2024_04_23_23_34_50/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/Control_Rate_10_Hz/13r24MGE315_ME109_Stepped/2024_04_23_23_34_50/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/Control_Rate_10_Hz/13r24MGE315_ME109_Stepped/2024_04_23_23_34_50/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 0.85  --load_path ~/behaviour_rl/Saved_models/Control_Rate_10_Hz/13r24MGE315_ME109_Stepped/2024_04_23_23_34_50/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 0.85  --load_path ~/behaviour_rl/Saved_models/Control_Rate_10_Hz/13r24MGE315_ME109_Stepped/2024_04_23_23_34_50/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 0.85  --load_path ~/behaviour_rl/Saved_models/Control_Rate_10_Hz/13r24MGE315_ME109_Stepped/2024_04_23_23_34_50/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 0.85  --load_path ~/behaviour_rl/Saved_models/Control_Rate_10_Hz/13r24MGE315_ME109_Stepped/2024_04_23_23_34_50/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 0.85  --load_path ~/behaviour_rl/Saved_models/Control_Rate_10_Hz/13r24MGE315_ME109_Stepped/2024_04_23_23_34_50/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 0.80  --load_path ~/behaviour_rl/Saved_models/Control_Rate_10_Hz/13r24MGE315_ME109_Stepped/2024_04_23_23_34_50/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 0.80  --load_path ~/behaviour_rl/Saved_models/Control_Rate_10_Hz/13r24MGE315_ME109_Stepped/2024_04_23_23_34_50/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 0.80  --load_path ~/behaviour_rl/Saved_models/Control_Rate_10_Hz/13r24MGE315_ME109_Stepped/2024_04_23_23_34_50/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 0.80  --load_path ~/behaviour_rl/Saved_models/Control_Rate_10_Hz/13r24MGE315_ME109_Stepped/2024_04_23_23_34_50/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 0.80  --load_path ~/behaviour_rl/Saved_models/Control_Rate_10_Hz/13r24MGE315_ME109_Stepped/2024_04_23_23_34_50/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    
    
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"



    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 200 --local_epoch_len 200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    
    
    

    
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "168:00:00"
done