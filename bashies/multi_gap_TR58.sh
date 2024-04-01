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

                      "ME78/r22TG1.3N"
                      "ME78/1r22TG1.3N"
                      "ME78/2r22TG1.3N"
                      "ME78/3r22TG1.3N"
                      "ME78/4r22TG1.3N"
                      "ME78/5r22TG1.3N"
                      "ME78/6r22TG1.3N"
                      "ME78/7r22TG1.3N"
                      "ME78/8r22TG1.3N"
                      "ME78/9r22TG1.3N"
                      "ME78/10r22TG1.3N"

                      "ME78/11r22TG1.3N"
                      "ME78/12r22TG1.3N"
                      "ME78/13r22TG1.3N"
                      "ME78/14r22TG1.3N"
                      "ME78/15r22TG1.3N"
                      "ME78/16r22TG1.3N"
                      "ME78/17r22TG1.3N"

                      "ME78/18r22TG1.3N"
                      "ME78/19r22TG1.3N"
                      "ME78/20r22TG1.3N"

                      "ME78/21r22TG1.3N"
                      "ME78/22r22TG1.3N"
                      "ME78/23r22TG1.3N"
                      "ME78/24r22TG1.3N"
                      "ME78/25r22TG1.3N"
                      "ME78/26r22TG1.3N"
                      "ME78/27r22TG1.3N"

                      "ME78/28r22TG1.3N"
                      "ME78/29r22TG1.3N"
                      "ME78/30r22TG1.3N"
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

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

    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"


    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r21TG1.5N_ME62_80_rand2_sem_final/2024_03_03_04_28_37/model.pt --experiment_3  --ray_wall_type 1 --randomness 2"
    
    
    

    
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "168:00:00"
done