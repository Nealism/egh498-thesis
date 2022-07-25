import numpy as np
import cv2
from mpi4py import MPI

class OccupancyMap():
    def __init__(self, box_info, im_size=[120,120,1], grid_size=0.1, initial_yaw=0, robot_pos=[0,0,0], args=None, rank=0):
        self.box_info = box_info
        self.im_size = im_size
        self.grid_size = grid_size
        self.initial_yaw = initial_yaw
        self.initial_robot_pos = robot_pos
        self.args = args
        self.rank = rank
        self.get_world_map()

    # def get_world_map(self, box_info=None):
    #     gz = False
    #     if gz:
    #         self.min_x = np.min(np.array(box_info[1])[:,0] - np.array(box_info[2])[:,0]/2)
    #         self.min_y = np.min(np.array(box_info[1])[:,1] - np.array(box_info[2])[:,1]/2)
    #         self.max_x = np.max(np.array(box_info[1])[:,0] + np.array(box_info[2])[:,0]/2)
    #         self.max_y = np.max(np.array(box_info[1])[:,1] + np.array(box_info[2])[:,1]/2)
    #     else:
    #         self.min_x = np.min(np.array(box_info[1])[:,0] - np.array(box_info[2])[:,0])
    #         self.min_y = np.min(np.array(box_info[1])[:,1] - np.array(box_info[2])[:,1])
    #         self.max_x = np.max(np.array(box_info[1])[:,0] + np.array(box_info[2])[:,0])
    #         self.max_y = np.max(np.array(box_info[1])[:,1] + np.array(box_info[2])[:,1])
    #     world_shape = [int((self.max_x - self.min_x + 2)/self.grid_size), int((self.max_y - self.min_y + 2)/self.grid_size)]

    #     om = np.ones([world_shape[0], world_shape[1]]).astype(np.float32)*-1
    #     if box_info is not None:
    #         positions = box_info[1]
    #         sizes = box_info[2]
    #         for pos, size in zip(positions, sizes):
    #             x, y, z = pos[0]/self.grid_size, pos[1]/self.grid_size, pos[2]
    #             if gz:
    #                 x_size, y_size, z_size = (size[0]/2)/self.grid_size, (size[1]/2)/self.grid_size, size[2]/2
    #             else:
    #                 x_size, y_size, z_size = (size[0])/self.grid_size, (size[1])/self.grid_size, size[2]
                
    #             ij = np.array([[i,j,1] for i in range(int(0-x_size), int(0+x_size)) for j in range(int(0-y_size), int(0+y_size))])

    #             om_pts = self.transform_rot_and_add(1*pos[5], [x+(-self.min_x+1)/self.grid_size, y+(-self.min_y+1)/self.grid_size], ij)
    #             for pt in om_pts:
    #                 try:
    #                     # Not sure why this doesn't work for larger z heights? Should be box z pos + box z size (half extent). It's because I wasn't copying a list properly..
    #                     if om[pt[0], pt[1]] < (z * 2):
    #                         om[pt[0], pt[1]] = (z * 2)
    #                 except Exception as e:
    #                     print(e)
    #                     print(pt)
    #     self.dx_forward, self.dx_back, self.dy = 36, 24, 20        
    #     self.ij = np.array([[i,j,1] for i in range(-self.dx_back, self.dx_forward) for j in range(-self.dy, self.dy)])
    #     self.om_ij = np.array([[i,j] for i in range(0, self.dx_back + self.dx_forward) for j in range(0, self.dy + self.dy)])
    #     self.om = np.ones([self.dx_back+self.dx_forward, 2*self.dy], dtype=np.float32)*-1
    #     return om

    def get_world_map(self):
        gz = True
        self.boxes = np.ones([1,3])
        # self.z_offset = None
        self.z_offset = 0
        if self.box_info is not None:
            for pos, size in zip(self.box_info[1], self.box_info[2]):
                x, y, z = pos[0]/self.grid_size, pos[1]/self.grid_size, pos[2]
                if gz:
                    x_size, y_size, z_size = (size[0]/2)/self.grid_size, (size[1]/2)/self.grid_size, size[2]/2
                else:
                    x_size, y_size, z_size = (size[0])/self.grid_size, (size[1])/self.grid_size, size[2]
                ij = np.array([[i,j, z + z_size] for i in range(int(0-x_size), int(0+x_size)) for j in range(int(0-y_size), int(0+y_size))])
                if self.z_offset == None:
                    self.z_offset = z + z_size
                # print(x,y, len(ij))
                om_pts = self.transform_rot3d(pos[5], [x, y, 0], ij)
                om_pts = self.transform_rot3d(self.initial_yaw, [int(self.initial_robot_pos[0]/self.grid_size), int(self.initial_robot_pos[1]/self.grid_size), 0], om_pts)
                self.boxes = np.concatenate([self.boxes, om_pts], axis=0)

        # print(ij); exit()
        self.boxes = self.boxes[1:,:]

        self.min_x, self.min_y, _ = np.min(self.boxes, axis=0)
        self.max_x, self.max_y, _ = np.max(self.boxes, axis=0)
        self.map_extents = [self.min_x*self.grid_size, self.max_x*self.grid_size, self.min_y*self.grid_size, self.max_y*self.grid_size]
        self.min_x = int(self.min_x - (self.im_size[0]/2))
        self.min_y = int(self.min_y - (self.im_size[1]/2))
        self.max_x = int(self.max_x + (self.im_size[0]/2))
        self.max_y = int(self.max_y + (self.im_size[1]/2))
        self.world_offset = np.array([self.min_x, self.min_y, 0])
        self.world = np.zeros([self.max_x - self.min_x, self.max_y - self.min_y],dtype=np.float32)
        # print("display offset", self.world_offset)
        self.boxes = self.boxes - self.world_offset
        for x, y, z in zip(self.boxes[:,0],self.boxes[:,1], self.boxes[:,2]):
            self.world[int(x),int(y)] = z - self.z_offset > 0.2
        #     print(self.world[int(x),int(y)])
        # print(self.world)
        print("DON'T FORGET TO FIX THE OCC MAP ROUNDING ISSUE")
        # cv2.imshow("frame", self.world)
        # cv2.waitKey(0); exit()
       
        self.om_ij = np.array([[i,j] for i in range(0, self.im_size[0]) for j in range(0, self.im_size[1])])


    def get_om(self, robot_pos, robot_yaw=None):
        ij = np.array([[i,j, 0] for i in range(int(0-self.im_size[0]/2), int(0+self.im_size[0]/2)) for j in range(int(0-self.im_size[1]/2), int(0+self.im_size[1]/2))])
        x_pos, y_pos = robot_pos[0]/self.grid_size , robot_pos[1]/self.grid_size
        if robot_yaw == None:
            robot_yaw = self.initial_yaw
        else:
            # robot_yaw = (robot_yaw )
            # robot_yaw = -robot_yaw
            robot_yaw = robot_yaw
        
        om_pts = self.transform_rot3d(robot_yaw, [int(x_pos), int(y_pos), 0], ij)
        # Not sure why this was here?
        # om_pts = self.transform_rot3d(self.initial_yaw, [int(self.initial_robot_pos[0]/self.grid_size), int(self.initial_robot_pos[1]/self.grid_size), 0], om_pts)
        om_pts = om_pts - self.world_offset
        self.om = np.ones(self.im_size)
        om_pts[:,0] = np.clip(om_pts[:,0], 0, self.world.shape[0]-1)
        om_pts[:,1] = np.clip(om_pts[:,1], 0, self.world.shape[1]-1)
        self.om[self.om_ij[:,0],self.om_ij[:,1], 0] = self.world[om_pts[:,0],om_pts[:,1]]
      
        # if pixel is white: with random probability, add square of random white/black
        white_idx = np.where(self.om == 1)
        noise_shape = 2
        for x,y in zip(white_idx[0], white_idx[1]):
            if x > noise_shape and y > noise_shape and x < self.im_size[0] - noise_shape and y < self.im_size[0] -noise_shape:
                if np.random.random() < 0.01:
                    self.om[x-noise_shape:x+noise_shape,y-noise_shape:y+noise_shape,0] = np.random.randint(0,2, size=[noise_shape*2,noise_shape*2])
        
        # im = cv2.resize(self.om,dsize=(int(self.om.shape[1] * 6), int(self.om.shape[0] * 6)))
        # cv2.imshow("frame", im)
        # cv2.waitKey(1)


        if self.args.display_im:
            # local = cv2.resize(self.om, ( self.om.shape[1] * 6, self.om.shape[0] * 6 ))



            cv2.imshow("frame", self.om)
            cv2.waitKey(0); exit()

            # x_min = int(- self.im_size[0]/2)
            # x_max = int(+ self.im_size[0]/2)
            # y_min = int(- self.im_size[1]/2)
            # y_max = int(+ self.im_size[1]/2)
            # x1, y1, x2, y2, x3, y3, x4, y4 = x_max, y_max, x_min, y_max, x_min, y_min, x_max, y_min
            # rect_pts = np.array([[x1,y1,0],[x2,y2,0],[x3,y3,0],[x4,y4,0]])
            # rect_pts = self.transform_rot3d(robot_yaw, [int(x_pos), int(y_pos), 0], rect_pts)
            # rect_pts = self.transform_rot3d(self.initial_yaw, [int(self.initial_robot_pos[0]/self.grid_size), int(self.initial_robot_pos[1]/self.grid_size), 0], rect_pts)
            # rect_pts = (rect_pts - self.world_offset)[:,:2]
            # rect_pts = np.array([[rect_pts[0][1], rect_pts[0][0]],[rect_pts[1][1], rect_pts[1][0]],[rect_pts[2][1], rect_pts[2][0]],[rect_pts[3][1], rect_pts[3][0]]])
            # wm_col = cv2.cvtColor(self.world,cv2.COLOR_GRAY2RGB)
            # cv2.polylines(wm_col, [rect_pts], True, (0,0,255), 2)
            # if self.rank == 0:
            #     cv2.imshow('wm_col' + str(self.rank), wm_col)
            #     cv2.waitKey(1)
            
            # local = np.ones_like(wm_col)
            # x1,x2,y1,y2 = int(local.shape[0]/2-self.om.shape[0]/2), int(local.shape[0]/2+self.om.shape[0]/2), int(local.shape[1]/2-self.om.shape[1]/2), int(local.shape[1]/2+self.om.shape[1]/2)
            # local[x1:x2, y1:y2] = self.om
            # cv2.imshow('im_col' + str(self.rank), local)
            # cv2.waitKey(1)
            
        return self.om
    
    def display_om(self, om, robot_pos, robot_yaw, initial_robot_pos, initial_yaw, world=None, rank=0):
        all_pos = MPI.COMM_WORLD.allgather(robot_pos)
        all_yaw = MPI.COMM_WORLD.allgather(robot_yaw)
        all_initial_pos = MPI.COMM_WORLD.allgather(initial_robot_pos)
        all_initial_yaw = MPI.COMM_WORLD.allgather(initial_yaw)
        if rank == 0:
            x_min = int(- self.im_size[0]/2)
            x_max = int(+ self.im_size[0]/2)
            y_min = int(- self.im_size[1]/2)
            y_max = int(+ self.im_size[1]/2)
            x1, y1, x2, y2, x3, y3, x4, y4 = x_max, y_max, x_min, y_max, x_min, y_min, x_max, y_min
            pts = np.array([[x1,y1,0],[x2,y2,0],[x3,y3,0],[x4,y4,0]])
            wm_col = cv2.cvtColor(world,cv2.COLOR_GRAY2RGB)
            colours = [(0,0,255), (0,255,125), (255,0,0), (0,255,0), (125,0,255),(0,0,255), (0,255,125), (255,0,0), (0,255,0), (125,0,255),(0,0,255), (0,255,125), (255,0,0), (0,255,0), (125,0,255)]

            # print(all_pos, all_yaw, all_initial_pos, all_initial_yaw)
            for num, (pos, yaw, initial_pos, initial_yaw) in enumerate(zip(all_pos, all_yaw, all_initial_pos, all_initial_yaw)):
                pos, yaw, initial_pos, initial_yaw = all_pos[num], all_yaw[num], all_initial_pos[num], all_initial_yaw[num]    
                x_pos, y_pos = pos[0]/self.grid_size , pos[1]/self.grid_size
                rect_pts = self.transform_rot3d(yaw, [int(x_pos), int(y_pos), 0], pts)
                # ? Why was I doing this?
                # rect_pts = self.transform_rot3d(initial_yaw, [int(initial_pos[0]/self.grid_size), int(initial_pos[1]/self.grid_size), 0], rect_pts)
                rect_pts = (rect_pts - self.world_offset)[:,:2]
                rect_pts = np.array([[rect_pts[0][1], rect_pts[0][0]],[rect_pts[1][1], rect_pts[1][0]],[rect_pts[2][1], rect_pts[2][0]],[rect_pts[3][1], rect_pts[3][0]]])
                colours = [(0,0,255), (0,255,125), (255,0,0), (0,255,0), (125,0,255),(0,0,255), (0,255,125), (255,0,0), (0,255,0), (125,0,255),(0,0,255), (0,255,125), (255,0,0), (0,255,0), (125,0,255)]
                cv2.polylines(wm_col, [rect_pts], True, colours[num], 2)

            local = np.ones([wm_col.shape[0], om.shape[1], wm_col.shape[2]])
            x1,x2,y1,y2 = int(local.shape[0]/2-om.shape[0]/2), int(local.shape[0]/2+om.shape[0]/2), int(local.shape[1]/2-om.shape[1]/2), int(local.shape[1]/2+om.shape[1]/2)
            local[x1:x2, y1:y2] = om
            cv2.imshow('wm_col', np.hstack([wm_col, local]))
            cv2.waitKey(1)
        # else:
            
        #     cv2.imshow('local_om_' + str(rank), om)
        #     cv2.waitKey(1)

    def transform_rot3d(self, yaw, pos, points):
        rot_mat = np.array(
                [[np.cos(yaw), -np.sin(yaw), 0],
                [np.sin(yaw), np.cos(yaw), 0],
                [0, 0, 1]])
        return np.add(np.dot(rot_mat,points.T).T, pos).astype(np.int32)

    def transform_rot2d(self, yaw, pos, points):
        rot_mat = np.array(
                [[np.cos(yaw), -np.sin(yaw)],
                [np.sin(yaw), np.cos(yaw)]])
        return np.add(np.dot(rot_mat,points.T).T, pos).astype(np.int32)

