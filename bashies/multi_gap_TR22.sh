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


                      # "ME35/r13TG1N"
                      # "ME35/r14TG1N"
                      # "ME35/r15TG1N"

                      # "ME35/r16TG1N"
                      # "ME35/r17TG1N"
                      # "ME35/r18TG1N"
                      # "ME35/r19TG1N"

                      # "ME35/r20TG1N"
                      # "ME35/r21TG1N"
                      "ME50/r13TG1N"
                      "ME50/r14TG1N"
                      "ME50/r15TG1N"
                      "ME50/r16TG1N"
                      "ME50/r17TG1N"
                      "ME50/r18TG1N"
                      "ME50/r19TG1N"
                      "ME50/r20TG1N"
                      "ME50/r21TG1N"
                      "ME50/r22TG1N"

                      "ME50/r23TG1N"
                      "ME50/r24TG1N"
                      "ME50/r25TG1N"
                      "ME50/r26TG1N"
                      "ME50/r27TG1N"
                      "ME50/r28TG1N"
                      "ME50/r29TG1N"

                      "ME50/r30TG1N"
                      "ME50/r31TG1N"
                      "ME50/r32TG1N"
                      "ME50/r33TG1N"
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 33 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 19 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"




    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05.5 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 14 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05.5 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 15 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05.5 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 16 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05.5 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 17 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05.5 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 18 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05.5 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 19 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05.5 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"


    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 20 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.5 --starting_gap_width 3 --final_gap_width 2  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.5 --starting_gap_width 3 --final_gap_width 2  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 0"

    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1500 --local_epoch_len 1500  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r16MGE103_ME41_100_randomness1/2024_02_15_19_15_23/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 14 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1500 --local_epoch_len 1500  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r16MGE103_ME41_100_randomness1/2024_02_15_19_15_23/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 15 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1500 --local_epoch_len 1500  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r16MGE103_ME41_100_randomness1/2024_02_15_19_15_23/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 16 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1500 --local_epoch_len 1500  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r16MGE103_ME41_100_randomness1/2024_02_15_19_15_23/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 17 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1500 --local_epoch_len 1500  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r16MGE103_ME41_100_randomness1/2024_02_15_19_15_23/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 18 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1500 --local_epoch_len 1500  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r16MGE103_ME41_100_randomness1/2024_02_15_19_15_23/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 19 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1500 --local_epoch_len 1500  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r16MGE103_ME41_100_randomness1/2024_02_15_19_15_23/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 20 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1500 --local_epoch_len 1500  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r16MGE103_ME41_100_randomness1/2024_02_15_19_15_23/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1500 --local_epoch_len 1500  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r16MGE103_ME41_100_randomness1/2024_02_15_19_15_23/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1500 --local_epoch_len 1500  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r16MGE103_ME41_100_randomness1/2024_02_15_19_15_23/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1500 --local_epoch_len 1500  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r16MGE103_ME41_100_randomness1/2024_02_15_19_15_23/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1500 --local_epoch_len 1500  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r16MGE103_ME41_100_randomness1/2024_02_15_19_15_23/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1500 --local_epoch_len 1500  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r16MGE103_ME41_100_randomness1/2024_02_15_19_15_23/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1500 --local_epoch_len 1500  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r16MGE103_ME41_100_randomness1/2024_02_15_19_15_23/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1500 --local_epoch_len 1500  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r16MGE103_ME41_100_randomness1/2024_02_15_19_15_23/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1500 --local_epoch_len 1500  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r16MGE103_ME41_100_randomness1/2024_02_15_19_15_23/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1500 --local_epoch_len 1500  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r16MGE103_ME41_100_randomness1/2024_02_15_19_15_23/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1500 --local_epoch_len 1500  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r16MGE103_ME41_100_randomness1/2024_02_15_19_15_23/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1500 --local_epoch_len 1500  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r16MGE103_ME41_100_randomness1/2024_02_15_19_15_23/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1500 --local_epoch_len 1500  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r16MGE103_ME41_100_randomness1/2024_02_15_19_15_23/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 33 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 1500 --local_epoch_len 1500  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r16MGE103_ME41_100_randomness1/2024_02_15_19_15_23/model.pt --experiment_3  --ray_wall_type 1 --randomness 1"
    
    
    

    
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "96:00:00"
done