#!/bin/bash

sbatch ./base_csiro.sh "train_single.py" "none" "--cpu 16 --exp single --episodes 200" "12:00:00"

