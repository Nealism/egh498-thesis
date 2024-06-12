#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      

                    
                      
                      #Simple Reward
                      "322/A1r29G1E3"
                      "322/A2r29G1E3"
                      "322/A3r29G1E3"
                      "322/A4r29G1E3"
                      "322/A5r29G1E3"
                      
                      




                      #Step Reward 2
                      "322/B1r29G85E3"
                      "322/B2r29G85E3"
                      "322/B3r29G85E3"
                      "322/B4r29G85E3"
                      "322/B5r29G85E3"
                      





                      #Regular Reward 
                      "322/C1r27G1E3"
                      "322/C2r27G1E3"
                      "322/C3r27G1E3"
                      "322/C4r27G1E3"
                      "322/C5r27G1E3"


                      #Regular Reward 2
                      "322/D1r27G85E3"
                      "322/D2r27G85E3"
                      "322/D3r27G85E3"
                      "322/D4r27G85E3"
                      "322/D5r27G85E3"



                      #Regular Reward 4
                      "322/E1r27G1E3SD"
                      "322/E2r27G1E3SD"
                      "322/E3r27G1E3SD"
                      "322/E4r27G1E3SD"
                      "322/E5r27G1E3SD"
                      






                      #Regular Reward 3
                      "322/F1r27G85E3SD"
                      "322/F2r27G85E3SD"
                      "322/F3r27G85E3SD"
                      "322/F4r27G85E3SD"
                      "322/F5r27G85E3SD"

                      


                      


                      # #Unclipped Reward 3
                      # "322/G1r27G1E3"
                      # "322/G2r27G1E3"
                      # "322/G3r27G1E3"
                      # "322/G4r27G1E3"
                      # "322/G5r27G1E3"


                      


                      # #Unclipped Reward 3
                      # "322/H1r29G1E3"
                      # "322/H2r29G1E3"
                      # "322/H3r29G1E3"
                      # "322/H4r29G1E3"
                      # "322/H5r29G1E3"
                      




                      # #Ray Reward 1
                      # "322/I1r250G1E3"
                      # "322/I2r250G1E3"
                      # "322/I3r250G1E3"
                      # "322/I4r250G1E3"
                      # "322/I5r250G1E3"

                      # #Ray Reward 1
                      # "322/J1r260G1E3"
                      # "322/J2r260G1E3"
                      # "322/J3r260G1E3"
                      # "322/J4r260G1E3"
                      # "322/J5r260G1E3"
                      




                      # #Ray Reward 2
                      # "322/K1r270G1E3"
                      # "322/K2r270G1E3"
                      # "322/K3r270G1E3"
                      # "322/K4r270G1E3"
                      # "322/K5r270G1E3"



                      # #Ray Reward 2
                      # "322/L1r280G1E3"
                      # "322/L2r280G1E3"
                      # "322/L3r280G1E3"
                      # "322/L4r280G1E3"
                      # "322/L5r280G1E3"



                      # #Ray Reward 2
                      # "322/M1r290G1E3"
                      # "322/M2r290G1E3"
                      # "322/M3r290G1E3"
                      # "322/M4r290G1E3"
                      # "322/M5r290G1E3"


                      # #Ray Reward 2
                      # "322/N1r300G1E3"
                      # "322/N2r300G1E3"
                      # "322/N3r300G1E3"
                      # "322/N4r300G1E3"
                      # "322/N5r300G1E3"
                      


 
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    
 



    #Step Reward 1
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.01 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.01 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.01 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.01 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.01 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    
    
    
    
    
    
    #Step Reward 2
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.001 --starting_gap_width 1.8 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.001 --starting_gap_width 1.8 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.001 --starting_gap_width 1.8 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.001 --starting_gap_width 1.8 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.001 --starting_gap_width 1.8 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"




    #Regular Reward 1
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.01 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.01 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.01 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.01 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.01 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"


    #Regular Reward 2
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.001 --starting_gap_width 1.8 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.001 --starting_gap_width 1.8 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.001 --starting_gap_width 1.8 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.001 --starting_gap_width 1.8 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.001 --starting_gap_width 1.8 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"


    


    

    #Regular Reward 3
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.01 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt --single_done"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.01 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt --single_done"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.01 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt --single_done"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.01 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt --single_done"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.01 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt --single_done"

    
    #Regular Reward 4
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.001 --starting_gap_width 1.8 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt --single_done"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.001 --starting_gap_width 1.8 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt --single_done"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.001 --starting_gap_width 1.8 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt --single_done"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.001 --starting_gap_width 1.8 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt --single_done"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.001 --starting_gap_width 1.8 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt --single_done"

    

    


    # #Ray Based Reward 1
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"





    # #Ray Based Reward 1
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"



    # #Regular Reward 3
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 250 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 250 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 250 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 250 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 250 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"


    # #Regular Reward 3
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 260 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 260 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 260 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 260 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 260 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"


    # #Regular Reward 3
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 270 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 270 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 270 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 270 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 270 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"


    # #Regular Reward 3
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 280 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 280 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 280 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 280 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 280 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"


    # #Regular Reward 3
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 290 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 290 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 290 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 290 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 290 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"


    # #Regular Reward 3
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 300 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 300 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 300 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 300 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 300 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
    
    
    
    
    



   
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "96:00:00"
done