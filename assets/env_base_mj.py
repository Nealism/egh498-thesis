from .env_base import EnvBase
import math
from utils import img_helpers
import mujoco
import numpy as np
from scipy.spatial.transform import Rotation
from lxml import etree
import shutil
import os
from mpi4py import MPI
from utils.xml_helper import indent_xml
comm = MPI.COMM_WORLD
from utils import gen_grass, gen_tree

class EnvBaseMJ(EnvBase):

    def set_position(self, pos=None, orn=None, joints=None, joint_vel=None):
        base_id = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_BODY, self.base_link)
        
        # For robots with a free joint, we need to set the qpos of the free joint to dynamically set the position of the base. 
        # Need to name the free joint "free" in the .xml
        free_joint_id = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_JOINT, "free")

        if pos is not None:
            for i in range(len(pos)):
                self.model.body_pos[base_id,i] = pos[i]
                if free_joint_id != -1:
                    self.data.qpos[free_joint_id+i] = pos[i]

        # Mujoco quaternions are w,x,y,z, handle that here. Treat as x,y,z,w, elsewhere
        if orn is not None:
            self.model.body_quat[base_id,0] = orn[3]
            self.model.body_quat[base_id,1] = orn[0]
            self.model.body_quat[base_id,2] = orn[1]
            self.model.body_quat[base_id,3] = orn[2]
            if free_joint_id != -1:
                self.data.qpos[free_joint_id+3] = orn[3]
                self.data.qpos[free_joint_id+4] = orn[0]
                self.data.qpos[free_joint_id+5] = orn[1]
                self.data.qpos[free_joint_id+6] = orn[2]

        if joints is not None:
            for value, name in zip(joints, self.motor_names):
                self.set_joint_qpos(name, value)
       
        if joint_vel is not None:
            for value, name in zip(joint_vel, self.motor_names):
                self.set_joint_qvel(name, value)

    # ====================================================================================
    # General assets stuff - Trees, Terrains etc.
    # ====================================================================================
    def save_xml(self, path):
        # Change the location of meshdir (when on the hpc) and save a copy of the current tree
        replay_scene_dir = self.xml_assets_dir + "/replay_scene" + path + ".xml"
        replay_tree_dir = self.xml_assets_dir + "/replay_tree" + path + ".xml"
        scene_dir = self.xml_assets_dir + "/scene_0.xml"
        tree_dir = self.xml_assets_dir + "/tree_0.xml"
        shutil.copyfile(tree_dir, replay_tree_dir)
        shutil.copyfile(scene_dir, replay_scene_dir)

        tree_xml = etree.parse(replay_scene_dir)
        for elem in tree_xml.getroot():
            if elem.tag == "include" and elem.attrib['file'] == "tree_0.xml":
                elem.attrib["file"] = "replay_tree" + path + ".xml"
        tree_xml.write(replay_scene_dir, pretty_print=True)

    def save_tree(self, best, test):
        if self.rank == 0:
            if best and test:
                self.save_xml("_best_test")
            if best:
                self.save_xml("_best")
            if test:
                self.save_xml("_test")
            self.save_xml("")

    def get_relative_assets_path(self, copy_path):
        """
        Returns the path from the experimental folder (/scratch1/... for hpc) 
        to the xmls assets folder
        """
        # path from experimental folder to normal assets folder
        dir_depth = len(copy_path.split("/")) - 2
        return "../" * (dir_depth - 1) + ".." + os.getcwd() + "/" + self.mesh_dir


    def set_up_xmls(self):
        """
        Creates process specific xml's for thread safe loading of general assets (not just trees). 
        xmls are loaded into the experiment directory for easy use. 
        
        xml's:
            robot_name.xml (common to all)
            scene_{rank}.xml 
            
            AND, OPTIONALLY:
                tree_{rank}.xml 
                terrain_{rank}.xml
        
        NOTE: all held in /xml_assets subdir. (was /trees)
        """
        self.xml_assets_dir = os.path.join(self.PATH, "xml_assets")
        # parent proc. creates robot_name.xml copy
        if self.rank == 0:
            print(f"\nxml assets dir: {self.xml_assets_dir}")
            if not os.path.exists(self.xml_assets_dir):
                os.mkdir(self.xml_assets_dir)

            if self.args.control_type == "torque":
                orig_path = self.get_parent_dir(self.model_path) + self.robot_name + "_torque.xml"
                copy_path = self.get_parent_dir(self.xml_assets_dir) + "xml_assets/" + self.robot_name + "_torque.xml"
            else:
                orig_path = self.get_parent_dir(self.model_path) + self.robot_name + ".xml"
                copy_path = self.get_parent_dir(self.xml_assets_dir) + "xml_assets/" + self.robot_name + ".xml"
            shutil.copyfile(orig_path, copy_path)

            # modify robot_name.xml's meshdir and texturedir path
            robot_xml = etree.parse(copy_path)
            for elem in robot_xml.findall("compiler"):
                elem.attrib['meshdir'] = self.get_relative_assets_path(copy_path)
                elem.attrib['texturedir'] = self.get_relative_assets_path(copy_path)
            robot_xml.write(copy_path, pretty_print=True)

        # Wait for rank == 0 to set up folders
        comm.Barrier()

        # each proc. creates a scene_{rank}.xml
        model_path = self.xml_assets_dir + "/scene_" + str(self.rank) + ".xml"
        shutil.copyfile(self.model_path, model_path)
        scene_xml = etree.parse(model_path)

        # each proc. optionally can create tree_{rank}.xml
        if self.args.tree_type:
            # copy blank tree to new dir
            orig_path = self.get_parent_dir(self.model_path) + "tree.xml"
            copy_path = self.get_parent_dir(self.xml_assets_dir) + "xml_assets/tree_" + str(self.rank) + ".xml"
            shutil.copyfile(orig_path, copy_path)

            # include tree_{rank}.xml in scene_{rank}.xml
            tree_include = etree.SubElement(scene_xml.getroot(), "include")
            tree_include.attrib["file"] = "tree_" + str(self.rank) + ".xml"

        # each proc. optionally can create terrain_{rank}.xml
        if self.args.add_terrain:
            # copy blank terrain to new dir
            orig_path = self.get_parent_dir(self.model_path) + self.base_terrain_xml
            copy_path = self.get_parent_dir(self.xml_assets_dir) + "xml_assets/terrain_" + str(self.rank) + ".xml"
            shutil.copyfile(orig_path, copy_path)

            # create compiler el and modify it's assetdir path (as in robot_xml)
            terrain_xml = etree.parse(copy_path)
            compiler = etree.SubElement(terrain_xml.getroot(), "compiler")
            compiler.attrib['assetdir'] = self.get_relative_assets_path(copy_path)
            terrain_xml.write(copy_path, pretty_print=True)
            
            # include terrain_{rank}.xml in scene_{rank}.xml
            terrain_include = etree.SubElement(scene_xml.getroot(), "include")
            terrain_include.attrib["file"] = "terrain_" + str(self.rank) + ".xml"

        #Then save the new model file
        indent_xml(scene_xml.getroot())
        scene_xml.write(model_path, pretty_print=True)

        # Update the model path
        self.model_path = model_path

    def generate_tree(self, radius=0.02, height=0.015, damping=50, stiffness=500, pos=[0,0,0], rot=[1,0,0,0], num=10, segs_per_branch=4, spread=[[0.4,0.8],[-0.4,0.4]], z_height=0.0):
        #Tree generation is handled in xml_gen.
        #This function writes that to the mujoco xml file and handles multiple threads.
        if self.args.tree_type == "tree":
            tree = gen_tree.tree(joint_damping=damping, joint_stiffness=stiffness, spread=spread)
            xml, self.tree = tree.generate_tree()
        elif self.args.tree_type == "grass":
            xml, self.tree = gen_grass.generate_tree(base_radius=radius, base_half_height=height, base_damping=damping, base_stiffness=stiffness, pos=pos, rot=rot, num=num, segs_per_branch=segs_per_branch, spread=spread, z_height=z_height)
        tree_path = os.path.join(self.xml_assets_dir, "tree_" + str(self.rank) + ".xml")
        etree.ElementTree(xml).write(tree_path, pretty_print=True)

    # ====================================================================================
    # Custom helpers
    # ====================================================================================

    def get_parent_dir(self, file_path):
        """
        Returns the parent directory of the given directory/file (cuts off path's last component)
        """
        return "/".join(file_path.split("/")[:-1]) + "/"

    def print_contacts(self):
        contact_list = self.data.contact
        for dim, contact1, contact2 in zip(contact_list.dim, contact_list.geom1, contact_list.geom2):
            if dim:
                geom_name1 = mujoco.mj_id2name(self.model, mujoco.mjtObj.mjOBJ_GEOM, contact1)
                geom_name2 = mujoco.mj_id2name(self.model, mujoco.mjtObj.mjOBJ_GEOM, contact2)
                # TODO: get the floor name
                if geom_name1 != "floor" and geom_name2 != "floor":
                    print("Contacts: ", self.data.ncon, [geom_name1, geom_name2])

    def set_targets(self, targets):
        if isinstance(targets, list):
            for target in targets:
                if len(target) == 3:
                    self.add_shape(pos=target[0], size=target[1], rgba=target[2])
                else:
                    self.add_axis(pos=target[0], orn=target[1])
    
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
    

    # ====================================================================================
    # Helpers from mujoco_py and custom (these aren't supported by 'mujoco' python module)
    # ====================================================================================
    def close(self):
        self.viewer.close()

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
