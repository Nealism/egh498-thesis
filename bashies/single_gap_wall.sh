#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      "sg12/r2GD.5EC9"
                      "sg12/r2GD.1EC9"
                      "sg12/r2GD.25EC9"
                      "sg12/r2EC9"
                      "sg12/r2GD.025EC9"
                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    

    
    "--cpu 64 --env multi_robot_pb --reward_fn 2 --cur_succ 9  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 2 --insert_wall --gap_curr"

    
    "--cpu 64 --env multi_robot_pb --reward_fn 2 --cur_succ 9  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"
    
    
    "--cpu 64 --env multi_robot_pb --reward_fn 2 --cur_succ 9  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.25"

    
    "--cpu 64 --env multi_robot_pb --reward_fn 2 --cur_succ 9  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 2 --insert_wall"

    "--cpu 64 --env multi_robot_pb --reward_fn 2 --cur_succ 9  --training_on_hpc --gap_avoidance --epochs 8400 --max_ep_len 3000 --local_epoch_len 3000 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.025"

   
    
    
    
    
   

    


    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "48:00:00"
done