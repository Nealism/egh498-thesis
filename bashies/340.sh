#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      

                    
                    

                      
                      #Simple Reward 
                      "340/A1r28G1E1"
                      "340/A2r28G1E1"
                      "340/A3r28G1E1"
                      "340/A4r28G1E1"
                      "340/A5r28G1E1"
                      
                      
                      #Simple Reward 
                      "340/B1r29G1E1"
                      "340/B2r29G1E1"
                      "340/B3r29G1E1"
                      "340/B4r29G1E1"
                      "340/B5r29G1E1"


                      #Simple Reward 
                      "340/C1r30G1E1"
                      "340/C2r30G1E1"
                      "340/C3r30G1E1"
                      "340/C4r30G1E1"
                      "340/C5r30G1E1"
                      
                      


                      #Simple Reward 2
                      "340/D1r31G1E1"
                      "340/D2r31G1E1"
                      "340/D3r31G1E1"
                      "340/D4r31G1E1"
                      "340/D5r31G1E1"



                      #Simple Reward 4
                      "340/E1r32G1E1"
                      "340/E2r32G1E1"
                      "340/E3r32G1E1"
                      "340/E4r32G1E1"
                      "340/E5r32G1E1"


                      #Simple Reward 
                      "340/F1r33G1E1"
                      "340/F2r33G1E1"
                      "340/F3r33G1E1"
                      "340/F4r33G1E1"
                      "340/F5r33G1E1"

                      #Simple Reward 
                      "340/G1r34G1E1"
                      "340/G2r34G1E1"
                      "340/G3r34G1E1"
                      "340/G4r34G1E1"
                      "340/G5r34G1E1"

                      #Simple Reward 
                      "340/H1r35G1E1"
                      "340/H2r35G1E1"
                      "340/H3r35G1E1"
                      "340/H4r35G1E1"
                      "340/H5r35G1E1"

                      #Simple Reward 
                      "340/I1r36G1E1"
                      "340/I2r36G1E1"
                      "340/I3r36G1E1"
                      "340/I4r36G1E1"
                      "340/I5r36G1E1"

                      #Simple Reward 
                      "340/J1r37G1E1"
                      "340/J2r37G1E1"
                      "340/J3r37G1E1"
                      "340/J4r37G1E1"
                      "340/J5r37G1E1"

                      #Simple Reward 
                      "340/K1r38G1E1"
                      "340/K2r38G1E1"
                      "340/K3r38G1E1"
                      "340/K4r38G1E1"
                      "340/K5r38G1E1"

                      #Simple Reward 
                      "340/L1r39G1E1"
                      "340/L2r39G1E1"
                      "340/L3r39G1E1"
                      "340/L4r39G1E1"
                      "340/L5r39G1E1"

                      #Simple Reward 
                      "340/M1r40G1E1"
                      "340/M2r40G1E1"
                      "340/M3r40G1E1"
                      "340/M4r40G1E1"
                      "340/M5r40G1E1"
                      






                      
                      


 
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    




    #Simple Reward 
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    
    
    #Simple Reward 
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"


    #Simple Reward 
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"


    #Simple Reward 
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"


  
    #Simple Reward 
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"


    #Simple Reward 
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 33 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 33 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 33 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 33 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 33 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    
    
    #Simple Reward 
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"


    #Simple Reward 
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 35 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 35 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 35 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 35 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 35 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"


    #Simple Reward 
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 36 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 36 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 36 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 36 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 36 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"


  
    #Simple Reward 
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 37 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 37 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 37 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 37 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 37 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"


    #Simple Reward 
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 38 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 38 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 38 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 38 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 38 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"

    #Simple Reward 
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 39 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 39 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 39 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 39 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 39 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"


    #Simple Reward 
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 40 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 40 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 40 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 40 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    "--cpu 64 --env multi_robot_pb --turtle_titan --num_robots 2 --multi_titans --reward_fn 40 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1 --starting_gap_width 5 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --load_path ~/behaviour_rl/Saved_models/Turtle_titan/D2r31G1E1/2024_07_22_21_03_59/model.pt"
    



    


    
    
    
    
    
    



   
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "96:00:00"
done