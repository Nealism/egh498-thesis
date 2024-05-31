#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      

                    
                      
                      #Step Reward
                      "307/A1r21G1E3"
                      "307/A2r21G1E3"
                      "307/A3r21G1E3"
                      "307/A4r21G1E3"
                      "307/A5r21G1E3"
                      
                      




                      #Step Reward 2
                      "307/B1r22G1E3"
                      "307/B2r22G1E3"
                      "307/B3r22G1E3"
                      "307/B4r22G1E3"
                      "307/B5r22G1E3"
                      





                      #Regular Reward 
                      "307/C1r23G1E3"
                      "307/C2r23G1E3"
                      "307/C3r23G1E3"
                      "307/C4r23G1E3"
                      "307/C5r23G1E3"


                      #Regular Reward 2
                      "307/CA1r24G1E3"
                      "307/CA2r24G1E3"
                      "307/CA3r24G1E3"
                      "307/CA4r24G1E3"
                      "307/CA5r24G1E3"



                      #Regular Reward 4
                      "307/CB1r26G1E3"
                      "307/CB2r26G1E3"
                      "307/CB3r26G1E3"
                      "307/CB4r26G1E3"
                      "307/CB5r26G1E3"
                      






                      #Regular Reward 3
                      "307/D1r25G1E3"
                      "307/D2r25G1E3"
                      "307/D3r25G1E3"
                      "307/D4r25G1E3"
                      "307/D5r25G1E3"
                      




                      #Ray Reward 1
                      "307/E1r27G1E3"
                      "307/E2r27G1E3"
                      "307/E3r27G1E3"
                      "307/E4r27G1E3"
                      "307/E5r27G1E3"
                      




                      #Ray Reward 2
                      "307/F1r29G1E3"
                      "307/F2r29G1E3"
                      "307/F3r29G1E3"
                      "307/F4r29G1E3"
                      "307/F5r29G1E3"
                      


 
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    
 



    #Step Reward 1
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 21 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    
    
    
    
    
    
    #Step Reward 2
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 22 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"




    #Regular Reward 1
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 23 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"


    #Regular Reward 2
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 24 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"


    #Regular Reward 4
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 26 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"


    #Regular Reward 3
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 25 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"


    #Ray Based Reward 1
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 27 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"


    #Ray Based Reward 1
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 29 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 2500 --max_ep_len 200 --local_epoch_len 2000  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1  --ray_wall_type 1 --randomness 2"
    
    
    
    
    



   
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "72:00:00"
done