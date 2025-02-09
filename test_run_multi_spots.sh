args="--env multi_robot_pb --num_robots 2  --cur_succ 0   --gap_avoidance --epochs 8400 
--max_ep_len 350 --local_epoch_len 3000  --insert_wall --exp 300105/E12r32G1E1 
--folder 2025_02_03_03_14_49 --reward_fn 27      --occupancy_map --use_perception  
--experiment_1 --hpc --gap_curr --starting_gap_width 1 --randomness 1 --multi_spots 
--turtle_titan --expert_cur --MA_bootstrap"
# --map_show_function
python3 run_test.py ${args}