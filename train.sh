args="--env multi_robot_pb --num_robots 1 --cur_succ 0   --gap_avoidance 
--epochs 8400 --max_ep_len 100 --local_epoch_len 100  --detect_distance 2 
--insert_wall   --experiment_1  --reward_fn 10  --starting_gap_width 1 
--final_gap_width 0.8 --gap_curr  --randomness 2 --use_perception --occupancy_map  
--multi_titans   --expert_cur  --render"

python3 run.py ${args}