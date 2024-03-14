#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      

                      # "ME41/r13TG1.5O"
                      # "ME41/r18TG1.5O"
                      # "ME41/r19TG1.5O"

                      # "ME41/r29TG1.5O"
                      # "ME41/r31TG1.5O"
                      # "ME41/r32TG1.5O"
                      # "ME41/r34TG1.5O"


                      "ME41/r13TG1.5N"
                      "ME41/r14TG1.5N"
                      "ME41/r15TG1.5N"

                      "ME41/r16TG1.5N"
                      "ME41/r17TG1.5N"
                      "ME41/r18TG1.5N"
                      "ME41/r19TG1.5N"

                      "ME41/r20TG1.5N"
                      "ME41/r21TG1.5N"

                      "ME41/r22TG1.5N"
                      "ME41/r23TG1.5N"
                      "ME41/r24TG1.5N"
                      "ME41/r25TG1.5N"
                      "ME41/r26TG1.5N"
                      "ME41/r27TG1.5N"
                      "ME41/r28TG1.5N"
                      "ME41/r29TG1.5N"
                      "ME41/r30TG1.5N"



                      "ME41/r32TG1.5N"
                      "ME41/r33TG1.5N"
                      "ME41/r33TG1.5N"

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 4 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 33 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 4 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 19 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 4 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 4 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 4 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 4 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 4 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1"




    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 14 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 15 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 16 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 17 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 18 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 19 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 1"


    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 20 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 1"
    
    
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 33 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 1"
    
    

    
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "96:00:00"
done