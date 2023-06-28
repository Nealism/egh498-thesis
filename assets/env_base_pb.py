import pybullet as p
from pybullet_utils import bullet_client
import numpy as np
import os
import math

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
    terrain = np.zeros(terrain_size)

    def load_robot(self):
        self.load_simulator()

        if not self.args.test or not self.loaded_sim:
            self.load_specific_robot()
        
        self.loaded_sim = True

    def load_simulator(self):
        if not self.loaded_sim:
            if self.args.frameless:
                if self.render and self.master:
                    self._p = bullet_client.BulletClient(connection_mode=p.GUI)
                    p.resetDebugVisualizerCamera(cameraDistance=7, cameraYaw=0, cameraPitch=-30, cameraTargetPosition=[0,0,0])
                else:
                    self._p = bullet_client.BulletClient()
            else:
                if self.render and self.master:
                    self.physicsClientId = p.connect(p.GUI)
                    p.resetDebugVisualizerCamera(cameraDistance=7, cameraYaw=0, cameraPitch=-70, cameraTargetPosition=[0.55,-0.35,0])
                else:
                    self.physicsClientId = p.connect(p.DIRECT) 

        if not self.args.test:
            p.resetSimulation()

        p.setPhysicsEngineParameter(deterministicOverlappingPairs=1)
        # #optionally enable EGL for faster headless rendering
        if self.args.frameless:
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

        
    def load_urdf_robot(self, model_path):
        objects = p.loadMJCF("./assets/xmls/ground.xml")
        self.worldId = objects[0]
        #self.worldId = p.loadURDF("/home/kom018/Phd_codes/Brendan/Wall_URDF/simpleplane.urdf")
        self.Id = p.loadURDF(model_path,
                            flags=
                                # p.URDF_USE_SELF_COLLISION | Turn off self collision, kills the titan
                                  p.URDF_USE_SELF_COLLISION_EXCLUDE_ALL_PARENTS |
                                  p.URDF_GOOGLEY_UNDEFINED_COLORS )
        
    def load_urdf_robot2(self, model_path):
        #objects = p.loadMJCF("./assets/xmls/ground.xml")
        #self.worldId = objects[0]
        #self.worldId = p.loadURDF("/home/kom018/Phd_codes/Brendan/Wall_URDF/simpleplane.urdf")
        self.Id2 = p.loadURDF(model_path,
                            flags=
                                # p.URDF_USE_SELF_COLLISION | Turn off self collision, kills the titan
                                  p.URDF_USE_SELF_COLLISION_EXCLUDE_ALL_PARENTS |
                                  p.URDF_GOOGLEY_UNDEFINED_COLORS )

    def load_xml_robot(self, model_path):
        objects = p.loadMJCF(model_path,
                            flags=p.URDF_USE_SELF_COLLISION |
                                  p.URDF_USE_SELF_COLLISION_EXCLUDE_ALL_PARENTS |
                                  p.URDF_GOOGLEY_UNDEFINED_COLORS )

        self.worldId = objects[0]
        self.Id = objects[1]

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

    def set_position2(self, pos=[3,3,0], orn=[0,0,0,1], joints=None, velocities=None, joint_vel=None, robot_id=None):
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

    def load_terrain(self, terrain=None, pos=[-2,0,0], angle=0):
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
        #self.worldId=p.loadMJCF("./assets/xmls/ground.xml")
        self.terrain_collision_shape = p.createCollisionShape(shapeType = p.GEOM_HEIGHTFIELD, flags=flags, meshScale=[.05,.05,0.35], heightfieldData=heightfieldData, numHeightfieldRows=rows, numHeightfieldColumns=cols)
        self.terrainId  = p.createMultiBody(self.worldId, self.terrain_collision_shape, basePosition=[0,0,0], baseOrientation=p.getQuaternionFromEuler([0,0,(1/4)*math.pi*angle]))
        
        p.configureDebugVisualizer(p.COV_ENABLE_RENDERING,1)


    

    def load_urdf_humanoid(self):
        ''' 
        Note on loading deep mimic humanoid from urdf:
        print("THIS IS TODO: currently has spherical joints, which requires setJointMotorControlMultiDofArray, essentially passing a list of lists, where sperhical joints require a quaterion. In the examples they use p.STABLE_PD control, don't know how this would work with torque (which is what we want)")
        '''

        p.loadMJCF("./assets/xmls/ground.xml")
        self.model_xml = "./assets/urdfs/humanoid_deep_mimic.urdf"

        # self.Id = p.loadURDF("assets./humanoid_deep_mimic.urdf",flags = p.URDF_USE_SELF_COLLISION | p.URDF_USE_SELF_COLLISION_EXCLUDE_ALL_PARENTS)
        self.Id = p.loadURDF(self.model_xml,
            flags=p.URDF_USE_SELF_COLLISION |
                p.URDF_USE_SELF_COLLISION_EXCLUDE_ALL_PARENTS |
                p.URDF_GOOGLEY_UNDEFINED_COLORS )

        # self.jdict = {}
        # self.feet_dict = {}
        # self.leg_dict = {}
        # self.body_dict = {}
        # self.feet = ["left_foot", "right_foot"]
        # self.feet_contact = {f:True for f in self.feet}
        # self.ordered_joints = []
        # self.ordered_joint_indices = []
        # self.shin_dict = {}
        # # self.shins = ["left_shin", "right_shin", "left_thigh", "right_thigh"]
        # for j in range( p.getNumJoints(self.Id) ):
        #     info = p.getJointInfo(self.Id, j)
        #     link_name = info[12].decode("ascii")
        #     if link_name in self.feet: self.feet_dict[link_name] = j
        #     # if link_name in self.shins: self.shin_dict[link_name] = j
        #     if link_name=="pelvis": self.body_dict["body_link"] = j
        #     self.ordered_joint_indices.append(j)
        #     if info[2] != p.JOINT_REVOLUTE: continue
        #     jname = info[1].decode("ascii")
        #     print(jname)
        #     lower, upper = (info[8], info[9])
        #     self.ordered_joints.append( (j, lower, upper) )
        #     self.jdict[jname] = j
    
        # self.motor_names += ["right_hip"] # left shoulder
        # self.motor_names += ["right_knee"] # left elbow
        # self.motor_names += ["right_ankle"]
        # self.motor_names += ["left_hip"] # right shoulder
        # self.motor_names += ["left_knee"]  # right elbow
        # self.motor_names += ["left_ankle"]
        # self.motor_names += ["neck"]
        # self.motor_names += ["chest"]
        # self.motor_names += ["abdomen_x"]
        # self.motor_names += ["right_shoulder"]
        # self.motor_names += ["right_elbow"]
        # self.motor_names += ["left_shoulder"]
        # self.motor_names += ["left_elbow"]

        # self.motor_power = [30]#"right_hip_y"]
        # self.motor_power += [20]#"right_hip_x"]
        # self.motor_power += [20]#"right_hip_z"]
        # self.motor_power += [20]#"right_knee"]
        # self.motor_power += [10]#"right_ankle_x"]
        # self.motor_power += [10]#"right_ankle_y"]
        # self.motor_power += [20]#"left_hip_z"]
        # self.motor_power += [20]#"left_hip_x"]
        # self.motor_power += [30]#"left_hip_y"]
        # self.motor_power += [20]#"left_knee"]
        # self.motor_power += [10]#"left_ankle_x"]
        # self.motor_power += [10]#"left_ankle_y"]
        # self.motor_power +=  [1]#"abdomen_z"]
        # self.motor_power += [1]#"abdomen_y"]
        # self.motor_power += [1]#"abdomen_x"]
        # self.motor_power += [10]#"right_shoulder1"]
        # self.motor_power += [10]#"right_shoulder2"]
        # self.motor_power += [10]#"right_elbow"]
        # self.motor_power += [10]#"left_shoulder1"]
        # self.motor_power += [10]#"left_shoulder2"]
        # self.motor_power += [10]#"left_elbow"]