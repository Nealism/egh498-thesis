from .env_base import EnvBase
import mujoco
import numpy as np
from scipy.spatial.transform import Rotation

class EnvBaseMJ(EnvBase):

    def set_position(self, pos=None, orn=None, joints=None, joint_vel=None):
        base_id = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_BODY, self.base_link)
        if pos is not None:
            for i in range(len(pos)):
                self.model.body_pos[base_id,i] = pos[i]
        # Mujoco quaternions are w,x,y,z, handle that here. Treat as x,y,z,w, elsewhere
        if orn is not None:
            self.model.body_quat[base_id,0] = orn[3]
            self.model.body_quat[base_id,1] = orn[0]
            self.model.body_quat[base_id,2] = orn[1]
            self.model.body_quat[base_id,3] = orn[2]
            
        if joints is not None:
            for value, name in zip(joints, self.motor_names):
                self.set_joint_qpos(name, value)
       
        if joint_vel is not None:
            for value, name in zip(joint_vel, self.motor_names):
                self.set_joint_qvel(name, value)

    # ==========================================================================
    # Helpers from mujoco_py and custom (these aren't supported by 'mujoco' python module)
    # ==========================================================================
    def add_axis(self, pos, orn):
        if isinstance(orn, Rotation):
            rot = orn
        elif len(orn) == 3:
            rot = Rotation.from_euler('xyz', orn, degrees=False)
        else:
            rot = Rotation.from_quat(orn)   
        q_rotz = Rotation.from_euler('xyz', [0, 0, np.pi/2], degrees=False)
        q_roty = Rotation.from_euler('xyz', [0, np.pi/2, 0], degrees=False)
        q_rotx = Rotation.from_euler('xyz', [np.pi/2, 0, 0], degrees=False)
        qx = (rot*q_rotx).as_quat()
        qy = (rot*q_roty).as_quat()
        qz = (rot*q_rotz).as_quat()
        self.add_shape(pos=pos, orn=qx, size=0.3, rgba=[1.0, 0.0, 0.0, 1.0], shape="line")        
        self.add_shape(pos=pos, orn=qy, size=0.3, rgba=[0.0, 1.0, 0  , 1.0], shape="line")        
        self.add_shape(pos=pos, orn=qz, size=0.3, rgba=[0.0, 0.0, 1.0, 1.0], shape="line")  

    def add_shape(self, pos, orn=[0,0,0], size=0.01, rgba=[1.0, 0.0, 0.0, 1.0], shape="sphere"):
        if shape == "line":  
            shape_type = mujoco.mjtGeom.mjGEOM_LINE
        elif shape == "sphere":
            shape_type = mujoco.mjtGeom.mjGEOM_SPHERE
        if isinstance(orn, Rotation):
            rot = orn       
        elif len(orn) == 3:
            rot = Rotation.from_euler('xyz', orn, degrees=False)
        else:
            rot = Rotation.from_quat(orn)        
        self.viewer.add_marker(pos=np.array(pos), mat=rot.as_matrix(), type=shape_type, label="", size=np.array([size]*3), rgba=np.array(rgba))
    
    # TODO: fix this function
    def get_joint_names(self):
        id2name = {i: None for i in range(self.model.njnt)}
        name2id = {}
        for i in range(self.model.njnt):
            print( self.model.name_jntadr[i])
            name = self.model.names + self.model.name_jntadr[i]
            decoded_name = name.decode()
            if decoded_name:
                obj_id = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_JOINT, name)
                assert 0 <= obj_id < self.model.njnt and id2name[obj_id] is None
                name2id[decoded_name] = obj_id
                id2name[obj_id] = decoded_name

        # sort names by increasing id to keep order deterministic
        return tuple(id2name[id] for id in sorted(name2id.values())), name2id, id2name

    def joint_name2id(self, name):
        if name not in self.model.joint_name2id:
            raise ValueError("No \"joint\" with name %s exists. Available \"joint\" names = %s." % (name, self.joint_names))
        return self.model.joint_name2id[name]

    def get_joint_qpos_addr(self, name):
        '''
        Returns the qpos address for given joint.

        Returns:
        - address (int, tuple): returns int address if 1-dim joint, otherwise
            returns the a (start, end) tuple for pos[start:end] access.
        '''
        joint_id = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_JOINT, name)
        joint_type = self.model.jnt_type[joint_id]
        joint_addr = self.model.jnt_qposadr[joint_id]
        if joint_type == mujoco.mjtJoint.mjJNT_FREE:
            ndim = 7
        elif joint_type == mujoco.mjtJoint.mjJNT_BALL:
            ndim = 4
        else:
            assert joint_type in (mujoco.mjtJoint.mjJNT_HINGE, mujoco.mjtJoint.mjJNT_SLIDE)
            ndim = 1

        if ndim == 1:
            return joint_addr
        else:
            return (joint_addr, joint_addr + ndim)

    def get_joint_qvel_addr(self, name):
        '''
        Returns the qvel address for given joint.

        Returns:
        - address (int, tuple): returns int address if 1-dim joint, otherwise
            returns the a (start, end) tuple for vel[start:end] access.
        '''
        # joint_id = self.joint_name2id(name)
        joint_id = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_JOINT, name)
        joint_type = self.model.jnt_type[joint_id]
        joint_addr = self.model.jnt_dofadr[joint_id]
        if joint_type == mujoco.mjtJoint.mjJNT_FREE:
            ndim = 6
        elif joint_type == mujoco.mjtJoint.mjJNT_BALL:
            ndim = 3
        else:
            assert joint_type in (mujoco.mjtJoint.mjJNT_HINGE, mujoco.mjtJoint.mjJNT_SLIDE)
            ndim = 1

        if ndim == 1:
            return joint_addr
        else:
            return (joint_addr, joint_addr + ndim)
    
    def get_body_xpos(self, name):
        id = self.model.body_name2id(name)
        return self.model._xpos[id]

    def get_xpos(self, name):
        raise RuntimeError("get_body_xpos should be used instead of get_xpos")

    def get_body_xquat(self, name):
        id = self.model.body_name2id(name)
        return self.model.xquat[id]

    def get_joint_qpos(self, name):
        addr = self.get_joint_qpos_addr(name)
        if isinstance(addr, (int, np.int32, np.int64)):
            return self.data.qpos[addr]
        else:
            start_i, end_i = addr
            return self.data.qpos[start_i:end_i]

    def set_joint_qpos(self, name, value):
        addr = self.get_joint_qpos_addr(name) 
        if isinstance(addr, (int, np.int32, np.int64)):
            self.data.qpos[addr] = value
        else:
            start_i, end_i = addr
            value = np.array(value)
            assert value.shape == (end_i - start_i,), (
                "Value has incorrect shape %s: %s" % (name, value))
            self.data.qpos[start_i:end_i] = value

    def get_joint_qvel(self, name):
        addr = self.get_joint_qvel_addr(name)
        if isinstance(addr, (int, np.int32, np.int64)):
            return self.data.qvel[addr]
        else:
            start_i, end_i = addr
            return self.data.qvel[start_i:end_i]

    def set_joint_qvel(self, name, value):
        addr = self.get_joint_qvel_addr(name)
        if isinstance(addr, (int, np.int32, np.int64)):
            self.data.qvel[addr] = value
        else:
            start_i, end_i = addr
            value = np.array(value)
            assert value.shape == (end_i - start_i,), (
                "Value has incorrect shape %s: %s" % (name, value))
            self.data.qvel[start_i:end_i] = value
