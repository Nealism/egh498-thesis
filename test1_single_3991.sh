args="--env multi_robot_pb --num_robots 2  --cur_succ 0   --gap_avoidance --epochs 8400 
--max_ep_len 150 --local_epoch_len 3000  --insert_wall --exp 3991/E6r32G1E1 
--folder 2024_10_11_00_43_36 --reward_fn 39      --occupancy_map --use_perception  
--experiment_1 --hpc --gap_curr --starting_gap_width 1 --randomness 1 --multi_titans 
--turtle_titan --map_show_function "

python3 run_test.py ${args}