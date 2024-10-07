args="--env multi_robot_pb --num_robots 2  --cur_succ 0   --gap_avoidance --epochs 8400 
--max_ep_len 100 --local_epoch_len 3000  --insert_wall --exp 347/B2r29G1E1 
--folder 2024_08_25_14_56_58 --reward_fn 31      --occupancy_map --use_perception  
--experiment_1 --hpc --gap_curr --starting_gap_width 1 --randomness 2 --multi_titans 
--turtle_titan --map_show"

python3 run_test.py ${args}