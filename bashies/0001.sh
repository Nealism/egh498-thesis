#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      
                      
                      

                    
                    

                      
 



                      "0001/all_5_5"
                      "0001/all_5_7"
                      "0001/all_3_5"
                      "0001/all_3_7"
                      "0001/all_7_7"
                      "0001/all_7_9"
                      "0001/Tall_5_5"
                      "0001/Tall_5_7"
                      "0001/Tall_3_5"
                      "0001/Tall_3_7"
                      "0001/Tall_7_7"
                      "0001/Tall_7_9"
                      


                      
                      






                      
                      


 
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      

                    
                      

                      
                      
                      
                      
                      
                      

                        )
declare -a Arguments=(
    



  
    #Simple Reward 
    "--cpu 64 --env spot_pb --cur --ang_vel_tracking_sigma 0.5 --cur_thres 0.5 --with_initial_cmd"  
    "--cpu 64 --env spot_pb --cur --ang_vel_tracking_sigma 0.5 --cur_thres 0.7 --with_initial_cmd"  
    "--cpu 64 --env spot_pb --cur --ang_vel_tracking_sigma 0.3 --cur_thres 0.5 --with_initial_cmd"  
    "--cpu 64 --env spot_pb --cur --ang_vel_tracking_sigma 0.3 --cur_thres 0.7 --with_initial_cmd"  
    "--cpu 64 --env spot_pb --cur --ang_vel_tracking_sigma 0.7 --cur_thres 0.7 --with_initial_cmd"  
    "--cpu 64 --env spot_pb --cur --ang_vel_tracking_sigma 0.7 --cur_thres 0.9 --with_initial_cmd"
    "--cpu 64 --env spot_pb --cur --ang_vel_tracking_sigma 0.5 --cur_thres 0.5 --with_initial_cmd --load_path /home/kom018/behaviour_rl/resources/spot/2024_05_13_11_11_30/model.pt"  
    "--cpu 64 --env spot_pb --cur --ang_vel_tracking_sigma 0.5 --cur_thres 0.7 --with_initial_cmd --load_path /home/kom018/behaviour_rl/resources/spot/2024_05_13_11_11_30/model.pt"  
    "--cpu 64 --env spot_pb --cur --ang_vel_tracking_sigma 0.3 --cur_thres 0.5 --with_initial_cmd --load_path /home/kom018/behaviour_rl/resources/spot/2024_05_13_11_11_30/model.pt"  
    "--cpu 64 --env spot_pb --cur --ang_vel_tracking_sigma 0.3 --cur_thres 0.7 --with_initial_cmd --load_path /home/kom018/behaviour_rl/resources/spot/2024_05_13_11_11_30/model.pt"  
    "--cpu 64 --env spot_pb --cur --ang_vel_tracking_sigma 0.7 --cur_thres 0.7 --with_initial_cmd --load_path /home/kom018/behaviour_rl/resources/spot/2024_05_13_11_11_30/model.pt"  
    "--cpu 64 --env spot_pb --cur --ang_vel_tracking_sigma 0.7 --cur_thres 0.9 --with_initial_cmd --load_path /home/kom018/behaviour_rl/resources/spot/2024_05_13_11_11_30/model.pt"
    

    
    
)
            
export SBATCH_ACCOUNT=OD-227420
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "72:00:00"
done