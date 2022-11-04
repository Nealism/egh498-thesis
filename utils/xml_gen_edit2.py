import numpy as np
from lxml import etree

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

def rotate_vector_by_quat(vector, quat):
    #Rotate a vector by a quaternion
    #https://math.stackexchange.com/questions/90081/quaternion-rotation-of-a-vector
    return vector + 2 * np.cross(quat[1:], np.cross(quat[1:], vector) + quat[0] * vector)

class body():
    def __init__(self, pos, branch_id, pos_id):
        self.name = str.join("", [str(branch_id), "B", str(pos_id)])
        self.pos = str.join(" ", [str(x) for x in pos])

    def generate_xml(self):
        return etree.Element("body", name=self.name, pos=self.pos)

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
    def __init__(self, branch_id, pos_id, quat, radius, half_height):
        self.branch_id = branch_id
        self.name = str.join("", [str(branch_id), "G", str(pos_id)])
        self.quat = str.join(" ", [str(x) for x in quat])
        self.radius = str(radius)
        self.half_height = str(half_height)
        self.size = str.join(" ", [str(radius), str(half_height)])

    def generate_xml(self):
        colour = "0.3 " + str(np.clip(self.branch_id / MAX_BRANCHES, 0.1, 1.0)) + " 0.1 1.0"
        return etree.Element("geom", name=self.name, quat=self.quat, rgba=colour, size=self.size, type="capsule")

class tree_segment():
    def generate_xml(self):
        xml = self.body.generate_xml()
        if(not self.root):
            xml.append(self.joint0.generate_xml())
            xml.append(self.joint1.generate_xml())
        xml.append(self.geom.generate_xml())
        return xml

    def __init__(self, radius, half_height, damping, stiffness, parent, branch_id, pos_id, pos, rot, spacing, chance_of_new_branch, prev_world_coords, root=False, target_pos=None, target_orn=None):
        self.radius = radius
        self.half_height = half_height
        self.damping = damping
        self.stiffness = stiffness
        self.parent = parent
        self.branch_id = branch_id
        self.pos_id = pos_id
        self.pos = pos
        self.rot = rot

        # if pos_id == 0:
        #     if parent is None:
        #         if root:
        #             print("making trunk, make longer")
        #             self.half_height = 1.0
        #         else:
        #             self.half_height = 
        #     elif parent.branch_id == 0:
        #         print("making branch off parent, put at height and rotation to encourage going through fruit")

        self.rot_spacing = rotate_vector_by_quat(np.array([0, 0, spacing]), self.rot)
        if(self.rot_spacing[2] < 0):
            self.rot_spacing = -self.rot_spacing
            self.rot = -self.rot
        self.world_coords = prev_world_coords + self.rot_spacing
        self.spacing = spacing
        self.root = root
        self.chance_of_new_branch = chance_of_new_branch
        
        if root and parent is None:
            self.body = body([self.pos[0], self.pos[1], self.pos[2] + 0.5], branch_id, pos_id)
            self.body = body([self.pos[0], self.pos[1], self.pos[2] + 0.5], branch_id, pos_id)
        else:
            self.body = body(self.pos, branch_id, pos_id)
 
 
        if(not self.root):
            self.joint0 = joint([0, 1, 0], 3, [spacing/2, 0, 0], branch_id, pos_id, 0, stiffness, damping)
            self.joint1 = joint([0, 0, 1], 3, [-spacing/2, 0, 0], branch_id, pos_id, 1, stiffness, damping)
        
        if root and parent is None:
            self.geom = geom(branch_id, pos_id, self.rot, self.radius, 0.5)
        else:
            self.geom = geom(branch_id, pos_id, self.rot, self.radius, self.half_height)
        self.xml = self.generate_xml()

    def next_segment(self):
        next_pos_id = self.pos_id + 1
        chance_of_new_branch = self.chance_of_new_branch * NEW_BRANCH_CHANCE_FACTOR
        return tree_segment(self.radius, self.half_height, self.damping, self.stiffness, self, 
                            self.branch_id, next_pos_id, self.rot_spacing, self.rot, self.spacing, 
                            self.chance_of_new_branch, self.world_coords)

def generate_tree(base_radius, base_half_height, base_damping, base_stiffness, spacing, target_pos=None, target_orn=None):
    root_pos = np.array([np.random.uniform(0.2, 0.5),np.random.uniform(-0.5, 0.5), 0])
    #Root branch is always upright
    root_seg = tree_segment(base_radius, base_half_height, base_damping, base_stiffness, 
                            None, 0, 0, root_pos, TRUNK_ROTATION, spacing, NEW_BRANCH_BASE_CHANCE, root_pos, root=True)
    #Generate the rest of the tree
    frontier_segments = [root_seg]
    all_segs = []
    branch_ends = []
    # branch_lengths = {0 : np.random.randint(MIN_BRANCH_LENGTH, MAX_BRANCH_LENGTH)}
    branch_lengths = {0 : 1}
    while frontier_segments:
        seg = frontier_segments.pop()
        all_segs.append(seg)
        new_seg = seg.next_segment()
        
        #Add the new segment to the tree
        seg.xml.append(new_seg.xml)

        #Check for a new branch
        if((np.random.uniform(0, 1) < new_seg.chance_of_new_branch and 
            len(branch_lengths) < MAX_BRANCHES) or 
            (len(branch_lengths) < MIN_BRANCHES and 
            seg.pos_id == branch_lengths[seg.branch_id])):

            new_branch_id = max(branch_lengths.keys()) + 1
            branch_lengths[new_branch_id] = np.random.randint(MIN_BRANCH_LENGTH, MAX_BRANCH_LENGTH)
            branch_rot = np.random.uniform(0, 2*np.pi, 4)
            branch_rot = branch_rot / np.linalg.norm(branch_rot)
            new_branch_seg = tree_segment(new_seg.radius * BRANCH_SIZE_LOSS_FACTOR, 
                                   new_seg.half_height * BRANCH_SIZE_LOSS_FACTOR, 
                                   new_seg.damping * BRANCH_SIZE_LOSS_FACTOR, 
                                   new_seg.stiffness * BRANCH_SIZE_LOSS_FACTOR, 
                                   new_seg, new_branch_id, 0, new_seg.pos, branch_rot, 
                                   new_seg.spacing * BRANCH_SIZE_LOSS_FACTOR, new_seg.chance_of_new_branch * NEW_BRANCH_CHANCE_LOSS_FACTOR, seg.world_coords, root=True, target_pos=target_pos, target_orn=target_orn)
            seg.xml.append(new_branch_seg.xml)
            frontier_segments.append(new_branch_seg)

        if(seg.pos_id == branch_lengths[seg.branch_id]):
            #print("Branch", seg.branch_id, "length", seg.pos_id)
            branch_ends.append(seg)
        else:
            #Add the new segment to the frontier
            frontier_segments.append(new_seg)

    #Generate the xml for the tree
    xml = etree.Element("mujocoinclude")
    xml.append(root_seg.xml)
        
    return xml, all_segs
    

if(__name__ == "__main__"):
    #seg = tree_segment(0.02, 0.015, 50, 500, "root", 1, 0, np.array([0.2, 0.2, 0]), np.array([0.707105, 0, -0.707108, 0]))
    #print(etree.tostring(seg.xml, pretty_print=True))

    xml = generate_tree(0.02, 0.015, 50, 500, 0.05)

    with open("assets/xmls/tree.xml", "wb") as f:
        f.write(etree.tostring(xml, pretty_print=True))