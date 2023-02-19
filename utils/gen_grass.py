import numpy as np
from lxml import etree
from scipy.spatial.transform import Rotation

NEW_BRANCH_BASE_CHANCE = 0.15
NEW_BRANCH_CHANCE_LOSS_FACTOR = 0.75
NEW_BRANCH_CHANCE_FACTOR = 1.05
BRANCH_SIZE_LOSS_FACTOR = 0.7
MAX_BRANCH_LENGTH = 21
MIN_BRANCH_LENGTH = 5
# MAX_BRANCHES = 10
MAX_BRANCHES = 5
MIN_BRANCHES = 3

MAX_BRANCHES_OFF_TRUNK = 5
MIN_BRANCHES_OFF_TRUNK = 3

TRUNK_ROTATION = np.array([1, 0, 0, 0])


class contact():
    def __init__(self, bodys):
        # Body's is a list of collison pairs
        self.bodys = bodys

    def generate_xml(self):
        xml = etree.Element("contact")
        for bodys in self.bodys:
            collision = etree.Element("exclude", body1=bodys[0], body2=bodys[1])
            xml.append(collision)
        return xml

class actuator():
    def __init__(self, joints):
        self.joints = joints

    def generate_xml(self):
        xml = etree.Element("actuator")
        for joint in self.joints:
            # joint = etree.Element("position", attrib={"class":"panda"}, name=joint, joint=joint, kp="120", forcerange="-12 12", ctrlrange="-0.0873 3.8223")
            # joint = etree.Element("position", name=joint, joint=joint, kp="120")
            joint = etree.Element("motor", joint=joint, gear="100")
            xml.append(joint)
        return xml

class body():
    def __init__(self, pos, rot, branch_id, pos_id):
        self.name = str.join("", [str(branch_id), "B", str(pos_id)])
        self.pos = str.join(" ", [str(x) for x in pos])
        self.rot = str.join(" ", [str(x) for x in rot])

    def generate_xml(self):
        return etree.Element("body", name=self.name, pos=self.pos, quat=self.rot)

class joint():
    def __init__(self, axis, group, pos, branch_id, pos_id, num, stiffness, damping):
        self.name = str.join("", [str(branch_id), "J", str(num), "_", str(pos_id)])
        self.axis = str.join(" ", [str(x) for x in axis])
        self.pos = str.join(" ", [str(x) for x in pos])
        self.damping = str(damping)
        self.stiffness = str(stiffness)
        self.group = str(group)
        self.num = str(num)

    def generate_xml(self):
        return etree.Element("joint", axis=self.axis, damping=self.damping, group=self.group, name=self.name, pos=self.pos, stiffness=self.stiffness)

class geom():
    def __init__(self, branch_id, pos_id, radius, fromto):
        self.branch_id = branch_id
        self.name = str.join("", [str(branch_id), "G", str(pos_id)])
        self.fromto = fromto
        self.size = str(radius)

    def generate_xml(self):
        # colour = "0.3 " + str(np.clip(int(self.branch_id[0]) / MAX_BRANCHES, 0.1, 1.0)) + " 0.1 1.0"
        colour = "0.3 0.8 0.1 1.0"
        # return etree.Element("geom", name=self.name, quat=self.quat, rgba=colour, size=self.size, type="capsule")
        return etree.Element("geom", name=self.name, rgba=colour, fromto=self.fromto, type="capsule", size=self.size)
        

class tree_segment():
    def generate_xml(self):
        xml = self.body.generate_xml()
        if(not self.root):
            xml.append(self.joint0.generate_xml())
            xml.append(self.joint1.generate_xml())
        xml.append(self.geom.generate_xml())
        return xml

    def __init__(self, radius, half_height, damping, stiffness, branch_id, pos_id, pos, rot=[1,0,0,0], root=False):
        self.root = root
        self.pos_id = pos_id
        self.half_height = half_height
        self.body = body(pos, rot, branch_id, pos_id)
 
        if (not self.root):        
            self.joint0 = joint([1, 0, 0], 3, [0, 0, 0], branch_id, pos_id, 0, stiffness, damping)
            self.joint1 = joint([0, 1, 0], 3, [0, 0, 0], branch_id, pos_id, 1, stiffness, damping)

        self.geom = geom(branch_id, pos_id, radius, fromto="0 0 0 0 0 " + str(self.half_height))
        self.xml = self.generate_xml()

def create_branch(pos, rot, radius, branch_id, branch_seg_lengths, damping, stiffness):
    branch = tree_segment(radius=radius, half_height=branch_seg_lengths[0], damping=damping, stiffness=stiffness, branch_id=branch_id, pos_id=0, pos=pos, rot=rot, root=True)
    prev_seg = branch
    joints = []
    contacts = []
    for half_height in branch_seg_lengths[1:]:
        seg = tree_segment(radius=radius, half_height=half_height, damping=damping, stiffness=stiffness, branch_id=branch_id, pos_id=prev_seg.pos_id+1, pos=[0,0, prev_seg.half_height])
        # radius *= 0.7

        joints.append(seg.joint0.name)
        joints.append(seg.joint1.name)
        contacts.append([prev_seg.body.name, seg.body.name])

        prev_seg.xml.append(seg.xml)
        prev_seg = seg
    return branch, joints, contacts

