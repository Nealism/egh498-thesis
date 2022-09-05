import xml.etree.ElementTree as ET
import rospy
import time
from geometry_msgs.msg import Pose
import numpy as np
from gazebo_msgs.srv import SetModelState,SetModelConfiguration, SpawnModel, DeleteModel, SpawnModelRequest, SpawnModelResponse
import time
import cv2
# from rand_heightmap_generator import HeightMapGenerator
from PIL import Image


class Obstacles():
    def __init__(self, rank=0, num_workers=1, args=None):
        '''
        Creates an xml, and saves to test.world. test.world is then roslaunched in run.py. 
        TODO explore reseting the simulation/reloading the world file
        '''
        self.rank = rank
        self.args = args
        # world shape must be 2^n + 1 [65, 129, 257, 513], change this to increase the resolution of the mesh
        # self.world_shape = [257,257]
        self.world_shape = [513, 513]
        # Made this so we can scale to 64 robots (move a max dist of 4 meters, with costmap of 4x4 = 8 meters all around)
        self.size = [64, 64, 3]
        self.pixel_scale = np.rint(self.world_shape[0] / self.size[0])
        
        self.pos = [self.size[0]/2,self.size[1]/2,0]
        self.orn = [0,0,0,1]
        # self.size = [100, 100, 3]
        self.colour = [1.0, 0.2, 0.0, 1.0]
        self.path = "$HOME/Dropbox/csiro_ws/src/behaviour_rl_nav/gazebo/worlds/heightmap_test.png"
    
    def initialise_ros_stuff(self):
        self.req = SpawnModelRequest()
        self.spawn_model_srv = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
        self.delete_model_srv = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)
        # self.box_num = 0
        # self.num_workers = num_workers
        # self.hm_gen = HeightMapGenerator()
        
    def spawn_model(self):
        try:
            self.delete_model()
        except Exception as e:
            print("No model to delete", e)

        sdf = ET.tostring(self.root).decode("utf-8") 
        # print(sdf)
        self.req.model_xml = sdf
        # print("waiting to spawn")
        # print(sdf)
        self.spawn_model_srv.wait_for_service()
        # t1 = time.time()
        spawned = self.spawn_model_srv(self.req)
        # print("spawned world took", time.time() - t1)
        return spawned
        # return self.get_box_info(), self.goals, self.aux_goals, self.detect_goals

        # time.sleep(2)

    def delete_model(self):
        # self.delete_model_srv.wait_for_service()
        deleted = self.delete_model_srv("heightmap")

    def generate_map(self):
        # template = (np.random.random([int(self.world_shape[2]/4),int(self.world_shape[2]/4)]) + 1.0) * self.terrain_difficulty 
        # template = (np.random.random([int(self.world_shape[0]/4),int(self.world_shape[1]/4)]) * 255.0).astype(np.uint8) 
        
        # TODO: define start and goal locations, make sure these are zero
        # TODO: Add some discrete obstacles (e.g. tree's, doorways)

        # This is how much we consider neighbouring pixels
        shrink_factor = 4
        template = np.zeros([int(self.world_shape[0]/shrink_factor),int(self.world_shape[1]/shrink_factor)])
        for i in range(template.shape[0]):
            for j in range(template.shape[1]):
                if np.random.random() < 0.1:
                    template[i,j] = np.random.random() * 1.0
                elif np.random.random() < 0.5:
                    template[i,j] = np.random.random() * 0.2

        # template = (np.random.random([int(self.world_shape[0]/20),int(self.world_shape[1]/20)]) * 255.0).astype(np.uint8) 
        template = (template * 255.0).astype(np.uint8) 
        hm = cv2.resize(template, dsize=(self.world_shape[0], self.world_shape[1])).reshape(self.world_shape)
        
        start_locations = [[int((4 + i*8)*self.pixel_scale),int((4 + j*8)*self.pixel_scale)] for i in range(8) for j in range(8)]
        # print(start_locations); exit()
        for location in start_locations:
            x_min = location[0] - int(0.5 * self.pixel_scale)
            x_max = location[0] + int(0.5 * self.pixel_scale)
            y_min = location[1] - int(0.5 * self.pixel_scale)
            y_max = location[1] + int(0.5 * self.pixel_scale)
            hm[x_min:x_max, y_min:y_max] = 0
            print(hm.shape, x_min, x_max, y_min, y_max)

        # # Make the edges smooth
        # template[:, 0] = 0.0
        # template[:, -1] = 0.0
        # template[0, :] = 0.0
        # template[-1, :] = 0.0
        

        # hm = np.zeros([129,129])
        # hm = (np.random.random(self.world_shape)*255.0).astype(np.uint8)
        path = "$HOME/Dropbox/csiro_ws/src/behaviour_rl_nav/gazebo/worlds/heightmap_test.png"
        cv2.imwrite(path, hm)   
        cv2.imshow("frame", hm)
        cv2.waitKey(0)
        
        # im = Image.fromarray(hm)

        # im = im.convert("L")
        # im = im.convert("RGB")
        # im.save(path)


    def generate_model(self, difficulty=1, individual=False, rank=0):

        # if self.world == 'stairs' or self.world == 'teb_world':
        # self.tree = ET.parse('gazebo/worlds/blank.world')
        self.tree = ET.parse('gazebo/worlds/blank.world')
        # self.tree = ET.parse('gazebo/worlds/empty.world')
        # self.tree = ET.parse('gazebo/worlds/empty2.world')
        # else:
        #   self.tree = ET.parse('gazebo/worlds/ground.world')
        self.root = self.tree.getroot()
        self.model = ET.SubElement(self.root[0], "model") 
        self.model.set("name", "heightmap")
        static = ET.SubElement(self.model, "static")
        static.text = "true"

        pos = self.pos
        orn = self.orn
        size = self.size
        path = self.path
        colour = self.colour

        link = ET.SubElement(self.model, "link")
        link.set("name", "heightmap")
        # Visual
        visual = ET.SubElement(link, "visual")
        visual.set("name", "heightmap_visual")

        pose = ET.SubElement(visual, "pose")
        pose.text = str(pos[0]) + " " + str(pos[1]) + " " + str(pos[2]) + " " + str(orn[0]) + " " + str(orn[1]) + " " + str(orn[2])
        geometry = ET.SubElement(visual, "geometry")
        box = ET.SubElement(geometry, "heightmap")
        uri = ET.SubElement(box, "uri")
        uri.text = path
        size_el = ET.SubElement(box, "size")
        size_el.text = str(size[0]) + " " + str(size[1]) + " " + str(size[2])
        
        material = ET.SubElement(visual, "material")
        ambient = ET.SubElement(material, "ambient")
        ambient.text = str(colour[0]) + " " + str(colour[1]) + " " + str(colour[2]) + " " + str(colour[3])
        diffuse = ET.SubElement(material, "diffuse")
        diffuse.text = "1 0 0 1"
        specular = ET.SubElement(material, "specular")
        # colour.text = str(box_colour[0]) + " " + str(box_colour[1]) + " " + str(box_colour[2]) + " " + str(box_colour[3])
        specular.text = "0.1 0.1 0.1 1"     
        emissive = ET.SubElement(material, "emissive")
        emissive.text = "0 0 0 0"

        # Collision
        collision = ET.SubElement(link, "collision")
        collision.set("name", "heightmap_collision")
        pose = ET.SubElement(collision, "pose")
        pose.text = str(pos[0]) + " " + str(pos[1]) + " " + str(pos[2]) + " " + str(orn[0]) + " " + str(orn[1]) + " " + str(orn[2])
        geometry = ET.SubElement(collision, "geometry")
        box = ET.SubElement(geometry, "heightmap")
        uri = ET.SubElement(box, "uri")
        uri.text = path
        size_el = ET.SubElement(box, "size")
        size_el.text = str(size[0]) + " " + str(size[1]) + " " + str(size[2])

        # self.box_id = []
        # self.positions = []
        # self.sizes = []
        # self.colours = []

        # if self.args.obstacle_type == "stairs":
        #     self.add_stairs_oct(difficulty=difficulty, individual=individual, rank=rank)
        # else:
        #     if self.args.oct:
        #         self.add_doors_oct(difficulty=difficulty, individual=individual, rank=rank)
        #     else:
        #         self.add_doors(difficulty=difficulty, individual=individual, rank=rank)

        self.tree.write('gazebo/models/test/model.sdf')

    # def generate_model(self, difficulty=1, individual=False, rank=0):

    #     # if self.world == 'stairs' or self.world == 'teb_world':
    #     # self.tree = ET.parse('gazebo/worlds/blank.world')
    #     # self.tree = ET.parse('gazebo/worlds/blank.world')
    #     self.tree = ET.parse('gazebo/worlds/empty.world')
    #     # self.tree = ET.parse('gazebo/worlds/empty2.world')
    #     # else:
    #     #   self.tree = ET.parse('gazebo/worlds/ground.world')
    #     self.root = self.tree.getroot()
    #     self.model = ET.SubElement(self.root[0], "model") 
    #     self.model.set("name", self.args.obstacle_type)
    #     static = ET.SubElement(self.model, "static")
    #     static.text = "true"

        

    #     # self.box_id = []
    #     # self.positions = []
    #     # self.sizes = []
    #     # self.colours = []

    #     # if self.args.obstacle_type == "stairs":
    #     #     self.add_stairs_oct(difficulty=difficulty, individual=individual, rank=rank)
    #     # else:
    #     #     if self.args.oct:
    #     #         self.add_doors_oct(difficulty=difficulty, individual=individual, rank=rank)
    #     #     else:
    #     #         self.add_doors(difficulty=difficulty, individual=individual, rank=rank)

    #     self.tree.write('gazebo/models/test/model.sdf')


    def terrain_from_height_map(self, hm):
        self.box_count = 0
        for thing in things:
            _, boxes = self.hm_gen.door_template(width=0.2, length=1.0, door_size=0.8, grid_size=0.1, width2=0.0, invert=False, temp_type=1)
            # boxes = self.hm_gen.box_list
            for box in boxes:
                pos, orn, size = box
                pos = pos + pos
                orn = orn + orn
                self.add_box(str(self.box_count), pos, orn, size, box_colour=[0.3,0.8,0.5,1])
                self.box_count += 1


    def add_stairs_oct(self, difficulty, individual=False, rank=0):
        floor = False
        self.num_workers = 48
        difficulty_range = 1
        dist = 45
        self.goals = {j:{i:{'x':0,'y':0} for i in range(5)} for j in range(self.num_workers)}
        self.detect_goals = {j:{i:{'x':0,'y':0} for i in range(4)} for j in range(self.num_workers)}
        self.aux_goals = {j:{i:{'x':0,'y':0,'yaw':0,'size':0, 'label':True} for i in range(2)} for j in range(self.num_workers)}

        for _ in range(difficulty_range):
            for j in range(self.num_workers):
                if j < 16:
                    k = 0
                else:
                    k = 1
                radius = dist*(k*0.75+1)
                x_offset = k*dist
                if j < 16:
                    theta = np.pi * (22.5 * (j + k*(22.5))) / 180
                else:
                    theta = np.pi * (11.25 * (j + k*(11.25))) / 180
                # ground_size = [15, np.random.uniform(3,6), 1]
                ground_size = [15, np.random.uniform(1.5,4), 1]
                
                x_offset = (radius) * np.cos(theta)
                y_offset = (radius) * np.sin(theta)

                ground_pos = [x_offset, y_offset, ground_size[2]]
                ground_orn = [0,0,theta]
                if floor:
                    self.add_box("g0" + str(j) + str(k), ground_pos, ground_orn, [ground_size[0]*2, ground_size[1]*2, ground_size[2]*2], box_colour=[0.3,0.3,0.8,1])
                
                x1 = ground_pos[0] + (ground_size[1] + 0.2)*np.cos(np.pi/2+theta)
                y1 = ground_pos[1] + (ground_size[1] + 0.2)*np.sin(np.pi/2+theta)
                x2 = ground_pos[0] - (ground_size[1] + 0.2)*np.cos(np.pi/2+theta)
                y2 = ground_pos[1] - (ground_size[1] + 0.2)*np.sin(np.pi/2+theta)
                x3 = ground_pos[0] + (ground_size[0] + 0.2)*np.cos(theta)
                y3 = ground_pos[1] + (ground_size[0] + 0.2)*np.sin(theta)
                x4 = ground_pos[0] - (ground_size[0] + 0.2)*np.cos(theta)
                y4 = ground_pos[1] - (ground_size[0] + 0.2)*np.sin(theta)

                # width = np.random.uniform(0.2, 0.3)
                # print("increased width")
                width = np.random.uniform(0.2, 0.5)

                size_x = [ground_size[0], width, 2]
                size_y = [width, ground_size[1] + size_x[1]*2, 2]

                self.add_box("g1" + str(j) + str(k), [x1, y1, size_x[2]], ground_orn,  [size_x[0]*2, size_x[1]*2, size_x[2]*2], box_colour=[0.3,0.8,0.5,1])
                self.add_box("g2" + str(j) + str(k), [x2, y2, size_x[2]], ground_orn,  [size_x[0]*2, size_x[1]*2, size_x[2]*2], box_colour=[0.3,0.8,0.5,1])
                if floor:
                    self.add_box("g3" + str(j) + str(k), [x3, y3, size_x[2]], ground_orn,  [size_y[0]*2, size_y[1]*2, size_y[2]*2], box_colour=[0.3,0.8,0.5,1])
                    self.add_box("g4" + str(j) + str(k), [x4, y4, size_x[2]], ground_orn,  [size_y[0]*2, size_y[1]*2, size_y[2]*2], box_colour=[0.3,0.8,0.5,1])
                
                ground_width = ground_size[1]*2
                if floor:
                    z_offset = ground_pos[2] + ground_size[2]/2
                else:
                    z_offset = 0
                
                # x = -ground_size[0]/3
                
                step_run = np.random.uniform(0.2, 0.5)
                step_height = min(np.random.uniform(0.1, 0.3), step_run)
                # size = [ground_size[0], step_run, 0]
                
                # first_wall = first_walls[i]
                # second_wall = wall - first_wall

                # x_offset1, y_offset1 = x_offset + x*np.cos(theta), y_offset + x*np.sin(theta)    
                # size1 = [width, first_wall, 3]

                # pos_y = (ground_width/2 - size1[1]/2)
                # pos = [x_offset +  pos_y*np.cos(theta - np.pi/2 ), y_offset + pos_y*np.sin(theta - np.pi/2 ), (z_offset + size1[2])/2]
                # pos = [x_offset, y_offset, z_offset]
                orn = [0,0,theta]
                # self.add_box("w1_" + str(i) + str(j) + str(k), pos, orn, [size1[0], size1[1], size1[2]], box_colour=[0.8,0.3,0.5,1])

                # num_stairs = np.random.randint(7,10)
                # stair_type = np.random.choice(["up", "down"])
                # if stair_type == "up":
                prev_height = z_offset
                # else:
                #     prev_height = z_offset + num_stairs*step_height
                
                x = -ground_size[0]/3
                # x_offset1, y_offset1 = x_offset + x*np.cos(theta), y_offset + x*np.sin(theta)

                start_pos = [x_offset + x*np.cos(theta), y_offset + x*np.sin(theta), z_offset]
                size=[step_run,ground_width,step_height]
                number = np.random.randint(5,10)

                dist_from_stairs = 1.5
                size_goal = [0.5, 0.5, 0.35]
                pos = [0,0,0]
                for l in range(2):
                    name = str(j) + str(k) + str(l)
                    fact = 1 if l == 0 else -1
                    if l == 1:
                        start_pos = [x_offset + x*np.cos(theta), y_offset + x*np.sin(theta), z_offset + l*step_height*number]
                    else:
                        start_pos = [x_offset + x*np.cos(theta), y_offset + x*np.sin(theta), z_offset + l*step_height*number]

                    
                    pos1 = [x_offset + (x-dist_from_stairs)*np.cos(theta), y_offset + (x- dist_from_stairs)*np.sin(theta ), z_offset + size_goal[2] + pos[2]]
                    self.goals[j][l*2] = {'x':pos1[0],'y':pos1[1], 'z':pos2[2]}
                    self.add_box("first_t2_" + str(l) + str(j) + str(k), pos1, orn, size_goal, box_colour=[0.8,0.8,0.8,1], vis_only=True, shape='cylinder')



                    # if l == 0:
                    # start_pos = [start_pos[0] + (size[1]/2+size[0]/2)*np.cos(orn[2]), start_pos[1] + (size[1]/2+size[0]/2)*np.sin(orn[2]), start_pos[2]+ fact*size[2]]
                    # else:
                    #     start_pos = [start_pos[0] + (size[1]/2+size[0]/2)*np.cos(orn[2]), start_pos[1] + (size[1]/2+size[0]/2)*np.sin(orn[2]), start_pos[2]+ fact*size[2]]
                    # start_pos = [start_pos[0] + (size[1]/2+size[0]/2)*np.cos(orn[2]), start_pos[1] + (size[1]/2+size[0]/2)*np.sin(orn[2]), start_pos[2]+ fact*size[2]]
                    # start_pos = [x_offset + x*np.cos(theta) + (size[1]/2+size[0]/2)*np.cos(orn[2]), y_offset + x*np.sin(theta) + (size[1]/2+size[0]/2)*np.sin(orn[2]), z_offset + fact*size[2]]
                    
                    for i in range(number):
                        box_size = size
                        pos = [size[0]*i*np.cos(orn[2]) + start_pos[0], size[0]*i*np.sin(orn[2])+start_pos[1], fact*(size[2]*i)+start_pos[2]]
                        self.add_box(box_name="stair_" + name + str(i), pos=pos, orn=orn, box_size=box_size)    
                        platform_size = [size[1],size[1],size[2]]
                        pos = [pos[0] + (size[1]/2+size[0]/2)*np.cos(orn[2]), pos[1] + (size[1]/2+size[0]/2)*np.sin(orn[2]), pos[2]+fact*size[2]]
                    if l == 0:
                        self.add_box(box_name="platform_" + name, pos=pos, orn=orn, box_size=platform_size)    
                    # x += ground_size[0]*2/3
                    
                    #     pos2 = [x_offset + (number*step_run + dist_from_stairs + x)*np.cos(theta), y_offset + (dist_from_stairs + number*step_run + x)*np.sin(theta ), pos[2]]
                    #     self.goals[j][l*2 + 1] = {'x':pos2[0],'y':pos2[1]}
                    #     self.add_box("second_t2_" + str(l) + str(j) + str(k), pos2, orn, size_goal, box_colour=[0.8,0.8,0.8,1], vis_only=True, shape='cylinder')
                    # else:
                    pos2 = [x_offset + (number*step_run + dist_from_stairs + x)*np.cos(theta), y_offset + (dist_from_stairs + number*step_run + x)*np.sin(theta ), pos[2] + size_goal[2]]
                    # pos2 = [x_offset + (number*step_run*2 + platform_size[0]*2)*np.cos(theta), start_pos[0] + (number*step_run*2 + platform_size[0]*2)*np.sin(theta ), pos[2]]
                    self.goals[j][l*2 + 1] = {'x':pos2[0],'y':pos2[1], 'z':pos2[2]}
                    self.add_box("second_t2_" + str(l) + str(j) + str(k), pos2, orn, size_goal, box_colour=[0.8,0.8,0.8,1], vis_only=True, shape='cylinder')

                    x += number*step_run + platform_size[0]


    def add_doors_oct(self, difficulty, individual=False, rank=0):
        # p.x = r1 * sin(M_PI * (45 * side - 22.5) / 180);
        # p.y = r1 * cos(M_PI * (45 * side - 22.5) / 180);
        # line_list.points.push_back(p);

        # p.x = r1 * sin(M_PI * (45 * (side + 1) - 22.5) / 180);
        # p.y = r1 * cos(M_PI * (45 * (side + 1) - 22.5) / 180);
        # line_list.points.push_back(p);
        # octagon
        # self.num_workers = 8
        # floor = True
        floor = False
        # self.num_workers = 32
        self.num_workers = 48
        # difficulty_range = 4
        difficulty_range = 1
        # self.small_goals = {j:{k:{i:{'y':0} for i in range(4)} for k in range(difficulty_range)} for j in range(self.num_workers)}
        self.goals = {j:{i:{'x':0,'y':0} for i in range(5)} for j in range(self.num_workers)}
        self.detect_goals = {j:{i:{'x':0,'y':0} for i in range(4)} for j in range(self.num_workers)}
        
        self.aux_goals = {j:{i:{'x':0,'y':0,'yaw':0,'size':0, 'label':True} for i in range(2)} for j in range(self.num_workers)}
        # self.goals = {j:{k:{'x': 0, 'y':0} for k in range(difficulty_range)} for j in range(self.num_workers)}
        # self.goals = {j:{'x': 0, 'y':0} for j in range(self.num_workers)}
        # self.goals = np.array([])
        # dist = 20
        # dist = 25
        # dist = 30
        # self.add_box("g", [0,0,0.01], [0,0,0,1], [40,40,0.01], box_colour=[0.8,0.3,0.3,1])

        dist = 45
        for _ in range(difficulty_range):
            # radius = dist*(k*0.5+1)
            # x_offset = k*dist
            # for j in range(self.num_workers):
            for j in range(self.num_workers):
                # theta = np.pi * (45 * j) / 180
                if j < 16:
                    k = 0
                else:
                    k = 1
                radius = dist*(k*0.75+1)
                x_offset = k*dist
                if j < 16:
                    theta = np.pi * (22.5 * (j + k*(22.5))) / 180
                else:
                    theta = np.pi * (11.25 * (j + k*(11.25))) / 180
                
                # y_offset = j*15
                # x_offset = (radius + k*20) * np.sin(theta)
                # ground_size = [9, np.random.uniform(3, 5), 1]
                # ground_size = [9, 3, 1]
                # ground_size = [9, 3, 1]

                # ground_size = [9, np.random.uniform(2,3), 1]
                # ground_size = [15, np.random.uniform(4,6), 1]
                ground_size = [15, np.random.uniform(3,6), 1]
                
                x_offset = (radius) * np.cos(theta)
                y_offset = (radius) * np.sin(theta)
                # print(j, theta, x_offset, y_offset, ground_size)

                # ground_size = [9, 2, 1]
                # ground_pos = [ground_size[0] - 1.0 + x_offset, y_offset, ground_size[2]]
                ground_pos = [x_offset, y_offset, ground_size[2]]
                ground_orn = [0,0,theta]
                if floor:
                    self.add_box("g0" + str(j) + str(k), ground_pos, ground_orn, [ground_size[0]*2, ground_size[1]*2, ground_size[2]*2], box_colour=[0.3,0.3,0.8,1])
                
                # x1 = ground_pos[0] + (ground_size[0] + 0.2)*np.sin(theta + np.pi/2) + (ground_size[0] + 0.2)*np.cos(theta + np.pi/2)
                # y1 = ground_pos[1] + (ground_size[0] + 0.2)*np.sin(theta + np.pi/2) + (ground_size[0] + 0.2)*np.cos(theta + np.pi/2)
                
                x1 = ground_pos[0] + (ground_size[1] + 0.2)*np.cos(np.pi/2+theta)
                y1 = ground_pos[1] + (ground_size[1] + 0.2)*np.sin(np.pi/2+theta)
                x2 = ground_pos[0] - (ground_size[1] + 0.2)*np.cos(np.pi/2+theta)
                y2 = ground_pos[1] - (ground_size[1] + 0.2)*np.sin(np.pi/2+theta)
                x3 = ground_pos[0] + (ground_size[0] + 0.2)*np.cos(theta)
                y3 = ground_pos[1] + (ground_size[0] + 0.2)*np.sin(theta)
                x4 = ground_pos[0] - (ground_size[0] + 0.2)*np.cos(theta)
                y4 = ground_pos[1] - (ground_size[0] + 0.2)*np.sin(theta)

                # width = np.random.uniform(0.2, 0.3)
                # print("increased width")
                width = np.random.uniform(0.2, 0.5)

                size_x = [ground_size[0], width, 2]
                size_y = [width, ground_size[1] + size_x[1]*2, 2]

                self.add_box("g1" + str(j) + str(k), [x1, y1, size_x[2]], ground_orn,  [size_x[0]*2, size_x[1]*2, size_x[2]*2], box_colour=[0.3,0.8,0.5,1])
                self.add_box("g2" + str(j) + str(k), [x2, y2, size_x[2]], ground_orn,  [size_x[0]*2, size_x[1]*2, size_x[2]*2], box_colour=[0.3,0.8,0.5,1])
                if floor:
                    self.add_box("g3" + str(j) + str(k), [x3, y3, size_x[2]], ground_orn,  [size_y[0]*2, size_y[1]*2, size_y[2]*2], box_colour=[0.3,0.8,0.5,1])
                    self.add_box("g4" + str(j) + str(k), [x4, y4, size_x[2]], ground_orn,  [size_y[0]*2, size_y[1]*2, size_y[2]*2], box_colour=[0.3,0.8,0.5,1])
                
                ground_width = ground_size[1]*2
                if floor:
                    z_offset = ground_pos[2] + ground_size[2]/2
                else:
                    z_offset = 0
                
                x = -ground_size[0]/3
                # x = (radius + k*20) * np.sin(theta)
                # 1-10   

                # door_width = 1.6 - difficulty*0.16
                # door_width = 0.8
                # door_width = 1.0
                # # door_width = 5.0
                # # difficulty = 5
                # wall =  (ground_width - door_width)
                # # if difficulty > 10:
                # if difficulty > 5:
                #     door_width = np.random.uniform(0.8,1.0)
                #     # door_width = 0.8
                #     fact = np.random.choice([-1,1])
                #     first_wall1 = fact*np.random.uniform(0,2) + wall/2
                #     first_wall2 = (-1*fact)*np.random.uniform(0,2) + wall/2
                # elif difficulty > 1:
                #     fact = np.random.choice([-1,1])
                #     first_wall1 = fact*difficulty*0.2 + wall/2
                #     first_wall2 = (-1*fact)*difficulty*0.2 + wall/2
                #     # first_wall1 = fact*difficulty*0.2 + wall/2
                #     # first_wall2 = (-1*fact)*difficulty*0.2 + wall/2
                # else:
                #     # door_placement = 1.5
                # # first_wall1 = np.random.uniform(door_placement, wall-door_placement)
                #     first_wall1 = wall/2
                #     first_wall2 = wall/2
                

                # # move then shrink, then random
                # if difficulty > 5:
                #     door_width = np.random.uniform(0.8,1.0)
                #     wall =  (ground_width - door_width)
                #     fact = np.random.choice([-1,1])
                #     first_wall1 = fact*np.random.uniform(0,ground_size[1]-0.8) + wall/2
                #     first_wall2 = (-1*fact)*np.random.uniform(0,ground_size[1]-0.8) + wall/2

                #     # door_width = 0.8
                #     # wall =  (ground_width - door_width)
                #     # fact = np.random.choice([-1,1])
                #     # first_wall1 = fact*np.random.uniform(0,ground_size[1]-0.5) + wall/2
                #     # first_wall2 = (-1*fact)*np.random.uniform(0,ground_size[1]-0.5) + wall/2
                # # elif difficulty > 5:
                # #     # door_width = np.random.uniform(0.8,1.0)
                # #     # door_width = 1.0 - difficulty*0.04
                # #     # door_width = 0.8
                # #     # door_width = np.random.uniform(0.8,1.0)
                # #     door_width = 1.3 - (difficulty-5)*0.1
                # #     wall =  (ground_width - door_width)
                # #     fact = np.random.choice([-1,1])
                # #     first_wall1 = fact*np.random.uniform(0,ground_size[1]-0.8) + wall/2
                # #     first_wall2 = (-1*fact)*np.random.uniform(0,ground_size[1]-0.8) + wall/2
                # else:
                #     # door_width = 1.25
                #     door_width = 0.8
                #     wall =  (ground_width - door_width)
                #     fact = np.random.choice([-1,1])
                #     first_wall1 = fact*difficulty*0.15 + wall/2
                #     first_wall2 = (-1*fact)*difficulty*0.15 + wall/2

                # door_width = 0.8
                if self.args.label_bit:
                    # Options are: 50% true (0.8-0.85), goal through door
                    # 50% false: small goal 25% (0-0.8) and goal through door, or 25% (0-0.85) and goal on this side 
                    # choice = np.random.choice([0,1,2], p=[0.25, 0.25, 0.5])
                    choice = np.random.choice([0,1,2], p=[0.1, 0.1, 0.8])
                    # if np.random.random() < 0.75:
                    if choice == 2:
                        door_width = np.random.uniform(0.8,0.85)
                        label = True
                    elif choice == 1:
                        door_width = np.random.uniform(0.0,0.75)
                        label = False
                    else:
                        door_width = np.random.uniform(0.0,0.85)
                        label = False
                elif self.args.train_detector:
                    if np.random.random() > 1.0:
                        # door_width = np.random.uniform(0.0,0.8)
                        door_width = np.random.uniform(0.0,0.6)
                        label = False
                    else:
                        door_width = np.random.uniform(0.8,0.85)
                    # door_width = np.random.uniform(0.0,0.4)
                        label = True
                else:
                    door_width = np.random.uniform(0.8,0.85)
                    # door_width = np.random.uniform(0.8,0.81)
                    label = True
                
                # door_width = np.random.uniform(0.9,1.0)
                wall =  (ground_width - door_width)
                fact = np.random.choice([-1,1])
                # Close to wall
                # first_wall1 = fact*np.random.uniform(0,ground_size[1]-0.8) + wall/2
                # first_wall2 = (-1*fact)*np.random.uniform(0,ground_size[1]-0.8) + wall/2
                first_wall1 = fact*np.random.uniform(0,ground_size[1]-3.0) + wall/2
                first_wall2 = (-1*fact)*np.random.uniform(0,ground_size[1]-3.0) + wall/2
                # first_wall1 = fact*(ground_size[1]-3.0) + wall/2
                # first_wall2 = (-1*fact)*(ground_size[1]-3.0) + wall/2


                # Shrink then move, then random
                # if difficulty > 10:
                #     door_width = np.random.uniform(0.8,1.0)
                #     wall =  (ground_width - door_width)
                #     fact = np.random.choice([-1,1])
                #     first_wall1 = fact*np.random.uniform(0,ground_size[1]-0.8) + wall/2
                #     first_wall2 = (-1*fact)*np.random.uniform(0,ground_size[1]-0.8) + wall/2
                # elif difficulty > 5:
                #     door_width = 0.8
                #     wall =  (ground_width - door_width)
                #     fact = np.random.choice([-1,1])
                #     first_wall1 = fact*(difficulty - 5)*0.15 + wall/2
                #     first_wall2 = (-1*fact)*(difficulty - 5)*0.15 + wall/2
                # else:
                #     door_width = 1.3 - (difficulty)*0.1
                #     wall =  (ground_width - door_width)
                #     fact = np.random.choice([-1,1])
                #     first_wall1 = fact*1*0.15 + wall/2
                #     first_wall2 = (-1*fact)*1*0.15 + wall/2
                
                
                # door_width = np.random.uniform(0.8,1.0)
                # door_width = 0.8
                # wall =  (ground_width - door_width)
                # fact = np.random.choice([-1,1])
                # first_wall1 = fact*np.random.uniform(0,ground_size[1]-0.5) + wall/2
                # first_wall2 = (-1*fact)*np.random.uniform(0,ground_size[1]-0.5) + wall/2
                # first_wall1 = fact*np.random.uniform(0,ground_size[1]-0.8) + wall/2
                # first_wall2 = (-1*fact)*np.random.uniform(0,ground_size[1]-0.8) + wall/2
                # first_wall1 = fact*np.random.uniform(0,ground_size[1]-0.8) + wall/2
                # first_wall2 = (-1*fact)*np.random.uniform(0,ground_size[1]-0.8) + wall/2

                # print(first_wall1, first_wall2)
                # fact = 1
                # first_wall1 = fact*5*0.4 + wall/2
                # first_wall2 = (-1*fact)*5*0.4 + wall/2
                # first_wall1 = np.random.choice([1.5, wall-1.5])
                # if first_wall1 == door_placement:
                # first_wall2 = wall-door_placement
                # first_wall2 = np.random.uniform(door_placement, wall-door_placement)

                # else:
                #     first_wall2 = door_placement
                first_walls = [first_wall1, first_wall2]
                
                # Choices are: - -, JL, TT, J-, -L, -T, T-, JT, TL

                for i in range(2):
                    
                    # config = np.random.randint(0,9)
                    # vis medium
                    # config = np.random.choice([0,1,2])
                    # config = np.random.choice([0,3,4,5,6])

                    # config = np.random.choice([0, 3, 4])
                    config = 1

                    # config = 3
                    # config = 1
                    # config = 0
                    
                    first_wall = first_walls[i]
                    second_wall = wall - first_wall

                    x_offset1, y_offset1 = x_offset + x*np.cos(theta), y_offset + x*np.sin(theta)
                    
                    size1 = [width, first_wall, 3]
                    pos_y = (ground_width/2 - size1[1]/2)
                    pos = [x_offset1 +  pos_y*np.cos(theta - np.pi/2 ), y_offset1 + pos_y*np.sin(theta - np.pi/2 ), (z_offset + size1[2])/2]
                    orn = [0,0,theta]
                    self.add_box("w1_" + str(i) + str(j) + str(k), pos, orn, [size1[0], size1[1], size1[2]], box_colour=[0.8,0.3,0.5,1])
                    

                    size2 = [size1[0], second_wall, 3]
                    pos_y = (-ground_width/2 + size2[1]/2)
                    pos = [x_offset1 +  pos_y*np.cos(theta - np.pi/2 ), y_offset1 + pos_y*np.sin(theta - np.pi/2 ), (z_offset + size2[2])/2]
                    orn = [0,0,theta]
                    self.add_box("w2_" + str(i) + str(j) + str(k), pos, orn, [size2[0], size2[1], size2[2]], box_colour=[0.8,0.3,0.5,1])
                                        
                    x_offset3, y_offset3 = x_offset1 + (-ground_width/2 + size2[1] + door_width/2) * np.cos(theta- np.pi/2), y_offset1 + (-ground_width/2 + size2[1] + door_width/2) * np.sin(theta- np.pi/2) 

                    # length_side1 = np.random.uniform(0.5,3.0)
                    # length_side1 = np.random.uniform(0.5,1.5)
                    length_side1 = np.random.uniform(0.5,0.85)
                    if config in [1,2,3,6,7,8]:
                        size_side1 = [length_side1, size1[0], 3]
                        # dist_side1 = np.sqrt((length_side1/2 + size1[0]/2)**2 + (door_width/2 + size1[0]/2)**2)
                        # if config in [1,3,7]:
                        #     angle_side1 = np.arctan2((length_side1/2 + size1[0]/2), (door_width/2 + size1[0]/2))
                        #     phi = np.random.uniform(0, np.pi/2)
                        #     phi = np.pi/2
                        # else:
                        #     angle_side1 = np.arctan2(-(length_side1/2 + size1[0]/2), (door_width/2 + size1[0]/2))
                        #     phi = np.random.uniform(-np.pi/2,0)
                        #     phi = 0

                        phi = np.random.uniform(-np.pi, 0)
                        # phi = 0
                        # phi = -np.pi/3 

                        # x_offset_side1, y_offset_side1 = dist_side1*np.sin(angle_side1-(theta + phi)), dist_side1*np.cos(angle_side1-(theta+phi))
                        # x_side1, y_side1 = x_offset3 + x_offset_side1, y_offset3 + y_offset_side1
                        # pos_side1 = [ x_side1 ,  y_side1, (z_offset + size1[2])/2]

                        door_pos = [x_offset3 - (door_width/2 + size1[0]/2)*np.cos(theta - np.pi/2),y_offset3 -  (door_width/2 + size1[0]/2)*np.sin(theta - np.pi/2),0]
                        x_side1, y_side1 = door_pos[0] + (length_side1/2)*np.cos(theta - phi), door_pos[1] + (length_side1/2)*np.sin(theta - phi)
                        pos_side1 = [ x_side1 ,  y_side1, (z_offset + size1[2])/2]
                        # orn = [0,0,theta + phi]
                        orn = [0,0,theta - phi]
                        self.add_box("w3_" + str(i) + str(j) + str(k), pos_side1, orn, size_side1, box_colour=[0.8,0.3,0.5,1])
                        
                    if config in [1,2,4,5,7,8]:
                        
                        size_side1 = [length_side1, size1[0], 3]
                        # dist_side1 = np.sqrt((length_side1/2 + size1[0]/2)**2 + (door_width/2 + size1[0]/2)**2)
                        # dist_side2 = length_side1/2
                        # if config in [1,4,8]:
                        #     angle_side1 = np.arctan2((length_side1/2 + size1[0]/2), -(door_width/2 + size1[0]/2))
                        #     phi = np.random.uniform(-np.pi/2,0)
                        #     phi = 0

                        # else:
                        #     angle_side1 = np.arctan2(-(length_side1/2 + size1[0]/2), -(door_width/2 + size1[0]/2))
                        #     phi = np.random.uniform(0,np.pi/2)
                        #     # phi = -np.pi/4
                        #     # phi = np.pi/2
                            
                        #     # phi = 0
                        #     phi = np.pi/2
                        phi = np.random.uniform(0,np.pi)

                        # door_pos = [x_offset3 + (door_width/2 )*np.cos(theta - np.pi/2),y_offset3 +  (door_width/2 )*np.sin(theta - np.pi/2),0]
                        door_pos = [x_offset3 + (door_width/2 + size1[0]/2)*np.cos(theta - np.pi/2),y_offset3 +  (door_width/2 + size1[0]/2)*np.sin(theta - np.pi/2),0]

                        # self.add_box("first_t2_" + str(i) + str(j) + str(k), door_pos, [0,0,0], [0.3, 0.3, 0.3], box_colour=[0.8,0.8,0.8,1], vis_only=True, shape='cylinder')

                        # x_offset_side1, y_offset_side1 = dist_side1*np.sin(angle_side1-(theta)) + dist_side2*np.cos(phi), dist_side1*np.cos(angle_side1-(theta)) + dist_side2*np.sin(phi)
                        # x_side1, y_side1 = x_offset3 + x_offset_side1, y_offset3 + y_offset_side1
                        x_side1, y_side1 = door_pos[0] + (length_side1/2)*np.cos(theta - phi), door_pos[1] + (length_side1/2)*np.sin(theta - phi)
                        pos_side1 = [ x_side1 ,  y_side1, (z_offset + size1[2])/2]
                        orn = [0,0,(theta-phi)]
                        self.add_box("w4_" + str(i) + str(j) + str(k), pos_side1, orn, size_side1, box_colour=[0.8,0.3,0.5,1])

                    # Choices are: - -, JL, TT, J-, -L, -T, T-, JT, TL
                    # if config == 0:
                    # dist_from_hole1 = 0.5 + size1[0]/2
                    dist_from_hole1 = 1.0 + size1[0]/2
                    dist_from_hole2 = 1.5 + size2[0]/2
                    # elif config in [1,3,4]:
                    #     dist_from_hole1 = 0.5 + size1[0]/2 
                    #     dist_from_hole2 = 1.5 + size2[0]/2 + length_side1
                    # elif config in [2,5,6]:
                    #     dist_from_hole1 = 0.5 + size1[0]/2 + length_side1
                    #     dist_from_hole2 = 1.5 + size2[0]/2 
                    # else:
                    #     dist_from_hole1 = 0.5 + size1[0]/2 + length_side1
                    #     dist_from_hole2 = 1.5 + size2[0]/2 + length_side1

                    size_goal = [0.5, 0.5, 0.35]

                    pos1 = [x_offset3 - dist_from_hole1*np.cos(theta ), y_offset3 - dist_from_hole1*np.sin(theta ), z_offset + size_goal[2]]
                    
                    self.goals[j][i*2] = {'x':pos1[0],'y':pos1[1]}
                    
                    # if floor:
                    self.add_box("first_t2_" + str(i) + str(j) + str(k), pos1, orn, size_goal, box_colour=[0.8,0.8,0.8,1], vis_only=True, shape='cylinder')

                    if not self.args.label_bit:
                        pos2 = [x_offset3 + dist_from_hole2*np.cos(theta ), y_offset3 + dist_from_hole2*np.sin(theta ), z_offset + size_goal[2]]
                    else:
                        # Goal on other side of gap
                        if choice in [1,2]:
                            x_rand = np.sqrt(np.random.uniform(0, dist_from_hole2)) * np.cos(np.random.uniform(0.0, 2.0*np.pi))
                            y_rand = np.sqrt(np.random.uniform(0, dist_from_hole2)) * np.sin(np.random.uniform(0.0, 2.0*np.pi))
                            pos2 = [x_offset3 + dist_from_hole2*np.cos(theta ) + x_rand, y_offset3 + dist_from_hole2*np.sin(theta ) + y_rand, z_offset + size_goal[2]]
                        # Goal on robot side
                        else:
                            dist_from_hole3 = 3.0
                            x_rand = np.sqrt(np.random.uniform(0, dist_from_hole3)) * np.cos(np.random.uniform(0.0, 2.0*np.pi))
                            y_rand = np.sqrt(np.random.uniform(0, dist_from_hole3)) * np.sin(np.random.uniform(0.0, 2.0*np.pi))
                            pos2 = [x_offset3 - dist_from_hole3*np.cos(theta ) + x_rand, y_offset3 - dist_from_hole3*np.sin(theta ) + y_rand, z_offset + size_goal[2]]

                    self.goals[j][i*2 + 1] = {'x':pos2[0],'y':pos2[1]}
                    
                    # if floor:
                    # Goal point
                    self.add_box("second_t2_" + str(i) + str(j) + str(k), pos2, orn, size_goal, box_colour=[0.8,0.8,0.8,1], vis_only=True, shape='cylinder')

                    size_goal = [0.4, 0.4, 0.4]
                    if config == 2:
                        dist_from_hole3 = length_side1
                        pos = [x_offset3 - dist_from_hole3*np.cos(theta ), y_offset3 - dist_from_hole3*np.sin(theta ), z_offset + size_goal[2]]
                    else:
                        pos = [x_offset3, y_offset3, z_offset + size_goal[2]]
                    
                    self.aux_goals[j][i] = {'x':pos[0],'y':pos[1],'yaw': theta,'door_size':door_width, 'label':label}
                    if floor:
                        self.add_box("aux_" + str(i) + str(j) + str(k), pos, orn, size_goal, box_colour=[0.2,0.2,0.8,1], vis_only=True, shape='cylinder')

                    if self.args.train_detector:
                        detect_dist = 3.0
                        x1 = x_offset + (x-detect_dist)*np.cos(theta) + np.sqrt(np.random.uniform(0, 2.0)) * np.cos(np.random.uniform(0.0, 2.0*np.pi)) 
                        y1 = y_offset + (x-detect_dist)*np.sin(theta) + np.sqrt(np.random.uniform(0, 2.0)) * np.sin(np.random.uniform(0.0, 2.0*np.pi))
                        x2 = x_offset + (x+detect_dist)*np.cos(theta) + np.sqrt(np.random.uniform(0, 2.0)) * np.cos(np.random.uniform(0.0, 2.0*np.pi)) 
                        y2 = y_offset + (x+detect_dist)*np.sin(theta) + np.sqrt(np.random.uniform(0, 2.0)) * np.sin(np.random.uniform(0.0, 2.0*np.pi))
                        pos_detect1 = [x1, y1, size_goal[2]]
                        pos_detect2 = [x2, y2, size_goal[2]]
                        self.detect_goals[j][i*2] = {'x':pos_detect1[0],'y':pos_detect1[1], 'door_size':None}
                        self.detect_goals[j][i*2 + 1] = {'x':pos_detect2[0],'y':pos_detect2[1], 'door_size':door_width}
                        # if label:
                        #     self.add_box("first_detect_" + str(i) + str(j) + str(k), pos_detect1, orn, size_goal, box_colour=[0.2,0.8,0.2,1], vis_only=True, shape='cylinder')
                        #     self.add_box("second_detect_" + str(i) + str(j) + str(k), pos_detect2, orn, size_goal, box_colour=[0.2,0.8,0.2,1], vis_only=True, shape='cylinder')
                        # else:
                        #     self.add_box("first_detect_" + str(i) + str(j) + str(k), pos_detect1, orn, size_goal, box_colour=[0.2,0.2,0.2,1], vis_only=True, shape='cylinder')
                        #     self.add_box("second_detect_" + str(i) + str(j) + str(k), pos_detect2, orn, size_goal, box_colour=[0.2,0.2,0.2,1], vis_only=True, shape='cylinder')

                    if i == 1:
                        size2 = [0.4, 0.4, 0.35]
                        x_offset2, y_offset2 = x_offset + 7.0*np.cos(theta), y_offset + 7.0*np.sin(theta)
                        pos = [x_offset2, y_offset2, z_offset + size2[2]]
                        self.goals[j][4] = {'x':x_offset2,'y':y_offset2}
                        # self.add_box("targ_" + str(i) + str(j) + str(k), [self.goals[j][4]['x'], self.goals[j][4]['y'], pos[2]], orn, size2, box_colour=[0.8,0.8,0.8,1], vis_only=True, shape='cylinder')
                    x += ground_size[0]*2/3
            
    def add_doors(self, difficulty, individual=False, rank=0):
        # Flat box
        # self.add_box([1, -1.5, 1], [0,0,0], [0.2,1,1], colour=[0.8,0.3,0.5,1])
        # self.add_box([1, 1.5, 1], [0,0,0.5], [0.2,1,1], colour=[0.8,0.3,0.5,1])


        # self.add_box([50, -1.5, 1], [0,0,0], [0.2,1,1], colour=[0.8,0.3,0.5,1])
        # self.add_box([50, 1.5, 1], [0,0,0.5], [0.2,1,1], colour=[0.8,0.3,0.5,1])
        difficulty_range = 4
        self.goals = {j:{k:{i:{'y':0} for i in range(4)} for k in range(difficulty_range)} for j in range(self.num_workers)}
        # self.goals = np.array([])
        for k in range(difficulty_range):
            x_offset = k*20
            if individual:
                j = rank
                y_offset = rank*15
                # ground_size = [9, np.random.uniform(3, 5), 1]
                ground_size = [9, 3, 1]
                # ground_size = [9, 2, 1]
                ground_pos = [ground_size[0] - 1.0 + x_offset, y_offset, ground_size[2]]
                ground_orn = [0,0,0]
                self.add_box("g0" + str(j) + str(k), ground_pos, ground_orn, [ground_size[0]*2, ground_size[1]*2, ground_size[2]*2], box_colour=[0.3,0.3,0.8,1])
                
                x_min = ground_pos[0] - ground_size[0] - 0.2
                x_max = ground_pos[0] + ground_size[0] + 0.2
                y_min = ground_pos[1] - ground_size[1] - 0.2
                y_max = ground_pos[1] + ground_size[1] + 0.2
                size_x = [ground_size[0], 0.2, 2]
                size_y = [0.2, ground_size[1] + size_x[1]*2, 2]

                self.add_box("g1" + str(j) + str(k), [ground_pos[0], y_min, size_x[2]],[0,0,0],  [size_x[0]*2, size_x[1]*2, size_x[2]*2], box_colour=[0.3,0.8,0.5,1])
                self.add_box("g2" + str(j) + str(k), [ground_pos[0], y_max, size_x[2]], [0,0,0], [size_x[0]*2, size_x[1]*2, size_x[2]*2], box_colour=[0.3,0.8,0.5,1])
                self.add_box("g3" + str(j) + str(k), [x_min, ground_pos[1], size_y[2]], [0,0,0], [size_y[0]*2, size_y[1]*2, size_y[2]*2], box_colour=[0.3,0.8,0.5,1])
                self.add_box("g4" + str(j) + str(k), [x_max, ground_pos[1], size_y[2]], [0,0,0], [size_y[0]*2, size_y[1]*2, size_y[2]*2], box_colour=[0.3,0.8,0.5,1])

                # pos = np.
                # for _ in range(10):
                ground_width = ground_size[1]*2
                # z_offset = ground_pos[2] + ground_size[2]*2
                z_offset = ground_pos[2] + ground_size[2]/2
                # x = np.random.uniform(6,8)

                x = 6
                # 1-10   
                for i in range(2):
                    #  x += 8
                    # door_width = (-0.261*difficulty + 3.26)
                    door_width = 0.9

                    wall =  (ground_width - door_width)

                    
                    # size = [0.2*2, wall/2, 2]
                    # size = [0.2, wall/2, 2]

                    first_wall = np.random.uniform(0.2, wall-0.2)
                    # first_wall = np.random.uniform(0.5, wall-0.5)
                    second_wall = wall - first_wall
                    # print(ground_width, door_width, wall, first_wall, second_wall)

                    # size = [0.2, first_wall, 2]
                    size = [1.0, first_wall, 2]
                    pos = [x + x_offset, (size[1]/2 + door_width/2) + y_offset, (z_offset + size[2])/2]
                    pos = [x + x_offset, (ground_width/2 - size[1]/2) + y_offset, (z_offset + size[2])/2]
                    # pos = [x + x_offset, (size[1] + door_width)/2 + y_offset, (z_offset + size[2])/2]
                    orn = [0,0,0]
                    self.add_box("w1_" + str(i) + str(j) + str(k), pos, orn, [size[0], size[1], size[2]], box_colour=[0.8,0.3,0.5,1])
                    # size = [size[0], wall/2, 2]

                    size = [size[0], second_wall, 2]
                    assert (first_wall > 0 and second_wall > 0)

                    pos = [x + x_offset, (-ground_width/2 + size[1]/2) + y_offset, (z_offset + size[2])/2]
                    # pos = [x + x_offset, -(size[1]/2 + door_width/2) + y_offset, (z_offset + size[2])/2]
                    orn = [0,0,0]
                    self.add_box("w2_" + str(i) + str(j) + str(k), pos, orn, [size[0], size[1], size[2]], box_colour=[0.8,0.3,0.5,1])
                    # x += np.random.uniform(5,7)

                    self.goals[j][k][i*2] = {'x':x + x_offset - 1.5,'y':(-ground_width/2 + size[1] + door_width/2) + y_offset}
                    self.goals[j][k][i*2+1] = {'x':x + x_offset + 1.5,'y':(-ground_width/2 + size[1] + door_width/2) + y_offset}
                    
                    # size1 = [0.2, 0.2, 0.4]
                    # pos = [x + x_offset, (-ground_width/2 + size[1] + door_width/2) + y_offset, z_offset + size1[2]]
                    # pos = [x + x_offset, pos[1] - size[1]/2 - door_width/2, z_offset]
                    # self.add_box("first_t1_" + str(i) + str(j) + str(k), [self.goals[j][k][i*2]['x'], self.goals[j][k][i*2]['y'], pos[2]], orn, size1, box_colour=[0.3,0.3,0.3,1], vis_only=True, shape='cylinder')
                    # self.add_box("second_t1_" + str(i) + str(j) + str(k), [self.goals[j][k][i*2+1]['x'], self.goals[j][k][i*2+1]['y'], pos[2]], orn, size1, box_colour=[0.3,0.3,0.3,1], vis_only=True, shape='cylinder')
                    size2 = [0.5, 0.5, 0.35]
                    pos = [x + x_offset, (-ground_width/2 + size[1] + door_width/2) + y_offset, z_offset + size2[2]]
                    # pos = [x + x_offset + 1.5, (ground_width/2 - size1[1]/2 - door_width/2) + y_offset, (z_offset + size1[2])/2 + 1.5]
                    self.add_box("first_t2_" + str(i) + str(j) + str(k), [self.goals[j][k][i*2]['x'], self.goals[j][k][i*2]['y'], pos[2]], orn, size2, box_colour=[0.8,0.8,0.8,1], vis_only=True, shape='cylinder')
                    self.add_box("second_t2_" + str(i) + str(j) + str(k), [self.goals[j][k][i*2+1]['x'], self.goals[j][k][i*2+1]['y'], pos[2]], orn, size2, box_colour=[0.8,0.8,0.8,1], vis_only=True, shape='cylinder')
                    x += 6
            else:
                for j in range(self.num_workers):
                    y_offset = j*15
                    # ground_size = [9, np.random.uniform(3, 5), 1]
                    ground_size = [9, 3, 1]
                    # ground_size = [9, 2, 1]
                    ground_pos = [ground_size[0] - 1.0 + x_offset, y_offset, ground_size[2]]
                    ground_orn = [0,0,0]
                    self.add_box("g0" + str(j) + str(k), ground_pos, ground_orn, [ground_size[0]*2, ground_size[1]*2, ground_size[2]*2], box_colour=[0.3,0.3,0.8,1])
                    
                    x_min = ground_pos[0] - ground_size[0] - 0.2
                    x_max = ground_pos[0] + ground_size[0] + 0.2
                    y_min = ground_pos[1] - ground_size[1] - 0.2
                    y_max = ground_pos[1] + ground_size[1] + 0.2
                    size_x = [ground_size[0], 0.2, 2]
                    size_y = [0.2, ground_size[1] + size_x[1]*2, 2]

                    self.add_box("g1" + str(j) + str(k), [ground_pos[0], y_min, size_x[2]],[0,0,0],  [size_x[0]*2, size_x[1]*2, size_x[2]*2], box_colour=[0.3,0.8,0.5,1])
                    self.add_box("g2" + str(j) + str(k), [ground_pos[0], y_max, size_x[2]], [0,0,0], [size_x[0]*2, size_x[1]*2, size_x[2]*2], box_colour=[0.3,0.8,0.5,1])
                    self.add_box("g3" + str(j) + str(k), [x_min, ground_pos[1], size_y[2]], [0,0,0], [size_y[0]*2, size_y[1]*2, size_y[2]*2], box_colour=[0.3,0.8,0.5,1])
                    self.add_box("g4" + str(j) + str(k), [x_max, ground_pos[1], size_y[2]], [0,0,0], [size_y[0]*2, size_y[1]*2, size_y[2]*2], box_colour=[0.3,0.8,0.5,1])

                    # pos = np.
                    # for _ in range(10):
                    ground_width = ground_size[1]*2
                    # z_offset = ground_pos[2] + ground_size[2]*2
                    z_offset = ground_pos[2] + ground_size[2]/2
                    # x = np.random.uniform(6,8)

                    x = 6
                    # 1-10   
                    #  x += 8
                    # difficulty = k
                    # door_width = (-0.078*np.random.uniform(difficulty-1, difficulty) + 1.578)
                    # door_width = (-0.3*np.random.uniform(difficulty-0.2, difficulty) + 2.3)
                    # door_width = (-0.325*difficulty + 2.325
                    # run_diff = min(difficulty + k, 10)
                    # door_width = (-0.261*run_diff + 3.26)
                    # door_width = (-0.255*run_diff + 3.25)
                    # door_width = (-0.24*run_diff + 3.2)
                    # door_width = (-0.13*run_diff + 2.1)
                    # door_width = 1.5
                    # door_width = (-0.1*difficulty + 1.5)


                    # door_width = (-0.44*difficulty + 5.4)
                    # door_width = (-0.11*difficulty + 2.1)
                    door_width = 2.0
                    # door_width = 1.0
                    # door_width = 5.0
                    wall =  (ground_width - door_width)
                    first_wall1 = np.random.choice([1.5, wall-1.5])
                    if first_wall1 == 1.5:
                        first_wall2 = wall-1.5
                    else:
                        first_wall2 = 1.5
                    first_walls = [first_wall1, first_wall2]
                    for i in range(2):


                        # door_width = np.random.uniform(0.7, 1.0)
                        # size = [0.2, np.random.uniform(ground_width/2-0.4, ground_width/2 + 0.4), 1]
                        # size = [0.2, np.random.uniform(ground_width/2-0.3, ground_width/2 + 0.3), 1]
                        # wall =  (ground_width - door_width - 0.35)

                        
                        # size = [0.2*2, wall/2, 2]
                        # size = [0.2, wall/2, 2]

                        # first_wall = np.random.uniform(0.2, wall-0.2)
                        # first_wall = np.random.uniform(1.5, wall-1.5)
                        # first_wall = np.random.choice([1.0, wall-1.0])
                        first_wall = first_walls[i]
                        # first_wall = np.random.uniform(0.5, wall-0.5)
                        second_wall = wall - first_wall
                        # print(ground_width, door_width, wall, first_wall, second_wall)

                        size = [1.5, first_wall, 3]
                        # pos = [x + x_offset, (size[1]/2 + door_width/2) + y_offset, (z_offset + size[2])/2]
                        pos = [x + x_offset, (ground_width/2 - size[1]/2) + y_offset, (z_offset + size[2])/2]
                        # pos = [x + x_offset, (size[1] + door_width)/2 + y_offset, (z_offset + size[2])/2]
                        orn = [0,0,0]
                        self.add_box("w1_" + str(i) + str(j) + str(k), pos, orn, [size[0], size[1], size[2]], box_colour=[0.8,0.3,0.5,1])
                        

                        size = [size[0], second_wall, size[2]]
                        assert (first_wall > 0 and second_wall > 0)

                        pos = [x + x_offset, (-ground_width/2 + size[1]/2) + y_offset, (z_offset + size[2])/2]
                        # pos = [x + x_offset, -(size[1]/2 + door_width/2) + y_offset, (z_offset + size[2])/2]
                        orn = [0,0,0]
                        self.add_box("w2_" + str(i) + str(j) + str(k), pos, orn, [size[0], size[1], size[2]], box_colour=[0.8,0.3,0.5,1])
                        # x += np.random.uniform(5,7)

                        self.goals[j][k][i*2] = {'x':x + x_offset - 2.0,'y':(-ground_width/2 + size[1] + door_width/2) + y_offset}
                        self.goals[j][k][i*2+1] = {'x':x + x_offset + 1.5,'y':(-ground_width/2 + size[1] + door_width/2) + y_offset}
                        
                        # size1 = [0.2, 0.2, 0.4]
                        # pos = [x + x_offset, (-ground_width/2 + size[1] + door_width/2) + y_offset, z_offset + size1[2]]
                        # pos = [x + x_offset, pos[1] - size[1]/2 - door_width/2, z_offset]
                        # self.add_box("first_t1_" + str(i) + str(j) + str(k), [self.goals[j][k][i*2]['x'], self.goals[j][k][i*2]['y'], pos[2]], orn, size1, box_colour=[0.3,0.3,0.3,1], vis_only=True, shape='cylinder')
                        # self.add_box("second_t1_" + str(i) + str(j) + str(k), [self.goals[j][k][i*2+1]['x'], self.goals[j][k][i*2+1]['y'], pos[2]], orn, size1, box_colour=[0.3,0.3,0.3,1], vis_only=True, shape='cylinder')
                        size2 = [0.5, 0.5, 0.1]
                        pos = [x + x_offset, (-ground_width/2 + size[1] + door_width/2) + y_offset, z_offset + size2[2]]
                        # pos = [x + x_offset + 1.5, (ground_width/2 - size1[1]/2 - door_width/2) + y_offset, (z_offset + size1[2])/2 + 1.5]
                        self.add_box("first_t2_" + str(i) + str(j) + str(k), [self.goals[j][k][i*2]['x'], self.goals[j][k][i*2]['y'], pos[2]], orn, size2, box_colour=[0.8,0.8,0.8,1], vis_only=True, shape='cylinder')
                        self.add_box("second_t2_" + str(i) + str(j) + str(k), [self.goals[j][k][i*2+1]['x'], self.goals[j][k][i*2+1]['y'], pos[2]], orn, size2, box_colour=[0.8,0.8,0.8,1], vis_only=True, shape='cylinder')
                        x += 6
                
        # return self.get_box_insfo(), self.goals

    def teb_world(self):
        # Tile floor with randomness
        # 40x40m
        for i in range(20):
            for j in range(20):
                z = np.random.random()/20
                self.add_box("b"+str(i)+'_'+str(j), [i*2,j*2,z/2], [0,0,0], box_size=[2,2,z])

    def subway(self):
        '''
        Subway platform, has two sets of rails, two stairs out, two platforms, stairs up to a larger block
        '''
        # Block1, Block2, Block3 the main parts
        # b1_size = [40,10,1.25]
        self.add_box("ground", [11,16,0], [0,0,0], box_size=[20,10,0.2])
        self.add_box("b1", [11,26,1.25], [0,0,0], box_size=[20,10,2.5])
        self.add_box("b2", [11,6,1.25], [0,0,0], box_size=[20,10,2.5])
        self.add_box("b3", [26,16,2.5], [0,0,0], box_size=[10,30,5])
        p1 = self.add_stairs(name='stairs1', start_pos=[14,12,0], orn=[0,0,0], size=[0.4,2.0,0.215], up_down='up', number=10)
        p2 = self.add_stairs(name='stairs2', start_pos=[14,20,0], orn=[0,0,0], size=[0.4,2.0,0.215], up_down='up', number=10)
        p3 = self.add_stairs(name='stairs3', start_pos=[14,2,2.4], orn=[0,0,0], size=[0.4,2.0,0.215], up_down='up', number=10)
        p4 = self.add_stairs(name='stairs4', start_pos=[14,30,2.4], orn=[0,0,0], size=[0.4,2.0,0.215], up_down='up', number=10)
        self.add_box("b4", [11,6,3], [0,0,0], box_size=[10,0.5,1])
        self.add_box("b5", [11,26,3], [0,0,0], box_size=[10,0.5,1])
        self.add_box("b6", [26,16,5.5], [0,0,0], box_size=[0.5,10,1])

        #Add tracks
        # self.add_box("t1", [20,35,1.25], [0,0,0], box_size=[40,10,2.5])
        # self.add_box("t2", [20,5,1.25], [0,0,0], box_size=[40,10,2.5])
        # self.add_box("t3", [40,20,2.5], [0,0,0], box_size=[10,40,5])
        # self.add_box("t4", [40,20,2.5], [0,0,0], box_size=[10,40,5])
        #Add a couple of tunnels
        self.respawn_pts = [p1, p2, p3, p4]
    def floor(self):
        self.add_box("floor", [0,0,0], [0,0,0], box_size=[100,100,0.2])
        self.respawn_pts = [[0,0,0.2]]

    def doughnut(self):
        self.respawn_pts = []

        pos_x = 8
        # self.add_box("ground", [pos_x,pos_x,0], [0,0,0], box_size=[16,16,0.2])
        pos = [pos_x,pos_x,0]
        radius = 6
        num_blocks = 10
        box_size = [3,(radius*np.pi*2/num_blocks)+1.2,0.2]
        for i in range(num_blocks):
            box_name = str(i)
            angle = i*2*np.pi/num_blocks
            x = radius*np.cos(angle) + pos_x
            y = radius*np.sin(angle) + pos_x
            self.add_box(box_name + "_floor", [x,y,1], [0,0,angle], box_size=box_size)
            self.respawn_pts.append([x,y,1])

        pos = [0,0,0]
        radius = 7.5
        num_blocks = 10
        box_size = [0.5,radius*np.pi*2/num_blocks,2]
        for i in range(num_blocks):
            box_name = str(i)
            angle = i*2*np.pi/num_blocks
            x = radius*np.cos(angle) + pos_x
            y = radius*np.sin(angle) + pos_x
            self.add_box(box_name + "_outer", [x,y,1], [0,0,angle], box_size=box_size)
            pos = [0,0,0]
            radius = 4.5
            num_blocks = 10
            box_size = [0.5,radius*np.pi*2/num_blocks,2]
        for i in range(num_blocks):
            box_name = str(i)
            angle = i*2*np.pi/num_blocks
            x = radius*np.cos(angle) + pos_x
            y = radius*np.sin(angle) + pos_x
            self.add_box(box_name + "_inner", [x,y,1], [0,0,angle], box_size=box_size)

        # self.respawn_pts = [[2,8,1],[8,2,1],[14,8,1],[8,14,1]]
        pos_x = 8
        pos = [pos_x*3,pos_x*3,0]
        radius = 6
        num_blocks = 10
        box_size = [3,(radius*np.pi*2/num_blocks)+1.2,0.2]
        for i in range(num_blocks):
                box_name = str(i)
                angle = i*2*np.pi/num_blocks
                x = radius*np.cos(angle) + pos_x*3
                y = radius*np.sin(angle) + pos_x*3
                self.add_box(box_name + "_floor2", [x,y,1], [0,0,angle], box_size=box_size)
                self.respawn_pts.append([x,y,1])
                # self.respawn_pts.extend([[pos_x*2+2,pos_x*2+6,1],[pos_x*2+6,pos_x*2+2,1],[pos_x*2+12,pos_x*2+2,1],[pos_x*2+2,pos_x*2+12,1]])
                # self.respawn_pts = [[pos_x*2+2,pos_x*2+6,1],[pos_x*2+6,pos_x*2+2,1],[pos_x*2+12,pos_x*2+2,1],[pos_x*2+2,pos_x*2+12,1]]
                

    def stairs(self, up_down='down'):
        # difficulty = 0
        # rise = difficuslty + np.random.random()
        # rise = 0.2 + -0.2*(1-min(difficulty, 2)/2) + (np.random.random())*0.05
        # run = 0.4 + (np.random.random()-0.5)*0.1*(min(difficulty, 1))
        # width = 6 - np.random.random()*(min(difficulty, 5))
        
        run = 0.4
        rise = 0.2
        width = 1.5
    
        qx,qy,qz,qw = 0,0,0,1
        # num = np.clip(num + (np.random.random()-0.5)/10, 0, 1)
        num = np.random.random()
        qz = np.random.choice((-1, 1))*num
        qw = np.random.choice((-1, 1))*np.sqrt(1 - num**2)
        
        yaw = np.arctan2(2.0 * (qz*qw + qx*qy) , - 1.0 + 2.0 * (qw*qw + qx*qx));
        
        platform_size = [width,width,rise]
        if up_down == 'down':
            p1 = [0,0,20]
        else:
            p1 = [0,0,0]
            p1 = [p1[0] + width + 1, p1[1]+width + 1, p1[2]+rise]   
            self.add_box(box_name="platform", pos=p1, orn=[0,0,yaw], box_size=platform_size)    
            p2 = self.add_stairs(name="stairs1", start_pos=p1, orn=[0,0,yaw], size=[run,width,rise], up_down=up_down, number=10)    
            p3 = self.add_stairs(name="stairs2", start_pos=p2, orn=[0,0,yaw], size=[run,width,rise], up_down=up_down, number=10)
            p4 = self.add_stairs(name="stairs3", start_pos=p3, orn=[0,0,yaw], size=[run,width,rise], up_down=up_down, number=10)
            self.respawn_pts = p1
            self.respawn_orn = [qx, qy, qz, qw]

    def stair_world3(self, x=0,y=0,z=0,difficulty=0):

        p1 = [x,y,0]
        for i in range(4):  
            if i%2 == 0:
                up_down = 'up'
                p1[2] = 0
            else:
                up_down = 'down'
                p1[2] = 8
            rise = 0.2
            run = 0.4
            width = 2
            platform_size = [width,width,rise]
            p2 = [p1[0] + width , p1[1]+width + i*7, p1[2]+rise]   
            self.add_box(box_name="platform"+str(i), pos=p2, orn=[0,0,0], box_size=platform_size)    
            p3 = self.add_stairs(name="stairs1"+str(i), start_pos=p2, orn=[0,0,0], size=[run,width,rise], up_down=up_down, number=10)    

            p4 = self.add_stairs(name="stairs2"+str(i), start_pos=p3, orn=[0,0,0], size=[run,width,rise], up_down=up_down, number=10)

            p5 = self.add_stairs(name="stairs3"+str(i), start_pos=p4, orn=[0,0,0], size=[run,width,rise], up_down=up_down, number=10)
            if i > 1:
                if up_down == 'up':
                    z = 3.25
                else:
                    z = -3.25
                p6 = [p2[0]+10, p2[1]-width/2 - rise/2, p2[2]+z]
                self.add_box(box_name="wall1"+str(i), pos=p6, orn=[0,0,0], box_size=[20,0.2,8])    
                p6 = [p2[0]+10, p2[1]+width/2 + rise/2, p2[2]+z]
                self.add_box(box_name="wall2"+str(i), pos=p6, orn=[0,0,0], box_size=[20,0.2,8])    

            # if i%2 == 0:
            self.respawn_pts.extend([p2, p5])
            # else:

    def stair_world(self, x=0,y=0,z=0,difficulty=0):
        self.respawn_pts = []
        p1 = [x,y,0]
        for i in range(10):  
            if i%2 == 0:
                up_down = 'up'
                p1[2] = 0
            else:
                up_down = 'down'
                p1[2] = 8
            rise = 0.2 + (np.random.random()-0.5)*0.2
            run = 0.45 + (np.random.random()-0.5)*0.2
            width = np.clip(2.5 + (np.random.random()-0.5)*2, 1.5,4.5)
            platform_size = [width,width,rise]
            p2 = [p1[0] + width , p1[1]+width + i*7, p1[2]+rise]   
            self.add_box(box_name="platform"+str(i), pos=p2, orn=[0,0,0], box_size=platform_size)    
            p3 = self.add_stairs(name="stairs1"+str(i), start_pos=p2, orn=[0,0,0], size=[run,width,rise], up_down=up_down, number=10)    
            rise = 0.2 + (np.random.random()-0.5)*0.2
            run = 0.45 + (np.random.random()-0.5)*0.2
            width = np.clip(width + (np.random.random()-0.5), 1.5, 4.5)

            p4 = self.add_stairs(name="stairs2"+str(i), start_pos=p3, orn=[0,0,0], size=[run,width,rise], up_down=up_down, number=10)
            rise = 0.2 + (np.random.random()-0.5)*0.2
            run = 0.45 + (np.random.random()-0.5)*0.2
            width = np.clip(width + (np.random.random()-0.5), 1.5, 4.5)

            p5 = self.add_stairs(name="stairs3"+str(i), start_pos=p4, orn=[0,0,0], size=[run,width,rise], up_down=up_down, number=10)
            # if i%2 == 0:
            self.respawn_pts.extend([p2, p5])
            # else:
                # self.respawn_pts.extend([p5, p2])


    def stair_world2(self, x=0,y=0,z=0,difficulty=0):
        
        rise = difficulty + np.random.random()

        rise = min(0.3, 0.05*difficulty + (np.random.random())*0.025)
        run = 0.4
        width = max(1.25, 6-1*difficulty + (np.random.random())*0.25)


        platform_size = [width,width,rise]
        p1 = [0+x,0+y,0+z]
        p1 = [p1[0] + width + 1, p1[1]+width + 1, p1[2]+rise]   

        # Longitudital near
        p2 = self.add_stairs(name="stairs1", start_pos=p1, orn=[0,0,0], size=[run,width,rise], up_down='up', number=10)    
        p3 = self.add_stairs(name="stairs2", start_pos=p2, orn=[0,0,0], size=[run,width,rise], up_down='up', number=10)
        # Lateral Far
        p4 = self.add_stairs(name="stairs3", start_pos=p3, orn=[0,0,np.pi/2], size=[run,width,rise], up_down='up', number=10)
        p5 = self.add_stairs(name="stairs4", start_pos=p4, orn=[0,0,np.pi/2], size=[run,width,rise], up_down='up', number=10)
        # Lateral Middle
        p6 = self.add_stairs(name="stairs5", start_pos=p2, orn=[0,0,np.pi/2], size=[run,width,rise], up_down='up', number=10)
        p7 = self.add_stairs(name="stairs6", start_pos=p6, orn=[0,0,np.pi/2], size=[run,width,rise], up_down='up', number=10)
        # # Longitudital Middle
        p8 = self.add_stairs(name="stairs7", start_pos=p4, orn=[0,0,np.pi], size=[run,width,rise], up_down='down', number=10)    
        p9 = self.add_stairs(name="stairs8", start_pos=p8, orn=[0,0,np.pi], size=[run,width,rise], up_down='down', number=10)
        # # Longitudital Far
        p10 = self.add_stairs(name="stairs9", start_pos=p5, orn=[0,0,np.pi], size=[run,width,rise], up_down='down', number=10)    
        p11 = self.add_stairs(name="stairs10", start_pos=p10, orn=[0,0,np.pi], size=[run,width,rise], up_down='down', number=10)
        # # Lateral Near
        p12 = self.add_stairs(name="stairs11", start_pos=p11, orn=[0,0,-np.pi/2], size=[run,width,rise], up_down='down', number=10)
        p13 = self.add_stairs(name="stairs12", start_pos=p12, orn=[0,0,-np.pi/2], size=[run,width,rise], up_down='down', number=10)
        # The order of platforms is 0,1,2, in order of height
        self.respawn_pts = [p13, p3, p9, p4, p11, p5]
        
    def add_stairs(self, name, start_pos, orn, size=[0.4,2,0.2], up_down='up', number=10):
        '''
        Creates stairs with a platform at the end. Handles up and down, and changes to orientation (tested for 90 deg turns at least).
        Returns final position of platform at the end.
        '''
        if up_down == 'up': fact = 1
        elif up_down == 'down': fact = -1
        start_pos = [start_pos[0] + (size[1]/2+size[0]/2)*np.cos(orn[2]), start_pos[1] + (size[1]/2+size[0]/2)*np.sin(orn[2]), start_pos[2]+ fact*size[2]]
        for i in range(number):
            box_size = size
            pos = [size[0]*i*np.cos(orn[2]) + start_pos[0], size[0]*i*np.sin(orn[2])+start_pos[1], fact*(size[2]*i)+start_pos[2]]
            self.add_box(box_name="stair_" + name + str(i), pos=pos, orn=orn, box_size=box_size)    
            platform_size = [size[1],size[1],size[2]]
            pos = [pos[0] + (size[1]/2+size[0]/2)*np.cos(orn[2]), pos[1] + (size[1]/2+size[0]/2)*np.sin(orn[2]), pos[2]+fact*size[2]]
            self.add_box(box_name="platform_" + name, pos=pos, orn=orn, box_size=platform_size)    
        return [pos[0], pos[1], pos[2]]

    # def add_box(self, box_name, pos, orn, box_size, box_colour=[0.8, 0.3, 0.3, 1], vis_only=False, shape='box'):
    def add_heightmap(self, hm_path, pos, orn, size, box_colour=[0.8, 0.3, 0.3, 1], vis_only=False):
        '''
        Inserts a box model into root xml. Each position and size is added to buffers (this is what we used to make a heightmap later)
        '''
        # model = ET.SubElement(self.root[0], "model") 
        # model.set("name", box_name)
        # static = ET.SubElement(model, "static")
        # static.text = "true"
        link = ET.SubElement(self.model, "heightmap")


        # link = ET.SubElement(self.model, "link")
        link.set("name", box_name + "_link")
        # Visual
        visual = ET.SubElement(link, "visual")
        visual.set("name", box_name + "_visual")
        pose = ET.SubElement(visual, "pose")
        pose.text = str(pos[0]) + " " + str(pos[1]) + " " + str(pos[2]) + " " + str(orn[0]) + " " + str(orn[1]) + " " + str(orn[2])
        geometry = ET.SubElement(visual, "geometry")
        if shape == 'box':
            box = ET.SubElement(geometry, "box")
            size = ET.SubElement(box, "size")
            size.text = str(box_size[0]) + " " + str(box_size[1]) + " " + str(box_size[2])
        else:
            box = ET.SubElement(geometry, "cylinder")
            radius = ET.SubElement(box, "radius")
            radius.text = str(box_size[0])
            length = ET.SubElement(box, "length")
            length.text = str(box_size[2])
        material = ET.SubElement(visual, "material")
        ambient = ET.SubElement(material, "ambient")
        ambient.text = str(box_colour[0]) + " " + str(box_colour[1]) + " " + str(box_colour[2]) + " " + str(box_colour[3])
        diffuse = ET.SubElement(material, "diffuse")
        diffuse.text = "1 0 0 1"
        specular = ET.SubElement(material, "specular")
        # colour.text = str(box_colour[0]) + " " + str(box_colour[1]) + " " + str(box_colour[2]) + " " + str(box_colour[3])
        specular.text = "0.1 0.1 0.1 1"     
        emissive = ET.SubElement(material, "emissive")
        emissive.text = "0 0 0 0"

    def add_box(self, box_name, pos, orn, box_size, box_colour=[0.8, 0.3, 0.3, 1], vis_only=False, shape='box'):
        '''
        Inserts a box model into root xml. Each position and size is added to buffers (this is what we used to make a heightmap later)
        '''
        # model = ET.SubElement(self.root[0], "model") 
        # model.set("name", box_name)
        # static = ET.SubElement(model, "static")
        # static.text = "true"
        link = ET.SubElement(self.model, "link")
        link.set("name", box_name + "_link")
        # Visual
        visual = ET.SubElement(link, "visual")
        visual.set("name", box_name + "_visual")
        pose = ET.SubElement(visual, "pose")
        pose.text = str(pos[0]) + " " + str(pos[1]) + " " + str(pos[2]) + " " + str(orn[0]) + " " + str(orn[1]) + " " + str(orn[2])
        geometry = ET.SubElement(visual, "geometry")
        if shape == 'box':
            box = ET.SubElement(geometry, "box")
            size = ET.SubElement(box, "size")
            size.text = str(box_size[0]) + " " + str(box_size[1]) + " " + str(box_size[2])
        else:
            box = ET.SubElement(geometry, "cylinder")
            radius = ET.SubElement(box, "radius")
            radius.text = str(box_size[0])
            length = ET.SubElement(box, "length")
            length.text = str(box_size[2])
        material = ET.SubElement(visual, "material")
        ambient = ET.SubElement(material, "ambient")
        ambient.text = str(box_colour[0]) + " " + str(box_colour[1]) + " " + str(box_colour[2]) + " " + str(box_colour[3])
        diffuse = ET.SubElement(material, "diffuse")
        diffuse.text = "1 0 0 1"
        specular = ET.SubElement(material, "specular")
        # colour.text = str(box_colour[0]) + " " + str(box_colour[1]) + " " + str(box_colour[2]) + " " + str(box_colour[3])
        specular.text = "0.1 0.1 0.1 1"     
        emissive = ET.SubElement(material, "emissive")
        emissive.text = "0 0 0 0"

        if not vis_only:
            # Collision
            collision = ET.SubElement(link, "collision")
            collision.set("name", box_name + "_collision")
            pose = ET.SubElement(collision, "pose")
            pose.text = str(pos[0]) + " " + str(pos[1]) + " " + str(pos[2]) + " " + str(orn[0]) + " " + str(orn[1]) + " " + str(orn[2])
            geometry = ET.SubElement(collision, "geometry")
            if shape == 'box':
                box = ET.SubElement(geometry, "box")
                size = ET.SubElement(box, "size")
                size.text = str(box_size[0]) + " " + str(box_size[1]) + " " + str(box_size[2])
            else:
                box = ET.SubElement(geometry, "cylinder")
                radius = ET.SubElement(box, "radius")
                radius.text = str(box_size[0])
                length = ET.SubElement(box, "length")
                length.text = str(box_size[2])
        # pose = ET.SubElement(model, "pose")
        self.box_id.append(len(self.box_id))
        self.positions.append(pos+orn)
        self.sizes.append(box_size)
        self.colours.append(box_colour)

    def get_box_info(self):
        return [self.box_id, self.positions, self.sizes, self.colours]

    
    def test_hm(self, with_pause=False):      
        box_info = self.get_box_info()
        self.world_map = self.get_world_map(box_info)
        # print(box_info)
        import cv2
        norm_wm = (np.min(self.world_map) - self.world_map)/(np.max(self.world_map) - np.min(self.world_map))
        wm_col = cv2.cvtColor(norm_wm,cv2.COLOR_GRAY2RGB)
        cv2.imshow('world_map', wm_col)
        if with_pause:
            cv2.waitKey(0)
            exit()
        else:
            cv2.waitKey(1)

    def transform_rot_and_add(self, yaw, pos, points):
        rot_mat = np.array(
                [[np.cos(yaw), -np.sin(yaw), pos[0]],
                [np.sin(yaw), np.cos(yaw), pos[1]],
                [0, 0, 1]])
        return np.dot(rot_mat,points.T).T.astype(np.int32)

    def get_world_map(self, box_info=None, world_shape=[30,10], grid_size=0.05):
        self.min_x = np.min(np.array(box_info[1])[:,0] - np.array(box_info[2])[:,0]/2)
        self.min_y = np.min(np.array(box_info[1])[:,1] - np.array(box_info[2])[:,1]/2)
        max_x = np.max(np.array(box_info[1])[:,0] + np.array(box_info[2])[:,0]/2)
        max_y = np.max(np.array(box_info[1])[:,1] + np.array(box_info[2])[:,1]/2)
        world_shape = [int((max_x - self.min_x + 2)/grid_size), int((max_y - self.min_y + 2)/grid_size)]

        hm = np.ones([world_shape[0], world_shape[1]]).astype(np.float32)*-1
        if box_info is not None:
            positions = box_info[1]
            sizes = box_info[2]
            for pos, size in zip(positions, sizes):
                x, y, z = pos[0]/grid_size, pos[1]/grid_size, pos[2]
                x_size, y_size, z_size = (size[0]/2)/grid_size, (size[1]/2)/grid_size, size[2]/2
                ij = np.array([[i,j,1] for i in range(int(0-x_size), int(0+x_size)) for j in range(int(0-y_size), int(0+y_size))])

                hm_pts = self.transform_rot_and_add(1*pos[5], [x+(-self.min_x+1)/grid_size, y+(-self.min_y+1)/grid_size], ij)
                for pt in hm_pts:
                    try:
                        if hm[pt[0], pt[1]] < (z + z_size):
                        # if hm[pt[0], pt[1]] == 0:
                            hm[pt[0], pt[1]] = (z + z_size)
                    except Exception as e:
                        print(e)
                        print(pt)

        self.grid_size = grid_size              
        self.dx_forward, self.dx_back, self.dy = 40, 20, 20        
        self.ij = np.array([[i,j,1] for i in range(-self.dx_back, self.dx_forward) for j in range(-self.dy, self.dy)])
        self.hm_ij = np.array([[i,j] for i in range(0, self.dx_back + self.dx_forward) for j in range(0, self.dy + self.dy)])
        return hm

