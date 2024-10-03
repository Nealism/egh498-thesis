args="--env multi_robot_pb --num_robots 2  --cur_succ 0   --gap_avoidance --epochs 8400 
--max_ep_len 300 --local_epoch_len 3000  --insert_wall --exp Saved_models/Turtle_titan/E1r32G1E1_0.85_406_single/ 
--folder 2024_09_21_12_12_32 --reward_fn 32      --occupancy_map --use_perception  
--experiment_1 --home --gap_curr --starting_gap_width 1 --randomness 1 --multi_titans 
--turtle_titan  "

python3 run_test.py ${args}