def gen_grass_patches(patches=[0.5, 0.5, 0.8], radius=0.02, height=0.015, damping=50, 
                    stiffness=500, rot=[1,0,0,0], num=10, segs_per_branch=4):

    #Generate the xml for the tree
    xml = etree.Element("mujocoinclude")
    worldbody = etree.Element("worldbody") 
    root_seg = etree.Element("body", name="root", pos="0 0 0", quat="1 0 0 0")
    worldbody.append(root_seg)

    # Mujoco quaternions are w,x,y,z
    all_joints = []
    all_contacts = []
    # rot = Rotation.random().as_quat()
    rot = rot
    for spread in patches:
        for j in range(1,num):
            root_pos = np.array([np.random.uniform(spread[0][0], spread[0][1]),np.random.uniform(spread[1][0], spread[1][1]), spread[2]])
            branch_seg_lengths = [height/segs_per_branch]*segs_per_branch
            branch, joints, contacts = create_branch(pos=root_pos, rot=rot, radius=radius, branch_id=str(root_pos)+"0"+str(j), branch_seg_lengths=branch_seg_lengths, damping=damping, stiffness=stiffness)
            all_joints.extend(joints)
            all_contacts.extend(contacts)
            worldbody.append(branch.xml)

    all_segs = []

    xml.append(worldbody)
    xml.append(actuator(all_joints).generate_xml())                 
    xml.append(contact(all_contacts).generate_xml())                 
        
    return xml, all_segs

def generate_tree(base_radius, base_half_height, base_damping, base_stiffness, pos=[0,0,0], spread=[[0.4, 0.8],[-0.4, 0.4]], 
                    rot=[1,0,0,0], num=10, segs_per_branch=4, z_height=0.0):

    #Generate the xml for the tree
    xml = etree.Element("mujocoinclude")
    worldbody = etree.Element("worldbody") 
    root_seg = etree.Element("body", name="root", pos="0 0 0", quat="1 0 0 0")
    worldbody.append(root_seg)

    # Mujoco quaternions are w,x,y,z
    all_joints = []
    all_contacts = []
    # rot = Rotation.random().as_quat()
    rot = rot
    for j in range(1,num):
        root_pos = np.array([np.random.uniform(spread[0][0], spread[0][1]),np.random.uniform(spread[1][0], spread[1][1]), z_height])
        root_pos += np.array(pos)
        radius = base_radius
        branch_seg_lengths = [base_half_height/segs_per_branch]*segs_per_branch
        # branch, joints, contacts = create_branch(pos=root_pos, rot=rot, radius=radius, branch_id="0"+str(j), branch_seg_lengths=branch_seg_lengths, damping=base_damping, stiffness=base_stiffness)
        branch, joints, contacts = create_branch(pos=root_pos, rot=rot, radius=radius, branch_id=str(pos)+"0"+str(j), branch_seg_lengths=branch_seg_lengths, damping=base_damping, stiffness=base_stiffness)
        all_joints.extend(joints)
        all_contacts.extend(contacts)
        # root_seg.xml.append(branch.xml)
        worldbody.append(branch.xml)

    all_segs = []


    xml.append(worldbody)
    xml.append(actuator(all_joints).generate_xml())                 
    xml.append(contact(all_contacts).generate_xml())                 
        
    return xml, all_segs

if(__name__ == "__main__"):

    import mujoco
    import mujoco_viewer
    
    scene=r"""
        <mujoco model="panda scene">
        
        <size njmax="8000" nconmax="4000"/>
        
        <include file="test_tree.xml"/>    
    
        <statistic center="0.3 0 0.4" extent="1"/>

        <visual>
            <headlight diffuse="0.6 0.6 0.6"  ambient="0.3 0.3 0.3" specular="0 0 0"/>
            <rgba haze="0.15 0.25 0.35 1"/>
            <global azimuth="120" elevation="-20"/>
        </visual>

        <asset>
            <texture type="skybox" builtin="gradient" rgb1="0.3 0.5 0.7" rgb2="0 0 0" width="512"
                height="3072"/>
            <texture type="2d" name="groundplane" builtin="checker" mark="edge" rgb1="0.2 0.3 0.4"
                rgb2="0.1 0.2 0.3" markrgb="0.8 0.8 0.8" width="300" height="300"/>
            <material name="groundplane" texture="groundplane" texuniform="true" texrepeat="5 5"
                reflectance="0.2"/>
        </asset>

        <worldbody>
            <light pos="0 0 1.5" dir="0 0 -1" directional="true"/>
            <geom name="floor" size="0 0 0.05" type="plane" material="groundplane"/>
        </worldbody>
        
        </mujoco>
        """

    # xml, _ = generate_tree(0.02, 0.015, base_damping=50, base_stiffness=500)
    # xml, _ = generate_tree(0.02, 0.015, base_damping=1, base_stiffness=10)
    xml, _ = generate_tree(0.02, 0.5, base_damping=1, base_stiffness=10)
    etree.ElementTree(xml).write("test_tree.xml", pretty_print=True)

    # xml, _ = generate_tree(0.02, 0.015, base_damping=1, base_stiffness=1)

    model = mujoco.MjModel.from_xml_string(scene)
    data = mujoco.MjData(model)
    viewer = mujoco_viewer.MujocoViewer(model, data)

    while True:
        # data.ctrl[:] = np.random.uniform(-1.0, 1.0, len(data.ctrl)) 
        mujoco.mj_step(model, data)
        viewer.render()
