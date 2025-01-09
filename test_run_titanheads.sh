args="--env multi_robot_pb --num_robots 2  --cur_succ 0   --gap_avoidance --epochs 8400 
--max_ep_len 250 --local_epoch_len 3000  --insert_wall --exp 100105/E14r32G1E1 
--folder 2025_01_08_16_32_38 --reward_fn 27      --occupancy_map --use_perception  
--experiment_1 --hpc --gap_curr --starting_gap_width 3 --randomness 2 --titanheads 
--turtle_titan "
# --map_show_function
python3 run_test.py ${args}