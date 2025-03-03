import torch
import os
import numpy as np
import glob
import time
from pathlib import Path
import default_arguments
from utils.plotter import Plotter
import pandas as pd
import copy
from scipy.ndimage import label, generate_binary_structure

import time
import matplotlib.pyplot as plt
import os
import pandas as pd

home = str(Path.home())

args = default_arguments.get_defaults()

if args.hpc:
    path_home = "/hpc-scratch/" + home.split("/")[-1]
elif args.home:
    path_home = home 
else:
    path_home = "/scratch3/" + home.split("/")[-1]


if args.home:
    path_home += "/behaviour_rl/" +  args.exp + "/"

else:
    path_home += "/results/" + args.env + "/" + args.exp + "/"

if args.folder == "":
    # Get latest experiment (eg: latest model inside test folder)
    folders = [folder.split("/")[-2] for folder in glob.glob(path_home + "*/")]
    latest_folder = "1900_01_01_01_01_01"
    latest_date_key = time.strptime(latest_folder, "%Y_%m_%d_%H_%M_%S")
    for folder in folders:
        new_date_key = time.strptime(folder, "%Y_%m_%d_%H_%M_%S")
        if new_date_key > latest_date_key:
            latest_date_key = new_date_key
            latest_folder = folder
else:
    latest_folder = args.folder

PATH = path_home + latest_folder

Env, args = default_arguments.get_env(args)   
args.render = True
# args.render = False
# if args.figure:
#     args.render = False
args.record_sim = False
env = Env(PATH=PATH, args=args)


if args.jit_model:
    # model_mu=torch.load("Saved_models/JIT_models/mu_net.jit")
    # model_z=torch.load("Saved_models/JIT_models/z_net.jit")
    model_mu=torch.load("/home/kom018/refarm/src/multi_robot_rl/scripts/JIT_models/FC/mu_net.jit")
    model_z=torch.load("/home/kom018/refarm/src/multi_robot_rl/scripts/JIT_models/FC/z_net.jit")
    
    
else:

    pol = torch.load(PATH + "/model.pt")


start_time=time.time()

# if args.num_robots>0:

r1_buffer_linear_action=[]
r1_buffer_angular_action=[]

r1_buffer_ego_pos_x_obs=[]
r1_buffer_ego_pos_y_obs=[]

r1_buffer_roll_obs=[]
r1_buffer_pitch_obs=[]

r1_buffer_linear_obs=[]
r1_buffer_angular_obs=[]

buffer_time=[]

r1_poses_x=[]
r1_poses_y=[]

if args.num_robots==2:
    r2_buffer_linear_action=[]
    r2_buffer_angular_action=[]

    r2_buffer_ego_pos_x_obs=[]
    r2_buffer_ego_pos_y_obs=[]

    r2_buffer_roll_obs=[]
    r2_buffer_pitch_obs=[]

    r2_buffer_linear_obs=[]
    r2_buffer_angular_obs=[]

    r2_poses_x=[]
    r2_poses_y=[]


