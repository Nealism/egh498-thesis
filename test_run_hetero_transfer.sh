args="--env multi_robot_pb --num_robots 2  --cur_succ 0   --gap_avoidance --epochs 8400 
--max_ep_len 200 --local_epoch_len 3000  --insert_wall --exp 400145/E13r32G1E1 
--folder 2025_03_04_12_49_04 --reward_fn 27      --occupancy_map --use_perception  
--experiment_1 --hpc --gap_curr --starting_gap_width 1 --randomness 2 --heterogeneous 
--turtle_titan "

# args="--env multi_robot_pb --num_robots 2  --cur_succ 0   --gap_avoidance --epochs 8400 
# --max_ep_len 200 --local_epoch_len 3000  --insert_wall --exp 400108/E8r32G1E1 
# --folder 2025_02_12_16_13_16 --reward_fn 27      --occupancy_map --use_perception  
# --experiment_1 --hpc --gap_curr --starting_gap_width 0.85 --randomness 2 --heterogeneous 
# --turtle_titan "


# args="--env multi_robot_pb --num_robots 2  --cur_succ 0   --gap_avoidance --epochs 8400 
# --max_ep_len 200 --local_epoch_len 3000  --insert_wall --exp Saved_models/Spot_Titan/
# --folder 104 --reward_fn 27      --occupancy_map --use_perception  
# --experiment_1 --home --gap_curr --starting_gap_width 0.85 --randomness 2 --heterogeneous 
# --turtle_titan "
# --map_show_function
python3 run_test.py ${args}