args="--env multi_robot_pb --num_robots 2  --cur_succ 0   --gap_avoidance --epochs 8400 
--max_ep_len 350 --local_epoch_len 3000  --insert_wall --exp 3002/E14r32G1E1 
--folder 2024_12_24_13_32_44 --reward_fn 27      --occupancy_map --use_perception  
--experiment_1 --hpc --gap_curr --starting_gap_width 5 --randomness 2 --titanheads 
--turtle_titan "
# --map_show_function
python3 run_test.py ${args}