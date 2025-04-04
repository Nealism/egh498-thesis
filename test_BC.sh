args="--env multi_robot_pb --num_robots 2 --multi_titans --turtle_titan --gap_avoidance --max_ep_len 300 --use_perception --occupancy_map --experiment_1 --insert_wall --starting_gap_width 2 --reward_fn 32   "
# --map_show
python3 run_test_BC.py ${args}