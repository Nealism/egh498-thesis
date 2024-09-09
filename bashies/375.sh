#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      

                    
                    

                      
 



                      #Simple Reward 4
                      "375/E1r32G1E1"
                      "375/E2r32G1E1"
                      "375/E3r32G1E1"
                      "375/E4r32G1E1"
                      "375/E5r32G1E1"
                      "375/E6r32G1E1"
                      "375/E7r32G1E1"
                      "375/E8r32G1E1"
                      "375/E9r32G1E1"
                      "375/E10r32G1E1"
                      "375/E11r32G1E1"
                      "375/E12r32G1E1"
                      "375/E13r32G1E1"
                      "375/E14r32G1E1"
                      "375/E15r32G1E1"
                      


                      
                      






                      
                      


 
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    



  
    #Simple Reward 
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --map_noise --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E14r32G1E1_no_Noise_100success/2024_09_08_22_55_49//model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --map_noise --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E14r32G1E1_no_Noise_100success/2024_09_08_22_55_49//model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --map_noise --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E14r32G1E1_no_Noise_100success/2024_09_08_22_55_49//model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --map_noise --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E14r32G1E1_no_Noise_100success/2024_09_08_22_55_49//model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --map_noise --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E14r32G1E1_no_Noise_100success/2024_09_08_22_55_49//model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --map_noise --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E14r32G1E1_no_Noise_100success/2024_09_08_22_55_49//model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --map_noise --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E14r32G1E1_no_Noise_100success/2024_09_08_22_55_49//model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --map_noise --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E14r32G1E1_no_Noise_100success/2024_09_08_22_55_49//model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --map_noise --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E14r32G1E1_no_Noise_100success/2024_09_08_22_55_49//model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --map_noise --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E14r32G1E1_no_Noise_100success/2024_09_08_22_55_49//model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --map_noise --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E14r32G1E1_no_Noise_100success/2024_09_08_22_55_49//model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --map_noise --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E14r32G1E1_no_Noise_100success/2024_09_08_22_55_49//model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --map_noise --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E14r32G1E1_no_Noise_100success/2024_09_08_22_55_49//model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --map_noise --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E14r32G1E1_no_Noise_100success/2024_09_08_22_55_49//model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --map_noise --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E14r32G1E1_no_Noise_100success/2024_09_08_22_55_49//model.pt"

    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "24:00:00"
done