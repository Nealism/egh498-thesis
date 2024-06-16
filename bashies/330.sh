#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      

                    
                      
                      # #Simple Reward
                      # "329/A1r21G1E3"
                      # "329/A2r21G1E3"
                      # "329/A3r21G1E3"
                      # "329/A4r21G1E3"
                      # "329/A5r21G1E3"
                      
                      




                      # #Step Reward 2
                      # "329/B1r22G1E3"
                      # "329/B2r22G1E3"
                      # "329/B3r22G1E3"
                      # "329/B4r22G1E3"
                      # "329/B5r22G1E3"
                      





                      # #Regular Reward 
                      # "329/C1r23G1E3"
                      # "329/C2r23G1E3"
                      # "329/C3r23G1E3"
                      # "329/C4r23G1E3"
                      # "329/C5r23G1E3"


                      # #Regular Reward 2
                      # "329/D1r24G1E3"
                      # "329/D2r24G1E3"
                      # "329/D3r24G1E3"
                      # "329/D4r24G1E3"
                      # "329/D5r24G1E3"



                      # #Regular Reward 4
                      # "329/E1r25G1E3"
                      # "329/E2r25G1E3"
                      # "329/E3r25G1E3"
                      # "329/E4r25G1E3"
                      # "329/E5r25G1E3"
                      






                      #Regular Reward 3
                      "330/F1r23G1E1"
                      "330/F2r23G1E1"
                      "330/F3r23G1E1"
                      "330/F4r23G1E1"
                      "330/F5r23G1E1"

                      


                      


                      #Unclipped Reward 3
                      "330/G1r24G1E1"
                      "330/G2r24G1E1"
                      "330/G3r24G1E1"
                      "330/G4r24G1E1"
                      "330/G5r24G1E1"


                      


                      #Unclipped Reward 3
                      "330/H1r25G1E1"
                      "330/H2r25G1E1"
                      "330/H3r25G1E1"
                      "330/H4r25G1E1"
                      "330/H5r25G1E1"
                      




                      #Ray Reward 1
                      "330/I1r26G85E1"
                      "330/I2r26G85E1"
                      "330/I3r26G85E1"
                      "330/I4r26G85E1"
                      "330/I5r26G85E1"

                      #Ray Reward 1
                      "330/J1r27G1E1"
                      "330/J2r27G1E1"
                      "330/J3r27G1E1"
                      "330/J4r27G1E1"
                      "330/J5r27G1E1"
                      




                      # #Ray Reward 2
                      # "329/K1r25G1E3"
                      # "329/K2r25G1E3"
                      # "329/K3r25G1E3"
                      # "329/K4r25G1E3"
                      # "329/K5r25G1E3"



                      # #Ray Reward 2
                      # "329/L1r280G1E3"
                      # "329/L2r280G1E3"
                      # "329/L3r280G1E3"
                      # "329/L4r280G1E3"
                      # "329/L5r280G1E3"



                      # #Ray Reward 2
                      # "329/M1r290G1E3"
                      # "329/M2r290G1E3"
                      # "329/M3r290G1E3"
                      # "329/M4r290G1E3"
                      # "329/M5r290G1E3"


                      # #Ray Reward 2
                      # "329/N1r300G1E3"
                      # "329/N2r300G1E3"
                      # "329/N3r300G1E3"
                      # "329/N4r300G1E3"
                      # "329/N5r300G1E3"
                      


 
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    
 



    # #Step Reward 1
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    
    
    
    
    
    
    # #Step Reward 2
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"




    # #Regular Reward 1
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"


    # #Regular Reward 2
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"


    


    

    # #Regular Reward 3
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/G4r25G1E3/2024_06_08_23_29_47/model.pt"

    
    #Regular Reward 4
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/E4r25G1E3_321_25r/2024_06_10_15_05_01/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/E4r25G1E3_321_25r/2024_06_10_15_05_01/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/E4r25G1E3_321_25r/2024_06_10_15_05_01/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/E4r25G1E3_321_25r/2024_06_10_15_05_01/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/E4r25G1E3_321_25r/2024_06_10_15_05_01/model.pt"

    

    


    #Ray Based Reward 1
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/E4r25G1E3_321_25r/2024_06_10_15_05_01/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/E4r25G1E3_321_25r/2024_06_10_15_05_01/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/E4r25G1E3_321_25r/2024_06_10_15_05_01/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/E4r25G1E3_321_25r/2024_06_10_15_05_01/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/E4r25G1E3_321_25r/2024_06_10_15_05_01/model.pt"





    #Ray Based Reward 1
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/E4r25G1E3_321_25r/2024_06_10_15_05_01/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/E4r25G1E3_321_25r/2024_06_10_15_05_01/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/E4r25G1E3_321_25r/2024_06_10_15_05_01/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/E4r25G1E3_321_25r/2024_06_10_15_05_01/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.2 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/E4r25G1E3_321_25r/2024_06_10_15_05_01/model.pt"



    #Regular Reward 3
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Final/F2r23G1E3_Final_329_penal50_complex/2024_06_15_15_08_35/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Final/F2r23G1E3_Final_329_penal50_complex/2024_06_15_15_08_35/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Final/F2r23G1E3_Final_329_penal50_complex/2024_06_15_15_08_35/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Final/F2r23G1E3_Final_329_penal50_complex/2024_06_15_15_08_35/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Final/F2r23G1E3_Final_329_penal50_complex/2024_06_15_15_08_35/model.pt"


    #Regular Reward 3
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Final/F2r23G1E3_Final_329_penal50_complex/2024_06_15_15_08_35/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Final/F2r23G1E3_Final_329_penal50_complex/2024_06_15_15_08_35/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Final/F2r23G1E3_Final_329_penal50_complex/2024_06_15_15_08_35/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Final/F2r23G1E3_Final_329_penal50_complex/2024_06_15_15_08_35/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Final/F2r23G1E3_Final_329_penal50_complex/2024_06_15_15_08_35/model.pt"


    # #Regular Reward 3
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/E4r25G1E3_321_25r/2024_06_10_15_05_01/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/E4r25G1E3_321_25r/2024_06_10_15_05_01/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/E4r25G1E3_321_25r/2024_06_10_15_05_01/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/E4r25G1E3_321_25r/2024_06_10_15_05_01/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.2 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/E4r25G1E3_321_25r/2024_06_10_15_05_01/model.pt"


    
    
    
    
    
    



   
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "96:00:00"
done