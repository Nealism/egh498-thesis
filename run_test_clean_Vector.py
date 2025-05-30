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
import pybullet as p

import time
import matplotlib.pyplot as plt
import os
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
import matplotlib.transforms as transforms
from itertools import product
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
args.render = False
args.record_sim = False

if args.jit_model:
    model_mu=torch.load("/home/kom018/refarm/src/multi_robot_rl/scripts/JIT_models/FC/mu_net.jit")
    model_z=torch.load("/home/kom018/refarm/src/multi_robot_rl/scripts/JIT_models/FC/z_net.jit")
else:
    pol = torch.load(PATH + "/model.pt")

start_time=time.time()

# Initialize buffers
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

if args.heterogeneous or args.titanheads:
    r1_buffer_lateral_action=[]

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
    action_per_second=[]
    actionr1x_per_second=[]
    actionr1y_per_second=[]
    Goal1_x_list=[]
    Goal1_y_list=[]
    Goal2_x_list=[]
    Goal2_y_list=[]
    if args.heterogeneous or args.titanheads:
        r2_buffer_lateral_action=[]

def run(args): 
    # p=2
    # q=0.6


    # Conservative approach - use the larger dimension (length) for safety
    min_distance = 1.2 + 0.5  # Robot length + safety buffer = 1.7m

    # More precise approach - diagonal distance
    robot_diagonal = np.sqrt(1.2**2 + 0.78**2)  # ≈ 1.426m
    min_distance = robot_diagonal + 0.3  # Add safety buffer = ~1.726m

    # Fixed obstacle and goal positions
    start_A = [0, 0]
    start_B = [0, 1.2]
    goal_A = [8, 1.2]
    goal_B = [8, 0]
    gap_center = [3.8,0.6]  # Fixed gap coordinate
    
    # Calculate obstacle boundaries based on fixed positions
    mid_x = gap_center[0]
    mid_y = gap_center[1]
    gap = 0.85
    half_gap = gap / 2
    obs_height = 0.75
    
    top_y_bottom = mid_y + half_gap 
    top_y_top = top_y_bottom + obs_height
    bot_y_top = mid_y - half_gap
    bot_y_bottom = bot_y_top - obs_height 
    horizontal_length = 0.1
    
    # Obstacle boundaries
    obs_x_min = mid_x - horizontal_length
    obs_x_max = mid_x + horizontal_length
    upper_obs_y_min = top_y_bottom
    upper_obs_y_max = top_y_top
    lower_obs_y_min = bot_y_bottom
    lower_obs_y_max = bot_y_top
    

    # # #for quick ccheck
    # for p in np.arange(0,6, 0.5):
    #     for q in np.arange(0, 1.5, 0.3):
    #         all_arrows_data = []
    #         for g in np.arange(0.53,0.54, 0.01):
    #             for h in np.arange(0.69, 0.7, 0.01):
    # Collect ALL arrow data before plotting
    
    ### For Stopping Point Detection
    # # p=2
    # # q=0.6
    # for g in np.arange(0.45,0.7, 0.01):
    #     for h in np.arange(0.55, 0.75, 0.01):


    # # p=2
    # # q=0.6
    # # g=-1.5
    # # h=0.6
    ## For Regular 1.2m 
    for p in np.arange(0,6, 0.5):
        for q in np.arange(0, 1.5, 0.3):
            all_arrows_data = []
            for g in np.arange(-2,6, 0.2):
                for h in np.arange(0, 1.4, 0.2):


    # ## For Observerd Velocity Based Vector Difference Check
    # for r in np.arange(-0.75,0.75, 0.25):
    #     for s in np.arange(-0.75, 0.75, 0.25):
            
    #         for t in np.arange(-0.75,0.75, 0.25):
    #             for u in np.arange(-0.75, 0.75, 0.25):
                    # Check if robots would overlap
                    distance = np.sqrt((g - p)**2 + (h - q)**2)
                    min_safe_distance = 1.2  # 1.2 + 0.5 safety buffer
                    
                    if distance < min_safe_distance:
                        continue  # Skip this position combination

                    # Check robot-obstacle collision
                    robot_half_length = 1.2 / 2  # 0.6
                    robot_half_width = 0.78 / 2  # 0.39
                    # safety_buffer = 0.1
                    safety_buffer = 0
                    
                    # Robot B's boundaries
                    robot_x_min = g - robot_half_length - safety_buffer
                    robot_x_max = g + robot_half_length + safety_buffer
                    robot_y_min = h - robot_half_width - safety_buffer
                    robot_y_max = h + robot_half_width + safety_buffer
                    
                    # Check if robot overlaps with upper obstacle
                    upper_overlap = (robot_x_min < obs_x_max and robot_x_max > obs_x_min and
                                robot_y_min < upper_obs_y_max and robot_y_max > upper_obs_y_min)
                    
                    # Check if robot overlaps with lower obstacle
                    lower_overlap = (robot_x_min < obs_x_max and robot_x_max > obs_x_min and
                                robot_y_min < lower_obs_y_max and robot_y_max > lower_obs_y_min)
                    
                    if upper_overlap or lower_overlap:
                        continue  # Skip this position


                    print("AAALLCHECKX",p,q,g,h)
                    env = Env(PATH=PATH, args=args)
                    env.reset(r1_loading_poses=[p,q],r2_loading_poses=[g,h])
            
                    n=0
                    counting_step=0
                    obs = env.reset()
                    # obs = [np.array([obs[0][0],obs[0][1],0,0,r,t]),np.array([obs[1][0],obs[1][1],0,0,s,u])]

                    if env.args.heterogeneous or env.args.titanheads:
                        if "titan" in str(env.robots[0]):
                            obs[0] = np.insert(obs[0], 0, 0)
                            obs[1] = np.insert(obs[1], 0, 1)
                        elif "spot" in str(env.robots[0]):
                            obs[0] = np.insert(obs[0], 0, 1)
                            obs[1] = np.insert(obs[1], 0, 0)
                    
                    print("ob_reset",obs)
                    if args.use_perception:
                        im = env.get_image()

                    time_saving=[]
                    action_saving1=[]
                    action_saving2=[]
                    st=time.time()
                    save_time=00.00
                    robot1_stop_duration = np.random.uniform(0, 6)
                    robot2_stop_duration = np.random.uniform(0, 6)
                    
                    current_time = env.steps*1/10

                    if args.use_perception and not args.jit_model:
                        if args.heterogeneous or args.titanheads:
                            a_spot,a_titan, v, logp_spot, logp_titan =pol.step(torch.as_tensor(np.array(obs), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32), stochastic=False)
                        else:
                            action = pol.step(torch.as_tensor(np.array(obs), dtype=torch.float32), torch.as_tensor(im, dtype=torch.float32), stochastic=False)[0]



                            r1_clipped_linear_vel_command=np.clip(action[0][0], -0.75, 0.75)
                            r1_clipped_angular_vel_command=np.clip(action[0][1], -0.75, 0.75)
                            r2_clipped_linear_vel_command=np.clip(action[1][0], -0.75, 0.75)
                            r2_clipped_angular_vel_command=np.clip(action[1][1], -0.75, 0.75)


                        if env.args.heterogeneous or env.args.titanheads:
                            if "titan" in str(env.robots[0]):
                                action=a_titan[0],a_spot[1]
                                logp=[logp_titan[0],logp_spot[1]]

                                # r1_clipped_linear_vel_command=np.clip(action[0][0], -0.75, 0.75)
                                # r1_clipped_angular_vel_command=np.clip(action[0][1], -0.75, 0.75)

                                
                            elif "spot" in str(env.robots[0]):
                                action=a_spot[0],a_titan[1]
                                logp=[logp_spot[0],logp_titan[1]]

                                # if env.robots[0].body_xyz[2] < 0.4 or (abs(np.array([env.robots[0].pitch, env.robots[0].roll])) > 0.8).any() or (np.array(env.robots[0].leg_contacts)).any():
                                #     # print("poregse---------------------")
                                #     r2_clipped_linear_vel_command=np.clip(action[1][0], -0.1, 0.5)
                                #     r2_clipped_lateral_vel_command=np.clip(action[1][1], -0.05, 0.05)
                                #     r2_clipped_angular_vel_command=np.clip(action[1][2], -0.5, 0.5)

                                # else:
                                #     r2_clipped_linear_vel_command=np.clip(action[1][0], -0.3, 0.75)
                                #     r2_clipped_lateral_vel_command=np.clip(action[1][1], -0.3, 0.3)
                                #     r2_clipped_angular_vel_command=np.clip(action[1][2], -0.75, 0.75)

                        r1_clipped_linear_vel_command=np.clip(action[0][0], -0.75, 0.75)
                        r1_clipped_angular_vel_command=np.clip(action[0][1], -0.75, 0.75)

                        if env.robots[1].body_xyz[2] < 0.4 or (abs(np.array([env.robots[1].pitch, env.robots[1].roll])) > 0.8).any() or (np.array(env.robots[1].leg_contacts)).any():
                            # print("poregse---------------------")
                            r2_clipped_linear_vel_command=np.clip(action[1][0], -0.1, 0.5)
                            r2_clipped_lateral_vel_command=np.clip(action[1][1], -0.05, 0.05)
                            r2_clipped_angular_vel_command=np.clip(action[1][2], -0.5, 0.5)

                        else:
                            r2_clipped_linear_vel_command=np.clip(action[1][0], -0.3, 0.75)
                            r2_clipped_lateral_vel_command=np.clip(action[1][1], -0.3, 0.3)
                            r2_clipped_angular_vel_command=np.clip(action[1][2], -0.75, 0.75)
                    
                    #  print("AC_VELS",r2_clipped_linear_vel_command,r2_clipped_angular_vel_command)
                            
                    sp_ac=np.array([[0., 0.],[0., 0.]])
                    obs, _, done,termination, _ = env.step(action,sp_ac)

                    if args.use_perception:
                        im = env.get_image()

                    if env.args.heterogeneous or env.args.titanheads:
                        if "titan" in str(env.robots[0]):
                            obs[0] = np.insert(obs[0], 0, 0)
                            obs[1] = np.insert(obs[1], 0, 1)
                        elif "spot" in str(env.robots[0]):
                            obs[0] = np.insert(obs[0], 0, 1)
                            obs[1] = np.insert(obs[1], 0, 0)
                    counting_step+=1

                    st=time.time()
                    buffer_time.append(current_time)
                    r1_buffer_linear_action.append(r1_clipped_linear_vel_command)
                    r1_buffer_angular_action.append(r1_clipped_angular_vel_command)
                    r1_buffer_ego_pos_x_obs.append(obs[0][0])
                    r1_buffer_ego_pos_y_obs.append(obs[0][1])
                    r1_buffer_roll_obs.append(obs[0][2])
                    r1_buffer_pitch_obs.append(obs[0][3])
                    r1_poses_x.append(env.robots_pos[0][0])
                    r1_poses_y.append(env.robots_pos[0][1])

                    Goal1_x_list.append(env.Goals_pos[0][0])
                    Goal1_y_list.append(env.Goals_pos[0][1])

                    

                    if args.num_robots==2:
                        r2_buffer_linear_action.append(r2_clipped_linear_vel_command)
                        r2_buffer_angular_action.append(r2_clipped_angular_vel_command)
                        r2_buffer_ego_pos_x_obs.append(obs[1][0])
                        r2_buffer_ego_pos_y_obs.append(obs[1][1])
                        r2_buffer_roll_obs.append(obs[1][2])
                        r2_buffer_pitch_obs.append(obs[1][3])
                        r2_poses_x.append(env.robots_pos[1][0])
                        r2_poses_y.append(env.robots_pos[1][1])
                        Goal2_x_list.append(env.Goals_pos[1][0])
                        Goal2_y_list.append(env.Goals_pos[1][1])
                        if env.args.heterogeneous or env.args.titanheads:
                            r2_buffer_lateral_action.append(r2_clipped_lateral_vel_command)
                    
                    if args.num_robots==2:
                        output_dir="/home/kom018/behaviour_rl/Results_plots/pybullet_excels/"
                        
                        # Plot trajectory
                        plt.figure(figsize=(10, 8))
                        plt.plot(r1_poses_x, r1_poses_y, label='Leading Robot Trajectory', marker='o', markersize=5, linestyle='-', color='orange')
                        for i in range(0, len(buffer_time), 10):
                            plt.annotate(f't={int(buffer_time[i])}', (r1_poses_x[i], r1_poses_y[i]), textcoords="offset points", xytext=(10, -10), ha='center', color='black')

                        plt.plot(r2_poses_x, r2_poses_y, label='Following Robot Trajectory', marker='o', markersize=5, linestyle='-', color='blue')
                        for i in range(0, len(buffer_time), 10):
                            plt.annotate(f't={int(buffer_time[i])}', (r2_poses_x[i], r2_poses_y[i]), textcoords="offset points", xytext=(10, -10), ha='center', color='black')

                        plt.xlabel('X position (m)')
                        plt.ylabel('Y position (m)')
                        plt.title('Two Robot Trajectories Over Time')
                        plt.legend()
                        plt.grid(True)
                        plt.savefig(os.path.join(output_dir, 'AMerged_trajectory.png'))
                        plt.close()

                        # Collect arrow data for this simulation run
                        start_A = [Goal2_x_list[0]-8,Goal2_y_list[0]]
                        start_B = [Goal1_x_list[0]-8,Goal1_y_list[0]]
                        goal_A = [Goal1_x_list[0],Goal1_y_list[0]]
                        goal_B = [Goal2_x_list[0],Goal2_y_list[0]]

                        i = len(buffer_time)-1
                        pos_A = [env.robots_pos[0][0],env.robots_pos[0][1]]
                        pos_B = [env.robots_pos[1][0],env.robots_pos[1][1]]


                        # print("INFO",start_A,start_B,goal_A,goal_B)
                        # Store data for vector field plotting

                        if env.args.heterogeneous or env.args.titanheads:
                            # Base components from linear and lateral velocities
                            dx_base = r2_buffer_linear_action[i] * 0.5   # Forward/backward component
                            dy_base = r2_buffer_lateral_action[i] * 0.5  # Left/right component
                            width2 = 0.1
                            alpha2 = 0.5
                            # Angular velocity modifies the direction of the resultant vector
                            # It can be thought of as adding a rotational bias to the motion
                            angular_influence = r2_buffer_angular_action[i] * 0.3  # Scale factor for angular effect
                            
                            # Method 1: Angular velocity rotates the linear+lateral vector
                            if abs(r2_buffer_linear_action[i]) > 0.01 or abs(r2_buffer_lateral_action[i]) > 0.01:
                                # There's translational motion - angular velocity modifies its direction
                                angle_offset = r2_buffer_angular_action[i] * (np.pi / 8)  # Convert angular vel to angle offset
                                
                                # Rotate the base vector by the angular influence
                                cos_offset = np.cos(angle_offset)
                                sin_offset = np.sin(angle_offset)
                                
                                dx2 = dx_base * cos_offset - dy_base * sin_offset
                                dy2 = dx_base * sin_offset + dy_base * cos_offset
                            else:
                                # Pure angular motion - create a tangential vector
                                if abs(r2_buffer_angular_action[i]) > 0.01:
                                    # Create a vector tangent to rotation at current position
                                    dx2 = -angular_influence  # Tangential component
                                    dy2 = angular_influence   # Tangential component
                                else:
                                    # No motion at all
                                    dx2 = 0
                                    dy2 = 0


                        
                        else:
                            theta2 = r2_buffer_angular_action[i] * (np.pi / 4)
                            length2 = r2_buffer_linear_action[i] * 0.5
                            width2 = 0.1
                            alpha2 = 0.5

                            dx2 = length2 * np.cos(theta2)
                            dy2 = length2 * np.sin(theta2)
                            aspect_ratio = ((((goal_A[0] + start_A[0]) / 2)+5) - (((goal_A[0] + start_A[0]) / 2)-5)) / ((((goal_A[1] + start_A[1]) / 2)+2) - (((goal_A[1] + start_A[1]) / 2)-1))
                            dy2=dy2/aspect_ratio

                        # Store arrow data
                        if env.args.heterogeneous or env.args.titanheads:
                            arrow_data = {
                            'x': g,
                            'y': h,
                            'dx': dx2,
                            'dy': dy2,
                            'linear_action': r2_buffer_linear_action[i],
                            'lateral_action': r2_buffer_lateral_action[i],
                            'angular_action': r2_buffer_angular_action[i],
                            'pos_A': pos_A,
                            'pos_B': pos_B,
                            'start_A': start_A,
                            'start_B': start_B,
                            'goal_A': goal_A,
                            'goal_B': goal_B,
                            'buffer_time': buffer_time[i],
                            'width2': width2,
                            'alpha2': alpha2
                            
                            
                            }
                        else:
                            arrow_data = {
                                'x': g,
                                'y': h,
                                'dx': dx2,
                                'dy': dy2,
                                'linear_action': r2_buffer_linear_action[i],
                                'angular_action': r2_buffer_angular_action[i],
                                'pos_A': pos_A,
                                'pos_B': pos_B,
                                'start_A': start_A,
                                'start_B': start_B,
                                'goal_A': goal_A,
                                'goal_B': goal_B,
                                'buffer_time': buffer_time[i],
                                'width2': width2,
                                'alpha2': alpha2
                            }
                        all_arrows_data.append(arrow_data)

                    env._p.disconnect()

            # NOW PLOT ALL ARROWS IN A SINGLE IMAGE
            if args.num_robots==2 and all_arrows_data:
                fig, ax2 = plt.subplots(nrows=1, ncols=1, figsize=(15, 9))
                
                # Use data from the first arrow for scene setup
                first_arrow = all_arrows_data[0]
                pos_A = first_arrow['pos_A']
                pos_B = first_arrow['pos_B']
                start_A = first_arrow['start_A']
                start_B = first_arrow['start_B']
                goal_A = first_arrow['goal_A']
                goal_B = first_arrow['goal_B']
                
                # Draw robots
                length = 1.2
                width = 0.78
                
                # # Robot B (Following Robot)
                # bottom_left_B = (pos_B[0] - length/2, pos_B[1] - width/2)
                # robot_rect1 = Rectangle(bottom_left_B, length, width, linewidth=10, edgecolor='blue', facecolor='blue')
                # ax2.add_patch(robot_rect1)
                
                # Robot A (Leading Robot)
                bottom_left_A = (pos_A[0] - length/2, pos_A[1] - width/2)
                robot_rect2 = Rectangle(bottom_left_A, length, width, linewidth=10, edgecolor='orange', facecolor='orange')
                ax2.add_patch(robot_rect2)
                
                # ax2.text(pos_A[0] + 0.1, pos_A[1], "Leading Robot", color='black', fontsize=15)
                
                # Plot ALL arrows
                for arrow_data in all_arrows_data:
                    x, y = arrow_data['x'], arrow_data['y']
                    dx, dy = arrow_data['dx'], arrow_data['dy']
                    linear_action = arrow_data['linear_action']
                    
                    # Determine arrow properties
                    # if round(linear_action, 3) == 0.0:
                    # if format(linear_action, ".2f") in ["0.00", "-0.00"]:
                    if abs(linear_action) < 0.01 and abs(linear_action) > - 0.01:
                        print("BINGO_________________")
                        dx = 0
                        arrow_color = 'black'
                        # widtharrow = 0.2
                        # hd = 0.1
                        # hl = 0.05

                        # widtharrow = 0.02
                        # hd = 0.01
                        # hl = 0.009
                        # dy=dy*0.5
                        alpha = 1
                        ax2.plot(x, y, marker='s', color='black', markersize=20, alpha=alpha)
                    else:
                        is_reverse = dx <= -0.01
                        arrow_color = 'red' if is_reverse else 'blue'
                        widtharrow = 0.01
                        hd = arrow_data['width2']
                        hl = 0.1

                        # # widtharrow=0.001
                        # # hd=0.01
                        # # hl=0.01
                        # # alpha = arrow_data['alpha2']
                        # # dx=dx*0.5

                        # widtharrow=0.0005
                        # hd=0.004
                        # hl=0.006
                        alpha = arrow_data['alpha2']
                        # dx=dx*0.2
                    
                    # Plot the arrow
                    
                        ax2.arrow(x, y, dx, dy, width=widtharrow, head_width=hd, head_length=hl, color=arrow_color, alpha=alpha)

                # Set up the scene (obstacles, goals, etc.)
                mid_x = (goal_A[0] + start_A[0]) / 2
                mid_y = (goal_A[1] + start_A[1]) / 2
                gap = 0.85
                half_gap = gap / 2
                obs_height = 0.75
                obs_thickness = 0.1
                
                top_y_bottom = mid_y + half_gap 
                top_y_top = top_y_bottom + obs_height
                bot_y_top = mid_y - half_gap
                bot_y_bottom = bot_y_top - obs_height 
                horizontal_length = 5.0
                
                # Draw obstacles
                ax2.plot([mid_x, mid_x], [top_y_bottom, top_y_top], 'r-', linewidth=8)
                ax2.plot([mid_x, mid_x], [bot_y_bottom, bot_y_top], 'r-', linewidth=8)
                ax2.plot([mid_x, mid_x + horizontal_length], [top_y_top, top_y_top], 'r-', linewidth=8)
                ax2.plot([mid_x, mid_x + horizontal_length], [bot_y_bottom, bot_y_bottom], 'r-', linewidth=8)
                ax2.plot([mid_x - horizontal_length, mid_x], [top_y_top, top_y_top], 'r-', linewidth=8)
                ax2.plot([mid_x - horizontal_length, mid_x], [bot_y_bottom, bot_y_bottom], 'r-', linewidth=8)
                
                # Plot start and goal positions
                # ax2.plot(*start_A, marker='>', color='orange', markersize=40)
                # ax2.plot(*start_B, marker='>', color='blue', markersize=40)
                ax2.plot(*goal_A, marker='o', color='orange', markersize=40)
                ax2.plot(*goal_B, marker='o', color='blue', markersize=40)
                
                # Set title and labels
                ax2.set_title(f"Robot B Vector Field Relative to Robot A", fontsize=25)
                ax2.set_xlabel("X position (m)", fontsize=25)
                ax2.set_ylabel("Y position (m)", fontsize=25)
                ax2.tick_params(axis='both', labelsize=25)
                
                #Set limits
                ax2.set_xlim(mid_x - 6, mid_x + 5)
                ax2.set_ylim(mid_y - 1.2, mid_y + 2)

                # ax2.set_xlim(mid_x - 3.45, mid_x - 3.25)
                # ax2.set_ylim(mid_y - 0.05, mid_y +0.15 )
                ax2.grid(True)
                
                # Legend
                handles = [
                    
                    Line2D([], [], color='blue', linewidth=2, marker='>', markersize=25, label='Forward Movement'),
                    Line2D([], [], color='red', linewidth=2, marker='>', markersize=25, label='Reverse Movement'),
                    # Line2D([], [], color='black', linewidth=2, marker='>', markersize=13, label='Following Robot Vector Field (Stopped)'),
                    Line2D([], [], color='black', linewidth=2, marker='s', markersize=25, label='Stopped'),
                    Line2D([], [], marker='s', color='orange', linestyle='None', markersize=25, label='Robot A'),
                    Line2D([], [], color='red', linewidth=8, label='Obstacle'),
                    # Line2D([], [], marker='>', color='black', markerfacecolor='none',linestyle='none', markersize=25, label='Start Position'),
                    Line2D([], [], marker='o', color='orange', linestyle='none', markersize=25, label='Goal of Robot A'),
                    Line2D([], [], marker='o', color='blue', linestyle='none', markersize=25, label='Goal of Robot B'),
                   
                ]
                ax2.legend(handles=handles, loc='upper left', fontsize=25, ncol=3, columnspacing=1.5)
                
                plt.tight_layout()
                output_dir = "/home/kom018/behaviour_rl/Results_plots/pybullet_excels/vector_fields/"
                filename = os.path.join(output_dir, f"combined_vector_field_all_arrows_{p}_{q}.png")
                plt.savefig(filename)
                plt.close()
                
                print(f"Plotted {len(all_arrows_data)} arrows in single image: {filename}")

if __name__== "__main__":
    run(args)