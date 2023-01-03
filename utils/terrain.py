import numpy as np
import cv2
from lxml import etree

# constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (0, 0, 255)

"""
Class to represent any terrains loaded into mujoco. Terrains are generated
loading numpy arrays as PNG images into mujoco hfield objects.
"""
class Terrain():
    def __init__(self, terr_arr, path, img_name):
        self.img_name = img_name
        self.img_path = path + img_name
        # terrain array (numpy array)
        self.terr_arr = terr_arr         
        # terrain image (PNG)
        self.terr_img = self.load_terr_img() 
        self.image_dim = self.terr_arr.shape

    def load_terr_img(self):
        """ 
        Loads the terrain image
        """ 
        cv2.imwrite(self.img_path, self.terr_arr)
        img = cv2.imread(self.img_path)
        return img
    
    def compute_sub_section(self, i, j, n, m):
        """
        Given an (i, j) index in the terrain array, compute the n x m subsection around (i, j)

        Params:
            i, j - (i, j) index in arr
            n, m - dimensions of sub-section to compute
        
        Returns:
            sub_section array
        """
        min_row, min_col, max_row, max_col = self.top_left_bot_right(i, j, n, m)
        # check sub-section is in range of the base arr
        if (max_row + 1 > self.terr_arr.shape[0] 
            or max_col + 1 > self.terr_arr.shape[1] 
            or min_row < 0 
            or min_col < 0):
            print("Sub-section out of range")
            return None
        
        return self.terr_arr[min_row:max_row, min_col:max_col]

    def rob_to_img_pos(self, pos, x_rad, y_rad):
        """
        Converts an position in mujoco to an (i, j) index in the terrain image

        NOTE: Assumes hfield is centred at pos == (0, 0) in mujoco

        Params:
            pos - mujoco position
            x_rad, y_rad - radii of mujoco hfield in x and y directions
        """
        # +x == +i (right in mujoco and right in image respectively)
        i = int((pos[0] + x_rad) * ((self.image_dim[0] // 2) // x_rad))
        # +y == -j (up-screen in mujoco and down-screen in image respectively)
        j = int((-1 * pos[1] + y_rad) * ((self.image_dim[1] // 2) // x_rad))
        return (i, j)
    
    def img_to_rob_pos(self, pos, x_rad, y_rad):
        """
        Converts an (i, j) index in the terrain image to an (x,y) position in
        mujoco

        Params:
            pos - image position
            x_rad, y_rad - radii of mujoco hfield in x and y directions
        """
        pass

    @staticmethod
    def draw_bounding_box(img, pos, n, m, colour=WHITE, thickness=3):
        """
        Draws a bounding box of dimensions nxm onto the given image 

        NOTE: this is used to show the robot's height map FOV on the map
        in real time

        Params:
            pos - (i,j) image position of box's centre
            n,m - dimensions of bounding box (pixels)
        """
        tl, br = Terrain.top_left_bot_right(pos[0], pos[1], n, m)
        # draw rectangle on copy to preserve the original
        cv2.rectangle(img, tl, br, colour, thickness)
    
    @staticmethod
    def draw_dot(img, pos, radius=5, color=RED, thickness=-1):
        cv2.circle(img, pos, radius=radius, color=color, thickness=thickness)

    @staticmethod
    def display_img(img, title="terrain map"):
        cv2.imshow(title, img)
        cv2.waitKey(1)

    @staticmethod
    def top_left_bot_right(i, j, n, m):
        """
        Returns the top left and bottom right positions of an nxm sub-section
        centred at (i, j)

        NOTE: this can be used for both the image array and mujoco positions 
        """
        min_row = i - n // 2
        min_col = j - m // 2
        max_row = i + n // 2 + 1 if n % 2 == 1 else i + m // 2
        max_col = j + m // 2 + 1 if m % 2 == 1 else j + m // 2
        return (min_row, min_col), (max_row - 1, max_col - 1)
    
    """
A class to generate terrain arrays for Terrain instances (see above)
"""
class TerrainGen():
    def gen_rand_ground_truth(self, zl, zh, dimensions):
        """
        Randomly generates a 2D numpy array that serves as the basis for the height map.
        NOTE: zl and zh define the range we sample from 
        """
        if len(dimensions) != 2:
            print("Dimensions of ground truth must be of form: (x, y) (or any numpy equivalent)")
            return None
        gt = np.random.uniform(low=zl, high=zh, size=dimensions)
        return gt

    def gen_curve(self, xl, xh, yl, yh, num_points, fn, plot=False):
        """
        fn is applied element-wise to generate a 2D numpy array that can serve as the basis of a surface in mujoco.
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

if __name__ == "__main__":
    pass