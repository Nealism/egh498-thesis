import numpy as np
import mujoco
from gym import spaces
from collections import deque
from mpi4py import MPI
comm = MPI.COMM_WORLD
from scipy.spatial.transform import Rotation
import mujoco_viewer
from pyquaternion import Quaternion
import os

from .env_base_mj import EnvBaseMJ
from utils.terrain import Hfield, TerrainGen
from utils import img_helpers
from utils.xml_helper import indent_xml
from lxml import etree
import math
from configs.anymal_cmd_mj_cfg import AnymalCmdMjCfg

class Env(EnvBaseMJ):
    # Timestep for mujoco is set in the .xml, and shows up under self.model.opt.timestep
    # Default is 0.002, changing this might affect the contact model. 
    simStep = 1/500
    timeStep = 1/100
    rank = comm.Get_rank()
    Kp = 400
    initial_Kp = Kp
    def __init__(self, PATH=None, args=None, writer=None):

        self.view_rank = 0
        self.args = args
        self.render = args.render and self.rank == self.view_rank
        self.PATH = PATH
        self.writer = writer
        self.master = True 

        ### CONFIGS ###

        self.cfg = AnymalCmdMjCfg
        self.env_cfg = self.cfg.env
        self.terr_cfg = self.cfg.terrain
        self.map_cfg = self.cfg.map
        self.rew_cfg = self.cfg.reward
        self.robot_cfg = self.cfg.robot

        super().__init__(PATH)

        self.robot_name = "anymal_c"

        ##### PATHS #####

        self.general_xml_path = "assets/xmls/anybotics_anymal_c/"
        self.base_terrain_xml = "base_terrain.xml"
        # Name of the base link in the xml, for setting the robot position on reset
        self.base_link = "base"
        if self.args.control_type == "torque":
            self.model_path = self.general_xml_path + "scene_torque.xml"
            self.action_multiplier = self.robot_cfg.torque_act_mult
        elif self.args.control_type == "position":
            self.model_path = self.general_xml_path + "scene.xml"
            self.action_multiplier = self.robot_cfg.pos_act_mult
        self.mesh_dir = self.general_xml_path + "assets/"
        
        # self.action_multiplier = 0.0
        
        self.viewer = None

        ##### WAY POINT STUFF #####

        self.wp_pos_mj = None # position in env
        self.wp_pos_im = None # position in map image
        self.last_wp_time = None # last time wp was generated
        self.max_vel_to_wp = self.map_cfg.max_vel_to_wp # max vel. expect robot to maintain moving towards wp

        ##### TERRAIN STUFF #####
        
        # set up base xml files for this rank/process (scene, tree, terrain etc.)
        if self.args.tree_type or self.args.add_terrain:
            self.set_up_xmls()

        # load mujoco model and data (robot itself, trees, terrains etc.)
        self.first_time = True
        self.load_robot()
        self.first_time = False

        self.ob_size = self.env_cfg.ob_size
        self.ac_size = self.env_cfg.ac_size
        self.im_size = [1] + list(self.terr_cfg.hm_img_dim)

        self.motor_names = self.robot_cfg.motor_names
        # Needed if importing as Gym environment
        self.action_space = spaces.Box(-10000*np.ones(self.ac_size), 10000*np.ones(self.ac_size), dtype=np.float32)
        self.observation_space = spaces.Box(-10000*np.ones(self.ob_size), 10000*np.ones(self.ob_size), dtype=np.float32)

        # left front, right front, left back, right back
        self.initial_joints = self.robot_cfg.init_joints
        self.right_swing = self.robot_cfg.right_swing
        self.left_swing = self.robot_cfg.left_swing

        self.initial_z = self.robot_cfg.init_z

        self.episodes = -1
        self.success = deque([0.0], maxlen=self.rew_cfg.goal.max_succ_len)
        self.sim_data = []
        self.best_return = 0

        self.steps = 0

        self.reward_names = ["Reward/goal", "Reward/joint", "Reward/orn", "Reward/contacts"]
        self.reward_dict = {reward:deque(maxlen=100) for reward in self.reward_names} 
        self.ep_reward_dict = {reward:0 for reward in self.reward_names} 

        # States that we want to restore, for resuming training after running a test
        # self.states_to_restore = ["pos", "orn", "joints", "joint_vel", "args", "paused", "ep_success", "cur_success", "steps", "ep_steps", "ob_dict", "step_count", "z_offset", "terrain", "Kp", "max_disturbance", "env_exp"]

    def load_terrains(self):
        """
        Generates all Terrain objects for this environment and adds them to the terrains array.

        NOTE: By default, always load the ground truth
        NOTE: can optionally create other terrains 
        """
        self.terrains = []
        self.terrain_generator = TerrainGen()
        # generate and load ground truth image

        # gt_arr = self.terrain_generator.gen_rand_ground_truth(0, 255, self.terr_cfg.gt_img_dim)
        gt_arr = np.ones((self.terr_cfg.gt_img_dim))
        gt_arr[200:300, 300:320] = 0.5

        gt_path = self.get_parent_dir(self.model_path)
        gt_name = f"ground_truth_{str(self.rank)}"
        gt_position = self.terr_cfg.hf_centre_pos
        gt_size = (*self.terr_cfg.gt_mj_dim, self.terr_cfg.hf_elev, self.terr_cfg.hf_depth)

        self.ground_truth = Hfield(gt_arr, gt_path, gt_name, gt_position, gt_size) 
        self.terrains.append(self.ground_truth)

        #generate and load any others below this
        ########################################
    
    def get_image(self):
        """

        """
        subsection = self.ground_truth.compute_sub_section(self.pos[0], self.pos[1], *self.terr_cfg.hm_img_dim)
        return np.reshape(subsection, self.im_size)

    def show_map(self):
        """
        Displays a birds-eye map of the ground truth the robot is traversing.
        Also draws a bounding box around the robot's sub-section (image
        the policy is fed)
        """
        img_copy = self.ground_truth.terr_img.copy()
        box_centre = self.ground_truth.rob_to_img_pos(self.pos) 
        img_helpers.draw_bounding_box(img_copy, box_centre, *self.terr_cfg.hm_img_dim) 
        if self.map_cfg.show_waypoint: 
            img_helpers.draw_dot(img_copy, self.wp_pos_im)
        img_helpers.display_img(img_copy)
    
    def populate_terrain_xml(self, file_path):
        """
        Builds up the terrain xml (for this process)  
        """
        xml = etree.parse(file_path)
        root = xml.getroot()
        # asset el - where all hfields and meshes live
        asset = etree.SubElement(root, "asset")
        # worldbody el - where all the referencing geoms live
        worldbody = etree.SubElement(root, "worldbody")

        # add all terrains to the xml file
        for terr in self.terrains:
            asset.append(terr.hfield_el)
            worldbody.append(terr.geom_el)
        indent_xml(root)
        xml.write(file_path)
    
    def reconfig_terrain_xml(self, file_path, terr_obj):
        """
        Reconfigure the xml for the given terrain object.
        NOTE: if only change is PNG image (name remains same), don't need to configure
        """
        xml = etree.parse(file_path)
        asset, worldbody = xml.findall('asset')[0], xml.findall('worldbody')[0]
        hfield = [hf for hf in asset.findall('hfield') if hf.attrib['name'] == terr_obj.name][0]
        geom = [gm for gm in worldbody.findall('geom') if gm.attrib['name'] == terr_obj.name][0]
        asset.remove(hfield)
        worldbody.remove(geom)
        asset.append(terr_obj.hfield_el)
        worldbody.append(terr_obj.geom_el)
        indent_xml(xml.getroot())
        xml.write(file_path)
        
    def can_gen_waypoint(self):
        """
        Returns True iff can generate a way point, False otherwise

        Conditions of wp generation:
            -have yet to generate one (this episode/rollout) OR;
            -have exceeded the max time to reach the wp OR;
        """
        if not self.wp_pos_mj:
            return True
        return self.data.time - self.last_wp_time >= self.wp_time_lim

    def gen_waypoint(self, point=None):
        """
        Generates a new waypoint for the environment 

            point - if not given, waypoint is generated randomly within the robot's current
                    height map
        """
        # custom 
        if point:
            x = point[0]
            y = point[1]
        # random 
        else:
            x_low, y_low = self.pos[0]-self.terr_cfg.hm_mj_dim[0], self.pos[1]-self.terr_cfg.hm_mj_dim[1]
            x_high, y_high = self.pos[0]+self.terr_cfg.hm_mj_dim[0], self.pos[1]+self.terr_cfg.hm_mj_dim[1]
            x = np.random.uniform(low=x_low, high=x_high)
            y = np.random.uniform(low=y_low, high=y_high)

        # set both its mj position AND image position
        self.wp_pos_mj = (x, y)
        self.wp_pos_im = self.ground_truth.rob_to_img_pos(self.wp_pos_mj)

        # set time at which waypoint was placed
        self.last_wp_time = self.data.time
        
        # set time limit for robot to reach the waypoint
        self.wp_time_lim = self.time_to_waypoint()
    
    def time_to_waypoint(self):
        """
        Calculates the app. time for the robot to reach the current wp 

        NOTE: this assumes: -robot maintains max. velocity to the wp
                            -the robot was facing the direction of the way point 
                             when it was set
        """
        # calculate straight line distance to wp
        dx = self.wp_pos_mj[0] - self.pos[0]
        dy = self.wp_pos_mj[1] - self.pos[1]
        abs_dist = math.sqrt(dx**2 + dy**2)
        
        # return estimate of time for robot to reach wp
        # NOTE: multiply by scalar to account for the assumptions made (see above)
        return self.map_cfg.wp_time_scalar * (abs_dist / self.max_vel_to_wp)

    def load_robot(self):
        # load in grass/trees
        if not self.args.replay and self.args.tree_type:
            if self.args.tree_type == "grass":
                self.generate_tree(**self.terr_cfg.grass_params)
            elif self.args.tree_type == "tree":
                self.generate_tree(**self.terr_cfg.tree_params)

        self.model = mujoco.MjModel.from_xml_path(self.model_path)
        self.data = mujoco.MjData(self.model)

        # load in terrains
        if not self.args.replay and self.args.add_terrain:
            self.load_terrains()
            terrain_path = self.get_parent_dir(self.model_path) + f"terrain_{str(self.rank)}.xml"
            if self.first_time:
                self.populate_terrain_xml(terrain_path)
            else:
                self.reconfig_terrain_xml(terrain_path, self.ground_truth)

        # Mujoco_viewer doesn't work on the hpc, shouldn't render there anyway
        if not self.args.training_on_hpc:
            if self.render:
                # new viewer every episode s.t. correct env appears every time
                if self.viewer:
                    self.viewer.close()
                self.viewer = mujoco_viewer.MujocoViewer(self.model, self.data)
            else:
                # Offscreen might help getting images?
                self.viewer = mujoco_viewer.MujocoViewer(self.model, self.data, 'offscreen')
        else:
            print("Can't view mujoco on the HPC.")
        
    def get_log_things(self):
        # Things we want to log each training step (print and add to tensorboard)
        return_dict = {"Kp": self.Kp, "Success": self.success, "Cur": self.args.cur}
        return_dict.update(self.reward_dict)
        return return_dict

    def get_success(self):
        # Success is time spent above a target goal
        min_goal_len = self.rew_cfg.goal.min_goal_len
        mean_goal_tgt = self.rew_cfg.goal.mean_goal_tgt
        return (len(self.goal) > min_goal_len and 
                np.mean(self.goal) > mean_goal_tgt)

    def check_for_success(self):
        max_len = self.rew_cfg.goal.max_succ_len
        return (len(self.success) == max_len and 
                (np.array(self.success) == True).all())

    def reset(self, test=False, model_path=None, restore_state=None):
        if self.steps > 0:
            for key in self.reward_dict:
                self.reward_dict[key].append(self.ep_reward_dict[key]/self.steps)
        self.ep_reward_dict = {reward:0 for reward in self.reward_names} 

        # reset way point
        self.wp_pos_mj = None

        if self.episodes > -1:
            self.success.append(self.get_success())
            target = None
            if self.args.tree_type:
                self.save_tree(best=self.total_return > self.best_return, test=test)
            self.record_sim_state(best=self.total_return > self.best_return, test=test, additional_arguments=target)
            if self.total_return > self.best_return:
                self.best_return = self.total_return
        self.total_return = 0
        self.paused = True

        if self.args.cur and self.Kp > 0 and self.check_for_success():
            self.Kp = 0.75*self.Kp
            if self.Kp < 5:
                self.Kp = 0
                self.args.cur = False
            self.success = deque([0.0], maxlen=5)
        
        if model_path is not None:
            self.model_path = model_path 

        # must reset mj model and data if loading new trees/grass/terrain every episode
        if self.args.tree_type or self.args.add_terrain or model_path is not None:
            self.load_robot()

        mujoco.mj_resetData(self.model, self.data)

        if restore_state is not None:
            self.set_position(pos=restore_state[0], orn=restore_state[1], joints=restore_state[2])
        else:
            # Rotate the base of the robot to simulate being on the back of a titan
            rot_range = 0.2
            # rot_range = 0.0
            self.rot = Rotation.from_euler('xyz', [np.random.uniform(-rot_range, rot_range), np.random.uniform(-rot_range, rot_range), 0], degrees=False)
            # self.rot = Rotation.from_euler('xyz', [np.random.uniform(-rot_range, rot_range), np.random.uniform(-rot_range, rot_range), np.pi], degrees=False)
            self.orn = self.rot.as_quat()
            self.pos = [0,0,self.initial_z]
            self.set_position(pos=self.pos, orn=self.orn, joints=self.initial_joints)

        self.steps = 0
        self.episodes += 1

        # Step the simulation once to get the initial state
        mujoco.mj_forward(self.model, self.data)
        self.get_observation()

        # Maybe randomise which legs swing first?
        self.current_swing = "right"
        self.expert_target = self.right_swing if self.current_swing == "right" else self.left_swing
        self.get_trajectory(self.expert_target)

        self.command_ranges = np.array(self.env_cfg.cmd_ranges)
        self.commands = list(np.random.uniform(-self.command_ranges, self.command_ranges))
        self.time_at_speed = 0
        self.goal = []

        self.prev_actions = self.joints
        state = self.imu + self.commands + self.joints + self.joint_vel + self.joint_force + [contact for contact in self.contacts.values()]
        return state

    def step(self, actions=None, replay_state=None, additional_stuff=None, cmds=None):
        """
        TODO: make a self.args.show_map argument
        we want to be able to show the map, bounding boxes and waypoints even if 
        person is not using ground truth

        -means we need a map to show people if they haven't loaded in any terrain
        (empty image)
        -which in turn means we need the auto xml load thing
        """
        if cmds is not None:
            self.commands = cmds
        
        if self.args.add_terrain:
            if self.can_gen_waypoint():
                self.gen_waypoint()

            if self.rank == self.view_rank and self.render and self.map_cfg.show_map:
                self.show_map()

        if self.paused:
            self.target_vx = 0.0
            expert = self.initial_joints    
        else:
            self.target_vx = 1.0
            if self.steps % self.traj_size == 0:
                self.current_swing = "right" if self.current_swing == "left" else "left"
                self.expert_target = self.right_swing if self.current_swing == "right" else self.left_swing
                self.get_trajectory(self.expert_target)
            expert = self.expert_traj[self.traj_i]
            if self.traj_i < self.traj_size - 1:
                self.traj_i += 1

        if actions is not None:
            self.actions = list(np.array(self.initial_joints) + np.array(actions))
        else:
            self.actions = self.initial_joints

        if self.args.cur:
            # Sample every 4 seconds
            if self.steps > 0 and self.steps % int(4 / self.timeStep)==0:
                self.commands = list(np.random.uniform(-self.command_ranges, self.command_ranges))
                self.success.append(self.get_success())
                self.time_at_speed = 0
                self.goal = []

            world_to_robot_rot_mat = np.array(
            [[np.cos(-self.yaw), -np.sin(-self.yaw), 0],
                [np.sin(-self.yaw), np.cos(-self.yaw), 0],
                [		0,			 0, 1]]
            )

            # Need to convert robot frame velocities and commands to world frame to apply forces
            robot_to_world_rot_mat = np.array(
            [[np.cos(-self.yaw), np.sin(-self.yaw), 0],
                [-np.sin(-self.yaw), np.cos(-self.yaw), 0],
                [		0,			 0, 1]]
            )

            vx_cmd, vy_cmd, _ = np.dot(robot_to_world_rot_mat, (self.commands[0], self.commands[1],0))
            vx, vy, _ = np.dot(robot_to_world_rot_mat, (self.vx, self.vy, self.vz))
            
            forces = np.zeros(6)
            error = np.abs(np.array(self.commands) - np.array([self.vx, self.vy, self.yaw_vel]))
            
            # This doesn't seem to work, instead using average goal reward
            if (error < 0.3).all():
                self.time_at_speed += 1
            gain = 50
            z_gain = 200
            forces[0] = gain * (self.Kp / self.initial_Kp) * np.clip((vx_cmd - vx), -1, 1)
            forces[1] = gain * (self.Kp / self.initial_Kp) * np.clip((vy_cmd - vy), -1, 1)
            forces[2] = z_gain * (self.Kp / self.initial_Kp) * np.clip((0.5 - self.pos[2]), -1, 1)
            forces[5] = gain * (self.Kp / self.initial_Kp) * np.clip((self.commands[2] - self.yaw_vel), -1, 1)
            self.data.xfrc_applied = forces

        # This might do something weird with mujoco contacts, and other things in the sim.
        for _ in range(int(np.rint(self.timeStep/self.simStep))):

            # self.set_position(pos=[0,0,0.5], orn=[0,0,0,1])

            if replay_state is not None:
                self.set_position(pos=replay_state[0], orn=replay_state[1])
            else:            
                if self.args.cur:
                    if self.args.just_expert:
                        self.data.ctrl[:self.ac_size] = (self.Kp / self.initial_Kp)*np.array(expert)
                    else:
                        self.data.ctrl[:self.ac_size] = self.action_multiplier*np.array(self.actions) + (self.Kp / self.initial_Kp) * np.array(expert)
                else:
                    self.data.ctrl[:self.ac_size] = self.action_multiplier*np.array(self.actions)
                            
            mujoco.mj_step(self.model, self.data)
        
        if self.render:
            self.viewer.render()

        self.get_observation()

        self.save_sim_state()
        reward, done = self.get_reward()
        self.prev_actions = self.actions
        self.total_return += reward
        self.steps += 1

        state = self.imu + self.commands + self.joints + self.joint_vel + self.joint_force + [contact for contact in self.contacts.values()]
        return np.array(state), reward, done, None
    
    def get_reward(self):
        done = False
        if self.pos[2] < 0.35 or abs(self.pitch) > 0.5 or abs(self.roll) > 0.5:
            done = True
        
        goal = 1.0*np.exp(-5.0*np.sum(np.array(self.commands[:2]) - np.array([self.vx, self.vy]) )**2)            
        goal += 0.5*np.exp(-2.5*np.sum(np.array(self.commands[2]) - np.array(self.yaw_vel) )**2)     
        self.goal.append(goal)

        joints = np.exp(-0.5*np.sum((np.array(self.joints) - np.array(self.initial_joints))**2))
        orn = np.exp(-10.0 * np.sum((np.array([self.roll, self.pitch]) - np.zeros(2))**2))
        
        # Contacts should match pair-wise. both front's should be off the ground, both backs shouldn't
        contacts = 0.25*(self.contacts["left_front"] - self.contacts["right_back"])**2 
        contacts += 0.25*(self.contacts["right_front"] - self.contacts["left_back"])**2 
        contacts += 0.25*((1 - self.contacts["left_front"]) - self.contacts["right_front"])**2 
        contacts += 0.25*((1 - self.contacts["left_back"]) - self.contacts["right_back"])**2 

        # reward = 1.5*goal + 0.5*joints + 0.25*orn - 0.25*contacts
        reward = 1.5*goal + 0.5*joints + 0.1*orn - 0.25*contacts
        
        # old
        # reward = 1.5*goal + 0.1*joints + 0.1*orn - 0.1*contacts

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/joint"] += joints
        self.ep_reward_dict["Reward/orn"] += orn
        self.ep_reward_dict["Reward/contacts"] += contacts
        return reward, done

    def get_observation(self):
        # Keep an eye on these to make sure they are getting what you think)
        self.pos = self.data.body(self.base_link).xpos.copy()
        orn = self.data.body(self.base_link).xquat.copy()
        self.orn = [orn[1],orn[2],orn[3],orn[0]]

        rot = Rotation(self.orn)
        self.roll, self.pitch, self.yaw = rot.as_euler('xyz', degrees=False)

        self.imu = [self.roll, self.pitch] + list(self.data.sensordata) 
        self.vx, self.vy, self.vz = self.data.sensordata[3:6]
        self.yaw_vel = self.data.sensordata[2]

        self.joints = [self.data.joint(name).qpos[0] for name in self.motor_names]
        self.joint_vel = [self.data.joint(name).qvel[0] for name in self.motor_names]
        self.joint_force = list(self.data.actuator_force[:self.ac_size])

        # Should be an easier way to get a specific contact?
        self.feet = ["left_front", "right_front", "left_back", "right_back"]
        contact_list = self.data.contact
        # self.contacts = [0] * len(self.feet)
        self.contacts = {foot:0 for foot in self.feet}
        for dim, contact1, contact2 in zip(contact_list.dim, contact_list.geom1, contact_list.geom2):
            if dim:
                geom_name1 = mujoco.mj_id2name(self.model, mujoco.mjtObj.mjOBJ_GEOM, contact1)
                geom_name2 = mujoco.mj_id2name(self.model, mujoco.mjtObj.mjOBJ_GEOM, contact2)
                if geom_name1 in self.feet:
                    # self.contacts[self.feet.index(geom_name1)] = 1
                    self.contacts[geom_name1] = 1
                elif geom_name2 in self.feet: 
                    # self.contacts[self.feet.index(geom_name2)] = 1
                    self.contacts[geom_name2] = 1

        if self.steps > 20 and np.array(self.contacts).all():
            # For some reason all feet are in contact on reset even when not touching the ground
            self.paused = False

    def get_trajectory(self, expert):
        # Extrapolate trajectory based on max_joint_vel
        max_joint_difference = 0  
        for joint, expert_joint in zip(self.joints, expert):
            if abs(joint - expert_joint) > max_joint_difference:
                max_joint_difference = abs(joint - expert_joint)
       
        # What number of trajectory points do we need to travel the max distance at a set velocity
        self.traj_size = int(np.rint(max_joint_difference / self.args.max_joint_vel / self.timeStep))
        self.expert_traj = []
        for i in range(self.traj_size):
            points = []            
            for j in range(len(self.joints)):
                point = i * ( (expert[j] - self.joints[j]) / self.traj_size ) + self.joints[j]
                points.append(point)
            self.expert_traj.append(points)
        self.traj_i = 0    
