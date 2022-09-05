## behaviour_rl ##
This is a repo of environments from various simulations including MuJoCo and PyBullet 

### Environments ###
#### MuJoCo: ####
- Franka Arm</br>
`python3 run.py --env franka_mj`

- Dual Franka Arm </br>
`python3 run.py --env bi_franka_mj`

- ANYmal</br>
`python3 run.py --env anymal_mj`

#### PyBullet: ####
- Humanoid walker </br>
`python3 run.py --env humanoid_pb`

- Humanoid walker - no feet</br>
`python3 run.py --env humanoid_pb_no_feet`

- Biped</br>
`python3 run.py --env biped_pb`

#### Gazebo: TODO ####
- Titan nav </br>
`roslaunch behaviour_rl env_titan.launch`
`python3 run.py --env humanoid_pb`


#### Arguments ####
- Use lots of parallel workers, gradients are averaged each update.</br>
`--cpu 8`
- Use curriculum learning (humanoid only at this stage), see Guided Curriculum Learning paper</br>
`--cur`

### RL algorithms ###
    Proximal Policy Optimisation - default

### Getting started ###

### Helpers TODO: ###
- Replay live training, rendering the robot from the latest episode specified by args.exp, or a specific folder of the experiment given by args.folder. </br>
`python3 replay_latest.py --env franka_mj --exp latest_test`</br>
`python3 replay_latest.py --env franka_mj --exp latest_test --folder 2022_06_08_9_15_30`

- Render fixed robot to assess joint limits etc. </br>
`python3 run_fixed.py`


### General ###

#### Setup new environment TODO: ####
- Environments are setup in the `assets` folder and stem from env_base.py -> env_base_<sim>.py -> env_<robot>_<sim>.py </br>
- At a minimum environments need: </br>
`reset()` </br>
`step()` </br>


#### Setup virtual environment ####
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


#### HPC helpful info ####
- https://confluence.csiro.au/display/SC/CSIRO+SC+Shared+Cluster+-+Petrichor and https://confluence.csiro.au/display/SC/Quick+Start+Guide+for+Linux
- To get access to the HPC you need to go to this link: https://sc.it.csiro.au/hpc.
- Then click "Register for Account" and "Find your Project"
- Then enter your project's O2D Id or name. This will then be submitted to the project manager for approval.
- On the CSIRO network, ssh in to petrichor:
`ssh -X $USER@petrichor.hpc.csiro.au`<br/>
- Mount directory to easily see files
    - first time: `mkdir ~/hpc-home` <br/>
    `sudo mount -t cifs //petrichorhome.csiro.au/home_intel/$USER $HOME/hpc-home -o user=$USER,dom=NEXUS,uid=1000`<br/>
- Mount scratch workspace, this is where results and data are typically saved (there isn't much room on the cluster for saving results). This is for temporary storage only. Need to use the datastore if need to save things for longer periods.
    - first time: `mkdir ~/hpc-scratch` <br/>
    `sudo sshfs -o allow_other $USER@petrichor.hpc.csiro.au:/scratch1/$USER ~/hpc-scratch`
- Create save directory to mirror what happens on the HPC, this is where results are saved locally:
    - first time: `sudo mkdir -p /scratch1/$USER/results` <br/>
- Copy code to HPC: <br/>
`rsync -avP --exclude-from=rsync_exclude.txt source destination`
- e.g.<br/>
`rsync -avP --exclude-from=rsync_exclude.txt $HOME/behaviour_rl $USER@petrichor.hpc.csiro.au:$HOME`
- setup environment on the HPC (for the first time, or when you need to add a package):
    - Load a module that you want to install packages on:
        - `module load python/3.9.4`
    - Install anything you need
        -  e.g `pip3 install -r requirements.txt`
    - Installing mujoco:
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
- Tensorboard and live progress updates
    - Provided you have mounted `hpc-scratch` you can view tensorboard plots:
        - Run:
        -  `tensorboard --logdir $HOME/hpc-scratch/results/experiment_folder`
        - And open a browser to the link


#### Adding Code - Follow the ideas from the reimagine farming / subt projects
- Develop on a new branch using naming conventions: feature/some_cool_feature, bugfix/some_bug_fix.
- Commit when code has been tested, treat commits as checkpoints to working code that you can easily return to if needed.
- Once happy that a feature works, submit a PR (pull request) to get the feature merged in with the master branch. The merged branch is deleted
- Try to get things merged into master so that cool features are available to other users (a branch should only be alive for days to weeks, not months)
- Create "tags" for meaningful checkpoints, for example for a code base used for a paper.

#### TODOs:
- Separate training from running behaviours for refarm stack (i.e. behavour_nav_rl)
- Run each env, train on HPC (esp mujoco)
- Fix gazebo env
- Move behaviour_rl into own space, check build works for ros stuff