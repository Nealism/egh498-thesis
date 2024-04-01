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

                      "ME77/r22TG1.5N"
                      "ME77/1r22TG1.5N"
                      "ME77/2r22TG1.5N"
                      "ME77/3r22TG1.5N"
                      "ME77/4r22TG1.5N"
                      "ME77/5r22TG1.5N"
                      "ME77/6r22TG1.5N"
                      "ME77/7r22TG1.5N"
                      "ME77/8r22TG1.5N"
                      "ME77/9r22TG1.5N"
                      "ME77/10r22TG1.5N"

                      "ME77/11r22TG1.5N"
                      "ME77/12r22TG1.5N"
                      "ME77/13r22TG1.5N"
                      "ME77/14r22TG1.5N"
                      "ME77/15r22TG1.5N"
                      "ME77/16r22TG1.5N"
                      "ME77/17r22TG1.5N"

                      "ME77/18r22TG1.5N"
                      "ME77/19r22TG1.5N"
                      "ME77/20r22TG1.5N"


                      "ME77/21r22TG1.5N"
                      "ME77/22r22TG1.5N"
                      "ME77/23r22TG1.5N"
                      "ME77/24r22TG1.5N"
                      "ME77/25r22TG1.5N"
                      "ME77/26r22TG1.5N"
                      "ME77/27r22TG1.5N"

                      "ME77/28r22TG1.5N"
                      "ME77/29r22TG1.5N"
                      "ME77/30r22TG1.5N"
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

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

    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"



    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r21MGE103_ME61_randomness2_full/2024_02_28_11_58_04/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    
    
    

    
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "168:00:00"
done