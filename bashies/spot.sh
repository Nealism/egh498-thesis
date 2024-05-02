#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                        "spot_pet/all_5_6"
                        "spot_pet/all_5_8"
                        "spot_pet/all_3_5"
                        "spot_pet/all_3_7"


                        )
declare -a Arguments=(
    "--cpu 64 --env spot_pb --cur --ang_vel_tracking_sigma 0.5 --cur_thres 0.5 --with_initial_cmd"  
    "--cpu 64 --env spot_pb --cur --ang_vel_tracking_sigma 0.5 --cur_thres 0.7 --with_initial_cmd"  
    "--cpu 64 --env spot_pb --cur --ang_vel_tracking_sigma 0.3 --cur_thres 0.5 --with_initial_cmd"  
    "--cpu 64 --env spot_pb --cur --ang_vel_tracking_sigma 0.3 --cur_thres 0.7 --with_initial_cmd"  
)
            
export SBATCH_ACCOUNT=OD-235390
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "24:00:00"
done