#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      "M3/r13MGD.5E"
                      "M3/r16MGD.5E"
                      "M3/r17MGD.5E"
                      "M3/r18MGD.5E"
                      # "M3/r13MGD.5E"
                      # "M3/r14MGD.5E"
                      # "M3/r15MGD.5E"

                      

                      # "M3/r10MG30E"
                      # "M3/r11MG30E"
                      # "M3/r12MG30E"
                      # "M3/r13MG30E"
                      # "M3/r14MG30E"
                      # "M3/r15MG30E"


                      

                      "M3/r13RGD.5EC"
                      "M3/r16RGD.5EC"
                      "M3/r17RGD.5EC"
                      "M3/r18RGD.5EC"
                      # "M3/r13RGD.5EC"
                      # "M3/r14RGD.5EC"
                      # "M3/r15RGD.5EC"

                      "M3/r13GD.5EC"
                      "M3/r16GD.5EC"
                      "M3/r17GD.5EC"
                      "M3/r18GD.5EC"




                      

                      # "M3/r10RG30EC"
                      # "M3/r11RG30EC"
                      # "M3/r12RG30EC"
                      # "M3/r13RG30EC"
                      # "M3/r14RG30EC"
                      # "M3/r15RG30EC"



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
    

    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall  --gap_curr  --gap_decrease 0.5 --MA_bootstrap --experiment_3"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 16 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall  --gap_curr  --gap_decrease 0.5 --MA_bootstrap --experiment_3"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 17 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall  --gap_curr --gap_decrease 0.5 --MA_bootstrap --experiment_3"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 18 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall  --gap_curr --gap_decrease 0.5 --MA_bootstrap --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall  --gap_curr  --gap_decrease 0.5 --MA_bootstrap --experiment_3"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 14 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall  --gap_curr --gap_decrease 0.5 --MA_bootstrap --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 15 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall  --gap_curr --gap_decrease 0.5 --MA_bootstrap --experiment_3"



    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall   --MA_bootstrap --experiment_3"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 11 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall  --MA_bootstrap --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall  --MA_bootstrap --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall   --MA_bootstrap --experiment_3"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 14 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall  --MA_bootstrap --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 15 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall  --MA_bootstrap --experiment_3"






    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall  --gap_curr  --gap_decrease 0.5 --regular_bootstrap --collision_likelihood --experiment_3"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 16 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall  --gap_curr  --gap_decrease 0.5 --regular_bootstrap --collision_likelihood --experiment_3"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 17 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall  --gap_curr --gap_decrease 0.5 --regular_bootstrap --collision_likelihood --experiment_3"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 18 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall  --gap_curr --gap_decrease 0.5 --regular_bootstrap --collision_likelihood --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall  --gap_curr  --gap_decrease 0.5 --regular_bootstrap --collision_likelihood --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 14 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall  --gap_curr --gap_decrease 0.5 --regular_bootstrap --collision_likelihood --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 15 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall  --gap_curr --gap_decrease 0.5 --regular_bootstrap --collision_likelihood --experiment_3"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall  --gap_curr  --gap_decrease 0.5  --collision_likelihood --experiment_3"
    
    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 16 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall  --gap_curr  --gap_decrease 0.5  --collision_likelihood --experiment_3"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 17 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall  --gap_curr --gap_decrease 0.5  --collision_likelihood --experiment_3"

    "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 18 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall  --gap_curr --gap_decrease 0.5  --collision_likelihood --experiment_3"


    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall   --regular_bootstrap --collision_likelihood --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 11 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall   --regular_bootstrap --collision_likelihood --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall   --regular_bootstrap --collision_likelihood --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall   --regular_bootstrap --collision_likelihood --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 14 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall   --regular_bootstrap --collision_likelihood --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 15 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200 --expert_curr --detect_distance 2 --insert_wall   --regular_bootstrap --collision_likelihood --experiment_3"



   

   
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 6 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall  --gap_curr  --gap_decrease 0.5 --collision_likelihood --experiment_3"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 7 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall  --gap_curr --gap_decrease 0.5 --collision_likelihood --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall  --gap_curr --gap_decrease 0.5 --collision_likelihood --experiment_3"



    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 6 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall   --collision_likelihood --experiment_3"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 7 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall   --collision_likelihood --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall   --collision_likelihood --experiment_3"



    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 6 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall   --experiment_3"
    
    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 7 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall  --experiment_3"

    # "--cpu 64 --env multi_robot_pb --num_robots 2 --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 2200 --local_epoch_len 2200  --detect_distance 2 --insert_wall  --experiment_3"
    
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "72:00:00"
done