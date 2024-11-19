#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      

                    
                    

                      
 



                      #Simple Reward 4
                      


                      "2002/6E1r32G1E1"
                      "2002/6E2r32G1E1"
                      "2002/6E3r32G1E1"
                      "2002/6E4r32G1E1"
                      "2002/6E5r32G1E1"

                      "2002/7E1r32G1E1"
                      "2002/7E2r32G1E1"
                      "2002/7E3r32G1E1"
                      "2002/7E4r32G1E1"
                      "2002/7E5r32G1E1"


                      "2002/8E1r32G1E1"
                      "2002/8E2r32G1E1"
                      "2002/8E3r32G1E1"
                      "2002/8E4r32G1E1"
                      "2002/8E5r32G1E1"

                      "2002/9E1r32G1E1"
                      "2002/9E2r32G1E1"
                      "2002/9E3r32G1E1"
                      "2002/9E4r32G1E1"
                      "2002/9E5r32G1E1"




                      "2002/cv8E1r32G1E1"
                      "2002/cv8E2r32G1E1"
                      "2002/cv8E3r32G1E1"
                      "2002/cv8E4r32G1E1"
                      "2002/cv8E5r32G1E1"

                      "2002/cv9E1r32G1E1"
                      "2002/cv9E2r32G1E1"
                      "2002/cv9E3r32G1E1"
                      "2002/cv9E4r32G1E1"
                      "2002/cv9E5r32G1E1"


                      
                      


                      
                      






                      
                      


 
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    



  
    #Simple Reward 
    


    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_shape "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_shape "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_shape "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_shape "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_shape "


    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_shape --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_shape --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_shape --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_shape --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_shape --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt "


    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_shape --IHPPO "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_shape --IHPPO "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_shape --IHPPO "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_shape --IHPPO "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_shape --IHPPO "


    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_shape --IHPPO --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_shape --IHPPO --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_shape --IHPPO --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_shape --IHPPO --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_shape --IHPPO --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt "



    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_shape --IHPPO --combined_value "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_shape --IHPPO --combined_value "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_shape --IHPPO --combined_value "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_shape --IHPPO --combined_value "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_shape --IHPPO --combined_value "


    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_shape --IHPPO --combined_value --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_shape --IHPPO --combined_value --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_shape --IHPPO --combined_value --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_shape --IHPPO --combined_value --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_shape --IHPPO --combined_value --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt "


    

    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "72:00:00"
done