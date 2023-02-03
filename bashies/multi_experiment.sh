#!/bin/bash

# ==================================================================================
# Experiment type
# ==================================================================================
declare -a Experiments=(
                      # "whole_terr"
                      # "patches"
                      "perc_and_patches"
                        )
declare -a Arguments=(
    # "--cpu 32 --env anymal_cmd_mj --training_on_hpc --epochs 3000 --max_ep_len 256 --local_epoch_len 1024 --wp_time_scalar 2.5 --reward_fn 3 --obs_fn 3 --add_terrain --rand_dz_mult 0.018"
    # "--cpu 32 --env anymal_cmd_mj --training_on_hpc --epochs 3000 --max_ep_len 256 --local_epoch_len 1024 --wp_time_scalar 2.5 --reward_fn 3 --obs_fn 3 --add_terrain --rand_dz_mult 0.018 --undul_patches 25"
    "--cpu 32 --env anymal_cmd_mj --training_on_hpc --epochs 3000 --max_ep_len 256 --local_epoch_len 1024 --wp_time_scalar 2.5 --reward_fn 3 --obs_fn 3 --add_terrain --rand_dz_mult 0.018 --undul_patches 25 --use_perception"

    )
            
export SBATCH_ACCOUNT=OD-219033
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  sbatch ./base_csiro_pet.sh "run.py" ${Experiments[$i]} "${Arguments[$i]}" "12:00:00"
done