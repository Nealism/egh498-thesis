args="--env multi_robot_pb --num_robots 2  --cur_succ 0   --gap_avoidance --epochs 8400 
--max_ep_len 100 --local_epoch_len 3000  --insert_wall --reward_fn 31      
--occupancy_map --use_perception  --experiment_1 --hpc --gap_curr --starting_gap_width 1 
--randomness 1 --multi_titans  --jit_model "

python3 run_test.py ${args}