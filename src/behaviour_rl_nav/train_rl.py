'''
Listen to command list, if we get a door:
- Consume hm and state
- send message to behaviour interface (Joy?)

'''
from datetime import datetime
import tensorboardX
from mpi4py import MPI
comm = MPI.COMM_WORLD

from models.ppo_perception import ppo
from utils.mpi_tools import mpi_fork
from utils.run_utils import setup_logger_kwargs
from assets.env_gz import Env
import default_arguments

# import os, inspect
# currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
import numpy as np
# import time
# from collections import deque
import rospy
# # from multiagent_msgs.msg import RobotStatus, Command, CommandList
# from nav_msgs.msg import OccupancyGrid
# # from rasg_nav_msgs.msg import DensePointCloud2, TopometricWaypointActionGoal
# from geometry_msgs.msg import Twist, TwistStamped, Vector3, Quaternion, Pose
# from std_msgs.msg import Float64, Header, String
# from visualization_msgs.msg import Marker, MarkerArray
# import cv2
# import tensorflow as tf
# import argparse
# from scipy.spatial.transform import Rotation
# from geometry_msgs.msg import Pose, Point, Vector3, Quaternion
# from std_msgs.msg import String, ColorRGBA
# import default_arguments
# from utils.mpi_tools import mpi_fork
# from models.ppo_perception import ppo
# from utils.run_utils import setup_logger_kwargs


