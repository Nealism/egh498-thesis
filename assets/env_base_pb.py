import pybullet as p
from pybullet_utils import bullet_client
import numpy as np
import os
import math
from copy import deepcopy

from .env_base import EnvBase

try:
    if os.environ["PYBULLET_EGL"]:
        import pkgutil
except:
    pass

class EnvBasePB(EnvBase):
    sim_data = []
    terrainId = None
    # terrain_size = [256,256]
    terrain_size = [1,256,64]
    loaded_sim = False

    def load_robot(self):
        self.load_simulator()

        if not self.args.test or not self.loaded_sim:
            if self.args.urdf:
                self.load_urdf_robot()
            else:
                self.load_xml_robot()
            
            self.motors = [self.jdict[n] for n in self.motor_names]
            
            forces = np.ones(len(self.motors))*240
            self.actions = {key:0.0 for key in self.motor_names}

            p.setJointMotorControlArray(self.Id, self.motors, controlMode=p.VELOCITY_CONTROL, forces=[0.] * len(self.motor_names))

            for key in self.feet_dict:
                p.changeDynamics(self.Id, self.feet_dict[key],lateralFriction=0.9, spinningFriction=0.9)
        
        self.loaded_sim = True

    def load_simulator(self):
        if not self.loaded_sim:
            if self.frameless:
                if self.render and self.master:
                    self._p = bullet_client.BulletClient(connection_mode=p.GUI)
                else:
                    self._p = bullet_client.BulletClient()
            else:
                if self.render and self.master:
                    self.physicsClientId = p.connect(p.GUI)
                else:
                    self.physicsClientId = p.connect(p.DIRECT) 

        if not self.args.test:
            p.resetSimulation()

        p.setPhysicsEngineParameter(deterministicOverlappingPairs=1)
        # #optionally enable EGL for faster headless rendering
        if self.frameless:
            try:
                if os.environ["PYBULLET_EGL"]:
                    con_mode = self._p.getConnectionInfo()['connectionMethod']
                    if con_mode==self._p.DIRECT:
                        egl = pkgutil.get_loader('eglRenderer')
                        if (egl):
                            self._p.loadPlugin(egl.get_filename(), "_eglRendererPlugin")
                        else:
                            self._p.loadPlugin("eglRendererPlugin")
            except:
                pass
            self.physicsClientId = self._p._client
            self._p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
        # ======================================================================

        p.setTimeStep(self.simStep)
        p.setGravity(0,0,-9.8)

        

    def load_urdf_robot(self):
        print("THIS IS TODO: currently has spherical joints, which requires setJointMotorControlMultiDofArray, essentially passing a list of lists, where sperhical joints require a quaterion. In the examples they use p.STABLE_PD control, don't know how this would work with torque (which is what we want)")
        exit()

        p.loadMJCF("./assets/xmls/ground.xml")
        self.model_xml = "./assets/urdfs/humanoid_deep_mimic.urdf"

        # self.Id = p.loadURDF("assets./humanoid_deep_mimic.urdf",flags = p.URDF_USE_SELF_COLLISION | p.URDF_USE_SELF_COLLISION_EXCLUDE_ALL_PARENTS)
        self.Id = p.loadURDF(self.model_xml,
            flags=p.URDF_USE_SELF_COLLISION |
                p.URDF_USE_SELF_COLLISION_EXCLUDE_ALL_PARENTS |
                p.URDF_GOOGLEY_UNDEFINED_COLORS )

        self.jdict = {}
        self.feet_dict = {}
        self.leg_dict = {}
        self.body_dict = {}
        self.feet = ["left_foot", "right_foot"]
        self.feet_contact = {f:True for f in self.feet}
        self.ordered_joints = []
        self.ordered_joint_indices = []
        self.shin_dict = {}
        # self.shins = ["left_shin", "right_shin", "left_thigh", "right_thigh"]
        for j in range( p.getNumJoints(self.Id) ):
            info = p.getJointInfo(self.Id, j)
            link_name = info[12].decode("ascii")
            if link_name in self.feet: self.feet_dict[link_name] = j
            # if link_name in self.shins: self.shin_dict[link_name] = j
            if link_name=="pelvis": self.body_dict["body_link"] = j
            self.ordered_joint_indices.append(j)
            if info[2] != p.JOINT_REVOLUTE: continue
            jname = info[1].decode("ascii")
            print(jname)
            lower, upper = (info[8], info[9])
            self.ordered_joints.append( (j, lower, upper) )
            self.jdict[jname] = j
    
        self.motor_names += ["right_hip"] # left shoulder
        self.motor_names += ["right_knee"] # left elbow
        self.motor_names += ["right_ankle"]
        self.motor_names += ["left_hip"] # right shoulder
        self.motor_names += ["left_knee"]  # right elbow
        self.motor_names += ["left_ankle"]
        self.motor_names += ["neck"]
        self.motor_names += ["chest"]
        self.motor_names += ["abdomen_x"]
        self.motor_names += ["right_shoulder"]
        self.motor_names += ["right_elbow"]
        self.motor_names += ["left_shoulder"]
        self.motor_names += ["left_elbow"]

        self.motor_power = [30]#"right_hip_y"]
        self.motor_power += [20]#"right_hip_x"]
        self.motor_power += [20]#"right_hip_z"]
        self.motor_power += [20]#"right_knee"]
        self.motor_power += [10]#"right_ankle_x"]
        self.motor_power += [10]#"right_ankle_y"]
        self.motor_power += [20]#"left_hip_z"]
        self.motor_power += [20]#"left_hip_x"]
        self.motor_power += [30]#"left_hip_y"]
        self.motor_power += [20]#"left_knee"]
        self.motor_power += [10]#"left_ankle_x"]
        self.motor_power += [10]#"left_ankle_y"]
        self.motor_power +=  [1]#"abdomen_z"]
        self.motor_power += [1]#"abdomen_y"]
        self.motor_power += [1]#"abdomen_x"]
        self.motor_power += [10]#"right_shoulder1"]
        self.motor_power += [10]#"right_shoulder2"]
        self.motor_power += [10]#"right_elbow"]
        self.motor_power += [10]#"left_shoulder1"]
        self.motor_power += [10]#"left_shoulder2"]
        self.motor_power += [10]#"left_elbow"]

    def load_xml_robot(self):

        if self.with_feet:
            self.model_xml = "./assets/xmls/humanoid.xml"
        else:
            self.model_xml = "./assets/xmls/humanoid_symmetric.xml"
        # if self.self_collision:
        # Ground and robot
        # self.objects = p.loadMJCF(os.path.join(pybullet_data.getDataPath(), "mjcf",
        #                                             self.model_xml),
        objects = p.loadMJCF(self.model_xml,
                                        flags=p.URDF_USE_SELF_COLLISION |
                                            p.URDF_USE_SELF_COLLISION_EXCLUDE_ALL_PARENTS |
                                            p.URDF_GOOGLEY_UNDEFINED_COLORS )

        # objects = p.loadMJCF(self.model_xml,
        #                                 flags=
        #                                     p.URDF_USE_SELF_COLLISION_EXCLUDE_ALL_PARENTS |
        #                                     p.URDF_GOOGLEY_UNDEFINED_COLORS )
        self.worldId = objects[0]
        self.Id = objects[1]
        self.jdict = {}
        self.feet_dict = {}
        self.leg_dict = {}
        self.body_dict = {}
        self.feet = ["left_foot", "right_foot"]
        self.feet_contact = {f:True for f in self.feet}
        self.ordered_joints = []
        self.ordered_joint_indices = []
        self.shin_dict = {}
        self.arm_dict = {}
        self.shins = ["left_shin", "right_shin", "left_thigh", "right_thigh"]
        self.arms = ["left_upper_arm", "left_lower_arm", "right_upper_arm", "right_lower_arm"]
        for j in range( p.getNumJoints(self.Id) ):
            info = p.getJointInfo(self.Id, j)
            link_name = info[12].decode("ascii")
            # print(link_name)
            if link_name in self.feet: self.feet_dict[link_name] = j
            if link_name in self.shins: self.shin_dict[link_name] = j
            if link_name in self.arms: self.arm_dict[link_name] = j
            if link_name=="pelvis": self.body_dict["body_link"] = j
            self.ordered_joint_indices.append(j)
            if info[2] != p.JOINT_REVOLUTE: continue
            jname = info[1].decode("ascii")
            lower, upper = (info[8], info[9])
            self.ordered_joints.append( (j, lower, upper) )
            self.jdict[jname] = j
        
        # Do not change this order!! Else joint postions will be wrong
        self.motor_names = ["abdomen_z"]
        self.motor_names += ["abdomen_y"]
        self.motor_names += ["abdomen_x"]
        self.motor_names += ["right_hip_x"] #1 
        self.motor_names += ["right_hip_z"] #0 
        self.motor_names += ["right_hip_y"] #2 5
        self.motor_names += ["right_knee"]  #3 6
        self.motor_names += ["right_ankle_y"] #5 7
        self.motor_names += ["right_ankle_x"] #4
        self.motor_names += ["left_hip_x"] #7
        self.motor_names += ["left_hip_z"] #6
        self.motor_names += ["left_hip_y"] #8 11
        self.motor_names += ["left_knee"] #9 12
        self.motor_names += ["left_ankle_y"] #11 13
        self.motor_names += ["left_ankle_x"] #10
        self.motor_names += ["right_shoulder1"]
        self.motor_names += ["right_shoulder2"]
        self.motor_names += ["right_elbow"]
        self.motor_names += ["left_shoulder1"]
        self.motor_names += ["left_shoulder2"]
        self.motor_names += ["left_elbow"]
        self.motor_power =  [10]#"abdomen_z"]
        self.motor_power += [10]#"abdomen_y"]
        self.motor_power += [10]#"abdomen_x"]
        self.motor_power += [20]#"right_hip_x"]
        self.motor_power += [20]#"right_hip_z"]
        self.motor_power += [30]#"right_hip_y"]
        self.motor_power += [20]#"right_knee"]
        self.motor_power += [10]#"right_ankle_y"]
        self.motor_power += [10]#"right_ankle_x"]
        self.motor_power += [20]#"left_hip_x"]
        self.motor_power += [20]#"left_hip_z"]
        self.motor_power += [30]#"left_hip_y"]
        self.motor_power += [20]#"left_knee"]
        self.motor_power += [10]#"left_ankle_y"]
        self.motor_power += [10]#"left_ankle_x"]
        self.motor_power += [10]#"right_shoulder1"]
        self.motor_power += [10]#"right_shoulder2"]
        self.motor_power += [10]#"right_elbow"]
        self.motor_power += [10]#"left_shoulder1"]
        self.motor_power += [10]#"left_shoulder2"]
        self.motor_power += [10]#"left_elbow"]

    def set_position(self, pos=[0,0,0], orn=[0,0,0,1], joints=None, velocities=None, joint_vel=None, robot_id=None):
        if robot_id is None:
            robot_id = self.Id
        pos = [pos[0], pos[1], pos[2]]
        p.resetBasePositionAndOrientation(robot_id, pos, orn)
        if joints is not None:
            if joint_vel is not None:
                for j, jv, m in zip(joints, joint_vel, self.motors):
                    p.resetJointState(robot_id, m, targetValue=j, targetVelocity=jv)
            else:
                for j, m in zip(joints, self.motors):
                    p.resetJointState(robot_id, m, targetValue=j)
        if velocities is not None:
            p.resetBaseVelocity(robot_id, velocities[0], velocities[1]) 
    
    def get_env_state(self):
        # For some reason getting the entire class dict doesn't work with MPI
        return deepcopy({state:self.__dict__[state] for state in self.states if state in self.__dict__})

    def restore_env_state(self, params):
        for key in params:
            self.__dict__[key] = params[key]
        self.set_position(self.pos, self.orn, self.joints, self.joint_vel) 

    def assign_terrain(self, ter):
        self.terrain = ter

    def reset_terrain(self, angle=0):
        # pos = self._p.getAABB(self.robot.objects[0])
        pos = self._p.getAABB(self.Id)
        rayStart = [(pos[0][0]+pos[1][0])/2,(pos[0][1]+pos[1][1])/2,-2]
        rayEnd = [(pos[0][0]+pos[1][0])/2,(pos[0][1]+pos[1][1])/2,2]
        # self._p.resetBasePositionAndOrientation(self.stadium_scene.t,[0,0,0], self._p.getQuaternionFromEuler([0,0,(1/4)*math.pi*angle]))
        self.load_terrain(angle, pos=[0,0,0])
        rayOutput = self._p.rayTest(rayStart, rayEnd)
        terrain_height = -rayOutput[0][3][2] + pos[0][2] - abs(pos[0][2]-pos[1][2])*2 - 0.3
        # self._p.resetBasePositionAndOrientation(self.stadium_scene.t,[0,0,terrain_height], self._p.getQuaternionFromEuler([0,0,(1/4)*math.pi*angle]))
        self.load_terrain(pos=[0,0,terrain_height], angle=angle)

    def load_terrain(self, terrain=None, pos=[7,0,0], angle=0):
        if terrain is not None:
            self.terrain = terrain

        # This works (removes terrain), but still a significant memory leak so reseting is required
        if self.args.test and self.terrainId:
            p.removeBody(self.terrainId)
            
        p.configureDebugVisualizer(p.COV_ENABLE_RENDERING,0)

        channels, rows, cols = self.terrain.shape
        heightfieldData = np.flip(self.terrain, 0).reshape(-1)
        flags = p.GEOM_CONCAVE_INTERNAL_EDGE
        # flags = None
        self.terrain_collision_shape = p.createCollisionShape(shapeType = p.GEOM_HEIGHTFIELD, flags=flags, meshScale=[.05,.05,0.35], heightfieldData=heightfieldData, numHeightfieldRows=rows, numHeightfieldColumns=cols)
        self.terrainId  = p.createMultiBody(self.worldId, self.terrain_collision_shape, basePosition=[7,0,0], baseOrientation=p.getQuaternionFromEuler([0,0,(1/4)*math.pi*angle]))
        
        p.configureDebugVisualizer(p.COV_ENABLE_RENDERING,1)
