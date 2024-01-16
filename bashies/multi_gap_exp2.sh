#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      "ME5/r10MGD.5E"
                      "ME5/r11MGD.5E"
                      "ME5/r12MGD.5E"
                      "ME5/r13MGD.5E"
                      "ME5/r14MGD.5E"
                      "ME5/r15MGD.5E"

                      

                      "ME5/r10MG30E"
                      "ME5/r11MG30E"
                      "ME5/r12MG30E"
                      "ME5/r13MG30E"
                      "ME5/r14MG30E"
                      "ME5/r15MG30E"


                      

                      "ME5/r10RGD.5EC"
                      "ME5/r11RGD.5EC"
                      "ME5/r12RGD.5EC"
                      "ME5/r13RGD.5EC"
                      "ME5/r14RGD.5EC"
                      "ME5/r15RGD.5EC"


                      

                      "ME5/r10RG30EC"
                      "ME5/r11RG30EC"
                      "ME5/r12RG30EC"
                      "ME5/r13RG30EC"
                      "ME5/r14RG30EC"
                      "ME5/r15RG30EC"



                      # "ME5/r6GD.5C"
                      # "ME5/r7GD.5C"
                      # "ME5/r12GD.5C"

                      # "ME5/r6G30C"
                      # "ME5/r7G30C"
                      # "ME5/r12G30C"

                      # "ME5/r6G30"
                      # "ME5/r7G30"
                      # "ME5/r12G30"


                      # "ME5/r6REC0"
                      # "ME5/r7REC0"
                      # # "ME5/r8REC0"
                      # # "ME5/r9REC0"
                      # "ME5/r10REC0"
                      # # "ME5/r11REC0"
                      # "ME5/r12REC0"



                      # "ME5/r6C0GD.1"
                      # "ME5/r7C0GD.1"
                      # "ME5/r12C0GD.1"
                      
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
    

    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.5 --MA_bootstrap --experiment_2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 11 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.5 --MA_bootstrap --experiment_2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.5 --MA_bootstrap --experiment_2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.5 --MA_bootstrap --experiment_2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 14 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.5 --MA_bootstrap --experiment_2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 15 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.5 --MA_bootstrap --experiment_2"



    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map  --MA_bootstrap --experiment_2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 11 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --MA_bootstrap --experiment_2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --MA_bootstrap --experiment_2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map  --MA_bootstrap --experiment_2"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 14 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --MA_bootstrap --experiment_2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 15 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --MA_bootstrap --experiment_2"







    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.5 --regular_bootstrap --collision_likelihood --experiment_2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 11 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.5 --regular_bootstrap --collision_likelihood --experiment_2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.5 --regular_bootstrap --collision_likelihood --experiment_2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.5 --regular_bootstrap --collision_likelihood --experiment_2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 14 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.5 --regular_bootstrap --collision_likelihood --experiment_2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 15 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.5 --regular_bootstrap --collision_likelihood --experiment_2"




    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map  --regular_bootstrap --collision_likelihood --experiment_2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 11 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map  --regular_bootstrap --collision_likelihood --experiment_2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map  --regular_bootstrap --collision_likelihood --experiment_2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map  --regular_bootstrap --collision_likelihood --experiment_2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 14 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map  --regular_bootstrap --collision_likelihood --experiment_2"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 15 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map  --regular_bootstrap --collision_likelihood --experiment_2"



   

   
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 6 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.5 --collision_likelihood --experiment_2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 7 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.5 --collision_likelihood --experiment_2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.5 --collision_likelihood --experiment_2"



    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 6 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map  --collision_likelihood --experiment_2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 7 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map  --collision_likelihood --experiment_2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map  --collision_likelihood --experiment_2"



    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 6 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map  --experiment_2"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 7 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --experiment_2"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --experiment_2"
    
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "72:00:00"
done