# args="--env multi_robot_pb --num_robots 2  --cur_succ 0   --gap_avoidance --epochs 8400 
# --max_ep_len 350 --local_epoch_len 3000  --insert_wall --exp 200110/E9r32G1E1 
# --folder 2025_02_03_03_17_14 --reward_fn 27      --occupancy_map --use_perception  
# --experiment_1 --hpc --gap_curr --starting_gap_width 1 --randomness 1 --heterogeneous 
# --turtle_titan "

# args="--env multi_robot_pb --num_robots 2  --cur_succ 0   --gap_avoidance --epochs 8400 
# --max_ep_len 350 --local_epoch_len 3000  --insert_wall --exp 200110/E7r32G1E1 
# --folder 2025_02_03_03_17_16 --reward_fn 27      --occupancy_map --use_perception  
# --experiment_1 --hpc --gap_curr --starting_gap_width 1 --randomness 1 --heterogeneous 
# --turtle_titan "


args="--env multi_robot_pb --num_robots 2  --cur_succ 0   --gap_avoidance --epochs 8400 
--max_ep_len 350 --local_epoch_len 3000  --insert_wall --exp 200108/E10r32G1E1 
--folder 2025_02_03_03_17_03 --reward_fn 27      --occupancy_map --use_perception  
--experiment_1 --hpc --gap_curr --starting_gap_width 1 --randomness 3 --heterogeneous 
--turtle_titan "


# args="--env multi_robot_pb --num_robots 2  --cur_succ 0   --gap_avoidance --epochs 8400 
# --max_ep_len 350 --local_epoch_len 3000  --insert_wall --exp 200107/E10r32G1E1 
# --folder 2025_02_03_03_16_45 --reward_fn 27      --occupancy_map --use_perception  
# --experiment_1 --hpc --gap_curr --starting_gap_width 1 --randomness 3 --heterogeneous 
# --turtle_titan "



# --map_show_function
python3 run_test.py ${args}