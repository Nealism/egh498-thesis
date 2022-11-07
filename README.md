## behaviour_rl ##
This is a repo of environments from various simulations including MuJoCo and PyBullet.

### Environments ###
#### MuJoCo: ####
- Franka Arm from: https://github.com/vikashplus/franka_sim</br>
`python3 run.py --env franka_reach_mj --render`

- Franka Arm from: https://github.com/deepmind/mujoco_menagerie/tree/main/franka_emika_panda</br>
`python3 run.py --env franka_reach_dm_mj --render`

- ANYmal from: https://github.com/deepmind/mujoco_menagerie/tree/main/anybotics_anymal_c</br>
`python3 run.py --env anymal_mj --render`

- Titan </br>
`python3 run.py --env titan_mj --render`

#### PyBullet: ####
- Humanoid walker from PyBullet</br>
`python3 run.py --env humanoid_pb --render`

- Titan</br>
`python3 run.py --env titan_pb --render`

- Pumpkin</br>
`python3 run.py --env pumpkin_pb --render`

- Biped</br>
`python3 run.py --env biped_pb --render`

#### Gazebo: TODO ####
- Titan </br>
`roslaunch behaviour_rl env_titan.launch`
`python3 run.py --env titan_gz`

#### Useful Arguments ####
- Render the simulator.</br>
`--render`
- Use lots of parallel workers, gradients are averaged each update.</br>
`--cpu 8`
- Use curriculum learning, (ANYmal, Franka, Humanoid, Biped), see Guided Curriculum Learning paper</br>
`--cur`
- Add a tree or grass (MuJoCo only):</br>
`--tree_type grass/tree`

See `default_arguments.py` for full list </br>

### RL algorithms ###
    Proximal Policy Optimisation - default

## Getting Started ##
### Install Packages ###
`pip3 install -r requirements.txt`

#### In a Virtual environment ####
- first time: </br>
    - If you want a specific python version (e.g. 3.xx):</br>
        `sudo apt install python3.xx python3-venv python3.xx-venv python3.xx-dev`
        `python3.xx -m venv venv`
    - Else:</br>
        `python3 -m venv venv`
    - source ./venv/bin/activate
    - Install other requirements (while virtual environment is active): </br>
    `pip3 install -r requirements.txt`

- every time: </br>
`source ./venv/bin/activate`
- when finished:</br>
`deactivate`


### Useful scripts: ###
- Replay live training, rendering the robot from the last episode from the latest_test, or a specific folder of the experiment given by args.folder. Also accepts `--test` and `--best` for the latest test run (no randomness) and best episode. </br>
`python3 replay_latest.py --env anymal_mj --exp latest_test`</br>
`python3 replay_latest.py --env anymal_mj --exp latest_test --folder 2022_06_08_9_15_30`

- Run a test with saved weights, rendering the robot from weights from the latest_test, or a specific folder of the experiment given by args.folder. </br>
`python3 run_test.py --env anymal_mj --exp latest_test`</br>
`python3 run_test.py --env anymal_mj --exp latest_test --folder 2022_06_08_9_15_30`

- Render fixed robot to assess joint limits etc (PyBullet envs only). </br>
`python3 run_fixed.py`

## General ##

#### HPC helpful info ####
- https://confluence.csiro.au/display/SC/CSIRO+SC+Shared+Cluster+-+Petrichor and https://confluence.csiro.au/display/SC/Quick+Start+Guide+for+Linux
- To get access to the HPC you need to go to this link: https://sc.it.csiro.au/hpc.
- Then click "Register for Account" and "Find your Project".
- Then enter your project's O2D Id or name. This will then be submitted to the project manager for approval.
- You will not be notified when your project manager adds you to the project, so check the registration form regularly. Once they do, follow the remaining prompts.
- On the CSIRO network, ssh in to petrichor:
`ssh -X $USER@petrichor.hpc.csiro.au`<br/>
- Mount directory to easily see files
    - first time: `mkdir ~/hpc-home` <br/>
    `sudo mount -t cifs //petrichorhome.csiro.au/home_intel/$USER $HOME/hpc-home -o user=$USER,dom=NEXUS,uid=1000`<br/>
