args="--env multi_robot_pb --num_robots 2  --cur_succ 0   --gap_avoidance --epochs 8400 
--max_ep_len 200 --local_epoch_len 3000  --insert_wall --exp Saved_models/Spot_Titan/
--folder Transfer_learning_0.85_400162 --reward_fn 32      --occupancy_map --use_perception  
--experiment_1 --home --gap_curr --starting_gap_width 0.85 --randomness 2 --heterogeneous 
--turtle_titan --separate_node "




# args="--env multi_robot_pb --num_robots 2  --cur_succ 0   --gap_avoidance --epochs 8400 
# --max_ep_len 200 --local_epoch_len 3000  --insert_wall --exp Saved_models/Spot_Titan/
# --folder Full_Train_0.85_200207E10_53 --reward_fn 32      --occupancy_map --use_perception  
# --experiment_0 --home --gap_curr --starting_gap_width 0.85 --randomness 2 --multi_titans 
# --turtle_titan  --map_show_function "





# args="--env multi_robot_pb --num_robots 2  --cur_succ 0   --gap_avoidance --epochs 8400 
# --max_ep_len 200 --local_epoch_len 3000  --insert_wall --exp Saved_models/Spot_Titan/
# --folder Noise_Added_hetero_0.85 --reward_fn 27      --occupancy_map --use_perception  
# --experiment_1 --home --gap_curr --starting_gap_width 0.85 --randomness 2 --heterogeneous 
# --turtle_titan --separate_node --map_show_function --noise_mixed"


# args="--env multi_robot_pb --num_robots 2  --cur_succ 0   --gap_avoidance --epochs 8400 
# --max_ep_len 200 --local_epoch_len 3000  --insert_wall --exp Saved_models/Spot_Titan/
# --folder 151_map_improved_no_noisey --reward_fn 27      --occupancy_map --use_perception  
# --experiment_1 --home --gap_curr --starting_gap_width 0.85 --randomness 2 --heterogeneous 
# --turtle_titan --separate_node --map_show_function"



# args="--env multi_robot_pb --num_robots 2  --cur_succ 0   --gap_avoidance --epochs 8400 
# --max_ep_len 200 --local_epoch_len 3000  --insert_wall --exp Saved_models/Spot_Titan/
# --folder 147_separate_node_2 --reward_fn 27      --occupancy_map --use_perception  
# --experiment_1 --home --gap_curr --starting_gap_width 0.85 --randomness 2 --heterogeneous 
# --turtle_titan --separate_node --map_show_function"

# args="--env multi_robot_pb --num_robots 2  --cur_succ 0   --gap_avoidance --epochs 8400 
# --max_ep_len 150 --local_epoch_len 3000  --insert_wall --exp 400147/E4r32G1E1 
# --folder 2025_03_04_12_48_58 --reward_fn 27      --occupancy_map --use_perception  
# --experiment_1 --hpc --gap_curr --starting_gap_width 0.85 --randomness 2 --heterogeneous 
# --turtle_titan --separate_node "


# args="--env multi_robot_pb --num_robots 2  --cur_succ 0   --gap_avoidance --epochs 8400 
# --max_ep_len 350 --local_epoch_len 3000  --insert_wall --exp 400142/E11r32G1E1 
# --folder 2025_03_03_15_56_46 --reward_fn 27      --occupancy_map --use_perception  
# --experiment_1 --hpc --gap_curr --starting_gap_width 0.85 --randomness 2 --heterogeneous 
# --turtle_titan --separate_node"
# --map_show_function
python3 run_test.py ${args}