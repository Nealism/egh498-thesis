#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      

                    
                    

                      
 



                      #Multi Titan Homogeneous Model Check with Rotated Robot ORN in MAP but exp 0 with 4 obs --behaviour_cloning 1 Continue Training through GAp
                      "200160/E1r32G1E1"
                      "200160/E2r32G1E1"
                      "200160/E3r32G1E1"
                      "200160/E4r32G1E1"
                      "200160/E5r32G1E1"
                      "200160/E6r32G1E1"
                      "200160/E7r32G1E1"
                      "200160/E8r32G1E1"
                      "200160/E9r32G1E1"
                      "200160/E10r32G1E1"
                      "200160/E11r32G1E1"
                      "200160/E12r32G1E1"
                      "200160/E13r32G1E1"
                      "200160/E14r32G1E1"
                      "200160/E15r32G1E1"
                      


                      
                      






                      
                      


 
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    



  
    #Simple Reward 
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200143/E1r32G1E1/2025_03_20_14_42_55/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200143/E2r32G1E1/2025_03_20_15_11_55/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200143/E3r32G1E1/2025_03_20_13_11_10/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200143/E4r32G1E1/2025_03_20_04_36_38/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200143/E5r32G1E1/2025_03_20_09_39_45/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200143/E6r32G1E1/2025_03_20_01_13_32/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200143/E7r32G1E1/2025_03_19_23_10_22/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200143/E8r32G1E1/2025_03_20_09_22_10/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200143/E9r32G1E1/2025_03_20_09_39_46/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200143/E10r32G1E1/2025_03_20_08_57_26/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200143/E11r32G1E1/2025_03_20_05_15_42/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200143/E12r32G1E1/2025_03_20_01_13_32/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200143/E13r32G1E1/2025_03_20_05_30_52/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200143/E14r32G1E1/2025_03_19_23_14_51/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_0  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200143/E15r32G1E1/2025_03_20_09_39_02/model.pt "

    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "24:00:00"
done