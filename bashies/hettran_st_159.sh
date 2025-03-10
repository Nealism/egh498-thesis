#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      

                    
                    

                      
 



                      #Separate Node Transfer with all Frozen Layers-- 1m Gap but Reward 27 --Rotated Map
                      "400159/E1r32G1E1"
                      "400159/E2r32G1E1"
                      "400159/E3r32G1E1"
                      "400159/E4r32G1E1"
                      "400159/E5r32G1E1"
                      "400159/E6r32G1E1"
                      "400159/E7r32G1E1"
                      "400159/E8r32G1E1"
                      "400159/E9r32G1E1"
                      "400159/E10r32G1E1"
                      "400159/E11r32G1E1"
                      "400159/E12r32G1E1"
                      "400159/E13r32G1E1"
                      "400159/E14r32G1E1"
                      "400159/E15r32G1E1"
                      


                      
                      






                      
                      


 
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    



  
    #Simple Reward 
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --heterogeneous --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --transfer_learning --separate_node  --titan_frozen_layer --spot_frozen_layer  --combined_value "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --heterogeneous --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --transfer_learning --separate_node  --titan_frozen_layer --spot_frozen_layer  --combined_value "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --heterogeneous --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --transfer_learning --separate_node  --titan_frozen_layer --spot_frozen_layer  --combined_value "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --heterogeneous --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --transfer_learning --separate_node  --titan_frozen_layer --spot_frozen_layer  --combined_value "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --heterogeneous --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --transfer_learning --separate_node  --titan_frozen_layer --spot_frozen_layer  --combined_value "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --heterogeneous --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --transfer_learning --separate_node  --titan_frozen_layer --spot_frozen_layer  --combined_value "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --heterogeneous --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --transfer_learning --separate_node  --titan_frozen_layer --spot_frozen_layer  --combined_value "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --heterogeneous --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --transfer_learning --separate_node  --titan_frozen_layer --spot_frozen_layer  --combined_value "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --heterogeneous --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --transfer_learning --separate_node  --titan_frozen_layer --spot_frozen_layer  --combined_value "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --heterogeneous --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --transfer_learning --separate_node  --titan_frozen_layer --spot_frozen_layer  --combined_value "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --heterogeneous --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --transfer_learning --separate_node  --titan_frozen_layer --spot_frozen_layer  --combined_value "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --heterogeneous --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --transfer_learning --separate_node  --titan_frozen_layer --spot_frozen_layer  --combined_value "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --heterogeneous --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --transfer_learning --separate_node  --titan_frozen_layer --spot_frozen_layer  --combined_value "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --heterogeneous --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --transfer_learning --separate_node  --titan_frozen_layer --spot_frozen_layer  --combined_value "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --heterogeneous --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --transfer_learning --separate_node  --titan_frozen_layer --spot_frozen_layer  --combined_value "

    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "72:00:00"
done