from utils.utils import get_attribute_dict

"""
NOTE NOTE NOTE

-some config values are set to None
-this is where we instead pass a CLI arg for the given value
-if NOT training on hpc:
     -dw about this, just override the None's with your own values
-if ARE training on hpc: 
    -if want to load multiple jobs at once, and 
     want to change certain values between jobs, have to do through command line args
    -jobs take time to start, so changes on a 'later' queued job may actually be adopted by
    'earlier' queued one (if you use config files). CLI args fix this
"""

class AnymalCmdMjCfg():
    class env:
        timeStepLLP = 1/100 # LLP time step
        timeStepHLP = 1/20  # HLP runs slower than LLP
        ob_sizes = [52, 53, 54] # ob_sizes[i] == len of ith obs vector (ie: output len of get_hlp_obs_{i+1})
        ac_size = 3 # (Vx, Vy, Vz) - output of hlp
        joints_size = 12  # robot joint positions - output of llp
        cmd_ranges = [1, 1, 1.5]
        simStep = 1/500
        timeStep = 1/100
        Kp = 400
        initial_Kp = Kp
        view_rank = 0
    
    class terrain:
        #### GROUND TRUTH CONFIG ####
        gt_img_dim = (100, 100) # image dimensions - (x, y) in pixels
        gt_mj_dim = (20, 20) # mj hfield dimensions - (x_rad, y_rad) in metres

        gt_centre_pos = (0, 0, 0) # position in mj gt centred at
        gt_max_elev = 2 # max elevation of ground truth
        gt_base_elev = 0.4 * gt_max_elev  # base elevation of ground truth's surface 
        gt_depth = 1 # -ve z component of gt (how far gt goes into floor)

        # proportion of max elev taken up by random undulation
        gt_rand_dz_mult = None
        # max height of the random undulation ABOVE the gt's base height (max random dz)
        gt_rand_dz = None
        
        # height of robot
        robot_init_z = 0.7
        # height robot is loaded at
        init_z = robot_init_z

        # height map dimensions
        hm_mj_dim = None
        hm_img_dim = None

        num_grass_patches = 5

        class grass:
            radius = 0.02
            height = 0.4
            damping = 1
            stiffness = 1.5
            rot = [1, 0, 0, 0]
            # spread = [[1.0, 7.0], [-1, 1]]
            # pos = (0, 0, 0.8)
            num = 30
            segs_per_branch = 4

        class tree:
            spread = [[1.0, 2.0], [-0.2, 0.2]]
        
        # dict of all class attributes eg: {'radius': 0.02, ... }
        grass_params = get_attribute_dict(grass)
        tree_params = get_attribute_dict(tree)

    class map:
        # represents a 'best case' vel. of the bot towards the waypoint
        max_vel_to_wp = 1.5
        # multiply expected time to wp by some scalar to give it some leeway
        wp_time_scalar = None

    class reward:
        class goal:
            min_goal_len = 100
            mean_goal_tgt = 1.0
            max_succ_len = 5
        
        class done:
            min_z = 0.35
            max_pitch = 0.5
            max_roll = 0.5
    
    class robot:
        torque_act_mult = 20
        pos_act_mult = 0.2
        cmd_limits = [1.0, 1.0, 1.5]
        init_joints = [-0.2,0.6,-1.0, 0.2,0.6,-1.0, -0.2,-0.6,1.0, 0.2,-0.6,1.0]
        right_swing = [-0.2,0.0,-0.8, 0.2,1.0,-1.0, -0.2,-0.4,1.0, 0.2,-1.0,0.0]
        left_swing = [-0.2,1.0,-1.0, 0.2,0.0,-0.8, -0.2,-1.0,0.0, 0.2,-0.4,1.0]
        motor_names = ['LF_HAA', 'LF_HFE', 'LF_KFE', 'RF_HAA', 'RF_HFE', 'RF_KFE', 'LH_HAA', 'LH_HFE', 'LH_KFE', 'RH_HAA', 'RH_HFE', 'RH_KFE'] 
        
    