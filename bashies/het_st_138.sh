#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      

                    
                    

                      
 



                      #Multi Titan Homogeneous Model Check with Rotated Robot ORN in MAP but exp 0 with 4 obs --- Random Uniform GAP ONLY
                      "200138/E1r32G1E1"
                      "200138/E2r32G1E1"
                      "200138/E3r32G1E1"
                      "200138/E4r32G1E1"
                      "200138/E5r32G1E1"
                      "200138/E6r32G1E1"
                      "200138/E7r32G1E1"
                      "200138/E8r32G1E1"
                      "200138/E9r32G1E1"
                      "200138/E10r32G1E1"
                      "200138/E11r32G1E1"
                      "200138/E12r32G1E1"
                      "200138/E13r32G1E1"
                      "200138/E14r32G1E1"
                      "200138/E15r32G1E1"
                      


                      
                      






                      
                      


 
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    



  
    #Simple Reward 
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2 --combined_value  --gap_random "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2 --combined_value  --gap_random "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2 --combined_value  --gap_random "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2 --combined_value  --gap_random "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2 --combined_value  --gap_random "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2 --combined_value  --gap_random "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2 --combined_value  --gap_random "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2 --combined_value  --gap_random "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2 --combined_value  --gap_random "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2 --combined_value  --gap_random "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2 --combined_value  --gap_random "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2 --combined_value  --gap_random "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2 --combined_value  --gap_random "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2 --combined_value  --gap_random "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2 --combined_value  --gap_random "

    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "72:00:00"
done