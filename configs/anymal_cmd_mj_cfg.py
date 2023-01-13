from utils.utils import get_attribute_dict

class AnymalCmdMjCfg():
    class env:
        ob_size = 54
        ac_size = 12
    
    class terrain:
        gt_img_dim = (500, 500) 
        gt_mj_dim = (10, 10)
        hm_img_dim = (gt_img_dim[0] // 5, gt_img_dim[1] // 5)
        hm_mj_dim = (gt_mj_dim[0] / (gt_img_dim[0] / hm_img_dim[0]),  
                               gt_mj_dim[1] / (gt_img_dim[1] / hm_img_dim[1])) 
        hf_centre_pos = (0, 0, 0)
        hf_elev = 0.01
        hf_depth = 1

        class grass:
            radius = 0.02
            height = 0.4
            damping = 1
            stiffness = 2
            pos = [0, 0, 0]
            rot = [1, 0, 0, 0]
            num = 200
            segs_per_branch = 4
            spread = [[1.0, 7.0], [-1, 1]]
            z_height = -0.05

        class tree:
            spread = [[1.0, 2.0], [-0.2, 0.2]]
        
        grass_params = get_attribute_dict(grass)
        tree_params = get_attribute_dict(tree)

    class map:
        show_map = False
        show_waypoint = False
        max_vel_to_waypoint = 1
        wp_time_scalar = 1.5

    
    class reward:
        class goal:
            min_goal_len = 100
            mean_goal_tgt = 1.0
            success_len = 5
        
        class done:
            min_z = 0.35
            max_pitch = 0.5
            max_roll = 0.5
    
    class robot:
        torque_act_mult = 20
        pos_act_mult = 0.2
        init_z = 0.7
        init_joints = [-0.2,0.6,-1.0, 0.2,0.6,-1.0, -0.2,-0.6,1.0, 0.2,-0.6,1.0]
        right_swing = [-0.2,0.0,-0.8, 0.2,1.0,-1.0, -0.2,-0.4,1.0, 0.2,-1.0,0.0]
        left_swing = [-0.2,1.0,-1.0, 0.2,0.0,-0.8, -0.2,-1.0,0.0, 0.2,-0.4,1.0]
        motor_names = ['LF_HAA', 'LF_HFE', 'LF_KFE', 'RF_HAA', 'RF_HFE', 'RF_KFE', 'LH_HAA', 'LH_HFE', 'LH_KFE', 'RH_HAA', 'RH_HFE', 'RH_KFE'] 
        
    




        
