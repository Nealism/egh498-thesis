#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      "ME3/r6MGD.5E"
                      "ME3/r7MGD.5E"
                      "ME3/r12MGD.5E"

                      "ME3/r6MG30E"
                      "ME3/r7MG30E"
                      "ME3/r12MG30E"


                      "ME3/r6RGD.5EC"
                      "ME3/r7RGD.5EC"
                      "ME3/r12RGD.5EC"


                      "ME3/r6RG30EC"
                      "ME3/r7RG30EC"
                      "ME3/r12RG30EC"



                      # "ME3/r6GD.5C"
                      # "ME3/r7GD.5C"
                      # "ME3/r12GD.5C"

                      # "ME3/r6G30C"
                      # "ME3/r7G30C"
                      # "ME3/r12G30C"

                      # "ME3/r6G30"
                      # "ME3/r7G30"
                      # "ME3/r12G30"


                      # "ME3/r6REC0"
                      # "ME3/r7REC0"
                      # # "ME3/r8REC0"
                      # # "ME3/r9REC0"
                      # "ME3/r10REC0"
                      # # "ME3/r11REC0"
                      # "ME3/r12REC0"



                      # "ME3/r6C0GD.1"
                      # "ME3/r7C0GD.1"
                      # "ME3/r12C0GD.1"
                      
                      # "M13/r41GD.025EC9"
                      # "M13/r42GD.025EC9"
                      # "M13/r43GD.025EC9"
                      # "M13/r44GD.025EC9"
                      # "M13/r45GD.025EC9"

                      # "M13/r36GDEC9"
                      # "M13/r37GDEC9"
                      # "M13/r38GDEC9"
                      # "M13/r39GDEC9"
                      # "M13/r40GDEC9"
                      # "M13/r41GDEC9"
                      # "M13/r42GDEC9"
                      # "M13/r43GDEC9"
                      # "M13/r44GDEC9"
                      # "M13/r45GDEC9"

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    

    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 6 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.5 --MA_bootstrap --experiment_3"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 7 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.5 --MA_bootstrap --experiment_3"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.5 --MA_bootstrap --experiment_3"



    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 6 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map  --MA_bootstrap --experiment_3"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 7 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --MA_bootstrap --experiment_3"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --MA_bootstrap --experiment_3"







    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 6 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.5 --regular_bootstrap --collision_likelihood --experiment_3"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 7 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.5 --regular_bootstrap --collision_likelihood --experiment_3"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.5 --regular_bootstrap --collision_likelihood --experiment_3"




    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 6 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map  --regular_bootstrap --collision_likelihood --experiment_3"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 7 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map  --regular_bootstrap --collision_likelihood --experiment_3"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map  --regular_bootstrap --collision_likelihood --experiment_3"



   

   
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 6 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.5 --collision_likelihood --experiment_3"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 7 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.5 --collision_likelihood --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.5 --collision_likelihood --experiment_3"



    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 6 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map  --collision_likelihood --experiment_3"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 7 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map  --collision_likelihood --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map  --collision_likelihood --experiment_3"



    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 6 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map  --experiment_3"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 7 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --experiment_3"
    
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "72:00:00"
done