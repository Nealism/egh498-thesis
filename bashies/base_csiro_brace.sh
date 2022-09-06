#!/bin/bash
sbatch <<EOT
#!/bin/bash
#SBATCH --job-name=$2
#SBATCH --time=$4
#SBATCH --mem=256g
#SBATCH --ntasks-per-node=14
#SBATCH --nodes=1
ulimit -s 10240
module load openmpi tensorflow/1.15.5-py37-cuda102
cd $HOME/behaviour_rl
echo python $1 --exp $2 $3
python $1 --exp $2 $3

hostname

exit 0
EOT