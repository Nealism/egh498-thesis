from utils.utils import get_attribute_dict

class AnymalCmdMjCfg():
    class env:
        ob_size = 52
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
        gt_img_dim = (250, 250) # image dimensions - (x, y) in pixels
        gt_mj_dim = (15, 15) # mj hfield dimensions - (x_rad, y_rad) in metres

        gt_centre_pos = (0, 0, 0) # position in mj gt centred at
        gt_max_elev = 2 # max elevation of ground truth
        gt_base_elev = 0.1 * gt_max_elev  # base elevation of ground truth's surface 
        # gt_rand_dz = 0.025 * gt_max_elev # max height of the random undulation ABOVE the base (dz)
        gt_depth = 1 # -ve z component of gt (how far gt goes into floor)

        init_z = 0.7 + gt_base_elev # initial elevation of the robot (height=0.7 normally)

        # height map dimensions
        hm_img_dim = (gt_img_dim[0] // 5, gt_img_dim[1] // 5) # image sub-section
        hm_mj_dim = (gt_mj_dim[0] / (gt_img_dim[0] / hm_img_dim[0]), 
                               gt_mj_dim[1] / (gt_img_dim[1] / hm_img_dim[1]))  # mj hfield sub-section

        class grass:
            radius = 0.02
            height = 0.4
            damping = 1
            stiffness = 1.5
            pos = [0, 0, 0.5]
            rot = [1, 0, 0, 0]
            num = 100
            segs_per_branch = 4
            spread = [[1.0, 7.0], [-1, 1]]
            z_height = -0.05

        class tree:
            spread = [[1.0, 2.0], [-0.2, 0.2]]
        
        # dict of all class attributes eg: {'radius': 0.02, ... }
        grass_params = get_attribute_dict(grass)
        tree_params = get_attribute_dict(tree)

    class map:
        # represents a 'best case' vel. of the bot towards the waypoint
        max_vel_to_wp = 0.8
        # multiply expected time to wp by some scalar to give it some leeway
        wp_time_scalar = 1.5

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
        init_joints = [-0.2,0.6,-1.0, 0.2,0.6,-1.0, -0.2,-0.6,1.0, 0.2,-0.6,1.0]
        right_swing = [-0.2,0.0,-0.8, 0.2,1.0,-1.0, -0.2,-0.4,1.0, 0.2,-1.0,0.0]
        left_swing = [-0.2,1.0,-1.0, 0.2,0.0,-0.8, -0.2,-1.0,0.0, 0.2,-0.4,1.0]
        motor_names = ['LF_HAA', 'LF_HFE', 'LF_KFE', 'RF_HAA', 'RF_HFE', 'RF_KFE', 'LH_HAA', 'LH_HFE', 'LH_KFE', 'RH_HAA', 'RH_HFE', 'RH_KFE'] 
        
    




        
