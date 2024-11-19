# args="--env multi_robot_pb --num_robots 1  --cur_succ 0   --gap_avoidance --epochs 8400 
# --max_ep_len 150 --local_epoch_len 3000  --insert_wall --exp 452/E2r10G1E1 
# --folder 2024_11_12_16_01_54 --reward_fn 32      --occupancy_map --use_perception  
# --experiment_1 --hpc --gap_curr --starting_gap_width 1 --randomness 1 --multi_titans 
# --turtle_titan  "

args="--env multi_robot_pb --num_robots 2  --cur_succ 0   --gap_avoidance --epochs 8400 
--max_ep_len 170 --local_epoch_len 3000  --insert_wall --exp Saved_models/Turtle_titan/E2r10G1E1_single_no_noise_1m_sync_1.5_2.5_Nov
--folder 2024_11_12_16_01_54 --reward_fn 32      --occupancy_map --use_perception  
--experiment_1 --home --gap_curr --starting_gap_width 1 --randomness 1 --multi_titans 
--turtle_titan  --noise_mixed --expert_cur --Road_rule "
#--map_show_function
python3 run_test.py ${args}