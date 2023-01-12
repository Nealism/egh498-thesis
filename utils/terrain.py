import numpy as np
import os 
import cv2
from lxml import etree
from utils import img_helpers

"""
Class to represent any terrains loaded. Terrains are represented as N x M numpy arrays, 
where each (i, j) element encodes a height.

The terrain is also saved in PNG format (useful for certain sim envs eg. mujoco)

NOTE: Both the original array AND the PNG format are stored
"""
class Terrain():
    def __init__(self, terr_arr, path, name):
        self.name = name
        self.img_name = self.name + ".png"
        self.img_path = path + self.img_name

        # terrain array (numpy array)
        self.terr_arr = terr_arr         
        # terrain image (PNG)
        self.terr_img = self.load_terr_img() 
        # (X, Y) image dimensions in pixels
        self.image_dim = (self.terr_arr.shape[1], self.terr_arr.shape[0]) # (X, Y) == (col, row)

    def load_terr_img(self):
        """ 
        Saves the terrain image to its path and returns it
        """ 
        cv2.imwrite(self.img_path, self.terr_arr)
        img = cv2.imread(self.img_path)
        return img
    
    def add_to_xml(self):
        raise NotImplementedError 
    
"""
Sub-class of Terrain to represent an hfield in mujoco 
"""
class Hfield(Terrain):
    def __init__(self, terr_arr, path, name, position=(0, 0, 0), size=(100, 100, 0.01, 0.01)):
        """
        Added params:
            position - x,y,z position the hfield is centred at in mujoco
            size - x_rad, y_rad, elevation, base_z:

                    x_rad, y_rad - mujoco uses radius instead of length/width
                    elevation - data is normalised between 0-1, which is then scaled by this elevation value
                    base_z - depth of box in -z direction (serves as 'base')
        """
        super().__init__(terr_arr, path, name)
        self.size = size
        self.position = position

        self.size_str = f"{size[0]} {size[1]} {size[2]} {size[3]}"
        self.position_str = f"{position[0]} {position[1]} {position[2]}"

        # hfield element and its referencing geom
        self.hfield_el, self.geom_el = self.config_hfield_geom()
        
    def config_hfield_geom(self):
        hfield_el = etree.Element("hfield", attrib={"name":self.name,
                                                    "file":self.img_path,
                                                    "size":self.size_str})

        geom_el = etree.Element("geom", attrib={"name":self.name,
                                                    "type":"hfield",
                                                    "pos":self.position_str,
                                                    "hfield":self.name})
        return hfield_el, geom_el

    def rob_to_img_pos(self, pos):
        """
        Converts a position in mujoco (x1, y1) to a position in the hfield image (x2, y2)

        NOTE: Assumes hfield is centred at pos == (0, 0, 0) in mujoco

        Params:
            pos - mujoco position (x1, y1)
        """
        x1, y1 = pos[0], pos[1]
        x1_rad, y1_rad = self.size[0], self.size[1]
        x2_rad, y2_rad = self.image_dim[0] // 2, self.image_dim[1] // 2
        # +x mj == +x im 
        x = int((x1 + x1_rad) * (x2_rad // x1_rad))
        # +y mj == -y im (up-screen in mujoco is downscreen in image)
        y = int((-1 * y1 + y1_rad) * (y2_rad // y1_rad))
        return (x, y)

    def compute_sub_section(self, x, y, X, Y):
        """
        Given a position in mujoco (x, y), compute the X x Y subsection of the hfield array 
        around it

        Params:
            x, y - position in mujoco
            X, Y - dimensions of sub-section to compute 
        
        Returns:
            sub_section array
        """
        # (x, y) position in image
        im_x, im_y = self.rob_to_img_pos((x, y))
        (min_x, min_y), (max_x, max_y) = img_helpers.top_left_bot_right(im_x, im_y, X, Y)
        # check sub-section is in range of the base arr
        if (max_x + 1 > self.image_dim[0]
            or max_y + 1 > self.image_dim[1]
            or min_x < 0 
            or min_y < 0):
            print("Sub-section out of range")
            return None

        # (x, y) == (col, row)
        return self.terr_arr[min_y:max_y+1, min_x:max_x+1]

"""
Class to represent a mesh in mujoco
"""
class Mesh(Terrain):
    pass


"""
A class to generate terrain arrays for Terrain objects (see above)

NOTE: Terrain objects DO NOT require their terrain arrays to be generated this way. One can load their own 
if they wish, this just provides some already-configured ones.
"""
class TerrainGen():
    def gen_rand_ground_truth(self, zl, zh, dimensions):
        """
        Randomly generates a 2D numpy array that serves as the basis for the height map.

        Params:
            zl-zh defines the range we sample heights from 
            dimensions - (X, Y), NOT (row, col)
        """
        if len(dimensions) != 2:
            print("Dimensions of ground truth must be of form: (x, y)")
            return None
        gt = np.random.uniform(low=zl, high=zh, size=(dimensions[1], dimensions[0]))
        return gt
    
    def gen_curve(self, xl, xh, yl, yh, num_points, fn):
        """
        fn is applied element-wise to generate a 2D numpy array that can serve as the basis of an 
        environment terrain
        NOTE: xl, xh, yl, yh define the x and y ranges (dimensions of the array)
        """
        x = np.linspace(xl, xh, num_points)
        y = np.linspace(yl, yh, num_points)
        x, y = np.meshgrid(x, y)
        fn = np.vectorize(fn)
        z = fn(x, y)
        # TODO : add plotting option
        return z

    ###################### TERRAIN FUNCTIONS ######################
    
    def saddle_func(self, x, y):
        return np.square(x) - np.square(y)

    def hump_func(self, x, y):
        z = 5*(np.square(x) + np.square(y))
        return z
    
    def gaussian(self, x, y, sigma=1):
        z = 25*(1/(2*np.pi*sigma**2)) * np.exp(-1*((0.1*x**2 + 0.1*y**2)/(2*sigma**2)))
        return z
