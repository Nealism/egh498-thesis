#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      

                    
                    

                      
 



                      #Simple Reward 4
                      "3991/E1r32G1E1"
                      "3991/E2r32G1E1"
                      "3991/E3r32G1E1"
                      "3991/E4r32G1E1"
                      "3991/E5r32G1E1"
                      "3991/E6r32G1E1"
                      "3991/E7r32G1E1"
                      "3991/E8r32G1E1"
                      "3991/E9r32G1E1"
                      "3991/E10r32G1E1"
                      "3991/E11r32G1E1"
                      "3991/E12r32G1E1"
                      "3991/E13r32G1E1"
                      "3991/E14r32G1E1"
                      "3991/E15r32G1E1"
                      


                      
                      






                      
                      


 
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    



  
    #Simple Reward 
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 39 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 400 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --generalise_cross --noise_mixed  --obstacle  --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 39 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 400 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --generalise_cross --noise_mixed  --obstacle  --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 39 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 400 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --generalise_cross --noise_mixed  --obstacle  --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 39 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 400 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --generalise_cross --noise_mixed  --obstacle  --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 39 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 400 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --generalise_cross --noise_mixed  --obstacle  --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 39 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 400 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --generalise_cross --noise_mixed  --obstacle  --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 39 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 400 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --generalise_cross --noise_mixed  --obstacle  --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 39 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 400 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --generalise_cross --noise_mixed  --obstacle  --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 39 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 400 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --generalise_cross --noise_mixed  --obstacle  --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 39 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 400 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --generalise_cross --noise_mixed  --obstacle  --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 39 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 400 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --generalise_cross --noise_mixed  --obstacle  --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 39 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 400 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --generalise_cross --noise_mixed  --obstacle  --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 39 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 400 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --generalise_cross --noise_mixed  --obstacle  --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 39 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 400 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --generalise_cross --noise_mixed  --obstacle  --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 39 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 400 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --generalise_cross --noise_mixed  --obstacle  --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt"

    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "72:00:00"
done