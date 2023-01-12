
class AnymalCmdMjCfg():
    class env:
        ob_size = 54
        ac_size = 12
    
    class terrain:
        gt_img_dim = (500, 500)
        gt_mj_dim = (100, 100)
        hm_img_dim = (gt_img_dim // 5, gt_img_dim // 5)
        hm_mj_dim = (gt_mj_dim[0] / (gt_img_dim[0] / hm_img_dim[0]),  
                               gt_mj_dim[1] / (gt_img_dim[1] / hm_img_dim[1])) 


        
