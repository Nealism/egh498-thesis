#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      "skyscrapers_v2"

                        )
declare -a Arguments=(
    "--cpu 64 --env anymal_cmd_mj --training_on_hpc --epochs 3000 --max_ep_len 512 --local_epoch_len 1024 --add_terrain --rand_dz_mult 0.40 --undul_patches 45 --use_perception --obs_fn 1 --reward_fn 1"
)
            
export SBATCH_ACCOUNT=OD-219033
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "01:00:00"
done