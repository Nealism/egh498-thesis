#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      

                    
                      
                      #Step Reward
                      "315/A1r21G1E3"
                      "315/A2r21G1E3"
                      "315/A3r21G1E3"
                      "315/A4r21G1E3"
                      "315/A5r21G1E3"
                      
                      




                      #Step Reward 2
                      "315/B1r22G1E3"
                      "315/B2r22G1E3"
                      "315/B3r22G1E3"
                      "315/B4r22G1E3"
                      "315/B5r22G1E3"
                      





                      #Regular Reward 
                      "315/C1r23G1E3"
                      "315/C2r23G1E3"
                      "315/C3r23G1E3"
                      "315/C4r23G1E3"
                      "315/C5r23G1E3"


                      #Regular Reward 2
                      "315/CA1r24G1E3"
                      "315/CA2r24G1E3"
                      "315/CA3r24G1E3"
                      "315/CA4r24G1E3"
                      "315/CA5r24G1E3"



                      #Regular Reward 4
                      "315/CB1r26G1E3"
                      "315/CB2r26G1E3"
                      "315/CB3r26G1E3"
                      "315/CB4r26G1E3"
                      "315/CB5r26G1E3"
                      






                      #Regular Reward 3
                      "315/D1r25G1E3"
                      "315/D2r25G1E3"
                      "315/D3r25G1E3"
                      "315/D4r25G1E3"
                      "315/D5r25G1E3"

                      #Regular Reward 3
                      "315/Vs1r25G1E3"
                      "315/Vs2r25G1E3"
                      "315/Vs3r25G1E3"
                      "315/Vs4r25G1E3"
                      "315/Vs5r25G1E3"


                      #Unclipped Reward 3
                      "315/U1r25G1E3"
                      "315/U2r25G1E3"
                      "315/U3r25G1E3"
                      "315/U4r25G1E3"
                      "315/U5r25G1E3"


                      #Unclipped Reward 3
                      "315/G1r25G1E3"
                      "315/G2r25G1E3"
                      "315/G3r25G1E3"
                      "315/G4r25G1E3"
                      "315/G5r25G1E3"


                      #Unclipped Reward 3
                      "315/GC1r250G1E3"
                      "315/GC2r250G1E3"
                      "315/GC3r250G1E3"
                      "315/GC4r250G1E3"
                      "315/GC5r250G1E3"
                      




                      #Ray Reward 1
                      "315/E1r27G1E3"
                      "315/E2r27G1E3"
                      "315/E3r27G1E3"
                      "315/E4r27G1E3"
                      "315/E5r27G1E3"

                      #Ray Reward 1
                      "315/NR1r28G1E3"
                      "315/NR2r28G1E3"
                      "315/NR3r28G1E3"
                      "315/NR4r28G1E3"
                      "315/NR5r28G1E3"
                      




                      #Ray Reward 2
                      "315/F1r29G1E3"
                      "315/F2r29G1E3"
                      "315/F3r29G1E3"
                      "315/F4r29G1E3"
                      "315/F5r29G1E3"
                      


 
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    
 



    #Step Reward 1
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    
    
    
    
    
    
    #Step Reward 2
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"




    #Regular Reward 1
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"


    #Regular Reward 2
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"


    #Regular Reward 4
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"


    #Regular Reward 3
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 250 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 250 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 250 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 250 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 250 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"

    #Regular Reward 3
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"

    #Unclipped Vel Regular Reward 3
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt --unclipped_vel"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt --unclipped_vel"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt --unclipped_vel"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt --unclipped_vel"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt --unclipped_vel"


    #Unclipped Vel Regular Reward 3
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt --unclipped_vel --gausian_clip"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt --unclipped_vel --gausian_clip"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt --unclipped_vel --gausian_clip"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt --unclipped_vel --gausian_clip"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt --unclipped_vel --gausian_clip"

    #Regular Reward 3
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 250 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt --unclipped_vel --gausian_clip"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 250 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt --unclipped_vel --gausian_clip"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 250 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt --unclipped_vel --gausian_clip"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 250 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt --unclipped_vel --gausian_clip"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 250 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt --unclipped_vel --gausian_clip"


    #Ray Based Reward 1
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"


    #Ray Based Reward 1
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"




    #Ray Based Reward 1
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 350 --local_epoch_len 3500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 10 --final_gap_width 10  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/D1r25G1E3/2024_05_31_22_22_17/model.pt"
    
    
    
    
    



   
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "96:00:00"
done