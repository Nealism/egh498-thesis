#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      

                    
                      
                      #Without Other Robot Info
                      "150/A1r27G1E1"
                      "150/A2r27G1E1"
                      "150/A3r27G1E1"
                      "150/A4r27G1E1"
                      "150/A5r27G1E1"
                      "150/A6r27G1E1"
                      "150/A7r27G1E1"
                      "150/A8r27G1E1"
                      "150/A9r27G1E1"
                      "150/A10r27G1E1"
                      "150/A11r27G1E1"
                      "150/A12r27G1E1"
                      "150/A13r27G1E1"
                      "150/A14r27G1E1"
                      "150/A15r27G1E1"
                      "150/A16r27G1E1"
                      "150/A17r27G1E1"
                      "150/A18r27G1E1"
                      "150/A19r27G1E1"
                      "150/A20r27G1E1"
                      "150/A21r27G1E1"
                      "150/A22r27G1E1"
                      "150/A23r27G1E1"
                      "150/A24r27G1E1"
                      "150/A25r27G1E1"
                      "150/A26r27G1E1"
                      "150/A27r27G1E1"
                      "150/A28r27G1E1"
                      "150/A29r27G1E1"
                      "150/A30r27G1E1"
                      




                      #Ray Mechanism Reward with Other Robot Info
                      "151/B1r27G1E3"
                      "151/B2r27G1E3"
                      "151/B3r27G1E3"
                      "151/B4r27G1E3"
                      "151/B5r27G1E3"
                      "151/B6r27G1E3"
                      "151/B7r27G1E3"
                      "151/B8r27G1E3"
                      "151/B9r27G1E3"
                      "151/B10r27G1E3"
                      "151/B11r27G1E3"
                      "151/B12r27G1E3"
                      "151/B13r27G1E3"
                      "151/B14r27G1E3"
                      "151/B15r27G1E3"
                      "151/B16r27G1E3"
                      "151/B17r27G1E3"
                      "151/B18r27G1E3"
                      "151/B19r27G1E3"
                      "151/B20r27G1E3"
                      "151/B21r27G1E3"
                      "151/B22r27G1E3"
                      "151/B23r27G1E3"
                      "151/B24r27G1E3"
                      "151/B25r27G1E3"
                      "151/B26r27G1E3"
                      "151/B27r27G1E3"
                      "151/B28r27G1E3"
                      "151/B29r27G1E3"
                      "151/B30r27G1E3"





                      #Regular Reward with Other Robot Info
                      "152/C1r28G1E3"
                      "152/C2r28G1E3"
                      "152/C3r28G1E3"
                      "152/C4r28G1E3"
                      "152/C5r28G1E3"
                      "152/C6r28G1E3"
                      "152/C7r28G1E3"
                      "152/C8r28G1E3"
                      "152/C9r28G1E3"
                      "152/C10r28G1E3"
                      "152/C11r28G1E3"
                      "152/C12r28G1E3"
                      "152/C13r28G1E3"
                      "152/C14r28G1E3"
                      "152/C15r28G1E3"
                      "152/C16r28G1E3"
                      "152/C17r28G1E3"
                      "152/C18r28G1E3"
                      "152/C19r28G1E3"
                      "152/C20r28G1E3"
                      "152/C21r28G1E3"
                      "152/C22r28G1E3"
                      "152/C23r28G1E3"
                      "152/C24r28G1E3"
                      "152/C25r28G1E3"
                      "152/C26r28G1E3"
                      "152/C27r28G1E3"
                      "152/C28r28G1E3"
                      "152/C29r28G1E3"
                      "152/C30r28G1E3"






                      #MA_BOOT cur only
                      "153/D1r27G1E3MB"
                      "153/D2r27G1E3MB"
                      "153/D3r27G1E3MB"
                      "153/D4r27G1E3MB"
                      "153/D5r27G1E3MB"
                      "153/D6r27G1E3MB"
                      "153/D7r27G1E3MB"
                      "153/D8r27G1E3MB"
                      "153/D9r27G1E3MB"
                      "153/D10r27G1E3MB"
                      "153/D11r27G1E3MB"
                      "153/D12r27G1E3MB"
                      "153/D13r27G1E3MB"
                      "153/D14r27G1E3MB"
                      "153/D15r27G1E3MB"
                      "153/D16r27G1E3MB"
                      "153/D17r27G1E3MB"
                      "153/D18r27G1E3MB"
                      "153/D19r27G1E3MB"
                      "153/D20r27G1E3MB"
                      "153/D21r27G1E3MB"
                      "153/D22r27G1E3MB"
                      "153/D23r27G1E3MB"
                      "153/D24r27G1E3MB"
                      "153/D25r27G1E3MB"
                      "153/D26r27G1E3MB"
                      "153/D27r27G1E3MB"
                      "153/D28r27G1E3MB"
                      "153/D29r27G1E3MB"
                      "153/D30r27G1E3MB"




                      #Gap cur only
                      "154/E1r27G1E3GC"
                      "154/E2r27G1E3GC"
                      "154/E3r27G1E3GC"
                      "154/E4r27G1E3GC"
                      "154/E5r27G1E3GC"
                      "154/E6r27G1E3GC"
                      "154/E7r27G1E3GC"
                      "154/E8r27G1E3GC"
                      "154/E9r27G1E3GC"
                      "154/E10r27G1E3GC"
                      "154/E11r27G1E3GC"
                      "154/E12r27G1E3GC"
                      "154/E13r27G1E3GC"
                      "154/E14r27G1E3GC"
                      "154/E15r27G1E3GC"
                      "154/E16r27G1E3GC"
                      "154/E17r27G1E3GC"
                      "154/E18r27G1E3GC"
                      "154/E19r27G1E3GC"
                      "154/E20r27G1E3GC"
                      "154/E21r27G1E3GC"
                      "154/E22r27G1E3GC"
                      "154/E23r27G1E3GC"
                      "154/E24r27G1E3GC"
                      "154/E25r27G1E3GC"
                      "154/E26r27G1E3GC"
                      "154/E27r27G1E3GC"
                      "154/E28r27G1E3GC"
                      "154/E29r27G1E3GC"
                      "154/E30r27G1E3GC"




                      #No Cur
                      "155/F1r27G1E3NC"
                      "155/F2r27G1E3NC"
                      "155/F3r27G1E3NC"
                      "155/F4r27G1E3NC"
                      "155/F5r27G1E3NC"
                      "155/F6r27G1E3NC"
                      "155/F7r27G1E3NC"
                      "155/F8r27G1E3NC"
                      "155/F9r27G1E3NC"
                      "155/F10r27G1E3NC"
                      "155/F11r27G1E3NC"
                      "155/F12r27G1E3NC"
                      "155/F13r27G1E3NC"
                      "155/F14r27G1E3NC"
                      "155/F15r27G1E3NC"
                      "155/F16r27G1E3NC"
                      "155/F17r27G1E3NC"
                      "155/F18r27G1E3NC"
                      "155/F19r27G1E3NC"
                      "155/F20r27G1E3NC"
                      "155/F21r27G1E3NC"
                      "155/F22r27G1E3NC"
                      "155/F23r27G1E3NC"
                      "155/F24r27G1E3NC"
                      "155/F25r27G1E3NC"
                      "155/F26r27G1E3NC"
                      "155/F27r27G1E3NC"
                      "155/F28r27G1E3NC"
                      "155/F29r27G1E3NC"
                      "155/F30r27G1E3NC"


 
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    
 



    #Without Other Robot Info

    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    
    
    
    
    
    #Ray Mechanism Reward with Other Robot Info
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    
    
    
    



   
    #Regular Reward with Other Robot Info
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    
    
    
    #MA_BOOT cur only
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"





    #GAP cur only
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 3 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"

    
    
    

    #NO CUR
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 100 --local_epoch_len 1000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "24:00:00"
done