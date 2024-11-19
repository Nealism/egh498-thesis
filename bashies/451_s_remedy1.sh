#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(                     
                      
                      

                    
                    

                      
                      



                      #Simple Reward 4
                      "451/E1r10G1E1"
                      "451/E2r10G1E1"
                      "451/E3r10G1E1"
                      "451/E4r10G1E1"
                      "451/E5r10G1E1"


                      # #Simple Reward 
                      # "400/F1r31G1E1"
                      # "400/F2r31G1E1"
                      # "400/F3r31G1E1"
                      # "400/F4r31G1E1"
                      # "400/F5r31G1E1"

                      # #Simple Reward 
                      # "400/G1r34G1E1"
                      # "400/G2r34G1E1"
                      # "400/G3r34G1E1"
                      # "400/G4r34G1E1"
                      # "400/G5r34G1E1"

                      # #Simple Reward 
                      # "400/H1r35G1E1"
                      # "400/H2r35G1E1"
                      # "400/H3r35G1E1"
                      # "400/H4r35G1E1"
                      # "400/H5r35G1E1"

                      # #Simple Reward 
                      # "400/I1r36G1E1"
                      # "400/I2r36G1E1"
                      # "400/I3r36G1E1"
                      # "400/I4r36G1E1"
                      # "400/I5r36G1E1"

                      # #Simple Reward 
                      # "400/J1r37G1E1"
                      # "400/J2r37G1E1"
                      # "400/J3r37G1E1"
                      # "400/J4r37G1E1"
                      # "400/J5r37G1E1"

                      # #Simple Reward 
                      # "400/K1r38G1E1"
                      # "400/K2r38G1E1"
                      # "400/K3r38G1E1"
                      # "400/K4r38G1E1"
                      # "400/K5r38G1E1"

                      # #Simple Reward 
                      # "400/L1r39G1E1"
                      # "400/L2r39G1E1"
                      # "400/L3r39G1E1"
                      # "400/L4r39G1E1"
                      # "400/L5r39G1E1"

                      # #Simple Reward 
                      # "400/M1r40G1E1"
                      # "400/M2r40G1E1"
                      # "400/M3r40G1E1"
                      # "400/M4r40G1E1"
                      # "400/M5r40G1E1"
                      






                      
                      


 
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    




    #Simple Reward 
    "--cpu 64 --env multi_robot_pb --num_robots 1 --multi_titans --turtle_titan --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2   --noise_mixed  "
    "--cpu 64 --env multi_robot_pb --num_robots 1 --multi_titans --turtle_titan --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2   --noise_mixed  "
    "--cpu 64 --env multi_robot_pb --num_robots 1 --multi_titans --turtle_titan --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2   --noise_mixed  "
    "--cpu 64 --env multi_robot_pb --num_robots 1 --multi_titans --turtle_titan --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2   --noise_mixed  "
    "--cpu 64 --env multi_robot_pb --num_robots 1 --multi_titans --turtle_titan --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0.1 --starting_gap_width 2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2   --noise_mixed  "
    
    
    # #Simple Reward 
    # "--cpu 64 --env multi_robot_pb --num_robots 1 --multi_titans --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1 --final_gap_width 0.8  --experiment_1  --ray_wall_type 1 --randomness 1 "
    # "--cpu 64 --env multi_robot_pb --num_robots 1 --multi_titans --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1 --final_gap_width 0.8  --experiment_1  --ray_wall_type 1 --randomness 1 "
    # "--cpu 64 --env multi_robot_pb --num_robots 1 --multi_titans --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1 --final_gap_width 0.8  --experiment_1  --ray_wall_type 1 --randomness 1 "
    # "--cpu 64 --env multi_robot_pb --num_robots 1 --multi_titans --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1 --final_gap_width 0.8  --experiment_1  --ray_wall_type 1 --randomness 1 "
    # "--cpu 64 --env multi_robot_pb --num_robots 1 --multi_titans --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1 --final_gap_width 0.8  --experiment_1  --ray_wall_type 1 --randomness 1 "

    # #Simple Reward 
    # "--cpu 64 --env multi_robot_pb --num_robots 1 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.8 --final_gap_width 0.8  --experiment_1  --ray_wall_type 1 --randomness 1 "
    # "--cpu 64 --env multi_robot_pb --num_robots 1 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.8 --final_gap_width 0.8  --experiment_1  --ray_wall_type 1 --randomness 1 "
    # "--cpu 64 --env multi_robot_pb --num_robots 1 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.8 --final_gap_width 0.8  --experiment_1  --ray_wall_type 1 --randomness 1 "
    # "--cpu 64 --env multi_robot_pb --num_robots 1 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.8 --final_gap_width 0.8  --experiment_1  --ray_wall_type 1 --randomness 1 "
    # "--cpu 64 --env multi_robot_pb --num_robots 1 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 0.8 --final_gap_width 0.8  --experiment_1  --ray_wall_type 1 --randomness 1 "
    
    
    # #Simple Reward 
    # "--cpu 64 --env multi_robot_pb --num_robots 1 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1 --final_gap_width 0.8  --experiment_1  --ray_wall_type 1 --randomness 1 "
    # "--cpu 64 --env multi_robot_pb --num_robots 1 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1 --final_gap_width 0.8  --experiment_1  --ray_wall_type 1 --randomness 1 "
    # "--cpu 64 --env multi_robot_pb --num_robots 1 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1 --final_gap_width 0.8  --experiment_1  --ray_wall_type 1 --randomness 1 "
    # "--cpu 64 --env multi_robot_pb --num_robots 1 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1 --final_gap_width 0.8  --experiment_1  --ray_wall_type 1 --randomness 1 "
    # "--cpu 64 --env multi_robot_pb --num_robots 1 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1 --final_gap_width 0.8  --experiment_1  --ray_wall_type 1 --randomness 1 "

    # #Simple Reward 
    # "--cpu 64 --env multi_robot_pb --num_robots 1 --multi_titans --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 1 "
    # "--cpu 64 --env multi_robot_pb --num_robots 1 --multi_titans --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 1 "
    # "--cpu 64 --env multi_robot_pb --num_robots 1 --multi_titans --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 1 "
    # "--cpu 64 --env multi_robot_pb --num_robots 1 --multi_titans --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 1 "
    # "--cpu 64 --env multi_robot_pb --num_robots 1 --multi_titans --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 1 "
    
    
    # #Simple Reward 
    # "--cpu 64 --env multi_robot_pb --num_robots 1 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 1 "
    # "--cpu 64 --env multi_robot_pb --num_robots 1 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 1 "
    # "--cpu 64 --env multi_robot_pb --num_robots 1 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 1 "
    # "--cpu 64 --env multi_robot_pb --num_robots 1 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 1 "
    # "--cpu 64 --env multi_robot_pb --num_robots 1 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --gap_curr  --gap_decrease 0 --starting_gap_width 1 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 1 "


    # #Simple Reward 
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "


    # #Simple Reward 
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "


  
    # #Simple Reward 
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "


    # #Simple Reward 
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 33 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 33 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 33 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 33 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 33 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    
    
    # #Simple Reward 
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "


    # #Simple Reward 
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 35 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 35 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 35 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 35 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 35 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "


    # #Simple Reward 
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 36 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 36 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 36 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 36 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 36 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "


  
    # #Simple Reward 
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 37 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 37 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 37 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 37 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 37 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "


    # #Simple Reward 
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 38 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 38 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 38 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 38 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 38 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "

    # #Simple Reward 
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 39 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 39 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 39 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 39 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 39 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "


    # #Simple Reward 
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 40 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 40 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 40 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 40 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 40 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    



    


    
    
    
    
    
    



   
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "48:00:00"
done