class TitanRL():

    dt = 1/10
    im_size = [80,80,1]
    # im_size = [120,120,1]
    def __init__(self, robot_name, pol, args):
        self.robot_name = robot_name
        self.pol = pol
        self.args = args
        self.run_policy = False
        self.initialise_subscribers()
        self.initialise_publishers()
        self.ij = np.array([[i,j] for i in range(-int(self.im_size[0]/2), int(self.im_size[0]/2)) for j in range(-int(self.im_size[1]/2), int(self.im_size[1]/2))])
        self.pos_cb = [0,0,0]
        self.orn_cb = [0,0,0,1]
        self.twist_ang_cb = [0,0,0]
        self.twist_lin_cb = [0,0,0]
        self.prev_pos = [0,0,0]
        self.prev_rot = [0,0,0]
        self.hm_cb = np.zeros([120,120,1])
        if self.args.display_hm:
            self.hm_cb2 = np.zeros([120,120,1])
                
    def initialise_publishers(self):
        self.door_markers_pub = rospy.Publisher('/' + self.robot_name + '/door_markers', MarkerArray, queue_size=1)        
        self.cmd_vel_publisher = rospy.Publisher('/' + self.robot_name + '/behaviour_door/rl_cmd_vel_stamped', TwistStamped, queue_size=1)

    def initialise_subscribers(self):
        rospy.Subscriber('/' + self.robot_name + '/command_list', CommandList, self.commandCallback)
        rospy.Subscriber('/' + self.robot_name + '/agent_interface_status', RobotStatus, self.statusCallback)
        # rospy.Subscriber('/' + self.robot_name + '/imu/data', Imu, self.imuCallback)
        # if self.args.costmap:
        #     rospy.Subscriber('/' + self.robot_name + '/heightmap_to_costmap/costmap', DensePointCloud2, self.hmCallback)
        # else:
        rospy.Subscriber('/' + self.robot_name + '/heightmap_to_costmap/occupancy_grid', OccupancyGrid, self.hmCallback)

    def run(self):
        markers = True
        if markers:
            self.doors = MarkerArray()
        
        while self.run_policy:
            self.get_observation()
            actions, _, _, _ = self.pol.step(self.ob, self.im)
            self.aux = self.pol.get_aux(self.ob, self.im)
            self.publish_actions(actions)
            self.t1 = time.time()
            while (time.time() - self.t1 < self.dt):
                time.sleep(0.00001)
            if markers:
                self.add_markers()
                self.door_markers_pub.publish(self.doors)
            if rospy.is_shutdown():
                break
          
        self.doors = MarkerArray()
        self.add_markers(delete=True)
        self.door_markers_pub.publish(self.doors)
          

    def get_observation(self):
        self.pos = self.pos_cb
        self.orn = self.orn_cb

        rot = Rotation.from_quat([self.orn[0], self.orn[1], self.orn[2], self.orn[3]])
        self.roll, self.pitch, self.yaw = rot.as_euler('xyz', degrees=False)
        
        # Finite differences for velocity (unsure if we have access to this through the imu?)
        self.body_vxyz = np.clip((np.array(self.pos) - np.array(self.prev_pos))/self.dt, -1.5, 1.5)
        self.base_rot_vel = np.clip((np.array([self.roll, self.pitch, self.yaw]) - np.array(self.prev_rot))/self.dt, -np.pi, np.pi)
        self.prev_pos = self.pos
        self.prev_rot = [self.roll, self.pitch, self.yaw]

        self.roll_vel = self.base_rot_vel[0]
        self.pitch_vel = self.base_rot_vel[1]
        self.yaw_vel = self.base_rot_vel[2]

        # Unsure why this is correct (negative yaw), but seems to be..
        rot = np.array(
        [[np.cos(-self.yaw), -np.sin(-self.yaw), 0],
            [np.sin(-self.yaw), np.cos(-self.yaw), 0],
            [		0,			 0, 1]]
        )

        self.vx, self.vy, self.vz = np.dot(rot, (self.body_vxyz[0],self.body_vxyz[1],self.body_vxyz[2]))
    
        self.ob = np.array([self.vx, self.roll, self.pitch, self.yaw, self.roll_vel, self.pitch_vel, self.yaw_vel])
    
        # self.ob = np.array([self.vx, self.roll, self.pitch, self.roll_vel, self.pitch_vel, self.yaw_vel])

        c_x, c_y = 60, 60
        im_x, im_y = 30, 30
        rect_pts = np.array([[-im_x, -im_y], [im_x, -im_y],[im_x, im_y],[-im_x, im_y]])
        rect_pts = self.transform_rot2d(-self.yaw, [0, 0], rect_pts) + np.array([c_x, c_y])
        pts = self.transform_rot2d(self.yaw, [0, 0], self.ij) + np.array([c_x, c_y])
        self.im = self.hm_cb[pts[:,0], pts[:,1]].reshape(self.im_size)

        if self.args.display_hm:
            self.im2 = np.rot90(np.rot90(self.hm_cb2[pts[:,0], pts[:,1]].reshape(self.im_size)))
            img = self.hm_cb2.astype(np.float32)
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

            cv2.polylines(img, np.int32([rect_pts]), True, (0,0,255), 2)

            cv2.imshow('frame2', img)
            cv2.imshow('frame1', self.im)
            cv2.imshow('frame0', self.im2)

            cv2.waitKey(1)

    def publish_actions(self, actions):
        # linear = Vector3()
        # angular = Vector3()
        cmd_vel_stamped = TwistStamped()
        cmd_vel_stamped.twist.linear.x = actions[0]
        cmd_vel_stamped.twist.angular.z = actions[1]
        cmd_vel_stamped.header = Header()
        cmd_vel_stamped.header.stamp = rospy.Time.now()
        self.cmd_vel_publisher.publish(cmd_vel_stamped)
    
    def transform_rot2d(self, yaw, pos, points):
        rot_mat = np.array(
                [[np.cos(yaw), -np.sin(yaw)],
                [np.sin(yaw), np.cos(yaw)]])
        return np.add(np.dot(rot_mat,points.T).T, pos).astype(np.int32)
    # =================================================
    # == Callbacks ====================================
    # =================================================
    def commandCallback(self, msg):
        self.run_policy = False
        for cl in msg.command_list:
            if cl.command_type == 18:
                self.run_policy = True
        if self.run_policy:
            print("running policy")
        else:
            print("received command not an RL command")


    def statusCallback(self, msg):
        self.pos_cb = [msg.pose.position.x, msg.pose.position.y, msg.pose.position.z]
        self.orn_cb = [msg.pose.orientation.x, msg.pose.orientation.y, msg.pose.orientation.z, msg.pose.orientation.w]
        self.twist_ang_cb = [0,0,0]
        self.twist_lin_cb = [0,0,0]

    def hmCallback(self, msg):
        if self.args.display_hm:
            self.hm_cb2 = np.flip(np.rot90((np.nan_to_num(np.array(msg.data).astype(np.float32).reshape(120,120,1)) + 1) / 101), axis=1)
        self.hm_cb = np.swapaxes(((np.nan_to_num(np.array(msg.data).astype(np.float32).reshape(120,120,1)) + 1) / 101), 0, 1)

    def get_hm(self):
        hm = np.ones(self.im_size).astype(np.float32)
        # [boxIds, positions, sizes, frictions, colours]
        grid_size = self.resolution
        x_offset = int(self.pos[0] / grid_size)
        y_offset = int(self.pos[1] / grid_size)
        x_min = x_offset - self.im_size[0]/2
        x_max = x_offset + self.im_size[0]/2
        y_min = y_offset - self.im_size[1]/2
        y_max = y_offset + self.im_size[1]/2
        if self.box_info is not None:
            positions = self.box_info[1]
            sizes = self.box_info[2]
            for pos, size in zip(positions, sizes):
                x, y, z = int(pos[0]/grid_size),int(pos[1]/grid_size), int(pos[2]/grid_size) 
                x_size, y_size, z_size = int(size[0]/grid_size), int(size[1]/grid_size), int(size[2]/grid_size)
                yaw = pos[5]
                points  = np.array([[dx, dy] for dx in range(x-x_size, x+x_size) for dy in range(y-y_size, y+y_size)]).T
                # print(points.shape)
                # hm_pts =  np.array([[y_offset, x_offset]]).T + self.transform_rot(yaw, pos[:2], points) 
                hm_pts = np.array([[x_offset, y_offset]]).T - self.transform_rot(yaw + np.pi/2, [pos[0], pos[1]], points)
                # print(hm_pts.shape)
                hm_pts[0,:] = np.clip(hm_pts[0,:], x_min, x_max)
                hm_pts[1,:] = np.clip(hm_pts[1,:], y_min, y_max)
                # print(y_min, y_max, x_min, x_max)
                # print(hm_pts.shape)
                # hm[hm_pts[0,:],hm_pts[1,:]] = (z + z_size/grid_size) > 0
                hm[hm_pts[0,:],hm_pts[1,:]] = (z + z_size/grid_size) < 0.2
                # hm[hm_pts[0,:],hm_pts[1,:]] = (z + z_size/grid_size) > 0.2

        return np.flip(np.swapaxes(hm, 0, 1), axis=0)
    
    def transform_rot(self, yaw, pos, points):
        rot_mat = np.array(
                [[np.cos(yaw), -np.sin(yaw)],
                [np.sin(yaw), np.cos(yaw)]])
        # return np.add(np.dot(rot_mat,points.T).T, pos).astype(np.int32)
        return np.add(np.dot(rot_mat,points).T, pos).astype(np.int32).T

    def make_arrow_points_marker(self, tail, tip, num, col, delete=False):
        # make a visualization marker array for the occupancy grid
        m = Marker()
        if delete:
            m.action = Marker.DELETE
        else:
            m.action = Marker.ADD
        m.header.frame_id = '/map'
        m.header.stamp = rospy.Time.now()
        m.ns = 'points_arrows'
        m.id = num
        m.type = Marker.ARROW
        m.pose.orientation.y = 0
        m.pose.orientation.w = 1
        # m.scale = scale
        m.scale = Vector3(0.2,0.5,0.5)
        m.color = col
        # m.color.r = 0.2
        # m.color.g = 0.5
        # m.color.b = 1.0
        # m.color.a = 1.0
        m.points = [ tail, tip ]
        return m

    # def make_marker(marker_type, scale, r, g, b, a):
    #     # make a visualization marker array for the occupancy grid
    #     m = Marker()
    #     m.action = Marker.ADD
    #     m.header.frame_id = '/base_link'
    #     m.header.stamp = rospy.Time.now()
    #     m.ns = 'marker_test_%d' % marker_type
    #     m.id = 0
    #     m.type = marker_type
    #     m.pose.orientation.y = 0
    #     m.pose.orientation.w = 1
    #     m.scale = scale
    #     m.color.r = 1.0
    #     m.color.g = 0.5
    #     m.color.b = 0.2
    #     m.color.a = 0.3
    #     m.color.r = r
    #     m.color.g = g
    #     m.color.b = b
    #     m.color.a = a
    #     return m

    def make_line(self, tail, tip, num, col, delete=False):
        # make a visualization marker array for the occupancy grid
        m = Marker()
        if delete:
            m.action = Marker.DELETE
        else:
            m.action = Marker.ADD
        m.header.frame_id = '/map'
        m.header.stamp = rospy.Time.now()
        # m.ns = 'marker_test_%d' % marker_type
        m.id = num + 32
        m.type = Marker.LINE_LIST
        # m.pose.position.x = pos[0]
        # m.pose.position.y = pos[1]
        # m.pose.position.z = pos[2]
        # m.pose.orientation.x = orn[0]
        # m.pose.orientation.y = orn[1]
        # m.pose.orientation.z = orn[2]
        m.pose.orientation.w = 1
        m.scale = Vector3(0.1, 1.0, 1.0)
        # m.color.a = 1.0
        # m.color.r = 1.
        # color = ColorRGBA(1,0,0,1)
        color = col

        m.colors = [color, color]
        # m.colors.push_back(color);
        m.points = [ tail, tip ]
        return m

    # def make_marker(marker_type, scale, r, g, b, a):
    def make_marker(self, pos, orn, num):
        # make a visualization marker array for the occupancy grid
        m = Marker()
        m.action = Marker.ADD
        m.header.frame_id = '/map'
        m.header.stamp = rospy.Time.now()
        # m.ns = 'marker_test_%d' % marker_type
        m.id = num + 16
        m.type = Marker.MESH_RESOURCE
        m.mesh_resource = "package://titan_rl/assets/Fixed_Titan.stl"
        m.pose.position.x = pos[0]
        m.pose.position.y = pos[1]
        m.pose.position.z = pos[2]
        m.pose.orientation.x = orn[0]
        m.pose.orientation.y = orn[1]
        m.pose.orientation.z = orn[2]
        m.pose.orientation.w = orn[3]
        m.scale = Vector3(1.0, 1.0, 1.0)
        m.color.a = 1.0
        m.color.r = 1.0
        return m

    def add_markers(self, delete=False):
        robot_x, robot_y, robot_yaw = self.pos[0], self.pos[1], self.yaw
        # pos = [robot_x, robot_y, 0.0]

        # rot = Rotation.from_euler('xyz', [0, 0, robot_yaw], degrees=False)        
        # orn = rot.as_quat() 
        # self.robots.markers.append(self.make_marker(pos, orn, num))
        num = int(self.robot_name[1:])
        if self.aux[0] > 0:

            angle, dist, target_angle, size = self.aux[1], self.aux[2], self.aux[3], self.aux[4]
            # If door_x, door_y provided, uncomment this: 
            # door_x, door_y, target_angle, size = self.aux[1], self.aux[2], self.aux[3], self.aux[4]
            # And comment out this:
            door_x, door_y = dist*np.cos(angle+robot_yaw) + robot_x, dist*np.sin(angle+robot_yaw) + robot_y  
            
            door_x2, door_y2 = size*np.cos(target_angle) + door_x, size*np.sin(target_angle) + door_y

            tail = Point(door_x, door_y, 0)
            tip = Point(door_x2, door_y2, 0)
            col = ColorRGBA(0.2,0.5,1,1)
            self.doors.markers.append(self.make_arrow_points_marker(tail, tip, num, col, delete=delete))

            x1, y1 = door_x + (size/2)*np.cos(target_angle - np.pi/2), door_y + (size/2)*np.sin(target_angle-np.pi/2)
            x2, y2 = door_x - (size/2)*np.cos(target_angle - np.pi/2), door_y - (size/2)*np.sin(target_angle-np.pi/2)

            tail = Point(x1, y1, 0)
            tip = Point(x2,y2,0)
            self.doors.markers.append(self.make_line(tail, tip, num, col, delete=delete))

        else:
            tail = Point(0, 0, 0)
            tip = Point(0, 0, 0)
            col = ColorRGBA(1,0,0,1)
            self.doors.markers.append(self.make_arrow_points_marker(tail, tip, num, col, delete=delete))
            self.doors.markers.append(self.make_line(tail, tip, num, col, delete=delete))

        # if self.est_aux[0] > 0:

        #     angle, dist, target_angle, size = self.est_aux[1], self.est_aux[2], self.est_aux[3], self.est_aux[4]
        #     # If door_x, door_y provided, uncomment this: 
        #     # door_x, door_y, target_angle, size = self.aux[1], self.aux[2], self.aux[3], self.aux[4]
        #     # And comment out this:
        #     door_x, door_y = dist*np.cos(angle+robot_yaw) + robot_x, dist*np.sin(angle+robot_yaw) + robot_y  
            
        #     door_x2, door_y2 = size*np.cos(target_angle) + door_x, size*np.sin(target_angle) + door_y

        #     col = ColorRGBA(0,1,0,1)
        #     tail = Point(door_x, door_y, 0)
        #     tip = Point(door_x2, door_y2, 0)
        #     self.doors.markers.append(self.make_arrow_points_marker(tail, tip, num+48, col))

        #     x1, y1 = door_x + (size/2)*np.cos(target_angle - np.pi/2), door_y + (size/2)*np.sin(target_angle-np.pi/2)
        #     x2, y2 = door_x - (size/2)*np.cos(target_angle - np.pi/2), door_y - (size/2)*np.sin(target_angle-np.pi/2)

        #     tail = Point(x1, y1, 0)
        #     tip = Point(x2,y2,0)
        #     self.doors.markers.append(self.make_line(tail, tip, num+48, col))

        # else:
        #     col = ColorRGBA(0,1,0,1)
        #     tail = Point(0, 0, 0)
        #     tip = Point(0, 0, 0)
        #     self.doors.markers.append(self.make_arrow_points_marker(tail, tip, num+48, col))
        #     self.doors.markers.append(self.make_line(tail, tip, num+48, col))


