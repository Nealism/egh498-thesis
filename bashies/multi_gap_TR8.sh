#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      

                      # "ME36/r13TG1O"
                      # "ME36/r18TG1O"
                      # "ME36/r19TG1O"

                      # "ME36/r29TG1O"
                      # "ME36/r31TG1O"
                      # "ME36/r32TG1O"
                      # "ME36/r34TG1O"


                      "ME36/r13TG1S"
                      "ME36/r14TG1S"
                      "ME36/r15TG1S"

                      "ME36/r16TG1S"
                      "ME36/r17TG1S"
                      "ME36/r18TG1S"
                      "ME36/r19TG1S"

                      "ME36/r20TG1S"
                      "ME36/r21TG1S"

                      "ME36/r22TG1S"
                      "ME36/r32TG1S"
                      "ME36/r33TG1S"
                      "ME36/r33TG1S"

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 4 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r9GD.1EC0_sgo27/2024_02_06_02_36_11 --experiment_1  --ray_wall_type 1 --MA_bootstrap --expert_curr"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 33 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 4 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r9GD.1EC0_sgo27/2024_02_06_02_36_11 --experiment_1  --ray_wall_type 1 --MA_bootstrap --expert_curr"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 19 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 4 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r9GD.1EC0_sgo27/2024_02_06_02_36_11 --experiment_1  --ray_wall_type 1 --MA_bootstrap --expert_curr"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 4 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r9GD.1EC0_sgo27/2024_02_06_02_36_11 --experiment_1  --ray_wall_type 1 --MA_bootstrap --expert_curr"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 4 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r9GD.1EC0_sgo27/2024_02_06_02_36_11 --experiment_1  --ray_wall_type 1 --MA_bootstrap --expert_curr"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 4 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r9GD.1EC0_sgo27/2024_02_06_02_36_11 --experiment_1  --ray_wall_type 1 --MA_bootstrap --expert_curr"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 4 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r9GD.1EC0_sgo27/2024_02_06_02_36_11 --experiment_1  --ray_wall_type 1 --MA_bootstrap --expert_curr"




    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r9GD.1EC0_sgo27/2024_02_06_02_36_11/model.pt --experiment_1  --ray_wall_type 1 --MA_bootstrap --expert_curr"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 14 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r9GD.1EC0_sgo27/2024_02_06_02_36_11/model.pt --experiment_1  --ray_wall_type 1 --MA_bootstrap --expert_curr"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 15 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r9GD.1EC0_sgo27/2024_02_06_02_36_11/model.pt --experiment_1  --ray_wall_type 1 --MA_bootstrap --expert_curr"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 16 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r9GD.1EC0_sgo27/2024_02_06_02_36_11/model.pt --experiment_1  --ray_wall_type 1 --MA_bootstrap --expert_curr"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 17 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r9GD.1EC0_sgo27/2024_02_06_02_36_11/model.pt --experiment_1  --ray_wall_type 1 --MA_bootstrap --expert_curr"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 18 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r9GD.1EC0_sgo27/2024_02_06_02_36_11/model.pt --experiment_1  --ray_wall_type 1 --MA_bootstrap --expert_curr"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 19 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r9GD.1EC0_sgo27/2024_02_06_02_36_11/model.pt --experiment_1  --ray_wall_type 1 --MA_bootstrap --expert_curr"


    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 20 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r9GD.1EC0_sgo27/2024_02_06_02_36_11/model.pt --experiment_1  --ray_wall_type 1 --MA_bootstrap --expert_curr"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r9GD.1EC0_sgo27/2024_02_06_02_36_11/model.pt --experiment_1  --ray_wall_type 1 --MA_bootstrap --expert_curr"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r9GD.1EC0_sgo27/2024_02_06_02_36_11/model.pt --experiment_1  --ray_wall_type 1 --MA_bootstrap --expert_curr"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r9GD.1EC0_sgo27/2024_02_06_02_36_11/model.pt --experiment_1  --ray_wall_type 1 --MA_bootstrap --expert_curr"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 33 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r9GD.1EC0_sgo27/2024_02_06_02_36_11/model.pt --experiment_1  --ray_wall_type 1 --MA_bootstrap --expert_curr"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 1  --load_path ~/behaviour_rl/Saved_models/r9GD.1EC0_sgo27/2024_02_06_02_36_11/model.pt --experiment_1  --ray_wall_type 1 --MA_bootstrap --expert_curr"
    
    

    
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "96:00:00"
done