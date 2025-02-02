import torch
import numpy as np
import glob
import time
from pathlib import Path
import default_arguments
import copy
import pybullet as p

from pybullet_utils import bullet_client
import numpy as np
import os
import math

from assets.env_base import EnvBase
from assets.env_base_pb import EnvBasePB

from assets.env_titan_pb_2 import Env as TitanEnv
from assets.env_spot_pb_2 import Env as SpotEnv

try:
    if os.environ["PYBULLET_EGL"]:
        import pkgutil
except:
    pass

home = str(Path.home())

def run(args): 
    args.env = "spot_pb_r2"
    if args.hpc:
        path_home = home + "/hpc-scratch/" + home.split("/")[-1]
    else:
        path_home = "/scratch3/" + home.split("/")[-1]

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
    
    print("Loading from ", PATH)
    
    Env, args = default_arguments.get_env(args)   
    args.render = True
    args.record_sim = False
    env = Env(PATH=PATH, args=args)
    # print("TH");exit()
    #TIME AND SIM STEP SET
    timeStep = 1/50
    timeStep_10Hz = 1/10
    simStep = 1/100


    #ADHOK PARAMETER FOR INIT
    ac_size = 12
    action_scale = 0.5
    kp = 20.0
    kd = 0.5
    default_joints = np.array([0.0, 1.2, -2.0]*4)
    default_joints2 = np.array([0.0, 1.2, -2.0]*4)
    loaded_sim = False

    max_vx = 0.5
    max_vy = 0.0
    max_yaw_vel = 0.0

    min_vx = 0.5
    min_vy = -0.0
    min_yaw_vel = -0.0

    #defining target velocity range for command curriculum
    target_max_vx = 1.0
    target_max_vy = 0.5
    target_max_yaw_vel = 1.5

    z_offset = 0
    target_yaw = 0.0


    z_offset2 = 0
    target_yaw2 = 0.0

    #Commands
    commands = np.random.uniform([min_vx, min_vy, min_yaw_vel],[max_vx, max_vy, max_yaw_vel])
    commands2 = np.random.uniform([min_vx, min_vy, min_yaw_vel],[max_vx, max_vy, max_yaw_vel])
    # commands[2] = np.random.choice([-1,1]) * np.random.uniform(target_max_yaw_vel - args.yaw_cmd_dif, target_max_yaw_vel)
    # Set low lin velocities to zeros
    if np.random.random() < 0.8:
        commands[2] = np.random.choice([-1,1]) * np.random.uniform(1.0, target_max_yaw_vel)
        commands2[2] = np.random.choice([-1,1]) * np.random.uniform(1.0, target_max_yaw_vel)
    else:
        commands[2] = np.random.choice([-1,1]) * np.random.uniform(0, 1.0)
        commands2[2] = np.random.choice([-1,1]) * np.random.uniform(0, 1.0)
    
    commands[0] *= abs(commands[0])>0.1
    commands[1] *= abs(commands[1])>0.1
    commands[2] *= abs(commands[2])>0.1

    commands2[0] *= abs(commands2[0])>0.1
    commands2[1] *= abs(commands2[1])>0.1
    commands2[2] *= abs(commands2[2])>0.1


    #LOAD SIMULATOR
    # EnvBasePB.load_simulator(env)
    # if not loaded_sim:
    #     if args.frameless:
    #         if render and master:
    #             _p = bullet_client.BulletClient(connection_mode=p.GUI)
    #             p.resetDebugVisualizerCamera(cameraDistance=7, cameraYaw=0, cameraPitch=-30, cameraTargetPosition=[0,0,0])
    #         else:
    #             _p = bullet_client.BulletClient()
    #     else:
    #         if render and master:
    #             physicsClientId = p.connect(p.GUI)
    #             p.resetDebugVisualizerCamera(cameraDistance=7, cameraYaw=0, cameraPitch=-70, cameraTargetPosition=[0.55,-0.35,0])
    #         else:
    #             physicsClientId = p.connect(p.DIRECT) 

    # if not args.test:
    #     p.resetSimulation()

    # p.setPhysicsEngineParameter(deterministicOverlappingPairs=1)
    # # #optionally enable EGL for faster headless rendering
    # if args.frameless:
    #     try:
    #         if os.environ["PYBULLET_EGL"]:
    #             con_mode = _p.getConnectionInfo()['connectionMethod']
    #             if con_mode==_p.DIRECT:
    #                 egl = pkgutil.get_loader('eglRenderer')
    #                 if (egl):
    #                     _p.loadPlugin(egl.get_filename(), "_eglRendererPlugin")
    #                 else:
    #                     _p.loadPlugin("eglRendererPlugin")
    #     except:
    #         pass
    #     physicsClientId = _p._client
    #     _p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
    # # ======================================================================

    # p.setTimeStep(simStep)
    # p.setGravity(0,0,-9.8)

    

    # def compute_torques( actions):
    #     return kp*(action_scale*actions + default_joints - np.array(joints)) - kd*(np.array(joint_vel))

    
    # #LOAD URDF Robot
    # # objects = p.loadMJCF("./assets/xmls/ground.xml")
    # # worldId = objects[0]
    # # #worldId = p.loadURDF("/home/kom018/Phd_codes/Brendan/Wall_URDF/simpleplane.urdf")
    # model_path="./assets/urdfs/spot/urdf/spot.urdf"
    # # EnvBasePB.load_urdf_robot(env,model_path)
    # # Id = p.loadURDF(model_path,
    # #                     flags=
    # #                         # p.URDF_USE_COLLISION | Turn off collision, kills the titan
    # #                             p.URDF_USE_SELF_COLLISION_EXCLUDE_ALL_PARENTS |
    # #                             p.URDF_GOOGLEY_UNDEFINED_COLORS )
    
    
    # Id2=p.loadURDF(model_path,
    #                         flags=
    #                             # p.URDF_USE_SELF_COLLISION | Turn off self collision, kills the titan
    #                               p.URDF_USE_SELF_COLLISION_EXCLUDE_ALL_PARENTS |
    #                               p.URDF_GOOGLEY_UNDEFINED_COLORS )
    Id=env.Id
    Id2=env.Id2
    
    #LOAD SPECIFIC ROBOT R1
    ob_dict = {}
    jdict = {}
    feet_dict = {}
    leg_dict = {}
    body_dict = {}
    feet = ["rear_left_lower_leg", "rear_right_lower_leg", "front_left_lower_leg", "front_right_lower_leg"]
    legs = ["rear_left_upper_leg", "rear_right_upper_leg", "front_left_upper_leg", "front_right_upper_leg"]
    feet_contact = {f:True for f in feet}
    ordered_joints = []
    ordered_joint_indices = []
    shin_dict = {}
    arm_dict = {}
    for j in range( p.getNumJoints(Id2) ):
        info = p.getJointInfo(Id2, j)
        link_name = info[12].decode("ascii")
        if link_name in feet: feet_dict[link_name] = j
        if link_name in legs: leg_dict[link_name] = j
        if link_name=="pelvis": body_dict["body_link"] = j
        ordered_joint_indices.append(j)
        if info[2] != p.JOINT_REVOLUTE: continue
        jname = info[1].decode("ascii")
        # print(jname)

        lower, upper = (info[8], info[9])
        ordered_joints.append( (j, lower, upper) )
        jdict[jname] = j
    
    # Do not change this order!! Else joint postions will be wrong
    motor_names = ["front_left_hip_x"]
    motor_names += ["front_left_hip_y"]
    motor_names += ["front_left_knee"]
    motor_names += ["front_right_hip_x"]
    motor_names += ["front_right_hip_y"]
    motor_names += ["front_right_knee"]
    motor_names += ["rear_left_hip_x"]
    motor_names += ["rear_left_hip_y"]
    motor_names += ["rear_left_knee"]
    motor_names += ["rear_right_hip_x"]
    motor_names += ["rear_right_hip_y"]
    motor_names += ["rear_right_knee"]
    motor_power =  [20]*len(motor_names)       

    motors = [jdict[n] for n in motor_names]
        
    forces = np.ones(len(motors))*240
    # actions =
    #  {key:0.0 for key in motor_names}

    p.setJointMotorControlArray(Id2, motors, controlMode=p.VELOCITY_CONTROL, forces=[0.] * len(motor_names))

    for key in feet_dict:
        p.changeDynamics(Id2, feet_dict[key],lateralFriction=0.9, spinningFriction=0.9)
    

    
    ob_dict = {}
    for foot in feet_dict:
        ob_dict[foot] = False
        ob_dict["prev_" + foot] = False
    

    #LOAD SPECIFIC ROBOT R2
    ob_dict2 = {}
    jdict2 = {}
    feet_dict2 = {}
    leg_dict2 = {}
    body_dict2 = {}
    feet2 = ["rear_left_lower_leg", "rear_right_lower_leg", "front_left_lower_leg", "front_right_lower_leg"]
    legs2 = ["rear_left_upper_leg", "rear_right_upper_leg", "front_left_upper_leg", "front_right_upper_leg"]
    feet_contact2 = {f:True for f in feet2}
    ordered_joints2 = []
    ordered_joint_indices2 = []
    shin_dict2 = {}
    arm_dict2 = {}
    for j in range( p.getNumJoints(Id2) ):
        info2 = p.getJointInfo(Id2, j)
        link_name2 = info2[12].decode("ascii")
        if link_name2 in feet2: feet_dict2[link_name2] = j
        if link_name2 in legs2: leg_dict2[link_name2] = j
        if link_name2=="pelvis": body_dict2["body_link"] = j
        ordered_joint_indices2.append(j)
        if info2[2] != p.JOINT_REVOLUTE: continue
        jname2 = info2[1].decode("ascii")
        # print(jname)

        lower2, upper2 = (info2[8], info2[9])
        ordered_joints2.append( (j, lower2, upper2) )
        jdict2[jname2] = j
    
    # Do not change this order!! Else joint postions will be wrong
    motor_names2 = ["front_left_hip_x"]
    motor_names2 += ["front_left_hip_y"]
    motor_names2 += ["front_left_knee"]
    motor_names2 += ["front_right_hip_x"]
    motor_names2 += ["front_right_hip_y"]
    motor_names2 += ["front_right_knee"]
    motor_names2 += ["rear_left_hip_x"]
    motor_names2 += ["rear_left_hip_y"]
    motor_names2 += ["rear_left_knee"]
    motor_names2 += ["rear_right_hip_x"]
    motor_names2 += ["rear_right_hip_y"]
    motor_names2 += ["rear_right_knee"]
    motor_power2 =  [20]*len(motor_names2)       

    motors2 = [jdict2[n] for n in motor_names2]
        
    forces2 = np.ones(len(motors2))*240
    # actions =
    #  {key:0.0 for key in motor_names2}

    p.setJointMotorControlArray(Id2, motors2, controlMode=p.VELOCITY_CONTROL, forces=[0.] * len(motor_names2))

    for key in feet_dict2:
        p.changeDynamics(Id2, feet_dict2[key],lateralFriction=0.9, spinningFriction=0.9)
    

    
    ob_dict2 = {}
    for foot2 in feet_dict2:
        ob_dict2[foot2] = False
        ob_dict2["prev_" + foot2] = False
    

    
    
    
    

    USE_SPOT = True
    # USE_SPOT = False
    if USE_SPOT:
        # SPOT_MODEL_PATH = "./resources/spot/2024_04_30_08_59_43/model.pt" 
        # SPOT_MODEL_PATH = "./resources/spot/2024_05_08_21_23_04/model.pt"
        if args.jit_model: 
            SPOT_MODEL_PATH="/home/kom018/refarm/src/multi_robot_rl/scripts/JIT_models/spot_walking1.jit"
            pol = torch.load(SPOT_MODEL_PATH)
        else:
            SPOT_MODEL_PATH = "./resources/spot/2024_05_13_11_11_30/model.pt" 
            
            pol = torch.load(SPOT_MODEL_PATH)
        # print("pol",pol);exit()
    else:
        print("loading from ", PATH)
        pol = torch.load(PATH + "/model.pt")

    # else:
        # pol = torch.jit.load("./logs/chuck/exported/Oct18_09-03-12_/policy_1.pt")

    # model1 = copy.deepcopy(pol.pi.mu_net).to('cpu')
    # traced_script_module1 = torch.jit.script(model1)
    # # traced_script_module1.save("/home/kom018/behaviour_rl/Saved_models/JIT_models/mu_net_s.jit")
    # traced_script_module1.save("/home/kom018/refarm/src/multi_robot_rl/scripts/JIT_models/spot_walking1.jit")


    # env.set_position([2,2,1],[0,0,0,1],robot_id=Id2)


    obs = env.reset()
    if args.use_perception:
        im = env.get_image()

    # obs2 = env.reset()
    # if args.use_perception:
    #     im2 = env.get_image()
    print("obs",obs)
    n=0
    while True:
        # obs[0][8:11]=[1,0,0]
        # print("chking",obs[0][8:11])
        # print("obs",len(obs[1][0]));exit()
        print('ob_0',obs[1])
        if args.use_perception:
            
            action = pol.step(torch.tensor(np.array(obs).astype(np.float32)), torch.tensor(np.array(im).astype(np.float32)), stochastic=False)[0]
        

        elif args.jit_model:
            concatenate_part_r1=torch.as_tensor(np.array([obs[0]]), dtype=torch.float32).unsqueeze(dim=0)[0]
            action = pol(concatenate_part_r1).detach().numpy()
            concatenate_part_r2=torch.as_tensor(np.array([obs[1]]), dtype=torch.float32).unsqueeze(dim=0)[0]
            action2 = pol(concatenate_part_r2).detach().numpy()
            # print("action",action,len(action[0]),type(action));exit()
        else:
            # action = pol(torch.tensor(np.array(obs).astype(np.float32))).detach().numpy()[0]
            
            action = pol.step(torch.tensor(np.array(obs).astype(np.float32)), stochastic=False)[0]
            # print("action",action,len(action[0]),type(action));exit()
        # obs, rew, done, _ = env.step(action)
        
        for _ in range(int(timeStep/simStep)):
            jointStates = p.getJointStates(Id,ordered_joint_indices)
            joints = list(np.array([jointStates[j[0]][0] for j in ordered_joints[:int(ac_size)]]))
            
            # Scale vels 
            joint_vel = list(np.array([jointStates[j[0]][1] for j in ordered_joints[:int(ac_size)]]) / 10) 

            # forces = compute_torques(action)
            forces=kp*(action_scale*action + default_joints - np.array(joints)) - kd*(np.array(joint_vel))
            
            forces = forces.reshape(-1)
            p.setJointMotorControlArray(Id, motors, controlMode=p.TORQUE_CONTROL, forces=forces)
            
            
            #R2___________________________________
            jointStates2 = p.getJointStates(Id2,ordered_joint_indices2)
            joints2 = list(np.array([jointStates2[j[0]][0] for j in ordered_joints2[:int(ac_size)]]))
            
            # Scale vels 
            joint_vel2 = list(np.array([jointStates2[j[0]][1] for j in ordered_joints2[:int(ac_size)]]) / 10) 

            # forces = compute_torques(action)
            forces2=kp*(action_scale*action2 + default_joints2 - np.array(joints2)) - kd*(np.array(joint_vel2))
            
            forces2 = forces2.reshape(-1)
            p.setJointMotorControlArray(Id2, motors2, controlMode=p.TORQUE_CONTROL, forces=forces2)

            p.stepSimulation()

        if args.render:
            time.sleep(timeStep)

        

        # env.get_observation1()
        # env.get_observation2()
        # obs = obs1,obs2

        commands=[-0.75,-0.5,-0.75]
        commands2=[-0.75,-0.5,-0.75]

        #Observation Robot 1
        jointStates = p.getJointStates(Id,ordered_joint_indices)
        joints = list(np.array([jointStates[j[0]][0] for j in ordered_joints[:int(ac_size)]]))
        
        # Scale vels 
        if args.load_path != "":
            # Used an additionally scaling for training translation.pt
            joint_vel = list(np.array([jointStates[j[0]][1] for j in ordered_joints[:int(ac_size)]]) / 10) 
        else:
            joint_vel = list(np.array([jointStates[j[0]][1] for j in ordered_joints[:int(ac_size)]])) 
        
        ob_dict.update({n + '_pos':j for n,j in zip(motor_names, joints)})


        body_xyz, (qx, qy, qz, qw) = p.getBasePositionAndOrientation(Id)
        pos = body_xyz
        orn = [qx, qy, qz, qw]
        roll, pitch, yaw = p.getEulerFromQuaternion([qx, qy, qz, qw])

        body_vxyz, base_rot_vel = p.getBaseVelocity(Id)
        
        roll_vel = base_rot_vel[0]
        pitch_vel = base_rot_vel[1]
        yaw_vel = base_rot_vel[2]

        rot_speed = np.array(
        [[np.cos(-yaw), -np.sin(-yaw), 0],
            [np.sin(-yaw), np.cos(-yaw), 0],
            [		0,			 0, 1]]
        )

        vx, vy, vz = np.dot(rot_speed, (body_vxyz[0],body_vxyz[1],body_vxyz[2]))
        
        # Policy shouldn't know yaw
        body = [vx, vy, vz, roll, pitch, roll_vel, pitch_vel, yaw_vel, body_xyz[2] - z_offset]

        leg_contacts = []
        for leg in leg_dict:
            ob_dict[leg] = len(p.getContactPoints(Id, -1, leg_dict[leg], -1))>0
            leg_contacts += [ob_dict[leg]]


        contacts = []
        for foot in feet_dict:
            ob_dict["prev_" + foot] = ob_dict[foot]
            ob_dict[foot] = len(p.getContactPoints(Id, -1, feet_dict[foot], -1))>0
            contacts += [ob_dict[foot], ob_dict["prev_" + foot]]

        target_yaw += commands[2] * timeStep 
        
        base_lin_vel = np.array([vx, vy, vz])
        base_ang_vel = np.array([roll_vel, pitch_vel, yaw_vel])
        dof_pos_s = np.array(joints)
        dof_vel_s = np.array(joint_vel)
        lin_vel = 1.0
        ang_vel = 1.0
        commands_scale = np.array([1.0, 1.0, 1.0])
        dof_pos = 1.0
        dof_vel = 0.05
        # print("len",len(actions))
        # print("command",commands)
        
        obs_buf = np.concatenate((  (base_lin_vel * lin_vel).reshape([1,3]),
                                (base_ang_vel  * ang_vel).reshape([1,3]),
                                np.array([[roll, pitch]]),
                                (commands[:3] * commands_scale).reshape([1,3]),
                                ((dof_pos_s - default_joints) * dof_pos).reshape([1,ac_size]),
                                (dof_vel_s * dof_vel).reshape([1,ac_size]),
                                (np.array(contacts)).reshape([1,8]),
                                action.reshape([1,ac_size])
                                ),axis=-1)

        obs1=obs_buf
        
        done = False
        # if body_xyz[2] < 0.3 or (abs(np.array([pitch, roll])) > 1.0).any() or (np.array(leg_contacts)).any():
        #     done = True



        #Observation Robot 2
        jointStates2 = p.getJointStates(Id2,ordered_joint_indices2)
        joints2 = list(np.array([jointStates2[j[0]][0] for j in ordered_joints2[:int(ac_size)]]))
        
        # Scale vels 
        if args.load_path != "":
            # Used an additionally scaling for training translation.pt
            joint_vel2 = list(np.array([jointStates2[j[0]][1] for j in ordered_joints2[:int(ac_size)]]) / 10) 
        else:
            joint_vel2 = list(np.array([jointStates2[j[0]][1] for j in ordered_joints2[:int(ac_size)]])) 
        
        ob_dict2.update({n + '_pos':j for n,j in zip(motor_names2, joints2)})


        body_xyz2, (qx2, qy2, qz2, qw2) = p.getBasePositionAndOrientation(Id2)
        pos2 = body_xyz2
        orn2 = [qx2, qy2, qz2, qw2]
        roll2, pitch2, yaw2 = p.getEulerFromQuaternion([qx2, qy2, qz2, qw2])

        body_vxyz2, base_rot_vel2 = p.getBaseVelocity(Id2)
        
        roll_vel2 = base_rot_vel2[0]
        pitch_vel2 = base_rot_vel2[1]
        yaw_vel2 = base_rot_vel2[2]

        rot_speed2 = np.array(
        [[np.cos(-yaw2), -np.sin(-yaw2), 0],
            [np.sin(-yaw2), np.cos(-yaw2), 0],
            [		0,			 0, 1]]
        )

        vx2, vy2, vz2 = np.dot(rot_speed2, (body_vxyz2[0],body_vxyz2[1],body_vxyz2[2]))
        
        # Policy shouldn't know yaw
        body2 = [vx2, vy2, vz2, roll2, pitch2, roll_vel2, pitch_vel2, yaw_vel2, body_xyz2[2] - z_offset2]

        leg_contacts2 = []
        for leg2 in leg_dict2:
            ob_dict2[leg2] = len(p.getContactPoints(Id2, -1, leg_dict2[leg2], -1))>0
            leg_contacts2 += [ob_dict2[leg2]]


        contacts2 = []
        for foot2 in feet_dict2:
            ob_dict2["prev_" + foot2] = ob_dict2[foot2]
            ob_dict2[foot2] = len(p.getContactPoints(Id2, -1, feet_dict2[foot2], -1))>0
            contacts2 += [ob_dict2[foot2], ob_dict2["prev_" + foot2]]

        target_yaw2 += commands2[2] * timeStep 
        
        base_lin_vel2 = np.array([vx2, vy2, vz2])
        base_ang_vel2 = np.array([roll_vel2, pitch_vel2, yaw_vel2])
        dof_pos_s2 = np.array(joints2)
        dof_vel_s2 = np.array(joint_vel2)
        lin_vel2 = 1.0
        ang_vel2 = 1.0
        commands_scale2 = np.array([1.0, 1.0, 1.0])
        dof_pos2 = 1.0
        dof_vel2 = 0.05
        # print("len",len(actions))
        # print("command",commands)
        
        
        obs_buf2 = np.concatenate((  (base_lin_vel2 * lin_vel2).reshape([1,3]),
                                (base_ang_vel2  * ang_vel2).reshape([1,3]),
                                np.array([[roll2, pitch2]]),
                                (commands2[:3] * commands_scale2).reshape([1,3]),
                                ((dof_pos_s2 - default_joints2) * dof_pos2).reshape([1,ac_size]),
                                (dof_vel_s2 * dof_vel2).reshape([1,ac_size]),
                                (np.array(contacts2)).reshape([1,8]),
                                action2.reshape([1,ac_size])
                                ),axis=-1)

        obs2=obs_buf2
        obs=obs1,obs2
        
        done2 = False
        # if body_xyz2[2] < 0.3 or (abs(np.array([pitch2, roll2])) > 1.0).any() or (np.array(leg_contacts2)).any():
        #     done2 = True
        # start = 100
        # if env.steps < start:
        #     env.commands = np.array([0., 0.0, 0.0])
        # elif env.steps < start + 200:
        #     env.commands = np.array([0., 0.0, 1.5])
        # elif env.steps < start + 400:
        #     env.commands = np.array([0., 0.0, -1.5])
        # elif env.steps < start + 500:
        #     env.commands = np.array([1., 0.0, 0])
        # elif env.steps < start + 700:
        #     env.commands = np.array([-0.5, 0.0, 0])
        # elif env.steps < start + 800:
        #     env.commands = np.array([0., 0.5, 0])
        # elif env.steps < start + 900:
        #     env.commands = np.array([0., -0.5, 0])
         
        # print(rew)
        # print(env.commands)
        # print(env.vx, env.vy, env.yaw_vel)
        # print()
        if args.use_perception:
            im = env.get_image()

        if done==True or env.steps > args.max_ep_len:
            obs = env.reset()
            # obs2 = env.reset()
            if args.use_perception:
                im = env.get_image()
                im2 = env.get_image()

        # if args.use_perception:
        #     im2 = env.get_image()

        # if done2==True or env.steps > args.max_ep_len:
        #     obs2 = env.reset()
        #     if args.use_perception:
        #         im2 = env.get_image()

if __name__== "__main__":
    args = default_arguments.get_defaults() 
    run(args)
