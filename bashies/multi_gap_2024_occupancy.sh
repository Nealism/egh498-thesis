#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      "MAO26/r6MGD.1EC0"
                      "MAO26/r7MGD.1EC0"
                      # "MAO26/r8MGD.1EC0"
                      # "MAO26/r9MGD.1EC0"
                      "MAO26/r10MGD.1EC0"
                      # "MAO26/r11MGD.1EC0"
                      "MAO26/r12MGD.1EC0"


                      "MAO26/r6RGD.1EC0"
                      "MAO26/r7RGD.1EC0"
                      # "MAO26/r8RGD.1EC0"
                      # "MAO26/r9RGD.1EC0"
                      "MAO26/r10RGD.1EC0"
                      # "MAO26/r11RGD.1EC0"
                      "MAO26/r12RGD.1EC0"


                      # "MAO26/r6REC0"
                      # "MAO26/r7REC0"
                      # # "MAO26/r8REC0"
                      # # "MAO26/r9REC0"
                      # "MAO26/r10REC0"
                      # # "MAO26/r11REC0"
                      # "MAO26/r12REC0"



                      "MAO26/r6C0GD.1"
                      "MAO26/r7C0GD.1"
                      # "MAO26/r8C0GD.1"
                      # "MAO26/r9C0GD.1"
                      "MAO26/r10C0GD.1"
                      # "MAO26/r11C0GD.1"
                      "MAO26/r12C0GD.1"
                      
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
    

    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 6 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 4000 --local_epoch_len 4000 --expert_curr --detect_distance 3 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --MA_bootstrap"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 7 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 4000 --local_epoch_len 4000 --expert_curr --detect_distance 3 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --MA_bootstrap"
     
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 8 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 4000 --local_epoch_len 4000 --expert_curr --detect_distance 3 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --MA_bootstrap"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 9 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 4000 --local_epoch_len 4000 --expert_curr --detect_distance 3 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --MA_bootstrap"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 4000 --local_epoch_len 4000 --expert_curr --detect_distance 3 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --MA_bootstrap"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 11 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 4000 --local_epoch_len 4000 --expert_curr --detect_distance 3 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --MA_bootstrap"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 4000 --local_epoch_len 4000 --expert_curr --detect_distance 3 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --MA_bootstrap"







    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 6 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 3 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.1 --regular_bootstrap"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 7 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 3 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --regular_bootstrap"
      
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 8 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 3 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --regular_bootstrap"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 9 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 3 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --regular_bootstrap"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 3 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --regular_bootstrap"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 11 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 3 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --regular_bootstrap"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 3 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.1 --regular_bootstrap"



    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 6 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 3 --insert_wall --use_perception --occupancy_map --regular_bootstrap"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 7 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 3 --insert_wall --use_perception --occupancy_map --regular_bootstrap"
      
    # # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 8 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 3 --insert_wall --use_perception --occupancy_map --regular_bootstrap"
    
    # # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 9 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 3 --insert_wall --use_perception --occupancy_map --regular_bootstrap"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 3 --insert_wall --use_perception --occupancy_map --regular_bootstrap"

    # # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 11 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 3 --insert_wall --use_perception --occupancy_map --regular_bootstrap"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --expert_curr --detect_distance 3 --insert_wall --use_perception --occupancy_map --regular_bootstrap"







    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 6 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --detect_distance 3 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 7 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --detect_distance 3 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1"
      
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 8 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --detect_distance 3 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 9 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --detect_distance 3 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --detect_distance 3 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 11 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --detect_distance 3 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2500 --local_epoch_len 2500 --detect_distance 3 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.1"

   

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