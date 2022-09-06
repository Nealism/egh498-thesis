#!/bin/bash
sbatch <<EOT
#!/bin/bash
#SBATCH --job-name=$2
#SBATCH --time=$4
#SBATCH --mem=512g
#SBATCH --ntasks-per-node=64
#SBATCH --nodes=1
ulimit -s 10240
module load openmpi/4.1.2-ofed51-simple python/3.9.4 glew/2.2.0 mesa/21.1.0 patchelf/0.14.3
cd $HOME/behaviour_rl
echo python $1 --exp $2 $3
python $1 --exp $2 $3

hostname

exit 0
EOT