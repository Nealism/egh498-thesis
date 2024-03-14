#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      

                      # "ME35/r13TG1O"
                      # "ME35/r18TG1O"
                      # "ME35/r19TG1O"

                      # "ME35/r29TG1O"
                      # "ME35/r31TG1O"
                      # "ME35/r32TG1O"
                      # "ME35/r34TG1O"


                      # "ME35/r13TG1.3N8"
                      # "ME35/r14TG1.3N8"
                      # "ME35/r15TG1.3N8"

                      # "ME35/r16TG1.3N8"
                      # "ME35/r17TG1.3N8"
                      # "ME35/r18TG1.3N8"
                      # "ME35/r19TG1.3N8"

                      # "ME35/r20TG1.3N8"
                      # "ME35/r21TG1.3N8"
                      "ME54/r13TG1.3N8"
                      "ME54/r14TG1.3N8"
                      "ME54/r15TG1.3N8"
                      "ME54/r16TG1.3N8"
                      "ME54/r17TG1.3N8"
                      "ME54/r18TG1.3N8"
                      "ME54/r19TG1.3N8"
                      "ME54/r20TG1.3N8"
                      "ME54/r21TG1.3N8"
                      "ME54/r22TG1.3N8"

                      "ME54/r23TG1.3N8"
                      "ME54/r24TG1.3N8"
                      "ME54/r25TG1.3N8"
                      "ME54/r26TG1.3N8"
                      "ME54/r27TG1.3N8"
                      "ME54/r28TG1.3N8"
                      "ME54/r29TG1.3N8"

                      "ME54/r30TG1.3N8"
                      "ME54/r31TG1.3N8"
                      "ME54/r32TG1.3N8"
                      "ME54/r33TG1.3N8"
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 33 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 19 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"




    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05.5 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 14 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05.5 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 15 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05.5 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 16 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05.5 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 17 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05.5 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 18 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05.5 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 19 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05.5 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"


    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 20 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.5 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.5 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"

    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r28TG1.5N_ME51_100_rand1/2024_02_20_03_49_02/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 14 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r28TG1.5N_ME51_100_rand1/2024_02_20_03_49_02/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 15 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r28TG1.5N_ME51_100_rand1/2024_02_20_03_49_02/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 16 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r28TG1.5N_ME51_100_rand1/2024_02_20_03_49_02/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 17 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r28TG1.5N_ME51_100_rand1/2024_02_20_03_49_02/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 18 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r28TG1.5N_ME51_100_rand1/2024_02_20_03_49_02/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 19 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r28TG1.5N_ME51_100_rand1/2024_02_20_03_49_02/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 20 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r28TG1.5N_ME51_100_rand1/2024_02_20_03_49_02/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r28TG1.5N_ME51_100_rand1/2024_02_20_03_49_02/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r28TG1.5N_ME51_100_rand1/2024_02_20_03_49_02/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r28TG1.5N_ME51_100_rand1/2024_02_20_03_49_02/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r28TG1.5N_ME51_100_rand1/2024_02_20_03_49_02/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r28TG1.5N_ME51_100_rand1/2024_02_20_03_49_02/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r28TG1.5N_ME51_100_rand1/2024_02_20_03_49_02/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r28TG1.5N_ME51_100_rand1/2024_02_20_03_49_02/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r28TG1.5N_ME51_100_rand1/2024_02_20_03_49_02/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r28TG1.5N_ME51_100_rand1/2024_02_20_03_49_02/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r28TG1.5N_ME51_100_rand1/2024_02_20_03_49_02/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r28TG1.5N_ME51_100_rand1/2024_02_20_03_49_02/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r28TG1.5N_ME51_100_rand1/2024_02_20_03_49_02/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 33 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1600 --local_epoch_len 1600  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.5 --final_gap_width 1.3  --load_path ~/behaviour_rl/Saved_models/r28TG1.5N_ME51_100_rand1/2024_02_20_03_49_02/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    
    
    

    
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "144:00:00"
done