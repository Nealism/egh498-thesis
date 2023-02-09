import numpy as np
import torch
import mujoco
from gym import spaces
from collections import deque
from mpi4py import MPI
comm = MPI.COMM_WORLD
from scipy.spatial.transform import Rotation
import mujoco_viewer
from pyquaternion import Quaternion
import os
from lxml import etree
import math
import time

from .env_base_mj import EnvBaseMJ
from utils.terrain import Hfield, TerrainGen
from utils import img_helpers
from utils.xml_helper import indent_xml
from configs.anymal_cmd_mj_cfg import AnymalCmdMjCfg

class Env(EnvBaseMJ):
    # Timestep for mujoco is set in the .xml, and shows up under self.model.opt.timestep
    # Default is 0.002, changing this might affect the contact model. 
    def __init__(self, PATH=None, args=None, writer=None):

        ### CONFIGS ###

        self.cfg = AnymalCmdMjCfg
        self.env_cfg = self.cfg.env
        self.terr_cfg = self.cfg.terrain
        self.map_cfg = self.cfg.map
        self.rew_cfg = self.cfg.reward
        self.robot_cfg = self.cfg.robot

        self.rank = comm.Get_rank()
        
        self.view_rank = self.env_cfg.view_rank
        self.args = args
        self.render = args.render and self.rank == self.view_rank 
        self.PATH = PATH
        self.writer = writer
        self.master = True 
        self.viewer = None

        ##### LOADING CONFIG VALUES THROUGH CLI ARGS (HPC-ONLY, SEE CFG) #####

        if self.args.rand_dz_mult:
            self.terr_cfg.gt_rand_dz = self.args.rand_dz_mult * self.terr_cfg.gt_max_elev
        self.map_cfg.wp_time_scalar = self.args.wp_time_scalar
        
        self.terr_cfg.init_z = self.terr_cfg.robot_init_z
        if self.args.add_terrain:
            self.terr_cfg.init_z += self.terr_cfg.gt_base_elev
        
        self.terr_cfg.hm_mj_dim = (self.args.hm_size, self.args.hm_size)
        self.terr_cfg.hm_img_dim = (self.terr_cfg.hm_mj_dim[0] * (self.terr_cfg.gt_img_dim[0] // self.terr_cfg.gt_mj_dim[0]), 
                                    self.terr_cfg.hm_mj_dim[1] * (self.terr_cfg.gt_img_dim[1] // self.terr_cfg.gt_mj_dim[1])) 
        ##### ENV PARAMS #####

        self.simStep = self.env_cfg.simStep
        self.timeStep = self.env_cfg.timeStep
        self.Kp = self.env_cfg.Kp
        self.initial_Kp = self.env_cfg.initial_Kp

        self.robot_name = "anymal_c"

        super().__init__(PATH)

        ##### PATHS #####

        self.LLP_PATH = "./resources/cmd_model/model.pt"
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
        
        ##### WAY POINT #####

        self.wp_pos_mj = None # position in env
        self.wp_pos_im = None # position in map image
        self.last_wp_time = None # last time wp was generated
        self.max_vel_to_wp = self.map_cfg.max_vel_to_wp # max vel. expect robot to maintain moving towards wp

        ##### TERRAIN #####

        # set up base xml files for this rank/process (scene, tree, terrain etc.)
        self.set_up_xmls()
        # load mujoco model and data (robot itself, trees, terrains etc.)
        self.first_time = True
        self.load_robot()
        self.first_time = False

        ##### ENV #####

        self.low_lev_pol = torch.load(self.LLP_PATH)
        # self.reward_fn = getattr(self, f'get_reward_{self.args.reward_fn}')
        # self.obs_fn = getattr(self, f'get_hlp_obs_{self.args.obs_fn}')
        self.reward_fn_name = f'get_reward_{self.args.reward_fn}'
        self.obs_fn_name = f'get_hlp_obs_{self.args.obs_fn}'

        self.ob_size = self.env_cfg.ob_sizes[self.args.obs_fn-1]
        self.ac_size = self.env_cfg.ac_size
        self.joints_size = self.env_cfg.joints_size
        self.im_size = [1] + list(self.cfg.terrain.hm_img_dim)

        # Needed if importing as Gym environment
        self.action_space = spaces.Box(-10000*np.ones(self.ac_size), 10000*np.ones(self.ac_size), dtype=np.float32)
        self.observation_space = spaces.Box(-10000*np.ones(self.ob_size), 10000*np.ones(self.ob_size), dtype=np.float32)
        
        self.episodes = -1
        self.success = deque([0.0], maxlen=self.rew_cfg.goal.max_succ_len)
        self.sim_data = []
        self.best_return = 0

        self.steps = 0

        self.reward_names = ["Reward/goal", "Reward/heading"]
        self.reward_dict = {reward:deque(maxlen=100) for reward in self.reward_names} 
        self.ep_reward_dict = {reward:0 for reward in self.reward_names} 

        ##### ROBOT #####

        self.motor_names = self.robot_cfg.motor_names
        # left front, right front, left back, right back
        self.initial_joints = self.robot_cfg.init_joints
        self.right_swing = self.robot_cfg.right_swing
        self.left_swing = self.robot_cfg.left_swing
        self.initial_z = self.terr_cfg.init_z if self.args.add_terrain else self.terr_cfg.robot_init_z

        # States that we want to restore, for resuming training after running a test
        # self.states_to_restore = ["pos", "orn", "joints", "joint_vel", "args", "paused", "ep_success", "cur_success", "steps", "ep_steps", "ob_dict", "step_count", "z_offset", "terrain", "Kp", "max_disturbance", "env_exp"]

    def load_terrains(self):
        """
        Generates all Terrain objects for this environment and adds them to the terrains array.

        NOTE: By default, always load the ground truth
        NOTE: can optionally create other terrains, but note that one ground truth can
              create a lot of terrain variability
        """
        self.terrains = []
        self.terrain_generator = TerrainGen()

        gt_arr = self.terrain_generator.gen_empty(self.terr_cfg.gt_img_dim)
        gt_path = self.get_parent_dir(self.model_path)
        gt_name = f"ground_truth_{str(self.rank)}"
        gt_position = self.terr_cfg.gt_centre_pos
        gt_size = (*self.terr_cfg.gt_mj_dim, self.terr_cfg.gt_max_elev, self.terr_cfg.gt_depth)

        self.ground_truth = Hfield(gt_arr, gt_path, gt_name, gt_position, gt_size) 

        # generate and load ground truth image
        if self.args.add_terrain:
            gt_arr = self.terrain_generator.gen_test(self.terr_cfg.gt_img_dim,
                                                    self.terr_cfg.gt_max_elev,
                                                    self.terr_cfg.gt_base_elev,
                                                    self.terr_cfg.gt_rand_dz,
                                                    self.ground_truth.rob_to_arr_pos((0,0)),
                                                    self.args.undul_patches)
            self.ground_truth.terr_arr = gt_arr
        
        self.ground_truth.load_hm_and_hm_img()

        self.terrains.append(self.ground_truth)

        #generate and load any others below this
        ########################################
    
    def get_image(self):
        """
        Returns an egocentric height map centred at the robot. 
        This takes the form of an NxM sub-section of the terrain array,
        where (N, M) == self.terr_cfg.hm_img_dim
        """
        subsection = self.ground_truth.compute_sub_section(self.pos[0], self.pos[1], *self.terr_cfg.hm_img_dim)
        return np.reshape(subsection, self.im_size)

    def show_map(self):
        """
        Displays a birds-eye map of the ground truth the robot is traversing.
        Also draws a bounding box around the robot's sub-section (image
        the policy is fed)
        """
        img_copy = self.ground_truth.height_map_img.copy()
        box_centre = self.ground_truth.rob_to_img_pos(self.pos) 
        img_helpers.draw_bounding_box(img_copy, box_centre, *self.terr_cfg.hm_img_dim) 
        # way point (green dot)
        img_helpers.draw_dot(img_copy, self.wp_pos_im, color=img_helpers.GREEN) 
        # robot position (red dot)
        img_helpers.draw_dot(img_copy, self.ground_truth.rob_to_img_pos(self.pos[:2]), color=img_helpers.RED)
        # img_helpers.draw_arrow(img_copy, self.ground_truth.rob_to_img_pos(self.pos[:2]), self.yaw, color=img_helpers.RED)
        # img_helpers.draw_arrow(img_copy, self.ground_truth.rob_to_img_pos(self.pos[:2]), self.target_angle, color=img_helpers.WHITE)
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
    
    def gen_patch_positions(self, num, x_rad, y_rad):
        """
        Generate an array of grass patch positions for the mj environment
        """
        dim = self.terr_cfg.gt_mj_dim
        border = 2
        xl, xh = -dim[0] + border, dim[0] - border
        yl, yh = -dim[1] + border, dim[1] - border
        patches = []
        for _ in range(num):
            pos = (np.random.uniform(xl, xh), np.random.uniform(yl, yh), self.terr_cfg.gt_base_elev)
            spread = [[pos[0] - x_rad, pos[0] + x_rad], [pos[1] - y_rad, pos[1] + y_rad], pos[2]]
            patches.append(spread)
        return patches
    
    def add_grass_heights(self, patches):
        """
        Add grass heights to the height map array
        """
        for (xl,xh), (yl,yh), _ in patches:
            (new_xl, new_yl), (new_xh, new_yh) = self.ground_truth.rob_to_arr_pos((xl, yl)), self.ground_truth.rob_to_arr_pos((xh, yh))
            self.ground_truth.terr_arr[new_yl:new_yh, new_xl:new_xh] = 1.5
            # reload opencv image based on terrain change
        self.ground_truth.load_hm_and_hm_img()
            
    def load_robot(self):
        # load in terrains
        self.load_terrains()
        # load in grass/trees
        patches = None
        if not self.args.replay and self.args.tree_type:
            if self.args.tree_type == "grass":
                patches = self.gen_patch_positions(self.terr_cfg.num_grass_patches, 0.75, 0.75)
                self.gen_grass_patches(patches, **self.terr_cfg.grass_params)
                # self.generate_tree(**self.terr_cfg.grass_params)
            elif self.args.tree_type == "tree":
                self.generate_tree(**self.terr_cfg.tree_params)

        if not self.args.replay and self.args.add_terrain:
            terrain_path = self.get_parent_dir(self.model_path) + f"terrain_{str(self.rank)}.xml"
            if self.first_time:
                self.populate_terrain_xml(terrain_path)
            else:
                self.reconfig_terrain_xml(terrain_path, self.ground_truth)
        
        self.model = mujoco.MjModel.from_xml_path(self.model_path)
        self.data = mujoco.MjData(self.model)

        # where we load the hfield into mj
        # NOTE: this is much faster than converting the array into a PNG
        #       and loading it
        if self.args.add_terrain:
            self.model.hfield_data = self.ground_truth.terr_arr.flatten()
        
        # only add grass heights to our copy of the terrain array (don't want it loaded into mj)
        if patches:
            self.add_grass_heights(patches)

        # Mujoco_viewer doesn't work on the hpc, shouldn't render there anyway
        if self.viewer:
            self.viewer.close()
        if not self.args.training_on_hpc:
            if self.render:
                # new viewer every episode s.t. correct env appears every time
                self.viewer = mujoco_viewer.MujocoViewer(self.model, self.data)

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
        
        if model_path is not None:
            self.model_path = model_path 

        # must reset mj model and data if loading new trees/grass/terrain every episode
        if self.args.tree_type or self.args.add_terrain or model_path is not None:
            self.load_robot()

        mujoco.mj_resetData(self.model, self.data)

        if restore_state is not None:
            self.set_position(pos=restore_state[0], orn=restore_state[1], joints=restore_state[2])
        else:
            self.orn = [0,0,0,1]
            self.pos = [0,0,self.initial_z]
            self.set_position(pos=self.pos, orn=self.orn, joints=self.initial_joints)

        self.steps = 0
        self.episodes += 1

        # Step the simulation once to get the initial state
        mujoco.mj_forward(self.model, self.data)

        # reset way point 
        self.gen_waypoint()

        self.get_observation()

        if self.args.cmd_ranges:
            self.env_cfg.cmd_ranges = eval(str(self.args.cmd_ranges))
        self.command_ranges = np.array(self.env_cfg.cmd_ranges)
        self.commands = list(np.random.uniform(-self.command_ranges, self.command_ranges))
        self.time_at_speed = 0
        self.goal = []

        self.prev_actions = self.joints
        hlp_obs_vec = getattr(self, self.obs_fn_name)()
        return hlp_obs_vec 

    def step(self, cmds=None, replay_state=None):
        if self.rank == self.view_rank and self.args.show_map and not self.args.training_on_hpc:
            self.show_map()

        if not self.args.one_wp_per_ep and self.can_gen_waypoint():
            self.gen_waypoint()

        # # ========================================================
        # # This could be used as an expert for curriculum learning:
        # # ========================================================
        # cmds = [0,0,0]
        # if abs(self.heading_error) < 0.5:
        #     cmds[0] = self.dist_to_wp
        # cmds[2] = self.heading_error

        if cmds is None:
            cmds = [0,0,0]

        self.commands = [np.clip(cmd*self.args.cmd_scaling*limit, -limit, limit) for cmd, limit in zip(cmds, self.robot_cfg.cmd_limits)]

        # Run LLP faster than HLP
        for _ in range(int(np.rint(self.env_cfg.timeStepHLP/self.env_cfg.timeStepLLP))):    
            self.get_observation()
            actions = self.low_lev_pol.step(torch.tensor(np.array(self.get_llp_obs()).astype(np.float32)), stochastic=False)[0]
            self.actions = list(np.array(self.initial_joints) + np.array(actions))

            # This might do something weird with mujoco contacts, and other things in the sim.
            for _ in range(int(np.rint(self.env_cfg.timeStepLLP/self.simStep))):                            
                self.data.ctrl[:self.joints_size] = self.action_multiplier*np.array(self.actions)

                mujoco.mj_step(self.model, self.data)
        
            if self.render:
                # time.sleep(0.1)
                self.viewer.render()

        self.get_observation()
        self.save_sim_state()

        reward, done = getattr(self, self.reward_fn_name)()
        hlp_obs_vec = getattr(self, self.obs_fn_name)()

        self.prev_actions = self.actions
        self.total_return += reward
        self.steps += 1
        
        return np.array(hlp_obs_vec), reward, done, None
    
    def get_hlp_obs_1(self):
        """
        Returns the obs. vector that is fed to the high-level policy (52-d)
        -----        
        Default AND wp dist 
        """
        return (self.imu + self.commands + self.joints + list(self.pos[:2] - np.array(self.wp_pos_mj)) +
                self.joint_vel + self.joint_force)

    def get_hlp_obs_2(self):
        """
        Returns the obs. vector that is fed to the high-level policy (49-d)
        -----
        Default WITHOUT commands
        """
        return (self.imu + self.commands + self.wp_pos_robot + [self.dist_to_wp] + self.joints +
                self.joint_vel + self.joint_force)

    def get_hlp_obs_3(self):
        """
        Returns the obs. vector that is fed to the high-level policy (52-d)
        -----        
        Default AND heading error AND wp dist
        """
        return (self.imu + self.commands + self.wp_pos_robot + [self.heading_error, self.dist_to_wp] + self.joints +
                self.joint_vel + self.joint_force)

    def get_hlp_obs_4(self):
        """
        Returns the obs. vector that is fed to the high-level policy (53-d)
        -----        
        Heading error AND wp dist
        """
        return [self.heading_error, self.dist_to_wp] 

    def get_llp_obs(self):
        """
        Returns the obs. vector that is fed to the low-level policy (54-d)
        """
        return (self.imu + self.commands + self.joints + 
                self.joint_vel + self.joint_force + 
                [contact for contact in self.contacts.values()])
    
    def get_reward(self):
        done = False
        if (self.pos[2] < self.rew_cfg.done.min_z or 
           abs(self.pitch) > self.rew_cfg.done.max_pitch or 
           abs(self.roll) > self.rew_cfg.done.max_roll):
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
        self.ep_reward_dict["Reward/joints"] += joints
        self.ep_reward_dict["Reward/orn"] += orn
        self.ep_reward_dict["Reward/contacts"] += contacts
        return reward, done
    
    def get_reward_1(self):
        # old wp dist
        done = self.is_done()

        diff = np.sum(np.abs(self.pos[:2] - np.array(self.wp_pos_mj)))
        goal = np.exp(-0.05 * diff**2)

        reward = goal

        self.ep_reward_dict["Reward/goal"] += reward
        return reward, done

    def get_reward_2(self):
        # new wp dist
        done = self.is_done()
        
        goal = np.exp(-0.05*self.dist_to_wp**2)
        
        reward = 1.0 * goal

        self.ep_reward_dict["Reward/goal"] += goal
        return reward, done

    def get_reward_3(self):
        # new wp dist
        done = self.is_done()
        
        # Want to make sure we are facing the right way before moving towards the waypoint
        if abs(self.heading_error) < 0.5:
            goal = np.exp(-0.05*self.dist_to_wp**2)
        else:
            goal = 0
        
        heading = np.exp(-5*self.heading_error**2)

        reward = 1.0 * goal + 0.5 * heading

        self.ep_reward_dict["Reward/goal"] += goal
        self.ep_reward_dict["Reward/heading"] += heading
        return reward, done

    def is_done(self):
        return (self.pos[2] < self.rew_cfg.done.min_z or 
            abs(self.pitch) > self.rew_cfg.done.max_pitch or 
            abs(self.roll) > self.rew_cfg.done.max_roll)

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
        self.joint_force = list(self.data.actuator_force[:self.joints_size])

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

        self.wp_pos_robot = self.world_to_robot(self.yaw, self.pos, self.wp_pos_mj)
        self.heading_error, self.target_angle = self.calc_angle_error(self.wp_pos_mj, self.pos, self.yaw)
        self.dist_to_wp = math.sqrt(self.wp_pos_robot[0]**2 + self.wp_pos_robot[1]**2)

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

    def world_to_robot(self, robot_yaw, robot, world):
        x,y = world[0] - robot[0], world[1] - robot[1]
        rot_mat = np.array([[np.cos(robot_yaw), np.sin(robot_yaw)],
                             [-np.sin(robot_yaw), np.cos(robot_yaw)]])
        return list(np.dot(rot_mat, np.array([x, y])))

    def calc_angle_error(self, world, robot, angle):
        target_angle = np.arctan2(world[1] - robot[1], world[0] - robot[0])
        if ( target_angle < 0 and angle > 0 ):
            angle_error = ( 2*np.pi + target_angle ) - angle
        elif ( target_angle > 0 and angle < 0 ):
            angle_error = target_angle - ( 2*np.pi + angle )
        else:
            angle_error = target_angle - angle
        return angle_error, target_angle

    # def yaw_diff(self):
    #     """
    #     Returns the absolute difference in angle of the robot's yaw and the way point (from robot's pos)
    #     """
    #     wp_ang = math.atan2((self.wp_pos_mj[1] - self.pos[1]), (self.wp_pos_mj[0] - self.pos[0]))
    #     diff = abs(self.yaw - wp_ang)
    #     if diff > (2 * math.pi):
    #         diff = diff - (2 * math.pi)
    #     if diff > math.pi:
    #         return 2*math.pi - diff
    #     else:
    #         return diff