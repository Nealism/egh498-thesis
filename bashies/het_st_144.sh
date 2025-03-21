#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      

                    
                    

                      
 



                      #Multi Titan Homogeneous Model Check with Rotated Robot ORN in MAP but exp 0 with 4 obs --behaviour_cloning 0
                      "200144/E1r32G1E1"
                      "200144/E2r32G1E1"
                      "200144/E3r32G1E1"
                      "200144/E4r32G1E1"
                      "200144/E5r32G1E1"
                      "200144/E6r32G1E1"
                      "200144/E7r32G1E1"
                      "200144/E8r32G1E1"
                      "200144/E9r32G1E1"
                      "200144/E10r32G1E1"
                      "200144/E11r32G1E1"
                      "200144/E12r32G1E1"
                      "200144/E13r32G1E1"
                      "200144/E14r32G1E1"
                      "200144/E15r32G1E1"
                      


                      
                      






                      
                      


 
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    



  
    #Simple Reward 
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 50 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap  --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 2  --experiment_0  --ray_wall_type 1 --randomness 2 --behaviour_cloning --clone_value 0   "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 50 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap  --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 2  --experiment_0  --ray_wall_type 1 --randomness 2 --behaviour_cloning --clone_value 0   "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 50 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap  --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 2  --experiment_0  --ray_wall_type 1 --randomness 2 --behaviour_cloning --clone_value 0   "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 50 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap  --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 2  --experiment_0  --ray_wall_type 1 --randomness 2 --behaviour_cloning --clone_value 0   "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 50 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap  --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 2  --experiment_0  --ray_wall_type 1 --randomness 2 --behaviour_cloning --clone_value 0   "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 50 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap  --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 2  --experiment_0  --ray_wall_type 1 --randomness 2 --behaviour_cloning --clone_value 0   "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 50 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap  --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 2  --experiment_0  --ray_wall_type 1 --randomness 2 --behaviour_cloning --clone_value 0   "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 50 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap  --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 2  --experiment_0  --ray_wall_type 1 --randomness 2 --behaviour_cloning --clone_value 0   "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 50 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap  --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 2  --experiment_0  --ray_wall_type 1 --randomness 2 --behaviour_cloning --clone_value 0   "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 50 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap  --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 2  --experiment_0  --ray_wall_type 1 --randomness 2 --behaviour_cloning --clone_value 0   "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 50 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap  --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 2  --experiment_0  --ray_wall_type 1 --randomness 2 --behaviour_cloning --clone_value 0   "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 50 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap  --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 2  --experiment_0  --ray_wall_type 1 --randomness 2 --behaviour_cloning --clone_value 0   "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 50 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap  --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 2  --experiment_0  --ray_wall_type 1 --randomness 2 --behaviour_cloning --clone_value 0   "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 50 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap  --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 2  --experiment_0  --ray_wall_type 1 --randomness 2 --behaviour_cloning --clone_value 0   "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 50 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap  --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 2  --experiment_0  --ray_wall_type 1 --randomness 2 --behaviour_cloning --clone_value 0   "

    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "24:00:00"
done