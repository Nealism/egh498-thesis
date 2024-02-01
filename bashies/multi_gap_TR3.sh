#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      "ME30/r31MGE10"
                      "ME30/r32MGE10"
                      "ME30/r33MGE10"
                      "ME30/r34MGE10"
                      "ME30/r35MGE10"
                      "ME30/r36MGE10"
                      "ME30/r37MGE10"
                      "ME30/r38MGE10"
                      "ME30/r39MGE10"
                      "ME30/r40MGE10"
                      "ME30/r41MGE10"
                      "ME30/r42MGE10"

                      "ME30/r13MGE102"
                      "ME30/r18MGE102"


                      "ME30/r13TG3"
                      "ME30/r18TG3"
                      "ME30/r19TG3"

                    
                      # "ME30/r25MGE10"
                      # "ME30/r26MGE10"
                      # "ME30/r27MGE10"
                      # "ME30/r28MGE10"
                      # "ME30/r29MGE10"
                      # "ME30/r30MGE10"
                      # "ME30/r31MGE10"
                      # "ME30/r32MGE10"
                      # "ME30/r33MGE10"

                      

                      # "ME30/r13METG5"
                      # "ME30/r18METG5"
                      # "ME27/r21METG5"
                      # "ME27/r23METG5"


                      # "ME27/r13MTGE10"
                      # "ME27/r14MTGE10"
                      # "ME27/r15MTGE10"
                      # "ME27/r16MTGE10"
                      # "ME27/r17MTGE10"
                      # "ME27/r18MTGE10"

                      # "ME27/r13MTGE1.5"
                      # "ME27/r14MTGE1.5"
                      # "ME27/r15MTGE1.5"
                      # "ME27/r16MTGE1.5"
                      # "ME27/r17MTGE1.5"
                      # "ME27/r18MTGE1.5"


                      # "ME27/r13TGE10"
                      # "ME27/r14TGE10"
                      # "ME27/r15TGE10"
                      # "ME27/r16TGE10"
                      # "ME27/r17TGE10"
                      # "ME27/r18TGE10"

                      # "ME18/r13TGE1.5"
                      # "ME18/r14TGE1.5"
                      # "ME18/r15TGE1.5"
                      # "ME18/r16TGE1.5"
                      # "ME18/r17TGE1.5"
                      # "ME18/r18TGE1.5"

                      

                      # "ME13/r10MG30E"
                      # "ME13/r11MG30E"
                      # "ME13/r12MG30E"
                      # "ME13/r13MG30E"
                      # "ME13/r14MG30E"
                      # "ME13/r15MG30E"


                      

                      # "ME13/r19RGD1EC"
                      # "ME13/r20RGD1EC"
                      # "ME13/r21RGD1EC"
                      # "ME13/r22RGD1EC"
                      # "ME13/r23RGD1EC"
                      # "ME13/r24RGD1EC"


                      

                      # "ME13/r10RG30EC"
                      # "ME13/r11RG30EC"
                      # "ME13/r12RG30EC"
                      # "ME13/r13RG30EC"
                      # "ME13/r14RG30EC"
                      # "ME13/r15RG30EC"



                      # "ME3/r6GD1C"
                      # "ME3/r7GD1C"
                      # "ME3/r12GD1C"

                      # "ME3/r6G30C"
                      # "ME3/r7G30C"
                      # "ME3/r12G30C"

                      # "ME3/r6G30"
                      # "ME3/r7G30"
                      # "ME3/r12G30"


                      # "ME3/r6REC0"
                      # "ME3/r7REC0"
                      # # "ME3/r8REC0"
                      # # "ME3/r9REC0"
                      # "ME3/r10REC0"
                      # # "ME3/r11REC0"
                      # "ME3/r12REC0"



                      # "ME3/r6C0GD.1"
                      # "ME3/r7C0GD.1"
                      # "ME3/r12C0GD.1"
                      
                      # "M13/r41GD.025EC9"
                      # "M13/r42GD.025EC9"
                      # "M13/r43GD.025EC9"
                      # "M13/r44GD.025EC9"
                      # "M13/r45GD.025EC9"

                      # "M13/r36GDEC9"
                      # "M13/r37GDEC9"
                      # "M13/r38GDEC9"
                      # "M13/r39GDEC9"
                      # "M13/r40GDEC9"
                      # "M13/r41GDEC9"
                      # "M13/r42GDEC9"
                      # "M13/r43GDEC9"
                      # "M13/r44GDEC9"
                      # "M13/r45GDEC9"

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    

    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 33 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 35 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 36 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 37 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 38 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 39 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 40 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 41 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 42 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3"



    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 2 --MA_bootstrap --experiment_3"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 18 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 2 --MA_bootstrap --experiment_3"

    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.0025 --starting_gap_width 3 --final_gap_width 2  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 18 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.0025 --starting_gap_width 3 --final_gap_width 2  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 19 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2400 --local_epoch_len 2400  --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.0025 --starting_gap_width 3 --final_gap_width 2  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3"
    
    
    
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 33 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --experiment_3"





    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 19 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 1.5 --MA_bootstrap --experiment_3"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 20 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 1.5 --MA_bootstrap --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 1.5 --MA_bootstrap --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 1.5 --MA_bootstrap --experiment_3"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 1.5 --MA_bootstrap --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --starting_gap_width 1.5 --MA_bootstrap --experiment_3"

    



    #~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt

    #--load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt


    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.25 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 14 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.25 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 15 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.25 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 16 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.25 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 17 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.25 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3"

    #  "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 18 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.25 --starting_gap_width 10 --final_gap_width 3 --MA_bootstrap --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3"





    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.25 --starting_gap_width 1.5 --MA_bootstrap --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 14 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.25 --starting_gap_width 1.5 --MA_bootstrap --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 15 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.25 --starting_gap_width 1.5 --MA_bootstrap --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 16 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.25 --starting_gap_width 1.5 --MA_bootstrap --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 17 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.25 --starting_gap_width 1.5 --MA_bootstrap --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3"

    #  "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 18 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.25 --starting_gap_width 1.5 --MA_bootstrap --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3" 



    





    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --starting_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 14 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.25 --starting_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 15 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.25 --starting_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 16 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.25 --starting_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 17 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.25 --starting_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 18 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 1 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.25 --starting_gap_width 1.5  --load_path ~/behaviour_rl/Saved_models/r18MGD.5E/2024_01_20_13_36_49/model.pt --experiment_3" 

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map  --MA_bootstrap --experiment_3"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 11 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --MA_bootstrap --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --MA_bootstrap --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map  --MA_bootstrap --experiment_3"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 14 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --MA_bootstrap --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 15 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --MA_bootstrap --experiment_3"







    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 19 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --regular_bootstrap --collision_likelihood --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 20 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --regular_bootstrap --collision_likelihood --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --regular_bootstrap --collision_likelihood --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --regular_bootstrap --collision_likelihood --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --regular_bootstrap --collision_likelihood --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --regular_bootstrap --collision_likelihood --experiment_3"




    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map  --regular_bootstrap --collision_likelihood --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 11 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map  --regular_bootstrap --collision_likelihood --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map  --regular_bootstrap --collision_likelihood --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map  --regular_bootstrap --collision_likelihood --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 14 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map  --regular_bootstrap --collision_likelihood --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 15 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map  --regular_bootstrap --collision_likelihood --experiment_3"



   

   
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 6 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 1 --collision_likelihood --experiment_3"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 7 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --collision_likelihood --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 1 --collision_likelihood --experiment_3"



    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 6 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map  --collision_likelihood --experiment_3"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 7 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map  --collision_likelihood --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map  --collision_likelihood --experiment_3"



    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 6 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map  --experiment_3"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 7 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall --use_perception --occupancy_map --experiment_3"
    
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "96:00:00"
done