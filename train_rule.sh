args="--env multi_robot_pb --num_robots 2 --cur_succ 0   --gap_avoidance --epochs 8400  --max_ep_len 150 --local_epoch_len 150  --detect_distance 2 --insert_wall   --experiment_1   --reward_fn 32  --starting_gap_width 1.5 --final_gap_width 1 --gap_curr  --randomness 2  --use_perception --occupancy_map      --generalise_cross --noise_mixed --turtle_titan   --multi_titans  --render  --Road_rule --load_path ~/behaviour_rl/Saved_models/Realistic_control_rate/H3r29G1E3_simple_1.5/2024_06_10_15_05_24/model.pt"
# --load_path ~/behaviour_rl/Saved_models/Turtle_titan/E2r10G1E1_single_no_noise_1m_sync_1.5_2.5_Nov/2024_11_12_16_01_54/model.pt
# "

python3 run.py ${args}