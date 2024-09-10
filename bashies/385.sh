#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      

                    
                    

                      
 



                      #Simple Reward 4
                      "385/E1r32G1E1"
                      "385/E2r32G1E1"
                      "385/E3r32G1E1"
                      "385/E4r32G1E1"
                      "385/E5r32G1E1"
                      "385/E6r32G1E1"
                      "385/E7r32G1E1"
                      "385/E8r32G1E1"
                      "385/E9r32G1E1"
                      "385/E10r32G1E1"
                      "385/E11r32G1E1"
                      "385/E12r32G1E1"
                      "385/E13r32G1E1"
                      "385/E14r32G1E1"
                      "385/E15r32G1E1"
                      


                      
                      






                      
                      


 
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    



  
    #Simple Reward 
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --generalise --map_noise --gap_offset --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E10r32G1E1_371_0.85_no_noise/2024_09_09_19_13_56/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --generalise --map_noise --gap_offset --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E10r32G1E1_371_0.85_no_noise/2024_09_09_19_13_56/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --generalise --map_noise --gap_offset --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E10r32G1E1_371_0.85_no_noise/2024_09_09_19_13_56/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --generalise --map_noise --gap_offset --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E10r32G1E1_371_0.85_no_noise/2024_09_09_19_13_56/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --generalise --map_noise --gap_offset --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E10r32G1E1_371_0.85_no_noise/2024_09_09_19_13_56/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --generalise --map_noise --gap_offset --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E10r32G1E1_371_0.85_no_noise/2024_09_09_19_13_56/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --generalise --map_noise --gap_offset --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E10r32G1E1_371_0.85_no_noise/2024_09_09_19_13_56/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --generalise --map_noise --gap_offset --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E10r32G1E1_371_0.85_no_noise/2024_09_09_19_13_56/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --generalise --map_noise --gap_offset --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E10r32G1E1_371_0.85_no_noise/2024_09_09_19_13_56/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --generalise --map_noise --gap_offset --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E10r32G1E1_371_0.85_no_noise/2024_09_09_19_13_56/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --generalise --map_noise --gap_offset --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E10r32G1E1_371_0.85_no_noise/2024_09_09_19_13_56/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --generalise --map_noise --gap_offset --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E10r32G1E1_371_0.85_no_noise/2024_09_09_19_13_56/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --generalise --map_noise --gap_offset --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E10r32G1E1_371_0.85_no_noise/2024_09_09_19_13_56/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --generalise --map_noise --gap_offset --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E10r32G1E1_371_0.85_no_noise/2024_09_09_19_13_56/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1500 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --generalise --map_noise --gap_offset --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E10r32G1E1_371_0.85_no_noise/2024_09_09_19_13_56/model.pt"

    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "48:00:00"
done