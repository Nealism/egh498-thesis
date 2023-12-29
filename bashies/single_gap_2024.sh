#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      # "sg13/r43GD.5EC9"
                      # "sg13/r43GD.1EC9"
                      # "sg13/r43GD.25EC9"


                      "sg20/r30GD.1EC0"
                      "sg20/r31GD.1EC0"
                      "sg20/r32GD.1EC0"
                      "sg20/r33GD.1EC0"
                      "sg20/r34GD.1EC0"
                      "sg20/r35GD.1EC0"
                      
                      
                      "sg20/r36GD.1EC0"
                      "sg20/r37GD.1EC0"
                      "sg20/r38GD.1EC0"
                      "sg20/r39GD.1EC0"
                      "sg20/r40GD.1EC0"
                      "sg20/r41GD.1EC0"
                      "sg20/r42GD.1EC0"
                      "sg20/r43GD.1EC0"
                      "sg20/r44GD.1EC0"
                      "sg20/r45GD.1EC0"


                      "sg20/r46GD.1EC0"
                      "sg20/r47GD.1EC0"
                      "sg20/r48GD.1EC0"

                      # "sg13/r36GDEC9"
                      # "sg13/r37GDEC9"
                      # "sg13/r38GDEC9"
                      # "sg13/r39GDEC9"
                      # "sg13/r40GDEC9"
                      # "sg13/r41GDEC9"
                      # "sg13/r42GDEC9"
                      # "sg13/r43GDEC9"
                      # "sg13/r44GDEC9"
                      # "sg13/r45GDEC9"

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    

    
    # "--cpu 64 --env multi_robot_pb --reward_fn 43 --cur_succ 9  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 2 --insert_wall --gap_curr"

    
    # "--cpu 64 --env multi_robot_pb --reward_fn 43 --cur_succ 9  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"
    
    
    # "--cpu 64 --env multi_robot_pb --reward_fn 43 --cur_succ 9  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.25"

    
    "--cpu 64 --env multi_robot_pb --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --reward_fn 32 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --reward_fn 33 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --reward_fn 34 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --reward_fn 35 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"



    "--cpu 64 --env multi_robot_pb --reward_fn 36 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --reward_fn 37 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --reward_fn 38 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --reward_fn 39 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --reward_fn 40 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --reward_fn 41 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --reward_fn 42 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --reward_fn 43 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --reward_fn 44 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --reward_fn 45 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"


    "--cpu 64 --env multi_robot_pb --reward_fn 46 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --reward_fn 47 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --reward_fn 48 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"


    # "--cpu 64 --env multi_robot_pb --reward_fn 36 --cur_succ 0 --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 2 --insert_wall"


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