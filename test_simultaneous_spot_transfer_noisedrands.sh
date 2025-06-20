args="--env multi_robot_pb --num_robots 2  --cur_succ 0   --gap_avoidance --epochs 8400 
--max_ep_len 150 --local_epoch_len 3000  --insert_wall --exp Saved_models/Noised_RANDOM_MULTI_SPOT/E10r32G1E1/ 
--folder 2025_06_16_08_31_30 --reward_fn 32      --occupancy_map --use_perception  
--experiment_1 --home --gap_curr --starting_gap_width 0.85 --randomness 1 --multi_spots 
    --map_show_function --spot_transfer --separate_node --extreme_noise_randomness"



#  args="--env multi_robot_pb --num_robots 2  --cur_succ 0   --gap_avoidance --epochs 8400 
# --max_ep_len 150 --local_epoch_len 3000  --insert_wall --exp Saved_models/Noised_RANDOM_MULTI_SPOT/E8r32G1E1/ 
# --folder 2025_06_16_08_20_55 --reward_fn 32      --occupancy_map --use_perception  
# --experiment_1 --home --gap_curr --starting_gap_width 0.85 --randomness 2 --multi_spots 
#  --noise_mixed   --map_show_function --spot_transfer_test --separate_node"

python3 run_test.py ${args}