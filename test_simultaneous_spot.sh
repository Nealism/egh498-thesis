args="--env multi_robot_pb --num_robots 2  --cur_succ 0   --gap_avoidance --epochs 8400 
--max_ep_len 150 --local_epoch_len 3000  --insert_wall --exp Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best 
--folder 2024_09_10_07_14_17 --reward_fn 32      --occupancy_map --use_perception  
--experiment_1 --home --gap_curr --starting_gap_width 0.85 --randomness 1 --multi_spots 
 --noise_mixed   --map_show"

python3 run_test.py ${args}