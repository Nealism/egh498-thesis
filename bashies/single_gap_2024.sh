#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      # "sg13/r43GD.5EC9"
                      # "sg13/r43GD.1EC9"
                      # "sg13/r43GD.25EC9"

                      "sg23/r6TC0"
                      "sg23/r7TC0"
                      "sg23/r8TC0"
                      "sg23/r9TC0"
                      "sg23/r10TC0"
                      "sg23/r11TC0"
                      "sg23/r12TC0"
                      "sg23/r13TC0"
                      "sg23/r14TC0"
                      "sg23/r15TC0"
                      "sg23/r16TC0"
                      "sg23/r17TC0"
                      "sg23/r18TC0"
                      "sg23/r19TC0"
                      "sg23/r20TC0"


                      "sg23/r6GD.1EC0"
                      "sg23/r7GD.1EC0"
                      "sg23/r8GD.1EC0"
                      "sg23/r9GD.1EC0"
                      "sg23/r10GD.1EC0"
                      "sg23/r11GD.1EC0"
                      "sg23/r12GD.1EC0"
                      "sg23/r13GD.1EC0"
                      "sg23/r14GD.1EC0"
                      "sg23/r15GD.1EC0"
                      "sg23/r16GD.1EC0"
                      "sg23/r17GD.1EC0"
                      "sg23/r18GD.1EC0"
                      "sg23/r19GD.1EC0"
                      "sg23/r20GD.1EC0"
                      
                      

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

    
    # "--cpu 64 --env multi_robot_pb --reward_fn 30 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1 --load_path /scratch3/kom018/results/multi_robot_pb/sg21/r47GD.1EC0/2023_12_30_05_05_57/model.pt"

    "--cpu 64 --env multi_robot_pb --reward_fn 6 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --detect_distance 2 --insert_wall --load_path /scratch3/kom018/results/multi_robot_pb/sg21/r47GD.1EC0/2023_12_30_05_05_57/model.pt"

    "--cpu 64 --env multi_robot_pb --reward_fn 7 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --detect_distance 2 --insert_wall --load_path /scratch3/kom018/results/multi_robot_pb/sg21/r47GD.1EC0/2023_12_30_05_05_57/model.pt"

    "--cpu 64 --env multi_robot_pb --reward_fn 8 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --detect_distance 2 --insert_wall --load_path /scratch3/kom018/results/multi_robot_pb/sg21/r47GD.1EC0/2023_12_30_05_05_57/model.pt"

    "--cpu 64 --env multi_robot_pb --reward_fn 9 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --detect_distance 2 --insert_wall --load_path /scratch3/kom018/results/multi_robot_pb/sg21/r47GD.1EC0/2023_12_30_05_05_57/model.pt"

    "--cpu 64 --env multi_robot_pb --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --detect_distance 2 --insert_wall --load_path /scratch3/kom018/results/multi_robot_pb/sg21/r47GD.1EC0/2023_12_30_05_05_57/model.pt"



    "--cpu 64 --env multi_robot_pb --reward_fn 11 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --detect_distance 2 --insert_wall --load_path /scratch3/kom018/results/multi_robot_pb/sg21/r47GD.1EC0/2023_12_30_05_05_57/model.pt"

    "--cpu 64 --env multi_robot_pb --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --detect_distance 2 --insert_wall --load_path /scratch3/kom018/results/multi_robot_pb/sg21/r47GD.1EC0/2023_12_30_05_05_57/model.pt"

    "--cpu 64 --env multi_robot_pb --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --detect_distance 2 --insert_wall --load_path /scratch3/kom018/results/multi_robot_pb/sg21/r47GD.1EC0/2023_12_30_05_05_57/model.pt"

    "--cpu 64 --env multi_robot_pb --reward_fn 14 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --detect_distance 2 --insert_wall --load_path /scratch3/kom018/results/multi_robot_pb/sg21/r47GD.1EC0/2023_12_30_05_05_57/model.pt"

    "--cpu 64 --env multi_robot_pb --reward_fn 15 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --detect_distance 2 --insert_wall --load_path /scratch3/kom018/results/multi_robot_pb/sg21/r47GD.1EC0/2023_12_30_05_05_57/model.pt"

    "--cpu 64 --env multi_robot_pb --reward_fn 16 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --detect_distance 2 --insert_wall --load_path /scratch3/kom018/results/multi_robot_pb/sg21/r47GD.1EC0/2023_12_30_05_05_57/model.pt"

    "--cpu 64 --env multi_robot_pb --reward_fn 17 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --detect_distance 2 --insert_wall --load_path /scratch3/kom018/results/multi_robot_pb/sg21/r47GD.1EC0/2023_12_30_05_05_57/model.pt"

    "--cpu 64 --env multi_robot_pb --reward_fn 18 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --detect_distance 2 --insert_wall --load_path /scratch3/kom018/results/multi_robot_pb/sg21/r47GD.1EC0/2023_12_30_05_05_57/model.pt"

    "--cpu 64 --env multi_robot_pb --reward_fn 19 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --detect_distance 2 --insert_wall --load_path /scratch3/kom018/results/multi_robot_pb/sg21/r47GD.1EC0/2023_12_30_05_05_57/model.pt"

    "--cpu 64 --env multi_robot_pb --reward_fn 20 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --detect_distance 2 --insert_wall --load_path /scratch3/kom018/results/multi_robot_pb/sg21/r47GD.1EC0/2023_12_30_05_05_57/model.pt"









    "--cpu 64 --env multi_robot_pb --reward_fn 6 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --reward_fn 7 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --reward_fn 8 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --reward_fn 9 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --reward_fn 10 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"



    "--cpu 64 --env multi_robot_pb --reward_fn 11 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --reward_fn 12 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --reward_fn 13 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --reward_fn 14 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --reward_fn 15 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --reward_fn 16 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --reward_fn 17 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --reward_fn 18 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --reward_fn 19 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"

    "--cpu 64 --env multi_robot_pb --reward_fn 20 --cur_succ 0  --training_on_hpc --gap_avoidance --epochs 10000 --max_ep_len 3200 --local_epoch_len 3200 --expert_curr --detect_distance 2 --insert_wall --gap_curr --gap_decrease 0.1"


    


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