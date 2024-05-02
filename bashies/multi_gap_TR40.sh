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


                      # "ME35/r21TG1.3N"
                      # "ME35/r21TG1.3N"
                      # "ME35/r21TG1.3N"

                      # "ME35/r21TG1.3N"
                      # "ME35/r21TG1.3N"
                      # "ME35/r21TG1.3N"
                      # "ME35/r21TG1.3N"

                      # "ME35/r21TG1.3N"
                      # "ME35/r21TG1.3N"

                      "ME67_8/r21TG1.3N"
                      "ME67_8/1r21TG1.3N"
                      "ME67_8/2r21TG1.3N"
                      "ME67_8/3r21TG1.3N"
                      "ME67_8/4r21TG1.3N"
                      "ME67_8/5r21TG1.3N"
                      "ME67_8/6r21TG1.3N"
                      "ME67_8/7r21TG1.3N"
                      "ME67_8/8r21TG1.3N"
                      "ME67_8/9r21TG1.3N"
                      "ME67_8/10r21TG1.3N"

                      "ME67_8/11r21TG1.3N"
                      "ME67_8/12r21TG1.3N"
                      "ME67_8/13r21TG1.3N"
                      "ME67_8/14r21TG1.3N"
                      "ME67_8/15r21TG1.3N"
                      
                      
                      
                      # "ME67_4/16r21TG1.3N"
                      # "ME67_4/17r21TG1.3N"

                      # "ME67_4/18r21TG1.3N"
                      # "ME67_4/19r21TG1.3N"
                      # "ME67_4/20r21TG1.3N"

                      # "ME67_4/21r21TG1.3N"
                      # "ME67_4/22r21TG1.3N"
                      # "ME67_4/23r21TG1.3N"
                      # "ME67_4/24r21TG1.3N"
                      # "ME67_4/25r21TG1.3N"
                      # "ME67_4/26r21TG1.3N"
                      # "ME67_4/27r21TG1.3N"

                      # "ME67_4/28r21TG1.3N"
                      # "ME67_4/29r21TG1.3N"
                      # "ME67_4/30r21TG1.3N"
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"




    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05.5 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05.5 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05.5 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05.5 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05.5 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05.5 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05.5 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"


    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.5 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.5 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"

    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 250 --local_epoch_len 250  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 250 --local_epoch_len 250  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 250 --local_epoch_len 250  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 250 --local_epoch_len 250  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 250 --local_epoch_len 250  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 250 --local_epoch_len 250  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 250 --local_epoch_len 250  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 250 --local_epoch_len 250  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 250 --local_epoch_len 250  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 250 --local_epoch_len 250  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 250 --local_epoch_len 250  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 250 --local_epoch_len 250  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 250 --local_epoch_len 250  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 250 --local_epoch_len 250  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 250 --local_epoch_len 250  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 250 --local_epoch_len 250  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    
    
    
    
    
    
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 250 --local_epoch_len 250  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 250 --local_epoch_len 250  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 250 --local_epoch_len 250  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 250 --local_epoch_len 250  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 250 --local_epoch_len 250  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"


    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 250 --local_epoch_len 250  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 250 --local_epoch_len 250  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 250 --local_epoch_len 250  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 250 --local_epoch_len 250  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 250 --local_epoch_len 250  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 250 --local_epoch_len 250  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 250 --local_epoch_len 250  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 250 --local_epoch_len 250  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 250 --local_epoch_len 250  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 250 --local_epoch_len 250  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    
    
    

    
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "168:00:00"
done