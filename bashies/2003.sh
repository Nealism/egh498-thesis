#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      

                    
                    

                      
 



                      #Simple Reward 4
                      


                      "2003/10E1r32G1E1"
                      "2003/10E2r32G1E1"
                      "2003/10E3r32G1E1"
                      "2003/10E4r32G1E1"
                      "2003/10E5r32G1E1"

                      "2003/11E1r32G1E1"
                      "2003/11E2r32G1E1"
                      "2003/11E3r32G1E1"
                      "2003/11E4r32G1E1"
                      "2003/11E5r32G1E1"


                      "2003/12E1r32G1E1"
                      "2003/12E2r32G1E1"
                      "2003/12E3r32G1E1"
                      "2003/12E4r32G1E1"
                      "2003/12E5r32G1E1"

                      "2003/13E1r32G1E1"
                      "2003/13E2r32G1E1"
                      "2003/13E3r32G1E1"
                      "2003/13E4r32G1E1"
                      "2003/13E5r32G1E1"




                      "2003/cv12E1r32G1E1"
                      "2003/cv12E2r32G1E1"
                      "2003/cv12E3r32G1E1"
                      "2003/cv12E4r32G1E1"
                      "2003/cv12E5r32G1E1"

                      "2003/cv13E1r32G1E1"
                      "2003/cv13E2r32G1E1"
                      "2003/cv13E3r32G1E1"
                      "2003/cv13E4r32G1E1"
                      "2003/cv13E5r32G1E1"


                      
                      


                      
                      






                      
                      


 
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    



  
    #Simple Reward 
    


    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_TITAN "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_TITAN "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_TITAN "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_TITAN "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_TITAN "


    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_TITAN --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_TITAN --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_TITAN --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_TITAN --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_TITAN --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt "


    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_TITAN --IHPPO "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_TITAN --IHPPO "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_TITAN --IHPPO "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_TITAN --IHPPO "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_TITAN --IHPPO "


    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_TITAN --IHPPO --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_TITAN --IHPPO --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_TITAN --IHPPO --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_TITAN --IHPPO --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_TITAN --IHPPO --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt "



    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_TITAN --IHPPO --combined_value "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_TITAN --IHPPO --combined_value "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_TITAN --IHPPO --combined_value "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_TITAN --IHPPO --combined_value "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_TITAN --IHPPO --combined_value "


    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_TITAN --IHPPO --combined_value --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_TITAN --IHPPO --combined_value --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_TITAN --IHPPO --combined_value --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_TITAN --IHPPO --combined_value --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 700 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2 --heterogeneous_DTR_TITAN --IHPPO --combined_value --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt "


    

    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "72:00:00"
done