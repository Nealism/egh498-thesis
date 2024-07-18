#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(                    
                      
                      

                    
                    

                      
                      #Simple Reward 
                      "334/A1r28G1E1"
                      "334/A2r28G1E1"
                      "334/A3r28G1E1"
                      "334/A4r28G1E1"
                      "334/A5r28G1E1"
                      
                      
                      #Simple Reward 
                      "334/B1r29G1E1"
                      "334/B2r29G1E1"
                      "334/B3r29G1E1"
                      "334/B4r29G1E1"
                      "334/B5r29G1E1"


                      # #Simple Reward 
                      # "334/C1r30G1E1"
                      # "334/C2r30G1E1"
                      # "334/C3r30G1E1"
                      # "334/C4r30G1E1"
                      # "334/C5r30G1E1"
                      
                      


                      # #Simple Reward 2
                      # "334/D1r31G1E1"
                      # "334/D2r31G1E1"
                      # "334/D3r31G1E1"
                      # "334/D4r31G1E1"
                      # "334/D5r31G1E1"



                      # #Simple Reward 4
                      # "334/E1r32G1E1"
                      # "334/E2r32G1E1"
                      # "334/E3r32G1E1"
                      # "334/E4r32G1E1"
                      # "334/E5r32G1E1"


                      # #Simple Reward 
                      # "334/F1r33G1E1"
                      # "334/F2r33G1E1"
                      # "334/F3r33G1E1"
                      # "334/F4r33G1E1"
                      # "334/F5r33G1E1"

                      # #Simple Reward 
                      # "334/G1r34G1E1"
                      # "334/G2r34G1E1"
                      # "334/G3r34G1E1"
                      # "334/G4r34G1E1"
                      # "334/G5r34G1E1"

                      # #Simple Reward 
                      # "334/H1r35G1E1"
                      # "334/H2r35G1E1"
                      # "334/H3r35G1E1"
                      # "334/H4r35G1E1"
                      # "334/H5r35G1E1"

                      # #Simple Reward 
                      # "334/I1r36G1E1"
                      # "334/I2r36G1E1"
                      # "334/I3r36G1E1"
                      # "334/I4r36G1E1"
                      # "334/I5r36G1E1"

                      # #Simple Reward 
                      # "334/J1r37G1E1"
                      # "334/J2r37G1E1"
                      # "334/J3r37G1E1"
                      # "334/J4r37G1E1"
                      # "334/J5r37G1E1"

                      # #Simple Reward 
                      # "334/K1r38G1E1"
                      # "334/K2r38G1E1"
                      # "334/K3r38G1E1"
                      # "334/K4r38G1E1"
                      # "334/K5r38G1E1"

                      # #Simple Reward 
                      # "334/L1r39G1E1"
                      # "334/L2r39G1E1"
                      # "334/L3r39G1E1"
                      # "334/L4r39G1E1"
                      # "334/L5r39G1E1"

                      # #Simple Reward 
                      # "334/M1r40G1E1"
                      # "334/M2r40G1E1"
                      # "334/M3r40G1E1"
                      # "334/M4r40G1E1"
                      # "334/M5r40G1E1"
                      






                      
                      


 
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    




    #Simple Reward 
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    
    
    #Simple Reward 
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr  --MA_bootstrap --gap_curr  --gap_decrease 0 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2 "


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
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "96:00:00"
done