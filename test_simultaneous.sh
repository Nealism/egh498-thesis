args="--env multi_robot_pb --num_robots 2  --cur_succ 0   --gap_avoidance --epochs 0 
--max_ep_len 0 --local_epoch_len 0  --insert_wall --exp Saved_models/Turtle_titan/E4r32G1E1_387_0.85_noised_best 
--folder 2024_09_10_07_14_17 --reward_fn 31      --occupancy_map --use_perception --experiment_1 --home --gap_curr --starting_gap_width 1.5 --randomness 4 --multi_titans 
--turtle_titan --figure  "
# --map_show
python3 run_test.py ${args}