def run(args):
    MY_WORKSPACE_NAME = "tid010"

    if args.render:
        args.test = True

    rank = comm.Get_rank()

    now = datetime.now()
    now = comm.bcast(now.strftime("%d_%m_%Y_%H_%M_%S"), root=0)  

    SAVE_PATH = "/scratch1/" + MY_WORKSPACE_NAME + "/results/"
    PATH = SAVE_PATH + "walker/" + args.exp + "/" + now + "/"

    if rank == 0:
        writer = tensorboardX.SummaryWriter(log_dir=PATH)
    else:
        writer = None
    
    logger_kwargs = setup_logger_kwargs(args.exp, args.seed)
    logger_kwargs["output_dir"] = PATH




    ppo(lambda : Env(PATH=PATH, args=args, writer=writer), ac_kwargs=dict(hidden_sizes=[64]*2), epochs=args.epochs, PATH=PATH, writer=writer, logger_kwargs=logger_kwargs, perception=args.perception)


if __name__=="__main__":
    args = default_arguments.get_defaults() 
    mpi_fork(args.cpu)

    # # Get robot name?
    # robot_name = 'r1'
    # rospy.init_node('titan_rl_node_' + robot_name, anonymous=False) 
    
    run(args)



    # from models.ppo import Model
    # pol = Model(ob_size=7, im_size=[80,80,1], args=args)


    # while not rospy.is_shutdown():
    #     titan_rl.get_observation()
    #     if titan_rl.run_policy:
    #         titan_rl.run()
        # print(inspect.getfile(CommandList))
        # rospy.spin()
