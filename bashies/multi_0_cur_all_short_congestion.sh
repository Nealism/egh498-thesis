#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      

                    
                      
                      #Without Other Robot Info
                      "195/A1r30G1E1"
                      "195/A2r30G1E1"
                      "195/A3r30G1E1"
                      "195/A4r30G1E1"
                      "195/A5r30G1E1"
                      
                      




                      #Ray Mechanism Reward with Other Robot Info
                      "195/B1r30G1E3"
                      "195/B2r30G1E3"
                      "195/B3r30G1E3"
                      "195/B4r30G1E3"
                      "195/B5r30G1E3"
                      





                      #Regular Reward with Other Robot Info
                      "195/C1r28G1E3"
                      "195/C2r28G1E3"
                      "195/C3r28G1E3"
                      "195/C4r28G1E3"
                      "195/C5r28G1E3"


                      #A different Reward with Other Robot Info
                      "195/C1r31G1E3"
                      "195/C2r31G1E3"
                      "195/C3r31G1E3"
                      "195/C4r31G1E3"
                      "195/C5r31G1E3"
                      






                      #MA_BOOT cur only
                      "195/D1r30G1E3MB"
                      "195/D2r30G1E3MB"
                      "195/D3r30G1E3MB"
                      "195/D4r30G1E3MB"
                      "195/D5r30G1E3MB"
                      




                      #Gap cur only
                      "195/E1r30G1E3GC"
                      "195/E2r30G1E3GC"
                      "195/E3r30G1E3GC"
                      "195/E4r30G1E3GC"
                      "195/E5r30G1E3GC"
                      




                      #No Cur
                      "195/F1r30G1E3NC"
                      "195/F2r30G1E3NC"
                      "195/F3r30G1E3NC"
                      "195/F4r30G1E3NC"
                      "195/F5r30G1E3NC"
                      


 
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    
 



    #Without Other Robot Info

    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_1 --ray_wall_type 1 --randomness 2"
    
    
    
    
    
    
    #Ray Mechanism Reward with Other Robot Info
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    
    
    
    
    



   
    #Regular Reward with Other Robot Info
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 28 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"



    #A Different Reward with Other Robot Info
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 31 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1   --experiment_3  --ray_wall_type 1 --randomness 2"
    
    
    
    
    #MA_BOOT cur only
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map --expert_curr --MA_bootstrap  --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    





    #GAP cur only
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map  --gap_curr  --gap_decrease 0.05 --starting_gap_width 1.8 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    

    
    
    

    #NO CUR
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    "--cpu 64 --env multi_robot_pb --num_robots 2 --multi_titans --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 1000 --max_ep_len 300 --local_epoch_len 1500  --detect_distance 1.8 --insert_wall --use_perception --occupancy_map   --gap_curr  --gap_decrease 0.0 --starting_gap_width 1 --final_gap_width 1  --experiment_3  --ray_wall_type 1 --randomness 2"
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "72:00:00"
done