def to_int(input):
    return np.rint(input).astype(np.int32)

if __name__=="__main__":
    import time
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--display_im', default=True, action='store_false')
    # parser.add_argument('--display_im', default=False, action='store_true')
    args = parser.parse_args()
    dt = 0.1
    num_random_boxes = 3
    box_id = [0] * num_random_boxes
    # positions = [[np.random.uniform(-5, 5), np.random.uniform(-5, 5), 0, 0, 0, np.random.uniform(-1.5, 1.5)]
    #              for _ in range(num_random_boxes)]
    # sizes = [[np.random.uniform(0.2, 2),np.random.uniform(0.2, 2), 1] 
    #         for _ in range(num_random_boxes)]
    positions = [[i, i*2, 0, 0, 0, i]
                 for i in range(num_random_boxes)]
    sizes = [[1, 1.5, 1] 
            for _ in range(num_random_boxes)]
    box_info = [box_id, positions, sizes]
    print(box_info)
    om = OccupancyMap(box_info, args=args)
    speed = np.random.uniform(-1,1, size=2)
    yaw_speed = np.random.uniform(-1,1, size=1)
    pos = [0,0]
    yaw = 0

    while True:
        print("running loop")
        current_om = om.get_om(pos, yaw)
        t1 = time.time()
        while t1 - time.time() < dt:
            time.sleep(0.000001)
        pos += speed * dt
        yaw += yaw_speed * dt
        print("new pos and yaw", pos, yaw)