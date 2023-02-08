declare -a Experiments=(
                      "skyscrapers_v2"

                        )
declare -a Arguments=(
    "--cpu 1 --env anymal_cmd_mj --epochs 3000 
    --render --show_map
    --max_ep_len 512 --local_epoch_len 1024 
    --add_terrain --rand_dz_mult 0.40 
    --undul_patches 45 
    --use_perception 
    --obs_fn 2 --reward_fn 2"
)
            
for (( i=0; i<${#Arguments[@]}; i++ )); do 
  python3 run.py --exp ${Experiments[$i]} ${Arguments[$i]}
done