def run(args): 

    
    

    n=0
    counting_step=0
    # print(pol)

    obs = env.reset()

    if env.args.heterogeneous or env.args.titanheads:
        # if ac_size==(2,3):
        if "titan" in str(env.robots[0]):
            # print("O_before",len(o[0]),o)
            obs[0] = np.insert(obs[0], 0, 0)
            obs[1] = np.insert(obs[1], 0, 1)
            # print("O_after",len(obs[0]),o)
        # elif ac_size==(3,2):
        elif "spot" in str(env.robots[0]):
            # print("O_before",len(obs[0]),o)
            obs[0] = np.insert(obs[0], 0, 1)
            obs[1] = np.insert(obs[1], 0, 0)
    
    # print("ob_reset",obs,len(obs[0]),len(obs[1]))
    if args.use_perception:
        im = env.get_image()
        # print(im,type(im),im[0][0][1].shape)
    # obs=[[obs[0],obs[0]]]
    # im=[im[0],im[0]]
    # obs=obs[0][0]
    # im=im[0]
    # print("im",im,im[0],im.shape)
    # print("OBS",obs,np.array(obs).shape)


    # print(pol)
    time_saving=[]
    action_saving1=[]
    action_saving2=[]

    # model1 = copy.deepcopy(pol.pi.mu_net).to('cpu')
    # traced_script_module1 = torch.jit.script(model1)
    # # traced_script_module1.save("/home/kom018/behaviour_rl/Saved_models/JIT_models/mu_net_s.jit")
    # traced_script_module1.save("/home/kom018/refarm/src/multi_robot_rl/scripts/JIT_models/turtle_titan85/mu_net_simul.jit")

    # model2 = copy.deepcopy(pol.pi.z_net).to('cpu')
    # traced_script_module2 = torch.jit.script(model2)
    # # traced_script_module2.save("/home/kom018/behaviour_rl/Saved_models/JIT_models/z_net_s.jit")
    # traced_script_module2.save("/home/kom018/refarm/src/multi_robot_rl/scripts/JIT_models/turtle_titan85/z_net_simul.jit")

    # model3 = copy.deepcopy(pol.v.v_net).to('cpu')
    # traced_script_module3 = torch.jit.script(model3)
    # # traced_script_module1.save("/home/kom018/behaviour_rl/Saved_models/JIT_models/mu_net_s.jit")
    # traced_script_module3.save("/home/kom018/refarm/src/multi_robot_rl/scripts/JIT_models/turtle_titan85/v_net_simul.jit")

    # model4 = copy.deepcopy(pol.v.z_net).to('cpu')
    # traced_script_module4 = torch.jit.script(model4)
    # # traced_script_module2.save("/home/kom018/behaviour_rl/Saved_models/JIT_models/z_net_s.jit")
    # traced_script_module4.save("/home/kom018/refarm/src/multi_robot_rl/scripts/JIT_models/turtle_titan85/vz_net_simul.jit")


    # print("traced_script_module1",traced_script_module1)
    # print("traced_script_module2",traced_script_module2)
    st=time.time()
    action_saving1=[]
    action_saving2=[]
    save_time=11
    robot1_stop_duration = np.random.uniform(0, 6)  # Random time between 1-3 seconds for robot 1
        # robot1_stop_duration = np.random.uniform(3.5, 4)  # Random time between 1-3 seconds for robot 2
    robot2_stop_duration = np.random.uniform(0, 6)  # Random time between 1-3 seconds for robot 2
    

    while True:
        # print(len(im))
        # print(robot1_stop_duration,robot2_stop_duration)
        current_time = env.steps*1/10
        # Initialize random stop durations for each robot
        
        # print(env)
        # if  current_time < 100:
        # # if current_time > 3 and current_time < 8:
        #     action = pol.step(torch.as_tensor(np.array(obs), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32), stochastic=False)[0]
        #     action[0] = [0, 0]  # Robot 1 stops
        #     action[1] = [0, 0]  # Robot 1 stops

        ##CLOSECALL with forward behaviour do need to code, only run 2 robot side by side withing 1m distance between them
        # #____GAP_ALIGNMENT_________
        # if  current_time < 1.5:
        # # if current_time > 3 and current_time < 8:
        #     action = pol.step(torch.as_tensor(np.array(obs), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32), stochastic=False)[0]
        #     action[0] = [0.8, 0.2]  # Robot 1 stops
        #     action[1] = [0.8, -0.2]  # Robot 1 stops


        ##__Cooperative_Backward
        # # if current_time > 3 and current_time < 8:
        #     action = pol.step(torch.as_tensor(np.array(obs), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32), stochastic=False)[0]
        #     action[0] = [-0.2, 0.0]  # Robot 1 moves backward


        ##__GIVEWAY__EXTENTION_5s
        # # if current_time > 3 and current_time < 8:
        #     action = pol.step(torch.as_tensor(np.array(obs), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32), stochastic=False)[0]
        #     action[0] = [-0.2, 0.0]  # Robot 1 stops
        


        # elif current_time > 3 and current_time < 5:
        #     action[0] = [0, 0]  # Robot 1 stops
        #     action[1] = [0, 0]  # Robot 1 stops
        # elif current_time > 8 and current_time < 10:
        #     action = pol.step(torch.as_tensor(np.array(obs), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32), stochastic=False)[0]
        #     # action=[[-1,0],[-1,0]]
        
        ####___RULE_BASED_TEST______
        # N=80
        # mid_x = N // 2
        # if np.any(im[0][0][:, mid_x:N] == 1):
        #     print("KOMOILLAA")
        # if current_time <1:
        #     # print(im.shape)
        #     action = pol.step(torch.as_tensor(np.array(obs), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32), stochastic=False)[0]
        #     # action = [[0, 0], [0, 0]]  # Default both robots to stop
        #     action = [[-0.2, 0], [-0.2, 0]]  # Default both robots to stop
        # #     # action=[[-1,0],[-1,0]]
        # #Second condition: Stop robots individually for a random time after 2 seconds
        # if current_time < 0 + robot1_stop_duration or current_time < 2 + robot2_stop_duration:
        #     # action = [[0, 0], [0, 0]]  # Default both robots to stop
        #     action = pol.step(torch.as_tensor(np.array(obs), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32), stochastic=False)[0]
            
        #     action_rl1 = pol.step(torch.as_tensor(np.array(obs[0]), dtype=torch.float32), torch.as_tensor(im[0], dtype=torch.float32), stochastic=False)[0]
            
        #     # print(action_rl)
        #     # Check if robot 1 should stop or continue moving
        #     if current_time < 0 + robot1_stop_duration:
        #         action[0] = [0, 0]  # Robot 1 stops
        #     else:
        #         action[0] = action_rl1  # Robot 1 resumes movement
            
        #     if args.num_robots==2:
        #         action_rl2 = pol.step(torch.as_tensor(np.array(obs[1]), dtype=torch.float32), torch.as_tensor(im[1], dtype=torch.float32), stochastic=False)[0]
        #         # Check if robot 2 should stop or continue moving
        #         if current_time < 0 + robot2_stop_duration:
        #             action[1] = [0, 0]  # Robot 2 stops
        #         else:
        #             action[1] = action_rl2  # Robot 2 resumes movement
        # else:
        # print("obs",len(obs),obs)
        if args.use_perception and not args.jit_model:
            # print(torch.as_tensor(np.array(obs), dtype=torch.float32))
            if args.heterogeneous or args.titanheads:
                a_spot,a_titan, v, logp_spot, logp_titan =pol.step(torch.as_tensor(np.array(obs), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32), stochastic=False)
            else:
                action = pol.step(torch.as_tensor(np.array(obs), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32), stochastic=False)[0]
            # print(a_spot,a_titan,len(a_spot),len(a_titan))
            # print(pol)


            if env.args.heterogeneous or env.args.titanheads:
                # if ac_size==(2,3):
                if "titan" in str(env.robots[0]):
                    action=a_titan[0],a_spot[1]
                    logp=[logp_titan[0],logp_spot[1]]
                # elif ac_size==(3,2):
                elif "spot" in str(env.robots[0]):
                    action=a_spot[0],a_titan[1]
                    logp=[logp_spot[0],logp_titan[1]]
            # print(pol)
            # if not args.titanheads or not args.heterogeneous:
            #     action_rl1 = pol.step(torch.as_tensor(np.array(obs[0]), dtype=torch.float32), torch.as_tensor(im[0], dtype=torch.float32), stochastic=False)[0]
            #     action[0] = action_rl1 
                
            #     if args.num_robots==2:
            #         action_rl2 = pol.step(torch.as_tensor(np.array(obs[1]), dtype=torch.float32), torch.as_tensor(im[1], dtype=torch.float32), stochastic=False)[0]
                
                
            #         action[1] = action_rl2

        # elif args.use_perception and args.jit_model:
        #     a_r1=torch.as_tensor(np.array([obs[0]]), dtype=torch.float32).unsqueeze(dim=0)
        #     b_r1=model_z(torch.as_tensor(im[0], dtype=torch.float32))
        #     # print(a_r1[0],"br1",b_r1)
        #     # print(np.array(a_r1[0].detach().numpy()).shape,np.array(b_r1.detach().numpy()).shape)
        #     concatenate_part_r1=torch.concat((a_r1[0],b_r1),-1)        
        #     action_r1 = model_mu(concatenate_part_r1)

        #     if args.num_robots==2:
        #         a_r2=torch.as_tensor(np.array([obs[1]]), dtype=torch.float32).unsqueeze(dim=0)
        #         b_r2=model_z(torch.as_tensor(im[1], dtype=torch.float32))
        #         # print(a_r2[0],"br2",b_r2)
        #         # print(np.array(a_r2[0].detach().numpy()).shape,np.array(b_r2.detach().numpy()).shape)
        #         concatenate_part_r2=torch.concat((a_r2[0],b_r2),-1)        
        #         action_r2 = model_mu(concatenate_part_r2)
        #         # print("ar1",action_r1,"ar2",action_r2)
        # else:
        #     action = pol.step(torch.tensor(np.array(obs).astype(np.float32)), stochastic=False)[0]
        #     # print ("action_before", action,type(action))
        # if not args.unclipped_vel and args.jit_model:
        #     r1_clipped_linear_vel_command=np.clip(action_r1[0][0].detach().numpy(), -0.5, 1)
        #     r1_clipped_angular_vel_command=np.clip(action_r1[0][1].detach().numpy(), -1.5, 1.5)
        #     action_r=torch.tensor([[r1_clipped_linear_vel_command,r1_clipped_angular_vel_command]])

        #     if args.num_robots==2:
        #         r2_clipped_linear_vel_command=np.clip(action_r2[0][0].detach().numpy(), -0.5, 1)
        #         r2_clipped_angular_vel_command=np.clip(action_r2[0][1].detach().numpy(), -1.5, 1.5)

        #         # action=[[r1_clipped_linear_vel_command,r1_clipped_angular_vel_command],[r2_clipped_linear_vel_command,r2_clipped_angular_vel_command]]
        #         # action=np.array([[r1_clipped_linear_vel_command,r1_clipped_angular_vel_command],[r2_clipped_linear_vel_command,r2_clipped_angular_vel_command]])
        #         action_r=torch.tensor([[r1_clipped_linear_vel_command,r1_clipped_angular_vel_command],[r2_clipped_linear_vel_command,r2_clipped_angular_vel_command]])
        
        # elif not args.unclipped_vel and not args.jit_model:
        #     # print("action",action,action[0][0],action[0][1])
        #     r1_clipped_linear_vel_command=np.clip(action[0][0], -0.5, 1)
        #     r1_clipped_angular_vel_command=np.clip(action[0][1], -0.75, 0.75)
        #     action_r=np.array([[r1_clipped_linear_vel_command,r1_clipped_angular_vel_command]])
            
        #     if args.num_robots==2:

        #         r2_clipped_linear_vel_command=np.clip(action[1][0], -0.5, 1)
        #         r2_clipped_angular_vel_command=np.clip(action[1][1], -1.5, 1.5)

        #         # action=[[r1_clipped_linear_vel_command,r1_clipped_angular_vel_command],[r2_clipped_linear_vel_command,r2_clipped_angular_vel_command]]
        #         action_r=np.array([[r1_clipped_linear_vel_command,r1_clipped_angular_vel_command],[r2_clipped_linear_vel_command,r2_clipped_angular_vel_command]])
        #     # print(action_r)
        # # print ("action", action)#;exit()
        # # start_time=time.time()
        # # current_time=0
        
        # # time_saving.append(current_time)

        # action=action_r
        # print(action)
        if env.args.Pretrained_cur:
            # obs = MUL.reset()
            # im = MUL.get_image()
            model_mu=torch.load("/home/kom018/behaviour_rl/Saved_models/Turtle_titan/choosen_models/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/mu_net_simul.jit")
            model_z=torch.load("/home/kom018/behaviour_rl/Saved_models/Turtle_titan/choosen_models/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/z_net_simul.jit")
            if env.args.multi_titans or env.args.multi_spots:
                a_r1=torch.as_tensor(np.array([obs[0]]), dtype=torch.float32).unsqueeze(dim=0)
            elif env.args.heterogeneous:
                a_r1=torch.as_tensor(np.array([obs[0][1:]]), dtype=torch.float32).unsqueeze(dim=0)
            b_r1=model_z(torch.as_tensor(im[0], dtype=torch.float32))
            # print(a_r1[0],"br1",b_r1)
            # print(np.array(a_r1[0].detach().numpy()).shape,np.array(b_r1.detach().numpy()).shape)
            concatenate_part_r1=torch.concat((a_r1[0],b_r1),-1)        
            action_r1 = model_mu(concatenate_part_r1)

            if env.args.num_robots==2:

                if env.args.multi_titans or env.args.multi_spots:
                    a_r2=torch.as_tensor(np.array([obs[1]]), dtype=torch.float32).unsqueeze(dim=0)
                elif env.args.heterogeneous:
                    a_r2=torch.as_tensor(np.array([obs[1][1:]]), dtype=torch.float32).unsqueeze(dim=0)
                # a_r2=torch.as_tensor(np.array([o[1]]), dtype=torch.float32).unsqueeze(dim=0)
                b_r2=model_z(torch.as_tensor(im[1], dtype=torch.float32))
                # print(a_r2[0],"br2",b_r2)
                # print(np.array(a_r2[0].detach().numpy()).shape,np.array(b_r2.detach().numpy()).shape)
                concatenate_part_r2=torch.concat((a_r2[0],b_r2),-1)        
                action_r2 = model_mu(concatenate_part_r2)
                # print("ar1",action_r1,"ar2",action_r2)
            
            r1_clipped_linear_vel_command=np.clip(action_r1[0][0].detach().numpy(), -0.75, 0.75)
            r1_clipped_angular_vel_command=np.clip(action_r1[0][1].detach().numpy(), -0.75, 0.75)
            action_r=torch.tensor([[r1_clipped_linear_vel_command,r1_clipped_angular_vel_command]])

            if env.args.num_robots==2:
                r2_clipped_linear_vel_command=np.clip(action_r2[0][0].detach().numpy(), -0.75, 0.75)
                r2_clipped_angular_vel_command=np.clip(action_r2[0][1].detach().numpy(), -0.75, 0.75)

                # action=[[r1_clipped_linear_vel_command,r1_clipped_angular_vel_command],[r2_clipped_linear_vel_command,r2_clipped_angular_vel_command]]
                # action=np.array([[r1_clipped_linear_vel_command,r1_clipped_angular_vel_command],[r2_clipped_linear_vel_command,r2_clipped_angular_vel_command]])
                action_r=torch.tensor([[r1_clipped_linear_vel_command,r1_clipped_angular_vel_command],[r2_clipped_linear_vel_command,r2_clipped_angular_vel_command]])
            # pol=torch.load("/home/kom018/behaviour_rl/Saved_models/Turtle_titan/choosen_models/E4r32G1E1_387_0.85_noised_best/2024_09_10_07_14_17/model.pt")
            # sp_ac = pol.step(torch.as_tensor(np.array(o), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32), stochastic=False)[0]
            sp_ac=action_r
            # print("sp_ac",sp_ac)
        else: 
            sp_ac=np.array([[0., 0.],[0., 0.]])
        obs, _, done,termination, _ = env.step(action,sp_ac)


        # print(obs[0],"obs?")
        if args.use_perception:
                im = env.get_image()
                # print(im,type(im),im[0][0][1].shape)

        if env.args.heterogeneous or env.args.titanheads:
        # if ac_size==(2,3):
            if "titan" in str(env.robots[0]):
                # print("O_before",len(o[0]),o)
                obs[0] = np.insert(obs[0], 0, 0)
                obs[1] = np.insert(obs[1], 0, 1)
                # print("O_after",len(obs[0]),o)
            # elif ac_size==(3,2):
            elif "spot" in str(env.robots[0]):
                # print("O_before",len(obs[0]),o)
                obs[0] = np.insert(obs[0], 0, 1)
                obs[1] = np.insert(obs[1], 0, 0)
        counting_step+=1
        # action_saving1.append(action[0][0])
        # action_saving2.append(action[0][1])
        # accc1=pd.DataFrame(action_saving1)
        # accc2=pd.DataFrame(action_saving2)
        # accc = pd.concat([accc1, accc2], axis=1)
        # # print(accc,type(accc))
        # accc.to_csv("action_test.csv")
        # current_time = time.time() - start_time
        





        # print(env.steps*1/10)
        st=time.time()
        buffer_time.append(current_time)

        r1_buffer_linear_action.append(action[0][0])
        r1_buffer_angular_action.append(action[0][1])

        r1_buffer_ego_pos_x_obs.append(obs[0][0])
        r1_buffer_ego_pos_y_obs.append(obs[0][1])

        r1_buffer_roll_obs.append(obs[0][2])
        r1_buffer_pitch_obs.append(obs[0][3])

        r1_buffer_linear_obs.append(obs[0][4])
        r1_buffer_angular_obs.append(obs[0][5])

        r1_poses_x.append(env.robots_pos[0][0])
        r1_poses_y.append(env.robots_pos[0][1])

        if args.num_robots==2:
            r2_buffer_linear_action.append(action[1][0])
            r2_buffer_angular_action.append(action[1][1])

            r2_buffer_ego_pos_x_obs.append(obs[1][0])
            r2_buffer_ego_pos_y_obs.append(obs[1][1])

            r2_buffer_roll_obs.append(obs[1][2])
            r2_buffer_pitch_obs.append(obs[1][3])

            r2_buffer_linear_obs.append(obs[1][4])
            r2_buffer_angular_obs.append(obs[1][5])

            r2_poses_x.append(env.robots_pos[1][0])
            r2_poses_y.append(env.robots_pos[1][1])
        
        
        if args.figure and current_time>save_time:
            
            

            # # print("TIME",time.time()-t1,R3.buffer_time,"ac")
            
            # output_dir_occupancy ="/home/kom018/behaviour_rl/Saved_models/titan/L3r39G1E1/2024_07_23_02_22_51/R1\'s_Occupancy.png"
            
            # r1_occupancy_map=im[0, 0, :, :]

            # # Create a new array for the modified occupancy map
            # # Function to find connected components and mark edge cells
            # # Function to find connected components and mark edge cells
            # def mark_edge_cells(occupancy_map):
            #     # Define a structure for connected components (8-connected neighborhood)
            #     structure = generate_binary_structure(2, 1)
                
            #     # Label connected components
            #     labeled_map, num_labels = label(occupancy_map, structure)
                
            #     # Find the unique labels (excluding background label 0)
            #     unique_labels = np.unique(labeled_map)[1:]
                
            #     # Create a new array for the modified occupancy map
            #     modified_occupancy_map = np.zeros_like(occupancy_map)
                
            #     # Iterate over each unique label (connected component)
            #     for labela in unique_labels:
            #         # Extract the mask for the current connected component
            #         component_mask = (labeled_map == labela).astype(np.uint8)
                    
            #         # Find edge cells that are adjacent to unoccupied cells (0)
            #         edge_mask = np.zeros_like(component_mask)
            #         edge_mask[1:-1, 1:-1] = (component_mask[1:-1, 1:-1] > 0) & \
            #                                 ((component_mask[:-2, 1:-1] == 0) | (component_mask[2:, 1:-1] == 0) | \
            #                                 (component_mask[1:-1, :-2] == 0) | (component_mask[1:-1, 2:] == 0))
                    
            #         # Mark edge cells as 2 in the modified map
            #         modified_occupancy_map[edge_mask > 0] = 1
                    
            #     return modified_occupancy_map

            # # Get the modified occupancy map
            # r1_modified_occupancy_map = mark_edge_cells(r1_occupancy_map)
            # # print(r1_modified_occupancy_map)
            # # Plotting the modified occupancy map
            # plt.figure(figsize=(30, 30))
            # plt.imshow(r1_modified_occupancy_map, cmap='Reds', origin='upper')

            # # Annotating the cells with thkeir values
            # for i in range(r1_modified_occupancy_map.shape[0]):
            #     for j in range(r1_modified_occupancy_map.shape[1]):
            #         cell_value = int(r1_modified_occupancy_map[i, j])
            #         color = 'Purple' if cell_value == 2 else 'white' if cell_value == 1 else 'black'
            #         plt.text(j, i, cell_value, ha='center', va='center', color=color)

            # # Customizing the plot
            # plt.xticks(np.arange(r1_modified_occupancy_map.shape[1]))
            # plt.yticks(np.arange(r1_modified_occupancy_map.shape[0]))
            # plt.grid(True, which='both', color='black', linestyle='-', linewidth=0.5)
            # plt.gca().set_xticks(np.arange(-0.5, r1_modified_occupancy_map.shape[1], 1), minor=True)
            # plt.gca().set_yticks(np.arange(-0.5, r1_modified_occupancy_map.shape[0], 1), minor=True)
            # plt.gca().grid(which='minor', color='black', linestyle='-', linewidth=0.5)
            # plt.gca().tick_params(which='minor', size=0)



            # # Save the plot to a file
            # plt.savefig(output_dir_occupancy, bbox_inches='tight')

            # if args.num_robots==2:
            #     r2_output_dir_occupancy ="/home/kom018/behaviour_rl/Saved_models/titan/L3r39G1E1/2024_07_23_02_22_51/R2\'s_Occupancy.png"
            
            #     r2_occupancy_map=im[1, 0, :, :]

            #     # Create a new array for the modified occupancy map
                
                
            #     # Get the modified occupancy map
            #     r2_modified_occupancy_map = mark_edge_cells(r2_occupancy_map)
            #     # print(r2_modified_occupancy_map)
            #     # Plotting the modified occupancy map
            #     plt.figure(figsize=(30, 30))
            #     plt.imshow(r2_modified_occupancy_map, cmap='Greens', origin='upper')

            #     # Annotating the cells with thkeir values
            #     for i in range(r2_modified_occupancy_map.shape[0]):
            #         for j in range(r2_modified_occupancy_map.shape[1]):
            #             cell_value = int(r2_modified_occupancy_map[i, j])
            #             color = 'Purple' if cell_value == 2 else 'white' if cell_value == 1 else 'black'
            #             plt.text(j, i, cell_value, ha='center', va='center', color=color)

            #     # Customizing the plot
            #     plt.xticks(np.arange(r2_modified_occupancy_map.shape[1]))
            #     plt.yticks(np.arange(r2_modified_occupancy_map.shape[0]))
            #     plt.grid(True, which='both', color='black', linestyle='-', linewidth=0.5)
            #     plt.gca().set_xticks(np.arange(-0.5, r2_modified_occupancy_map.shape[1], 1), minor=True)
            #     plt.gca().set_yticks(np.arange(-0.5, r2_modified_occupancy_map.shape[0], 1), minor=True)
            #     plt.gca().grid(which='minor', color='black', linestyle='-', linewidth=0.5)
            #     plt.gca().tick_params(which='minor', size=0)

            #     # Save the plot to a file
            #     plt.savefig(r2_output_dir_occupancy, bbox_inches='tight')



            #     r_output_dir_occupancy ="/home/kom018/behaviour_rl/Saved_models/titan/L3r39G1E1/2024_07_23_02_22_51/Merged_Occupancy.png"
            #     # Get the modified occupancy maps
            #     modified_r1_occupancy_map = mark_edge_cells(r1_occupancy_map)
            #     modified_r2_occupancy_map = mark_edge_cells(r2_occupancy_map)

            #     # Create a figure with two subplots
            #     fig, axes = plt.subplots(1, 2, figsize=(30, 15))

            #     # Plotting the modified occupancy map for Robot 1
            #     axes[0].imshow(modified_r1_occupancy_map, cmap='Reds', origin='upper')
            #     axes[0].set_title("Robot 1 Occupancy Map")

            #     for i in range(modified_r1_occupancy_map.shape[0]):
            #         for j in range(modified_r1_occupancy_map.shape[1]):
            #             cell_value = int(modified_r1_occupancy_map[i, j])
            #             color = 'blue' if cell_value == 2 else 'red' if cell_value == 1 else 'black'
            #             axes[0].text(j, i, cell_value, ha='center', va='center', color=color)

            #     # Customizing the subplot for Robot 1
            #     axes[0].set_xticks(np.arange(modified_r1_occupancy_map.shape[1]))
            #     axes[0].set_yticks(np.arange(modified_r1_occupancy_map.shape[0]))
            #     axes[0].grid(True, which='both', color='black', linestyle='-', linewidth=0.5)
            #     axes[0].set_xticks(np.arange(-0.5, modified_r1_occupancy_map.shape[1], 1), minor=True)
            #     axes[0].set_yticks(np.arange(-0.5, modified_r1_occupancy_map.shape[0], 1), minor=True)
            #     axes[0].grid(which='minor', color='black', linestyle='-', linewidth=0.5)
            #     axes[0].tick_params(which='minor', size=0)

            #     # Plotting the modified occupancy map for Robot 2
            #     axes[1].imshow(modified_r2_occupancy_map, cmap='Greens', origin='upper')
            #     axes[1].set_title("Robot 2 Occupancy Map")

            #     for i in range(modified_r2_occupancy_map.shape[0]):
            #         for j in range(modified_r2_occupancy_map.shape[1]):
            #             cell_value = int(modified_r2_occupancy_map[i, j])
            #             color = 'blue' if cell_value == 2 else 'red' if cell_value == 1 else 'black'
            #             axes[1].text(j, i, cell_value, ha='center', va='center', color=color)

            #     # Customizing the subplot for Robot 2
            #     axes[1].set_xticks(np.arange(modified_r2_occupancy_map.shape[1]))
            #     axes[1].set_yticks(np.arange(modified_r2_occupancy_map.shape[0]))
            #     axes[1].grid(True, which='both', color='black', linestyle='-', linewidth=0.5)
            #     axes[1].set_xticks(np.arange(-0.5, modified_r2_occupancy_map.shape[1], 1), minor=True)
            #     axes[1].set_yticks(np.arange(-0.5, modified_r2_occupancy_map.shape[0], 1), minor=True)
            #     axes[1].grid(which='minor', color='black', linestyle='-', linewidth=0.5)
            #     axes[1].tick_params(which='minor', size=0)

            #     plt.savefig(r_output_dir_occupancy, bbox_inches='tight')
            # # plt.savefig(os.path.join(output_dir, 'R1\'s_Occupancy.png'))
            # # output_dir ="/refarm/src/multi_robot_rl/scripts"

            # # if np.array(R3.buffer_time).shape != np.array(R3.buffer_linear_obs).shape:
            # #     R3.buffer_linear_obs = np.zeros_like(R3.buffer_time)

            # # output_dir ="/refarm/src/multi_robot_rl/scripts"
            # # print("R3.buffer_linear_obs",R3.buffer_linear_obs,R3.buffer_time)

            # output_dir ="/home/kom018/behaviour_rl/Saved_models/titan/L3r39G1E1/2024_07_23_02_22_51"

            # plt.figure()
            # plt.plot(buffer_time, r1_buffer_ego_pos_x_obs, label='Robot1\'s Ego Pos X')
            # plt.xlabel('Time (s)')
            # plt.ylabel('Robot1\'s Ego Pos X')
            # plt.title('Robot1\'s Ego Pos X over Time')
            # plt.legend()
            # plt.grid(True)
            # plt.savefig(os.path.join(output_dir, 'Robot1\'s_Ego_Pos_X_plot.png'))

            # plt.figure()
            # plt.plot(buffer_time, r1_buffer_ego_pos_y_obs, label='Robot1\'s Ego Pos Y')
            # plt.xlabel('Time (s)')
            # plt.ylabel('Robot1\'s Ego Pos Y')
            # plt.title('Robot1\'s Ego Pos Y over Time')
            # plt.legend()
            # plt.grid(True)
            # plt.savefig(os.path.join(output_dir, 'Robot1\'s_Ego_Pos_Y_plot.png'))


            # plt.figure()
            # plt.plot(buffer_time, r1_buffer_roll_obs, label='Robot1\'s Roll')
            # plt.xlabel('Time (s)')
            # plt.ylabel('Robot1\'s Roll')
            # plt.title('Robot1\'s Roll over Time')
            # plt.legend()
            # plt.grid(True)
            # plt.savefig(os.path.join(output_dir, 'Robot1\'s_Roll_plot.png'))


            # plt.figure()
            # plt.plot(buffer_time, r1_buffer_pitch_obs, label='Robot1\'s Pitch')
            # plt.xlabel('Time (s)')
            # plt.ylabel('Robot1\'s Pitch')
            # plt.title('Robot1\'s Pitch over Time')
            # plt.legend()
            # plt.grid(True)
            # plt.savefig(os.path.join(output_dir, 'Robot1\'s_Pitch_plot.png'))


            # plt.figure()
            # plt.plot(buffer_time, r1_buffer_linear_obs, label='Robot1\'s Linear Velocity')
            # plt.xlabel('Time (s)')
            # plt.ylabel('Robot1\'s Linear Velocity')
            # plt.title('Robot1\'s Linear Velocity over Time')
            # plt.legend()
            # plt.grid(True)
            # plt.savefig(os.path.join(output_dir, 'R1\'s_Linear_Velocity_plot.png'))

            # # Plot the angular velocity actions over time
            # plt.figure()
            # plt.plot(buffer_time, r1_buffer_angular_obs, label='Robot1\'s Angular Velocity')
            # plt.xlabel('Time (s)')
            # plt.ylabel('Robot1\'s Angular Velocity')
            # plt.title('Robot1\'s Angular Velocity over Time')
            # plt.legend()
            # plt.grid(True)
            # plt.savefig(os.path.join(output_dir, 'R1\'s_Angular_Velocity_plot.png'))

            # plt.figure()
            # plt.plot(buffer_time, r1_buffer_linear_action, label='Command Linear Velocity')
            # plt.xlabel('Time (s)')
            # plt.ylabel('Command Linear Velocity')
            # plt.title('Robot1\'s Command Linear Velocity over Time')
            # plt.legend()
            # plt.grid(True)
            # plt.savefig(os.path.join(output_dir, 'R1_Command_Linear_Velocity_plot.png'))

            # # Plot the angular velocity actions over time
            # plt.figure()
            # plt.plot(buffer_time, r1_buffer_angular_action, label='Command Angular Velocity')
            # plt.xlabel('Time (s)')
            # plt.ylabel('Command Angular Velocity')
            # plt.title('Robot1\'s Command Angular Velocity over Time')
            # plt.legend()
            # plt.grid(True)
            # plt.savefig(os.path.join(output_dir, 'R1_Command_angular_velocity_plot.png'))



            # # Plot the trajectory
            # plt.figure(figsize=(10, 6))
            # plt.plot(r1_poses_x, r1_poses_y, label='Trajectory', marker='o', markersize=5, linestyle='-')

            # # Annotate with time points
            # for i in range(0, len(buffer_time), 10):  # Annotate every 10th current_time step
            #     plt.annotate(f't={buffer_time[i]:.1f}', (r1_poses_x[i], r1_poses_y[i]), textcoords="offset points", xytext=(10,-10), ha='center')

            # # Labels and title
            # plt.xlabel('X position')
            # plt.ylabel('Y position')
            # plt.title('Robot1 Trajectory Over current_time')
            # plt.legend()
            # plt.grid(True)
            # plt.savefig(os.path.join(output_dir, 'R1_trajectory.png'))


            # # # Save plot to a file
            # # output_directory = 'plots'
            # # os.makedirs(output_directory, exist_ok=True)
            # # file_path = os.path.join(output_directory, 'robot_trajectory.png')
            # # plt.savefig(file_path)

            # data = {
            # "Time": buffer_time,
            # "Command Linear Velocity": r1_buffer_linear_action,
            # "Command Angular Velocity": r1_buffer_angular_action,
            # "Robot's Linear Velocity": r1_buffer_linear_obs,
            # "Robot's Angular Velocity": r1_buffer_angular_obs
            # }
            # df = pd.DataFrame(data)
            # csv_path = os.path.join(output_dir, 'r1_actions_data.csv')
            # df.to_csv(csv_path, index=False)
            # df = pd.DataFrame(r1_modified_occupancy_map)
            # csv_path = os.path.join(output_dir, 'r1_occu.csv')
            # df.to_csv(csv_path, index=False)

            if args.num_robots==2:


            #     plt.figure()
            #     plt.plot(buffer_time, r2_buffer_ego_pos_x_obs, label='Robot2\'s Ego Pos X')
            #     plt.xlabel('Time (s)')
            #     plt.ylabel('Robot2\'s Ego Pos X')
            #     plt.title('Robot2\'s Ego Pos X over Time')
            #     plt.legend()
            #     plt.grid(True)
            #     plt.savefig(os.path.join(output_dir, 'Robot2\'s_Ego_Pos_X_plot.png'))

            #     plt.figure()
            #     plt.plot(buffer_time, r2_buffer_ego_pos_y_obs, label='Robot2\'s Ego Pos Y')
            #     plt.xlabel('Time (s)')
            #     plt.ylabel('Robot2\'s Ego Pos Y')
            #     plt.title('Robot2\'s Ego Pos Y over Time')
            #     plt.legend()
            #     plt.grid(True)
            #     plt.savefig(os.path.join(output_dir, 'Robot2\'s_Ego_Pos_Y_plot.png'))


            #     plt.figure()
            #     plt.plot(buffer_time, r2_buffer_roll_obs, label='Robot2\'s Roll')
            #     plt.xlabel('Time (s)')
            #     plt.ylabel('Robot2\'s Roll')
            #     plt.title('Robot2\'s Roll over Time')
            #     plt.legend()
            #     plt.grid(True)
            #     plt.savefig(os.path.join(output_dir, 'Robot2\'s_Roll_plot.png'))


            #     plt.figure()
            #     plt.plot(buffer_time, r2_buffer_pitch_obs, label='Robot2\'s Pitch')
            #     plt.xlabel('Time (s)')
            #     plt.ylabel('Robot2\'s Pitch')
            #     plt.title('Robot2\'s Pitch over Time')
            #     plt.legend()
            #     plt.grid(True)
            #     plt.savefig(os.path.join(output_dir, 'Robot2\'s_Pitch_plot.png'))

                
            #     plt.figure()
            #     plt.plot(buffer_time, r2_buffer_linear_obs, label='Robot2\'s Linear Velocity')
            #     plt.xlabel('Time (s)')
            #     plt.ylabel('Robot2\'s Linear Velocity')
            #     plt.title('Robot2\'s Linear Velocity over Time')
            #     plt.legend()
            #     plt.grid(True)
            #     plt.savefig(os.path.join(output_dir, 'R2\'s_Linear_Velocity_plot.png'))

            #     # Plot the angular velocity actions over time
            #     plt.figure()
            #     plt.plot(buffer_time, r2_buffer_angular_obs, label='Robot2\'s Angular Velocity')
            #     plt.xlabel('Time (s)')
            #     plt.ylabel('Robot2\'s Angular Velocity')
            #     plt.title('Robot2\'s Angular Velocity over Time')
            #     plt.legend()
            #     plt.grid(True)
            #     plt.savefig(os.path.join(output_dir, 'R2\'s_Angular_Velocity_plot.png'))

            #     plt.figure()
            #     plt.plot(buffer_time, r2_buffer_linear_action, label='Command Linear Velocity')
            #     plt.xlabel('Time (s)')
            #     plt.ylabel('Command Linear Velocity')
            #     plt.title('Robot2\'s Command Linear Velocity over Time')
            #     plt.legend()
            #     plt.grid(True)
            #     plt.savefig(os.path.join(output_dir, 'R2_Command_Linear_Velocity_plot.png'))

            #     # Plot the angular velocity actions over time
            #     plt.figure()
            #     plt.plot(buffer_time, r2_buffer_angular_action, label='Command Angular Velocity')
            #     plt.xlabel('Time (s)')
            #     plt.ylabel('Command Angular Velocity')
            #     plt.title('Robot2\'s Command Angular Velocity over Time')
            #     plt.legend()
            #     plt.grid(True)
            #     plt.savefig(os.path.join(output_dir, 'R2_Command_angular_velocity_plot.png'))


            #     # Plot the trajectory
            #     plt.figure(figsize=(10, 6))
            #     plt.plot(r2_poses_x, r2_poses_y, label='Trajectory', marker='o', markersize=5, linestyle='-')

            #     # Annotate with time points
            #     for i in range(0, len(buffer_time), 10):  # Annotate every 10th current_time step
            #         plt.annotate(f't={buffer_time[i]:.1f}', (r2_poses_x[i], r2_poses_y[i]), textcoords="offset points", xytext=(10,-10), ha='center')

            #     # Labels and title
            #     plt.xlabel('X position')
            #     plt.ylabel('Y position')
            #     plt.title('Robot2 Trajectory Over current_time')
            #     plt.legend()
            #     plt.grid(True)
            #     plt.savefig(os.path.join(output_dir, 'R2_trajectory.png'))

                output_dir="/home/kom018/behaviour_rl/Results_plots/pybullet_excels/"
                #PLOT BOTH ROBOT TRAJECTORY IN ONE PLOT
                # Plot the first trajectory
                plt.plot(r1_poses_x, r1_poses_y, label='Robot 1 Trajectory', marker='o', markersize=5, linestyle='-', color='blue')
                # Annotate the first trajectory with time points
                for i in range(0, len(buffer_time), 10):  # Annotate every 10th buffer_time step
                    plt.annotate(f't={buffer_time[i]:.1f}', (r1_poses_x[i], r1_poses_y[i]), textcoords="offset points", xytext=(10, -10), ha='center', color='black')

                # Plot the second trajectory
                plt.plot(r2_poses_x, r2_poses_y, label='Robot 2 Trajectory', marker='o', markersize=5, linestyle='-', color='orange')
                # Annotate the second trajectory with buffer_time points
                for i in range(0, len(buffer_time), 10):  # Annotate every 10th buffer_time step
                    plt.annotate(f't={buffer_time[i]:.1f}', (r2_poses_x[i], r2_poses_y[i]), textcoords="offset points", xytext=(10, -10), ha='center', color='black')

                # Labels and title
                plt.xlabel('X position')
                plt.ylabel('Y position')
                plt.title('Two Robot Trajectories Over Time')
                plt.legend()
                plt.grid(True)
                plt.savefig(os.path.join(output_dir, 'Merged_trajectory.png'))


                # data = {
                # "Time": buffer_time,
                # "Command Linear Velocity": r2_buffer_linear_action,
                # "Command Angular Velocity": r2_buffer_angular_action,
                # "Robot's Linear Velocity": r2_buffer_linear_obs,
                # "Robot's Angular Velocity": r2_buffer_angular_obs
                # }
                # df = pd.DataFrame(data)
                # csv_path = os.path.join(output_dir, 'r2_actions_data.csv')
                # df.to_csv(csv_path, index=False)
                # df = pd.DataFrame(r2_modified_occupancy_map)
                # csv_path = os.path.join(output_dir, 'r2_occu.csv')
                # df.to_csv(csv_path, index=False)
                
            
            
            # # print("overal",time.time()-R3.t1)
            if current_time>save_time:
                print("THAM");exit()

    
        
        
        # print(counting_step*1/10)
            

        # if done==[True] or termination==[True] or env.steps > args.max_ep_len:
        if all(done) or all(termination) or env.steps > args.max_ep_len:
            
            obs = env.reset()
            if args.use_perception:
                im = env.get_image()
                # print(im,type(im),im[0][0][1].shape)

            if env.args.heterogeneous or env.args.titanheads:
                # if ac_size==(2,3):
                if "titan" in str(env.robots[0]):
                    # print("O_before",len(o[0]),o)
                    obs[0] = np.insert(obs[0], 0, 0)
                    obs[1] = np.insert(obs[1], 0, 1)
                    # print("O_after",len(obs[0]),o)
                # elif ac_size==(3,2):
                elif "spot" in str(env.robots[0]):
                    # print("O_before",len(obs[0]),o)
                    obs[0] = np.insert(obs[0], 0, 1)
                    obs[1] = np.insert(obs[1], 0, 0)
            n=n+1
            print("Trial_no",n)
            if n==100:
                print("100 Iteration Done")
            for a in done:
                if a:
                    print(n,a)
        
            #print(obs)

if __name__== "__main__":
    
    # print(pol)
    
    

    # start_time=time.time()
    
    run(args)
    # current_time=0
