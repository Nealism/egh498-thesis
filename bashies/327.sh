#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      

                    
                      
                      # #Simple Reward
                      # "328/A1r21G1E3"
                      # "328/A2r21G1E3"
                      # "328/A3r21G1E3"
                      # "328/A4r21G1E3"
                      # "328/A5r21G1E3"
                      
                      




                      # #Step Reward 2
                      # "328/B1r22G1E3"
                      # "328/B2r22G1E3"
                      # "328/B3r22G1E3"
                      # "328/B4r22G1E3"
                      # "328/B5r22G1E3"
                      





                      #Regular Reward 
                      "328/C1r23G1E3"
                      "328/C2r23G1E3"
                      "328/C3r23G1E3"
                      "328/C4r23G1E3"
                      "328/C5r23G1E3"


                      #Regular Reward 2
                      "328/D1r24G1E3"
                      "328/D2r24G1E3"
                      "328/D3r24G1E3"
                      "328/D4r24G1E3"
                      "328/D5r24G1E3"



                      #Regular Reward 4
                      "328/E1r25G1E3"
                      "328/E2r25G1E3"
                      "328/E3r25G1E3"
                      "328/E4r25G1E3"
                      "328/E5r25G1E3"
                      






                      #Regular Reward 3
                      "328/F1r23G1E3"
                      "328/F2r23G1E3"
                      "328/F3r23G1E3"
                      "328/F4r23G1E3"
                      "328/F5r23G1E3"

                      


                      


                      #Unclipped Reward 3
                      "328/G1r24G1E3"
                      "328/G2r24G1E3"
                      "328/G3r24G1E3"
                      "328/G4r24G1E3"
                      "328/G5r24G1E3"


                      


                      #Unclipped Reward 3
                      "328/H1r25G1E3"
                      "328/H2r25G1E3"
                      "328/H3r25G1E3"
                      "328/H4r25G1E3"
                      "328/H5r25G1E3"
                      




                      #Ray Reward 1
                      "328/I1r23G1E3"
                      "328/I2r23G1E3"
                      "328/I3r23G1E3"
                      "328/I4r23G1E3"
                      "328/I5r23G1E3"

                      #Ray Reward 1
                      "328/J1r24G1E3"
                      "328/J2r24G1E3"
                      "328/J3r24G1E3"
                      "328/J4r24G1E3"
                      "328/J5r24G1E3"
                      




                      #Ray Reward 2
                      "328/K1r25G1E3"
                      "328/K2r25G1E3"
                      "328/K3r25G1E3"
                      "328/K4r25G1E3"
                      "328/K5r25G1E3"



                      # #Ray Reward 2
                      # "328/L1r280G1E3"
                      # "328/L2r280G1E3"
                      # "328/L3r280G1E3"
                      # "328/L4r280G1E3"
                      # "328/L5r280G1E3"



                      # #Ray Reward 2
                      # "328/M1r290G1E3"
                      # "328/M2r290G1E3"
                      # "328/M3r290G1E3"
                      # "328/M4r290G1E3"
                      # "328/M5r290G1E3"


                      # #Ray Reward 2
                      # "328/N1r300G1E3"
                      # "328/N2r300G1E3"
                      # "328/N3r300G1E3"
                      # "328/N4r300G1E3"
                      # "328/N5r300G1E3"
                      


 
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    
 



    # #Step Reward 1
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    
    
    
    
    
    
    # #Step Reward 2
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"




    #Regular Reward 1
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr   --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr   --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr   --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr   --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr   --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"


    #Regular Reward 2
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr   --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr   --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr   --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr   --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr   --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"


  
    #Regular Reward 3
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr   --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr   --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr   --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr   --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr   --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"

    



    #Regular Reward 4
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --num_layers 3 --num_nodes 356  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --num_layers 3 --num_nodes 356  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --num_layers 3 --num_nodes 356  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --num_layers 3 --num_nodes 356  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --num_layers 3 --num_nodes 356  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"

  

    #Ray Based Reward 1
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --num_layers 3 --num_nodes 356  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --num_layers 3 --num_nodes 356  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --num_layers 3 --num_nodes 356  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --num_layers 3 --num_nodes 356  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --num_layers 3 --num_nodes 356  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"


    #Ray Based Reward 1
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --num_layers 3 --num_nodes 356  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --num_layers 3 --num_nodes 356  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --num_layers 3 --num_nodes 356  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --num_layers 3 --num_nodes 356  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2 --num_layers 3 --num_nodes 356  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"







    #Regular Reward 3
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"


    #Regular Reward 3
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"


    #Regular Reward 3
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 5000 --max_ep_len 300 --local_epoch_len 3000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 0.85  --experiment_1  --ray_wall_type 1 --randomness 2  --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/A5r29G1E3_322_SimleBEST/2024_06_11_16_07_06/model.pt"


    
    
    
    
    
    



   
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "96:00:00"
done