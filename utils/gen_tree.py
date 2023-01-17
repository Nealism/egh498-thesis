import numpy as np
from lxml import etree

# RIGID_TRUNK = True
RIGID_TRUNK = False
TRUNK_ROTATION = np.array([1, 0, 0, 0])
# Unsure what the upper limit for body number is
MAX_BODIES = 190

def rotate_vector_by_quat(vector, quat):
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
    def __init__(self, branch_id, pos_id, quat, radius, half_height, type):
        self.name = str.join("", [str(branch_id), "G", str(pos_id)])
        self.quat = str.join(" ", [str(x) for x in quat])
        self.radius = str(radius)
        self.half_height = str(half_height)
        self.size = str.join(" ", [str(radius), str(half_height)])
        self.type = type

    def generate_xml(self):
        return etree.Element("geom", name=self.name, quat=self.quat, rgba="0.3 0.1 0.1 1.0", size=self.size, type=self.type)

class tree_segment():

    def generate_xml(self):
        xml = self.body.generate_xml()
        if(not self.root and not self.rigid):
            xml.append(self.joint0.generate_xml())
            xml.append(self.joint1.generate_xml())
        xml.append(self.geom.generate_xml())
        return xml

    def __init__(self, tree, radius, half_height, damping, stiffness, parent, 
                 branch_id, pos_id, pos, rot, spacing, 
                 chance_of_new_branch, prev_world_coords, root = False):
        self.parent_tree = tree
        self.radius = radius
        self.half_height = half_height
        self.damping = damping
        self.stiffness = stiffness
        self.parent = parent
        self.branch_id = branch_id
        self.pos_id = pos_id
        self.pos = pos
        self.rot = rot
        self.rot_spacing = rotate_vector_by_quat(np.array([0, 0, spacing]), rot)
        if(self.rot_spacing[2] < 0):
            self.rot_spacing = -self.rot_spacing
            self.rot = -self.rot
        self.world_coords = prev_world_coords + self.rot_spacing
        self.spacing = spacing
        self.root = root
        self.chance_of_new_branch = chance_of_new_branch

        if(branch_id == 0 and RIGID_TRUNK):
            self.rigid = True
        else:
            self.rigid = False
        
        # Create XML elements
        self.body = body(pos, branch_id, pos_id)
        if(not self.root and not self.rigid):
            self.joint0 = joint([0, 1, 0], 3, [spacing/2, 0, 0], branch_id, pos_id, 0, stiffness, damping)
            self.joint1 = joint([0, 0, 1], 3, [-spacing/2, 0, 0], branch_id, pos_id, 1, stiffness, damping)
        
        if(self.rigid):
            self.geom = geom(branch_id, pos_id, rot, radius, half_height, "capsule")
        else:
            self.geom = geom(branch_id, pos_id, rot, radius, half_height, "capsule")
        self.xml = self.generate_xml()

    def next_segment(self):
        next_pos_id = self.pos_id + 1
        chance_of_new_branch = self.chance_of_new_branch * self.parent_tree.new_branch_chance_per_segment_gain
        return tree_segment(self.parent_tree, self.radius, self.half_height, self.damping, self.stiffness, self, 
                            self.branch_id, next_pos_id, self.rot_spacing, self.rot, self.spacing, 
                            self.chance_of_new_branch, self.world_coords)

