#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      

                    
                    

                      
 



                      #Separate Node with Not Frozen Layers --reward 32 -- rand_gap_cur only in transfer leanring without separate node
                      "400188/E1r32G1E1"
                      "400188/E2r32G1E1"
                      "400188/E3r32G1E1"
                      "400188/E4r32G1E1"
                      "400188/E5r32G1E1"
                      "400188/E6r32G1E1"
                      "400188/E7r32G1E1"
                      "400188/E8r32G1E1"
                      "400188/E9r32G1E1"
                      "400188/E10r32G1E1"
                      "400188/E11r32G1E1"
                      "400188/E12r32G1E1"
                      "400188/E13r32G1E1"
                      "400188/E14r32G1E1"
                      "400188/E15r32G1E1"
                      


                      
                      






                      
                      


 
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    



  
    #Simple Reward 
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --heterogeneous --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2000 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.00 --starting_gap_width 3 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --transfer_learning  --freezing_off  --gap_random  --noise_mixed"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --heterogeneous --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2000 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.00 --starting_gap_width 3 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --transfer_learning  --freezing_off  --gap_random  --noise_mixed"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --heterogeneous --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2000 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.00 --starting_gap_width 3 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --transfer_learning  --freezing_off  --gap_random  --noise_mixed"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --heterogeneous --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2000 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.00 --starting_gap_width 3 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --transfer_learning  --freezing_off  --gap_random  --noise_mixed"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --heterogeneous --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2000 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.00 --starting_gap_width 3 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --transfer_learning  --freezing_off  --gap_random  --noise_mixed"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --heterogeneous --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2000 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.00 --starting_gap_width 3 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --transfer_learning  --freezing_off  --gap_random  --noise_mixed"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --heterogeneous --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2000 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.00 --starting_gap_width 3 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --transfer_learning  --freezing_off  --gap_random  --noise_mixed"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --heterogeneous --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2000 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.00 --starting_gap_width 3 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --transfer_learning  --freezing_off  --gap_random  --noise_mixed"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --heterogeneous --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2000 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.00 --starting_gap_width 3 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --transfer_learning  --freezing_off  --gap_random  --noise_mixed"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --heterogeneous --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2000 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.00 --starting_gap_width 3 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --transfer_learning  --freezing_off  --gap_random  --noise_mixed"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --heterogeneous --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2000 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.00 --starting_gap_width 3 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --transfer_learning  --freezing_off  --gap_random  --noise_mixed"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --heterogeneous --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2000 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.00 --starting_gap_width 3 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --transfer_learning  --freezing_off  --gap_random  --noise_mixed"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --heterogeneous --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2000 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.00 --starting_gap_width 3 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --transfer_learning  --freezing_off  --gap_random  --noise_mixed"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --heterogeneous --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2000 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.00 --starting_gap_width 3 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --transfer_learning  --freezing_off  --gap_random  --noise_mixed"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --heterogeneous --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2000 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.00 --starting_gap_width 3 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --transfer_learning  --freezing_off  --gap_random  --noise_mixed"

    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "72:00:00"
done