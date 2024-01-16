#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      "ME4/r10MGD.5E"
                      "ME4/r11MGD.5E"
                      "ME4/r12MGD.5E"
                      "ME4/r13MGD.5E"
                      "ME4/r14MGD.5E"
                      "ME4/r15MGD.5E"

                      

                      "ME4/r10MG30E"
                      "ME4/r11MG30E"
                      "ME4/r12MG30E"
                      "ME4/r13MG30E"
                      "ME4/r14MG30E"
                      "ME4/r15MG30E"


                      

                      "ME4/r10RGD.5EC"
                      "ME4/r11RGD.5EC"
                      "ME4/r12RGD.5EC"
                      "ME4/r13RGD.5EC"
                      "ME4/r14RGD.5EC"
                      "ME4/r15RGD.5EC"


                      

                      "ME4/r10RG30EC"
                      "ME4/r11RG30EC"
                      "ME4/r12RG30EC"
                      "ME4/r13RG30EC"
                      "ME4/r14RG30EC"
                      "ME4/r15RG30EC"



                    

                      "ME4/r10GD.5C"
                      "ME4/r11GD.5C"
                      "ME4/r12GD.5C"
                      "ME4/r13GD.5C"
                      "ME4/r14GD.5C"
                      "ME4/r15GD.5C"



                      "ME4/r10G30C"
                      "ME4/r11G30C"
                      "ME4/r12G30C"
                      "ME4/r13G30C"
                      "ME4/r14G30C"
                      "ME4/r15G30C"

                      


                      "ME4/r10G30"
                      "ME4/r11G30"
                      "ME4/r12G30"
                      "ME4/r13G30"
                      "ME4/r14G30"
                      "ME4/r15G30"


                      # "ME4/r6REC0"
                      # "ME4/r7REC0"
                      # # "ME4/r8REC0"
                      # # "ME4/r9REC0"
                      # "ME4/r10REC0"
                      # # "ME4/r11REC0"
                      # "ME4/r12REC0"



                      # "ME4/r6C0GD.1"
                      # "ME4/r7C0GD.1"
                      # "ME4/r12C0GD.1"
                      
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
    

    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.5 --MA_bootstrap --experiment_1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 11 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.5 --MA_bootstrap --experiment_1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.5 --MA_bootstrap --experiment_1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.5 --MA_bootstrap --experiment_1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 14 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.5 --MA_bootstrap --experiment_1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 15 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.5 --MA_bootstrap --experiment_1"



    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map  --MA_bootstrap --experiment_1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 11 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --MA_bootstrap --experiment_1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --MA_bootstrap --experiment_1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map  --MA_bootstrap --experiment_1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 14 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --MA_bootstrap --experiment_1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 15 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --MA_bootstrap --experiment_1"







    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.5 --regular_bootstrap --collision_likelihood --experiment_1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 11 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.5 --regular_bootstrap --collision_likelihood --experiment_1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.5 --regular_bootstrap --collision_likelihood --experiment_1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.5 --regular_bootstrap --collision_likelihood --experiment_1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 14 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.5 --regular_bootstrap --collision_likelihood --experiment_1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 15 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.5 --regular_bootstrap --collision_likelihood --experiment_1"




    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map  --regular_bootstrap --collision_likelihood --experiment_1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 11 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map  --regular_bootstrap --collision_likelihood --experiment_1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map  --regular_bootstrap --collision_likelihood --experiment_1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map  --regular_bootstrap --collision_likelihood --experiment_1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 14 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map  --regular_bootstrap --collision_likelihood --experiment_1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 15 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000 --expert_curr --detect_distance 2 --insert_wall --use_perception --occupancy_map  --regular_bootstrap --collision_likelihood --experiment_1"



   

   
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.5 --collision_likelihood --experiment_1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 11 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.5 --collision_likelihood --experiment_1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.5 --collision_likelihood --experiment_1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr  --gap_decrease 0.5 --collision_likelihood --experiment_1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 14 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.5 --collision_likelihood --experiment_1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 15 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --gap_curr --gap_decrease 0.5 --collision_likelihood --experiment_1"



    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map  --collision_likelihood --experiment_1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 11 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map  --collision_likelihood --experiment_1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map  --collision_likelihood --experiment_1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map  --collision_likelihood --experiment_1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 14 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map  --collision_likelihood --experiment_1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 15 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map  --collision_likelihood --experiment_1"



    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map  --experiment_1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 11 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --experiment_1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --experiment_1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map  --experiment_1"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 14 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --experiment_1"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 15 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2000 --local_epoch_len 2000  --detect_distance 2 --insert_wall --use_perception --occupancy_map --experiment_1"
    
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "72:00:00"
done