- Mount scratch workspace, this is where results and data are typically saved (there isn't much room on the cluster for saving results). This is for temporary storage only. Need to use the datastore if need to save things for longer periods.
    - first time: `sudo mkdir -p /hpc-scratch/$USER` <br/>
    `sudo sshfs -o allow_other $USER@petrichor.hpc.csiro.au:/scratch1/$USER /hpc-scratch/$USER`
- Create save directory to mirror what happens on the HPC, this is where results are saved locally:
    - first time: `sudo mkdir -p /scratch1/$USER/results` <br/>
- Copy code to HPC: <br/>
`rsync -avP --exclude-from=rsync_exclude.txt source destination`
- e.g.<br/>
`rsync -avP --exclude-from=rsync_exclude.txt $HOME/behaviour_rl $USER@petrichor.hpc.csiro.au:$HOME`
- setup environment on the HPC (for the first time, or when you need to add a package):
    - Load a module that you want to install packages on:
        - `module load python/3.11.0`
    - Install anything you need
        -  e.g `pip3 install -r requirements.txt`
    - Installing mujoco (LEGACY, for franka_reach_mj and franka_ball_mj. Now just `pip3 install mujoco`):
        - pip3 install mujoco_py==2.0.2.9
        - Download mujoco file from: https://mujoco.org/download/mujoco210-linux-x86_64.tar.gz 
        - Extract the file to give mujoco210
        - Copy this Install mujoco210 file to $HOME/.mujoco on the HPC: <br/>
            `rsync -avP $HOME/Downloads/mujoco210 $USER@petrichor.hpc.csiro.au:$HOME/.mujoco` <br/>
        - echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/.mujoco/mujoco210/bin' >> ~/.bashrc
        - echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/nvidia' >> ~/.bashrc
        

- Test environment on the HPC (do not use to run jobs!)
    - module load openmpi/4.1.2-ofed51-simple python/3.9.4 glew/2.2.0 mesa/21.1.0 patchelf/0.14.3
    - python3 run.py --ident $USER

- Useful commands:<br/>
    - `squeue -u $USER`<br/>
    - `scancel jobid`<br/>


#### Running experiments
- Run bash script of commands: <br/>
    - Add experiment name, and arguments to Experiments and Arguments lists in `bashies/multi_experiment.sh`
    - rsync changes to HPC <br/>
        `rsync -avP --exclude-from=rsync_exclude.txt $HOME/behaviour_rl $USER@petrichor.hpc.csiro.au:$HOME`
    - Run on HPC: <br/>
    `cd bashies` <br/>
    `./multi_experiment.sh`<br/>
    - bash logs from training are populated where you start the job, i.e. in `bashies`
    - If you have mounted the to hpc-home, you can look at the training logs under `$HOME/hpc-home/behaviour_rl/bashies`
    - periodically flush the `bashies` script: `rm *.out`, these can take up lots of room for large jobs

- From mid November 2022 a project code is required for scheduling jobs. <br/>
    - `get_project_codes` from petrichor <br/>
    - Add the code to: <br/>
        - `base_csiro_pet.sh` <br/>
    - Default: refarm project: <br/>
        - `#SBATCH --OD-227199` <br/>

- Tensorboard and live progress updates
    - Provided you have mounted `hpc-scratch` you can view tensorboard plots:
        - Run:
        -  `tensorboard --logdir $HOME/hpc-scratch/results/experiment_folder`
        - And open a browser to the link



#### Setup new environment (WIP): ####
- Environments are setup in the `assets` folder and stem from env_base.py => env_base_`sim`.py => env_`robot`_`sim`.py </br>

#### Adding Code - Follow the ideas from the reimagine farming / subt projects
- Develop on a new branch using naming conventions: feature/some_cool_feature, bugfix/some_bug_fix.
- Commit when code has been tested, treat commits as checkpoints to working code that you can easily return to if needed.
- Once happy that a feature works, submit a PR (pull request) to get the feature merged in with the master branch. The merged branch is usually deleted, but can be preserved for working experiments.
- Try to get things merged into master so that cool features are available to other users (a branch should only be alive for days to weeks, not months).
- Create "tags" for meaningful checkpoints, for example for a code used in a paper.