import xml.etree.ElementTree as ET
import rospy
import time
from geometry_msgs.msg import Pose
import numpy as np
from gazebo_msgs.srv import SetModelState,SetModelConfiguration, SpawnModel, DeleteModel, SpawnModelRequest, SpawnModelResponse
import time
# from rand_heightmap_generator import HeightMapGenerator

class Obstacles():
    def __init__(self, rank=0, num_workers=1, args=None):
        '''
        Creates an xml, and saves to test.world. test.world is then roslaunched in run.py. 
        TODO explore reseting the simulation/reloading the world file
        '''
        self.rank = rank
        self.args = args
        self.req = SpawnModelRequest()
        self.spawn_model_srv = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
        self.delete_model_srv = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)
        self.box_num = 0
        self.num_workers = num_workers
        # self.hm_gen = HeightMapGenerator()
        
    def spawn_model(self):
        sdf = ET.tostring(self.root).decode("utf-8") 
        # print(sdf)
        self.req.model_xml = sdf
        # print("waiting to spawn")
        # print(sdf)
        self.spawn_model_srv.wait_for_service()
        # t1 = time.time()
        spawned = self.spawn_model_srv(self.req)
        # print("spawned world took", time.time() - t1)

        return self.get_box_info(), self.goals, self.aux_goals, self.detect_goals

        # time.sleep(2)

    def delete_model(self):
        self.delete_model_srv.wait_for_service()
        deleted = self.delete_model_srv(self.args.obstacle_type)
        # print(deleted)
        # time.sleep(1)
    
    def generate_model(self, difficulty=1, individual=False, rank=0):

        # if self.world == 'stairs' or self.world == 'teb_world':
        self.tree = ET.parse('gazebo/worlds/blank.world')
        # self.tree = ET.parse('gazebo/worlds/empty2.world')
        # else:
        #   self.tree = ET.parse('gazebo/worlds/ground.world')
        self.root = self.tree.getroot()
        self.model = ET.SubElement(self.root[0], "model") 
        self.model.set("name", self.args.obstacle_type)
        static = ET.SubElement(self.model, "static")
        static.text = "true"
                        
        

        self.write_data()
        
    
    def write_data(self):
        self.tree.write('gazebo/models/test/model.sdf')


if __name__=="__main__":
    import roslaunch 
    import subprocess 
    import os
    from gazebo_msgs.srv import SetModelState,SetModelConfiguration, SpawnModel, DeleteModel, SpawnModelRequest, SpawnModelResponse

    # stairs = Stairs(world='stairs')
    # stairs = Stairs(world='subway')
    stairs = Stairs(world='doughnut')
    # stairs = Stairs(world='teb_world')
    stairs.generate_model()
    stairs.test_hm(with_pause=True)

    port = 4
    rank = 0
    os.environ["ROS_MASTER_URI"] = 'http://localhost:1131' + str(rank+port)
    os.environ["GAZEBO_MASTER_URI"] = 'http://localhost:1134' + str(rank+port)
    roscore = subprocess.Popen(['roscore', '-p 1131' + str(rank+port)])
    time.sleep(2)
    
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    # uuid = str(84)
    cli_args = ['launch/world_test.launch', '-p 1131' + str(rank+port), 'use_gui:=true']
    # cli_args = ['launch/world_test.launch', 'use_gui:=true']
    roslaunch_args = cli_args[1:]
    roslaunch_file = [(roslaunch.rlutil.resolve_launch_arguments(cli_args)[0], roslaunch_args)]
    parent = roslaunch.parent.ROSLaunchParent(uuid, roslaunch_file)
    parent.start()
    print("ROSLAUNCH STARTED..")
    time.sleep(2)
    rospy.init_node('insert_object',log_level=rospy.INFO,  anonymous=False)

    # Need to give nodes time to come up, should be a better way?
    time.sleep(2)
    t1 = time.time()

    while not rospy.is_shutdown():
        pass
