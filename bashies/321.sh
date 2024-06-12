#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      

                    
                      
                      #Simple Reward
                      "321/A1r21G1E3"
                      "321/A2r21G1E3"
                      "321/A3r21G1E3"
                      "321/A4r21G1E3"
                      "321/A5r21G1E3"
                      
                      




                      #Step Reward 2
                      "321/B1r22G1E3"
                      "321/B2r22G1E3"
                      "321/B3r22G1E3"
                      "321/B4r22G1E3"
                      "321/B5r22G1E3"
                      





                      #Regular Reward 
                      "321/C1r23G1E3"
                      "321/C2r23G1E3"
                      "321/C3r23G1E3"
                      "321/C4r23G1E3"
                      "321/C5r23G1E3"


                      #Regular Reward 2
                      "321/D1r24G1E3"
                      "321/D2r24G1E3"
                      "321/D3r24G1E3"
                      "321/D4r24G1E3"
                      "321/D5r24G1E3"



                      #Regular Reward 4
                      "321/E1r25G1E3"
                      "321/E2r25G1E3"
                      "321/E3r25G1E3"
                      "321/E4r25G1E3"
                      "321/E5r25G1E3"
                      






                      #Regular Reward 3
                      "321/F1r26G1E3"
                      "321/F2r26G1E3"
                      "321/F3r26G1E3"
                      "321/F4r26G1E3"
                      "321/F5r26G1E3"

                      


                      


                      #Unclipped Reward 3
                      "321/G1r27G1E3"
                      "321/G2r27G1E3"
                      "321/G3r27G1E3"
                      "321/G4r27G1E3"
                      "321/G5r27G1E3"


                      


                      #Unclipped Reward 3
                      "321/H1r29G1E3"
                      "321/H2r29G1E3"
                      "321/H3r29G1E3"
                      "321/H4r29G1E3"
                      "321/H5r29G1E3"
                      




                      #Ray Reward 1
                      "321/I1r250G1E3"
                      "321/I2r250G1E3"
                      "321/I3r250G1E3"
                      "321/I4r250G1E3"
                      "321/I5r250G1E3"

                      #Ray Reward 1
                      "321/J1r260G1E3"
                      "321/J2r260G1E3"
                      "321/J3r260G1E3"
                      "321/J4r260G1E3"
                      "321/J5r260G1E3"
                      




                      #Ray Reward 2
                      "321/K1r270G1E3"
                      "321/K2r270G1E3"
                      "321/K3r270G1E3"
                      "321/K4r270G1E3"
                      "321/K5r270G1E3"



                      #Ray Reward 2
                      "321/L1r280G1E3"
                      "321/L2r280G1E3"
                      "321/L3r280G1E3"
                      "321/L4r280G1E3"
                      "321/L5r280G1E3"



                      #Ray Reward 2
                      "321/M1r290G1E3"
                      "321/M2r290G1E3"
                      "321/M3r290G1E3"
                      "321/M4r290G1E3"
                      "321/M5r290G1E3"


                      #Ray Reward 2
                      "321/N1r300G1E3"
                      "321/N2r300G1E3"
                      "321/N3r300G1E3"
                      "321/N4r300G1E3"
                      "321/N5r300G1E3"
                      


 
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    
 



    #Step Reward 1
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    
    
    
    
    
    
    #Step Reward 2
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"




    #Regular Reward 1
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"


    #Regular Reward 2
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"


    


    

    #Regular Reward 3
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"

    
    #Regular Reward 4
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"

    

    


    #Ray Based Reward 1
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"





    #Ray Based Reward 1
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"



    #Regular Reward 3
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 250 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 250 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 250 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 250 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 250 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"


    #Regular Reward 3
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 260 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 260 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 260 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 260 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 260 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"


    #Regular Reward 3
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 270 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 270 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 270 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 270 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 270 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"


    #Regular Reward 3
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 280 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 280 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 280 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 280 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 280 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"


    #Regular Reward 3
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 290 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 290 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 290 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 290 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 290 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"


    #Regular Reward 3
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 300 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 300 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 300 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 300 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 300 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    
    
    
    
    



   
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "96:00:00"
done