#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      

                    
                    

                      
 



                      #Multi Titan Homogeneous Model Check with Rotated Robot ORN in MAP but exp 0 with 4 obs --- Random Uniform GAP ONLY
                      "200194/E1r32G1E1"
                      "200194/E2r32G1E1"
                      "200194/E3r32G1E1"
                      "200194/E4r32G1E1"
                      "200194/E5r32G1E1"
                      "200194/E6r32G1E1"
                      "200194/E7r32G1E1"
                      "200194/E8r32G1E1"
                      "200194/E9r32G1E1"
                      "200194/E10r32G1E1"
                      "200194/E11r32G1E1"
                      "200194/E12r32G1E1"
                      "200194/E13r32G1E1"
                      "200194/E14r32G1E1"
                      "200194/E15r32G1E1"
                      


                      
                      






                      
                      


 
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    



  
    #Simple Reward 
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --expert_curr  --MA_bootstrap   --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --combined_value  --gap_random "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --expert_curr  --MA_bootstrap   --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --combined_value  --gap_random "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --expert_curr  --MA_bootstrap   --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --combined_value  --gap_random "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --expert_curr  --MA_bootstrap   --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --combined_value  --gap_random "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --expert_curr  --MA_bootstrap   --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --combined_value  --gap_random "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --expert_curr  --MA_bootstrap   --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --combined_value  --gap_random "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --expert_curr  --MA_bootstrap   --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --combined_value  --gap_random "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --expert_curr  --MA_bootstrap   --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --combined_value  --gap_random "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --expert_curr  --MA_bootstrap   --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --combined_value  --gap_random "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --expert_curr  --MA_bootstrap   --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --combined_value  --gap_random "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --expert_curr  --MA_bootstrap   --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --combined_value  --gap_random "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --expert_curr  --MA_bootstrap   --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --combined_value  --gap_random "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --expert_curr  --MA_bootstrap   --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --combined_value  --gap_random "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --expert_curr  --MA_bootstrap   --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --combined_value  --gap_random "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --expert_curr  --MA_bootstrap   --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --combined_value  --gap_random "

    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "48:00:00"
done