#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      

                    
                    

                      
 



                      #Multi Titan Homogeneous Model Check with Rotated Robot ORN in MAP but exp 0 with 4 obs --behaviour_cloning 0.50 Continue Training through GAp
                      "200163/E1r32G1E1"
                      "200163/E2r32G1E1"
                      "200163/E3r32G1E1"
                      "200163/E4r32G1E1"
                      "200163/E5r32G1E1"
                      "200163/E6r32G1E1"
                      "200163/E7r32G1E1"
                      "200163/E8r32G1E1"
                      "200163/E9r32G1E1"
                      "200163/E10r32G1E1"
                      "200163/E11r32G1E1"
                      "200163/E12r32G1E1"
                      "200163/E13r32G1E1"
                      "200163/E14r32G1E1"
                      "200163/E15r32G1E1"
                      


                      
                      






                      
                      


 
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    



  
    #Simple Reward 
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200146/E1r32G1E1/2025_03_20_12_20_33/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200146/E2r32G1E1/2025_03_20_15_32_52/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200146/E3r32G1E1/2025_03_20_15_32_16/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200146/E4r32G1E1/2025_03_20_15_11_55/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200146/E5r32G1E1/2025_03_20_15_33_28/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200146/E6r32G1E1/2025_03_20_13_16_20/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200146/E7r32G1E1/2025_03_20_02_57_08/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200146/E8r32G1E1/2025_03_20_00_24_47/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200146/E9r32G1E1/2025_03_20_02_29_41/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200146/E10r32G1E1/2025_03_19_23_48_01/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200146/E11r32G1E1/2025_03_20_19_43_57/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200146/E12r32G1E1/2025_03_20_15_47_59/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200146/E13r32G1E1/2025_03_20_15_36_11/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200146/E14r32G1E1/2025_03_20_16_06_21/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200146/E15r32G1E1/2025_03_20_15_54_35/model.pt "

    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "24:00:00"
done