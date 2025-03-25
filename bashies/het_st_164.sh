#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      

                    
                    

                      
 



                      #Multi Titan Homogeneous Model Check with Rotated Robot ORN in MAP but exp 0 with 4 obs --behaviour_cloning 0.75 Continue Training through GAp
                      "200164/E1r32G1E1"
                      "200164/E2r32G1E1"
                      "200164/E3r32G1E1"
                      "200164/E4r32G1E1"
                      "200164/E5r32G1E1"
                      "200164/E6r32G1E1"
                      "200164/E7r32G1E1"
                      "200164/E8r32G1E1"
                      "200164/E9r32G1E1"
                      "200164/E10r32G1E1"
                      "200164/E11r32G1E1"
                      "200164/E12r32G1E1"
                      "200164/E13r32G1E1"
                      "200164/E14r32G1E1"
                      "200164/E15r32G1E1"
                      


                      
                      






                      
                      


 
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    



  
    #Simple Reward 
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200147/E1r32G1E1/2025_03_20_18_16_55/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200147/E2r32G1E1/2025_03_20_16_06_19/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200147/E3r32G1E1/2025_03_20_16_13_44/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200147/E4r32G1E1/2025_03_20_16_07_02/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200147/E5r32G1E1/2025_03_20_22_47_21/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200147/E6r32G1E1/2025_03_20_21_36_06/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200147/E7r32G1E1/2025_03_20_21_22_57/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200147/E8r32G1E1/2025_03_20_21_27_34/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200147/E9r32G1E1/2025_03_20_20_57_11/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200147/E10r32G1E1/2025_03_20_20_47_32/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200147/E11r32G1E1/2025_03_20_18_45_02/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200147/E12r32G1E1/2025_03_20_19_07_41/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200147/E13r32G1E1/2025_03_20_18_40_51/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200147/E14r32G1E1/2025_03_20_19_25_37/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200147/E15r32G1E1/2025_03_20_19_24_48/model.pt "

    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "24:00:00"
done