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
        # (X, Y) image dimensions in pixels
        self.image_dim = (self.terr_arr.shape[1], self.terr_arr.shape[0]) # (X, Y) == (col, row)

    def load_terr_img(self):
        """ 
        Saves the terrain image to its path and returns it
        """ 
        im = self.terr_arr * 255
        cv2.imwrite(self.img_path, im)
        img = cv2.imread(self.img_path)
        self.terr_img = img
    
    def add_to_xml(self):
        raise NotImplementedError 
    
"""
Sub-class of Terrain to represent an hfield in mujoco 
"""
class Hfield(Terrain):
    def __init__(self, terr_arr, path, name, 
                position=(0,0,0), size=(10, 10, 0.1, 1), from_PNG=False):
        """
        Added params:
            position - x,y,z position the hfield is centred at in mujoco
            size - x_rad, y_rad, elevation, base_z:

                    x_rad, y_rad - mujoco uses radius instead of length/width
                    elevation - data is normalised between 0-1, which is then scaled by this 
                                elevation value
                    base_z - depth of box in -z direction (serves as 'base')

            from_PNG - iff true, generate hfield from PNG, otherwise, load yourself later   
                     - loaded like so: 
                            self.model.hfield_data = {numpy array of els in interval [0, 1]}
        """
        super().__init__(terr_arr, path, name)
        self.size = size
        self.position = position

        self.size_str = f"{size[0]} {size[1]} {size[2]} {size[3]}"
        self.position_str = f"{position[0]} {position[1]} {position[2]}"

        self.from_PNG = from_PNG

        # hfield element and its referencing geom
        self.hfield_el, self.geom_el = self.config_hfield_geom()
        
    def config_hfield_geom(self):
        # generate hfield el
        hfield_el = etree.Element("hfield", attrib={"name":self.name, "size":self.size_str})
        if self.from_PNG:
            hfield_el["file"] = self.img_path
        else:
            hfield_el.attrib["nrow"] = str(self.image_dim[1])
            hfield_el.attrib["ncol"] = str(self.image_dim[0])

        # generate referencing geom
        geom_attr = {"name":self.name,"type":"hfield","pos":self.position_str, "hfield":self.name}
        geom_el = etree.Element("geom", geom_attr)
        
        return hfield_el, geom_el

    def rob_to_img_pos(self, pos):
        """
        Converts a position in mujoco (x1, y1) to a position in the hfield image (x2, y2)

        NOTE: Assumes hfield is centred at pos == (0, 0, 0) in mujoco
        """
        x1, y1 = pos[0], pos[1]
        x1_rad, y1_rad = self.size[0], self.size[1]
        x2_rad, y2_rad = self.image_dim[0] // 2, self.image_dim[1] // 2
        # +x mj == +x im 
        x = int((x1 + x1_rad) * (x2_rad / x1_rad))
        # +y mj == -y im (up-screen in mujoco is downscreen in image)
        y = int((-1 * y1 + y1_rad) * (y2_rad / y1_rad))
        return (x, y)
    
    def rob_to_arr_pos(self, pos):
        """
        Converts a position in mujoco (x1, y1) to a position in the hfield array (x2, y2)

        NOTE: Assumes hfield is centred at pos == (0, 0, 0) in mujoco
        """
        x1, y1 = pos[0], pos[1]
        x1_rad, y1_rad = self.size[0], self.size[1]
        x2_rad, y2_rad = self.image_dim[0] // 2, self.image_dim[1] // 2
        # +x mj == +x im 
        x = int((x1 + x1_rad) * (x2_rad / x1_rad))
        # +y mj == y im (up-screen in mujoco is downscreen in image)
        y = int((y1 + y1_rad) * (y2_rad / y1_rad))
        return (x, y)


    def compute_sub_section(self, x, y, X, Y):
        """
        Compute the X x Y subsection of the hfield array around the robot, who is centred
        at mujoco position (x, y)

        Params:
            x, y - position in mujoco
            X, Y - dimensions of sub-section to compute 
        
        Returns:
            sub_section array
        """
        # (x, y) position in image
        im_x, im_y = self.rob_to_arr_pos((x, y))
        (min_x, min_y), (max_x, max_y) = img_helpers.top_left_bot_right(im_x, im_y, X, Y)
        # check sub-section is in range of the base arr
        if (max_x + 1 > self.image_dim[0]
            or max_y + 1 > self.image_dim[1]
            or min_x < 0 
            or min_y < 0):
            # print("Sub-section out of range")
            return np.zeros((Y, X))
            # return None

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
    def gen_uniform_rand(self, zl, zh, dim):
        """
        Generates a uniformly random terrain array between height zl and zh

        Params:
            zl-zh defines the range we sample heights from 
            dims - (X, Y), NOT (row, col)
        """
        if len(dim) != 2:
            print("Dimensions of ground truth must be of form: (x, y)")
            return None
        arr = np.random.uniform(low=zl, high=zh, size=(dim[1], dim[0]))
        return arr
    
    def gen_flat(self, dim, base_z):
        arr = np.full((dim[1], dim[0]), base_z)
        return arr

    def gen_empty(self, dim):
        """
        Empty terrain array (useful to generate so maps still shows when don't have any terrain loaded)
        """
        arr = np.zeros((dim[1], dim[0]))
        return arr

    def add_hole_mound(self, base_arr, pos, radius, max_min):
        """
        Adds a hole/mound to the given terrain array. 

        The hole mound is a curve of the form: z = a*(x^2 + y^2), where a is some
        scalar (visualise here: https://www.geogebra.org/3d?lang=en)

        NOTE: the curve defines the DIFFERENCE in heights, which we then add to the 
              given array
    
        Params: 
            base_arr - terrain array to add the curve to
            pos - (x, y) position in array the curve will be centred at
            radius - radius of curve 
            max_min - defines either the maximum z (for mound) or minimum z (for hole)
                      NOTE: this minimum/maximum occurs at point pos (obviously)
        """
        x0, y0 = pos[0], pos[1]
        # -ve max_min == hole (+ve scalar), +ve max_min == mound (-ve scalar)
        scalar = -1*max_min / radius**2
        f = self.hump(scalar, x0, y0, max_min, radius)
        # vectorized lambda function to compute the function for a given (x, y)
        fn = np.vectorize(f, otypes=[float])
        # array of heights to be added to our base array
        arr = np.fromfunction(fn, base_arr.shape, dtype=float)
        base_arr+=arr
        return base_arr

    def add_wall(self, base_arr, pos, xwid, ywid, height):
        """
        Adds a wall to the given terrain array 
        """
        x0, y0 = pos[0], pos[1]
        xl, xh = x0 - xwid // 2, x0 + xwid // 2
        yl, yh = y0 - ywid // 2, y0 + ywid // 2
        base_arr[yl:yh, xl:xh] = height
        return base_arr
    
    def add_local_undul(self, base_arr, pos, xwid, ywid, base_z, dz):
        """
        Adds local undulation of given dz, centred at given pos
        """
        x0, y0 = pos[0], pos[1]
        xl, xh = int(x0 - xwid // 2), int(x0 + xwid // 2)
        yl, yh = int(y0 - ywid // 2), int(y0 + ywid // 2)
        
        base_undul = np.random.uniform(low=base_z, high=base_z+dz, size=base_arr.shape)
        base_arr[yl:yh, xl:xh] = base_undul[yl:yh, xl:xh]
        return base_arr
    
    def add_local_undul_patches(self, base_arr, n, xwid_range, ywid_range, base_z, dz_range):
        """
        Adds n patches of local undulation to the given terrain array.
        Patches have:
            -x and y widths within the given ranges AND;
            -dz heights within the given range
        
        NOTE:
            if want deterministic widths and dz, just pass (a,) instead of (a,b)
        """
        for _ in range(n):
            dz = np.random.uniform(low=dz_range[0], high=dz_range[1]) if len(dz_range) > 1 else dz_range[0]
            xwid = np.random.uniform(low=xwid_range[0], high=xwid_range[1]+1) if len(xwid_range) > 1 else xwid_range[1]
            ywid = np.random.uniform(low=ywid_range[0], high=ywid_range[1]+1) if len(ywid_range) > 1 else ywid_range[1]
            border = base_arr.shape[1] // 5
            x = int(np.random.uniform(low=xwid // 2 + border, high=base_arr.shape[1] - xwid // 2 - border))
            y = int(np.random.uniform(low=ywid // 2 + border, high=base_arr.shape[0] - ywid // 2 - border))
            pos = (x,y)
            self.add_local_undul(base_arr, pos, xwid, ywid, base_z, dz)
        return base_arr
    
    def add_flat(self, base_arr, pos, xwid, ywid, base_height):
        """
        Adds a flat section of terrain 
        """
        return self.add_wall(base_arr, pos, xwid, ywid, base_height)

    def gen_test(self, dim, mj_max_elev, mj_base_elev, mj_rand_dz, robot_im_pos_init, num_patches):
        """
        Test bed to generate the terrain arrays in
        """
        im_base_elev = (1 / mj_max_elev) * mj_base_elev
        
        # terrain has discrete patches of undulation
        if num_patches:
            gt = self.gen_flat(dim, im_base_elev)
            patch_ranges = [[gt.shape[1] // 25, gt.shape[1] // 15], [gt.shape[0] // 25, gt.shape[0] // 15]]
            gt = self.add_local_undul_patches(gt, num_patches, patch_ranges[0] , patch_ranges[1], 
                                              im_base_elev, (mj_rand_dz, 1.3*mj_rand_dz))
            gt = self.add_flat(gt, robot_im_pos_init, 5, 5, im_base_elev)
            # gt = self.add_wall(gt, (300,250), 20, 50, 1.0)
            return gt
        # whole terrain is undulated
        else:
            gt = self.gen_uniform_rand(im_base_elev, im_base_elev + mj_rand_dz, dim)
        return gt

    """
    Below this, can define any functions you want to be applied element-wise 
    to the array. 

    eg: hump is a lambda function used by add_hole_mound (above)
    """

    def hump(self, scalar, x0, y0, z0, radius):
        """
        Returns a lambda function to compute:
            z = scalar * ((x - x0)^2 + (y - y0)^2) + z0
        for all elements in an NxM matrix that lie within the given radius

        Params:
            x0, y0 - (x,y)/(col, row) the hump is to centred at
            z0 - base height of hump
            radius - ""

        NOTE: all elements outside the radius are given value 0
        """
        return (lambda row, col: 
                scalar*((col - x0)**2 + (row - y0)**2) + z0 
                if (col - x0)**2 + (row - y0)**2 < radius**2 
                else 0)

    
    # --------------------------------------------------
    # NOTE: DEPRECATED
    #       Instead, use lambda functions like in hump (above)
    # --------------------------------------------------

    # def gen_curve(self, xl, xh, yl, yh, fn):
    #     """
    #     fn is applied element-wise to generate a 2D numpy array that can serve as the basis of an 
    #     environment terrain
    #     NOTE: xl, xh, yl, yh define the x and y ranges (dimensions of the array)
    #     """
    #     x = np.linspace(xl, xh, xh-xl+1)
    #     y = np.linspace(yl, yh, yh-xl+1)
    #     x, y = np.meshgrid(x, y)
    #     fn = np.vectorize(fn)
    #     z = fn(x, y)
    #     # TODO : add plotting option
    #     return z
    
    # def saddle_func(self, x, y):
    #     return np.square(x) - np.square(y)

    # def gaussian(self, x, y, sigma=1):
    #     z = 25*(1/(2*np.pi*sigma**2)) * np.exp(-1*((0.1*x**2 + 0.1*y**2)/(2*sigma**2)))
    #     return z