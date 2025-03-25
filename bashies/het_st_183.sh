#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      

                    
                    

                      
 



                      #Multi Titan Homogeneous Model Check with Rotated Robot ORN in MAP but exp 0 with 4 obs --behaviour_cloning 0.25 Continue Training through 0.85 GAp
                      "200183/E1r32G1E1"
                      "200183/E2r32G1E1"
                      "200183/E3r32G1E1"
                      "200183/E4r32G1E1"
                      "200183/E5r32G1E1"
                      "200183/E6r32G1E1"
                      "200183/E7r32G1E1"
                      "200183/E8r32G1E1"
                      "200183/E9r32G1E1"
                      "200183/E10r32G1E1"
                      "200183/E11r32G1E1"
                      "200183/E12r32G1E1"
                      "200183/E13r32G1E1"
                      "200183/E14r32G1E1"
                      "200183/E15r32G1E1"
                      


                      
                      






                      
                      


 
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    



  
    #Simple Reward 
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_0  --ray_wall_type 1 --randomness 2 --rand_gap_cur  --load_path /scratch3/kom018/results/multi_robot_pb/200145/E1r32G1E1/2025_03_20_15_32_16/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_0  --ray_wall_type 1 --randomness 2 --rand_gap_cur  --load_path /scratch3/kom018/results/multi_robot_pb/200145/E2r32G1E1/2025_03_20_15_32_16/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_0  --ray_wall_type 1 --randomness 2 --rand_gap_cur  --load_path /scratch3/kom018/results/multi_robot_pb/200145/E3r32G1E1/2025_03_20_09_38_59/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_0  --ray_wall_type 1 --randomness 2 --rand_gap_cur  --load_path /scratch3/kom018/results/multi_robot_pb/200145/E4r32G1E1/2025_03_20_15_32_16/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_0  --ray_wall_type 1 --randomness 2 --rand_gap_cur  --load_path /scratch3/kom018/results/multi_robot_pb/200145/E5r32G1E1/2025_03_20_03_45_10/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_0  --ray_wall_type 1 --randomness 2 --rand_gap_cur  --load_path /scratch3/kom018/results/multi_robot_pb/200145/E6r32G1E1/2025_03_20_15_32_14/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_0  --ray_wall_type 1 --randomness 2 --rand_gap_cur  --load_path /scratch3/kom018/results/multi_robot_pb/200145/E7r32G1E1/2025_03_20_15_01_29/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_0  --ray_wall_type 1 --randomness 2 --rand_gap_cur  --load_path /scratch3/kom018/results/multi_robot_pb/200145/E8r32G1E1/2025_03_20_15_32_13/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_0  --ray_wall_type 1 --randomness 2 --rand_gap_cur  --load_path /scratch3/kom018/results/multi_robot_pb/200145/E9r32G1E1/2025_03_20_15_32_15/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_0  --ray_wall_type 1 --randomness 2 --rand_gap_cur  --load_path /scratch3/kom018/results/multi_robot_pb/200145/E10r32G1E1/2025_03_20_06_26_20/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_0  --ray_wall_type 1 --randomness 2 --rand_gap_cur  --load_path /scratch3/kom018/results/multi_robot_pb/200145/E11r32G1E1/2025_03_20_09_40_34/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_0  --ray_wall_type 1 --randomness 2 --rand_gap_cur  --load_path /scratch3/kom018/results/multi_robot_pb/200145/E12r32G1E1/2025_03_20_12_21_18/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_0  --ray_wall_type 1 --randomness 2 --rand_gap_cur  --load_path /scratch3/kom018/results/multi_robot_pb/200145/E13r32G1E1/2025_03_20_15_32_15/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_0  --ray_wall_type 1 --randomness 2 --rand_gap_cur  --load_path /scratch3/kom018/results/multi_robot_pb/200145/E14r32G1E1/2025_03_20_15_32_15/model.pt "
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 650 --max_ep_len 350 --local_epoch_len 1750  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0 --starting_gap_width 0.85 --final_gap_width 0.85  --experiment_0  --ray_wall_type 1 --randomness 2 --rand_gap_cur  --load_path /scratch3/kom018/results/multi_robot_pb/200145/E15r32G1E1/2025_03_20_15_11_08/model.pt "

    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "24:00:00"
done