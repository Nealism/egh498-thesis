#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      "ME33/r13MGE101"
                      "ME33/r14MGE101"
                      "ME33/r15MGE101"
                      "ME33/r16MGE101"
                      "ME33/r17MGE101"
                      "ME33/r18MGE101"
                      "ME33/r19MGE101"
                      "ME33/r20MGE101"
                      "ME33/r21MGE101"
                      "ME33/r24MGE101"
                      "ME33/r23MGE101"
                      "ME33/r24MGE101"
                      "ME33/r25MGE101"
                      "ME33/r26MGE101"
                      "ME33/r27MGE101"
                      "ME33/r28MGE101"
                      "ME33/r29MGE101"
                      "ME33/r30MGE101"

                      "ME33/r31MGE101"
                      "ME33/r32MGE101"
                      "ME33/r33MGE101"
                      "ME33/r34MGE101"
                      "ME33/r35MGE101"
                      "ME33/r36MGE101"
                      "ME33/r37MGE101"
                      "ME33/r38MGE101"
                      "ME33/r39MGE101"
                      "ME33/r40MGE101"


                    


                      "ME33/r13TG1O"
                      "ME33/r18TG1O"
                      "ME33/r19TG1O"

                      "ME33/r29TG1O"
                      "ME33/r31TG1O"
                      "ME33/r32TG1O"
                      "ME33/r34TG1O"


                      "ME33/r13TG1N"
                      "ME33/r18TG1N"
                      "ME33/r19TG1N"

                      "ME33/r29TG1N"
                      "ME33/r31TG1N"
                      "ME33/r32TG1N"
                      "ME33/r34TG1N"

                      "ME33/r36TG1N"
                      "ME33/r41TG1N"

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1 --MA_bootstrap --experiment_3  --ray_wall_type 1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 14 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1 --MA_bootstrap --experiment_3  --ray_wall_type 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 15 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1 --MA_bootstrap --experiment_3  --ray_wall_type 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 16 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1 --MA_bootstrap --experiment_3  --ray_wall_type 1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 17 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1 --MA_bootstrap --experiment_3  --ray_wall_type 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 18 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1 --MA_bootstrap --experiment_3  --ray_wall_type 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 19 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1 --MA_bootstrap --experiment_3  --ray_wall_type 1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 20 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1 --MA_bootstrap --experiment_3  --ray_wall_type 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1 --MA_bootstrap --experiment_3  --ray_wall_type 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1 --MA_bootstrap --experiment_3  --ray_wall_type 1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1 --MA_bootstrap --experiment_3  --ray_wall_type 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1 --MA_bootstrap --experiment_3  --ray_wall_type 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1 --MA_bootstrap --experiment_3  --ray_wall_type 1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1 --MA_bootstrap --experiment_3  --ray_wall_type 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1 --MA_bootstrap --experiment_3  --ray_wall_type 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1 --MA_bootstrap --experiment_3  --ray_wall_type 1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1 --MA_bootstrap --experiment_3  --ray_wall_type 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1 --MA_bootstrap --experiment_3  --ray_wall_type 1"

    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1 --MA_bootstrap --experiment_3  --ray_wall_type 1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1 --MA_bootstrap --experiment_3  --ray_wall_type 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 33 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1 --MA_bootstrap --experiment_3  --ray_wall_type 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1 --MA_bootstrap --experiment_3  --ray_wall_type 1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 35 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1 --MA_bootstrap --experiment_3  --ray_wall_type 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 36 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1 --MA_bootstrap --experiment_3  --ray_wall_type 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 37 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1 --MA_bootstrap --experiment_3  --ray_wall_type 1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 38 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1 --MA_bootstrap --experiment_3  --ray_wall_type 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 39 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1 --MA_bootstrap --experiment_3  --ray_wall_type 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 40 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1 --MA_bootstrap --experiment_3  --ray_wall_type 1"
    



    

    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500  --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 4 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 33 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500  --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 4 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 19 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500  --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 4 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500  --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 4 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500  --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 4 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500  --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 4 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500  --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 4 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3  --ray_wall_type 1"




    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500  --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 33 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500  --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 19 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500  --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500  --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500  --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500  --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500  --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 3 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 1"


    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 36 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500  --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 3 --final_gap_width 2  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 1"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 41 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500  --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 3 --final_gap_width 2  --load_path ~/behaviour_rl/Saved_models/r13TG2_ME32_r19TG3/2024_02_04_20_19_48/model.pt --experiment_3  --ray_wall_type 1"
    
    

    
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "96:00:00"
done