#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      

                    
                    

                      
 



                      #Multi Titan Homogeneous Model Check with Rotated Robot ORN in MAP but exp 0 with 4 obs --kp 50
                      "200186/E1r32G1E1"
                      "200186/E2r32G1E1"
                      "200186/E3r32G1E1"
                      "200186/E4r32G1E1"
                      "200186/E5r32G1E1"
                      "200186/E6r32G1E1"
                      "200186/E7r32G1E1"
                      "200186/E8r32G1E1"
                      "200186/E9r32G1E1"
                      "200186/E10r32G1E1"
                      "200186/E11r32G1E1"
                      "200186/E12r32G1E1"
                      "200186/E13r32G1E1"
                      "200186/E14r32G1E1"
                      "200186/E15r32G1E1"
                      


                      
                      






                      
                      


 
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    



  
    #Simple Reward 
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2   --initial_kp 50 "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2   --initial_kp 50 "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2   --initial_kp 50 "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2   --initial_kp 50 "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2   --initial_kp 50 "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2   --initial_kp 50 "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2   --initial_kp 50 "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2   --initial_kp 50 "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2   --initial_kp 50 "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2   --initial_kp 50 "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2   --initial_kp 50 "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2   --initial_kp 50 "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2   --initial_kp 50 "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2   --initial_kp 50 "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2   --initial_kp 50 "

    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "24:00:00"
done