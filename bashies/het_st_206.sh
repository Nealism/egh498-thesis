#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      

                    
                    

                      
 



                      #Multi Titan Homogeneous Model Check with Rotated Robot ORN in MAP but exp 0 with 4 obs --Behaviour Cloning Continue Training through 0.85 GAp, gap cur and random gap
                      "200206/E1r32G1E1"
                      "200206/E2r32G1E1"
                      "200206/E3r32G1E1"
                      "200206/E4r32G1E1"
                      "200206/E5r32G1E1"
                      "200206/E6r32G1E1"
                      "200206/E7r32G1E1"
                      "200206/E8r32G1E1"
                      "200206/E9r32G1E1"
                      "200206/E10r32G1E1"
                      "200206/E11r32G1E1"
                      "200206/E12r32G1E1"
                      "200206/E13r32G1E1"
                      "200206/E14r32G1E1"
                      "200206/E15r32G1E1"
                      


                      
                      






                      
                      


 
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    



  
    #Simple Reward 
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200203/E1r32G1E1/2025_04_04_04_19_17/model_49.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200203/E2r32G1E1/2025_04_04_04_24_19/model_49.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200203/E3r32G1E1/2025_04_04_04_25_37/model_49.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200203/E4r32G1E1/2025_04_04_04_42_40/model_49.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200203/E5r32G1E1/2025_04_04_04_24_22/model_99.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200203/E6r32G1E1/2025_04_04_05_36_54/model_82.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200203/E7r32G1E1/2025_04_04_05_38_53/model_99.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200203/E8r32G1E1/2025_04_04_05_17_42/model_162.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200203/E9r32G1E1/2025_04_04_04_51_50/model_96.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200203/E10r32G1E1/2025_04_04_05_08_36/model_171.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 0.85 --gap_random  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200203/E11r32G1E1/2025_04_04_04_26_53/model_123.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 0.85 --gap_random  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200203/E12r32G1E1/2025_04_04_05_38_54/model_71.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 0.85 --gap_random  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200203/E13r32G1E1/2025_04_04_05_37_55/model_160.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 0.85 --gap_random  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200203/E14r32G1E1/2025_04_04_05_09_03/model_90.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 2 --final_gap_width 0.85 --gap_random  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path /scratch3/kom018/results/multi_robot_pb/200203/E15r32G1E1/2025_04_04_05_38_24/model_62.pt "

    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "24:00:00"
done