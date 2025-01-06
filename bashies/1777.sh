#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      

                    
                    

                      
 



                      #Simple Reward 4
                      "1677/E1r32G1E1"
                      "1677/E2r32G1E1"
                      "1677/E3r32G1E1"
                      "1677/E4r32G1E1"
                      "1677/E5r32G1E1"
                      "1677/E6r32G1E1"
                      "1677/E7r32G1E1"
                      "1677/E8r32G1E1"
                      "1677/E9r32G1E1"
                      "1677/E10r32G1E1"
                      "1677/E11r32G1E1"
                      "1677/E12r32G1E1"
                      "1677/E13r32G1E1"
                      "1677/E14r32G1E1"
                      "1677/E15r32G1E1"
                      


                      
                      






                      
                      


 
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    



  
    #Simple Reward 
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 1 --multi_titans --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 1 --multi_titans --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 1 --multi_titans --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 1 --multi_titans --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 1 --multi_titans --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 1 --multi_titans --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 1 --multi_titans --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 1 --multi_titans --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 1 --multi_titans --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 1 --multi_titans --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 1 --multi_titans --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 1 --multi_titans --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 1 --multi_titans --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 1 --multi_titans --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 1 --multi_titans --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 "
    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "48:00:00"
done