class tree():
    def __init__(self, segment_radius=0.02, segment_height=0.03, joint_damping=50, 
                 joint_stiffness=500, segment_spacing=0.05, chance_of_new_branch=0.15, 
                 new_branch_chance_per_branch_decay=0.75, 
                 new_branch_chance_per_segment_gain=1.05,
                 branch_param_decay=0.7, max_branch_segments=21,
                 min_branch_segments=5, max_branches=10, min_branches=3, spread=[[0.2, 0.5],[-0.5, 0.5]]):
        '''
        Initialise a tree with the given parameters ready for the generate tree method.

        Parameters
        ----------
        segment_radius : float, optional
            The radius of the tree segments. 
        
        segment_height : float, optional
            The height of the tree segments.
        
        joint_damping : float, optional
            The damping of the tree joints.

        joint_stiffness : float, optional
            The stiffness of the tree joints.

        segment_spacing : float, optional
            The spacing between tree segments. Used to ensure segments don't clip into each other.

        chance_of_new_branch : float, optional
            The chance of a new branch being created at each segment.

        new_branch_chance_per_branch_decay : float, optional
            The amount the chance of a new branch being created is reduced by when a new branch is created.

        new_branch_chance_per_segment_gain : float, optional
            The amount the chance of a new branch being created is increased by when a new segment is created along the same branch.

        branch_param_decay : float, optional
            The amount the radius, height, damping, stiffness and spacing of a branch is reduced by when a new branch is created.

        max_branch_segments : int, optional
            The maximum number of segments a branch can have.

        min_branch_segments : int, optional
            The minimum number of segments a branch can have.
        
        max_branches : int, optional
            The maximum number of branches a tree can have.

        min_branches : int, optional
            The minimum number of branches a tree can have.
        '''
        self.radius = segment_radius
        self.half_height = segment_height/2
        self.damping = joint_damping
        self.stiffness = joint_stiffness
        self.spacing = segment_spacing
        self.chance_of_new_branch = chance_of_new_branch
        self.new_branch_chance_per_branch_decay = new_branch_chance_per_branch_decay
        self.new_branch_chance_per_segment_gain = new_branch_chance_per_segment_gain
        self.branch_param_decay = branch_param_decay
        self.max_branch_segments = max_branch_segments
        self.min_branch_segments = min_branch_segments
        self.max_branches = max_branches
        self.min_branches = min_branches
        self.spread = spread

    def generate_tree(self):
        # root_pos = np.array([self.pos[0] + np.random.uniform(0.2, 0.5), self.pos[1] + np.random.uniform(-0.5, 0.5), self.pos[2]])
        root_pos = np.array([np.random.uniform(self.spread[0][0], self.spread[0][1]),np.random.uniform(self.spread[1][0], self.spread[1][1]), 0])
        # Root branch is always upright
        root_seg = tree_segment(self, self.radius, self.half_height, self.damping, self.stiffness, 
                                None, 0, 0, root_pos, TRUNK_ROTATION, self.spacing, self.chance_of_new_branch, root_pos, root=True)
        # Generate the rest of the tree
        frontier_segments = [root_seg]
        all_segs = []
        branch_ends = []
        body_count = 0
        branch_lengths = {0 : np.random.randint(self.min_branch_segments, self.max_branch_segments)}
        while frontier_segments:
            seg = frontier_segments.pop()
            all_segs.append(seg)
            new_seg = seg.next_segment()
            
            # Add the new segment to the tree
            seg.xml.append(new_seg.xml)
            body_count += 1
            if MAX_BODIES <= body_count:
                print("Reached max tree size", MAX_BODIES, " ", body_count)
                break

            # Check for a new branch
            if((np.random.uniform(0, 1) < new_seg.chance_of_new_branch and 
                len(branch_lengths) < self.max_branches) or 
                (len(branch_lengths) < self.min_branches and 
                seg.pos_id == branch_lengths[seg.branch_id])):

                # Generate the new branch
                new_branch_id = max(branch_lengths.keys()) + 1
                branch_lengths[new_branch_id] = np.random.randint(self.min_branch_segments, self.max_branch_segments)
                branch_rot = np.random.uniform(0, 2*np.pi, 4)
                branch_rot = branch_rot / np.linalg.norm(branch_rot)
                new_branch_seg = tree_segment(self, new_seg.radius * self.branch_param_decay, 
                                    new_seg.half_height * self.branch_param_decay, 
                                    new_seg.damping * self.branch_param_decay, 
                                    new_seg.stiffness * self.branch_param_decay, 
                                    new_seg, new_branch_id, 0, new_seg.pos, branch_rot, 
                                    new_seg.spacing * self.branch_param_decay, 
                                    new_seg.chance_of_new_branch * self.new_branch_chance_per_branch_decay, 
                                    seg.world_coords, root=True)
                seg.xml.append(new_branch_seg.xml)
                body_count += 1
                frontier_segments.append(new_branch_seg)

            # Check if the branch has ended
            if(seg.pos_id == branch_lengths[seg.branch_id]):
                branch_ends.append(seg)
            else:
                # Add the new segment to the frontier
                frontier_segments.append(new_seg)

        # Generate the xml for the tree
        xml = etree.Element("mujocoinclude")
        body = etree.Element("worldbody")
        body.append(root_seg.xml)
        xml.append(body)
            
        return xml, all_segs
    

if(__name__ == "__main__"):

    a_tree = tree()
    xml = a_tree.generate_tree()

    with open("assets/xmls/tree.xml", "wb") as f:
        f.write(etree.tostring(xml, pretty_print=True))