if __name__=="__main__":
  import roslaunch 
  import subprocess 
  import os
  from gazebo_msgs.srv import SetModelState,SetModelConfiguration, SpawnModel, DeleteModel, SpawnModelRequest, SpawnModelResponse

  # stairs = Stairs(world='stairs')
  # stairs = Stairs(world='subway')
  # stairs = Stairs(world='teb_world')
  obstacles = Obstacles()
  obstacles.generate_map()

#   obstacles.initialise_ros_stuff()
#   obstacles.generate_model()
#   obstacles.spawn_model()

#   obstacles.test_hm(with_pause=True)

#   port = 4
#   rank = 0
#   os.environ["ROS_MASTER_URI"] = 'http://localhost:1131' + str(rank+port)
#   os.environ["GAZEBO_MASTER_URI"] = 'http://localhost:1134' + str(rank+port)
#   roscore = subprocess.Popen(['roscore', '-p 1131' + str(rank+port)])
#   time.sleep(2)
  
#   uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
#   # uuid = str(84)
#   cli_args = ['launch/world_test.launch', '-p 1131' + str(rank+port), 'use_gui:=true']
#   # cli_args = ['launch/world_test.launch', 'use_gui:=true']
#   roslaunch_args = cli_args[1:]
#   roslaunch_file = [(roslaunch.rlutil.resolve_launch_arguments(cli_args)[0], roslaunch_args)]
#   parent = roslaunch.parent.ROSLaunchParent(uuid, roslaunch_file)
#   parent.start()
#   print("ROSLAUNCH STARTED..")
#   time.sleep(2)
#   rospy.init_node('insert_object',log_level=rospy.INFO,  anonymous=False)

#   # Need to give nodes time to come up, should be a better way?
#   time.sleep(2)
#   t1 = time.time()

#   while not rospy.is_shutdown():
#     pass

