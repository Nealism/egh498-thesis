#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      "MA21/r33GD.1EC0"
                      "MA21/r48GD.1EC0"
                      "MA21/r49GD.1EC0"
                      
                      "MA21/r50GD.1EC0"
                      "MA21/r51GD.1EC0"
                      "MA21/r52GD.1EC0"
                      "MA21/r53GD.1EC0"
                      "MA21/r54GD.1EC0"
                      # "MA13/r41GD.025EC9"
                      # "MA13/r42GD.025EC9"
                      # "MA13/r43GD.025EC9"
                      # "MA13/r44GD.025EC9"
                      # "MA13/r45GD.025EC9"

                      # "MA13/r36GDEC9"
                      # "MA13/r37GDEC9"
                      # "MA13/r38GDEC9"
                      # "MA13/r39GDEC9"
                      # "MA13/r40GDEC9"
                      # "MA13/r41GDEC9"
                      # "MA13/r42GDEC9"
                      # "MA13/r43GDEC9"
                      # "MA13/r44GDEC9"
                      # "MA13/r45GDEC9"

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    

    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 33 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 4000 --local_epoch_len 4000 --expert_curr --detect_distance 3 --insert_wall --gap_curr  --gap_decrease 0.1"

    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 48 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 4000 --local_epoch_len 4000 --expert_curr --detect_distance 3 --insert_wall --gap_curr --gap_decrease 0.1"
    
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 49 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 4000 --local_epoch_len 4000 --expert_curr --detect_distance 3 --insert_wall --gap_curr --gap_decrease 0.1"

    
    

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 50 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 4000 --local_epoch_len 4000 --expert_curr --detect_distance 3 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 51 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 4000 --local_epoch_len 4000 --expert_curr --detect_distance 3 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 52 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 4000 --local_epoch_len 4000 --expert_curr --detect_distance 3 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 53 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 4000 --local_epoch_len 4000 --expert_curr --detect_distance 3 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 54 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 4000 --local_epoch_len 4000 --expert_curr --detect_distance 3 --insert_wall --gap_curr --gap_decrease 0.1"

    # "--cpu 64 --env multi_robot_pb --reward_fn 41 --cur_succ 9  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"

    # "--cpu 64 --env multi_robot_pb --reward_fn 42 --cur_succ 9  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.025"

    # "--cpu 64 --env multi_robot_pb --reward_fn 43 --cur_succ 9  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.025"

    # "--cpu 64 --env multi_robot_pb --reward_fn 44 --cur_succ 9  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.025"

    # "--cpu 64 --env multi_robot_pb --reward_fn 45 --cur_succ 9  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.025"


    # "--cpu 64 --env multi_robot_pb --reward_fn 36 --cur_succ 9  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 2 --insert_wall"


    # "--cpu 64 --env multi_robot_pb --reward_fn 37 --cur_succ 9  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 2 --insert_wall"

    # "--cpu 64 --env multi_robot_pb --reward_fn 38 --cur_succ 9  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 2 --insert_wall"

    # "--cpu 64 --env multi_robot_pb --reward_fn 39 --cur_succ 9  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 2 --insert_wall"

    # "--cpu 64 --env multi_robot_pb --reward_fn 40 --cur_succ 9  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 2 --insert_wall"

    # "--cpu 64 --env multi_robot_pb --reward_fn 41 --cur_succ 9  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 2 --insert_wall"

    # "--cpu 64 --env multi_robot_pb --reward_fn 42 --cur_succ 9  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 2 --insert_wall"

    # "--cpu 64 --env multi_robot_pb --reward_fn 43 --cur_succ 9  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 2 --insert_wall"

    # "--cpu 64 --env multi_robot_pb --reward_fn 44 --cur_succ 9  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 2 --insert_wall"

    # "--cpu 64 --env multi_robot_pb --reward_fn 45 --cur_succ 9  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 2 --insert_wall"

   
    
    
    
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "72:00:00"
done