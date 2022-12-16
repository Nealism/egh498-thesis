from PIL import Image
import numpy as np
from pathlib import Path
import cv2

class TerrainGen():
    def load_im_from_arr(self, arr, path, name, file_type, grayscale=True):
        """
        Creates an image of the given type from the given numpy array and saves it to the given path
        """
        im = Image.fromarray(arr)
        if grayscale:
            im = im.convert("L") 
        im.save(path + name, file_type)
        return im
    
    def load_im_from_arr_2(self, arr, path, name, file_type):
        img = cv2.imwrite(path + name, arr)
        return img
    
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
    
    def get_sub_section(self, arr, i, j, n, m):
        """
        Given an (i, j) index in a 2D numpy array, compute the n x m subsection around (i, j)

        Params:
            arr - ""
            i, j - (i, j) index in arr
            n, m - dimensions of sub-section to compute
        
        Returns:
            top_left, bot_right, sub_section_arr
        
        where:
            top_left = (i, j) of top left point
            bot_right = (i, j) of bottom right point
            sub_section_arr = computed subsection
        """
        min_row = i - n // 2
        min_col = j - m // 2
        max_row = i + n // 2 + 1 if n % 2 == 1 else i + n // 2
        max_col = j + m // 2 + 1 if m % 2 == 1 else j + m // 2

        # check sub-section is in range of the base arr
        if max_row > arr.shape[0] or max_col > arr.shape[1] or min_row < 0 or min_col < 0:
            print("Sub-section out of range")
            return None
        
        return (min_row, min_col), (max_row - 1, max_col - 1), arr[min_row:max_row, min_col:max_col]

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
    t = TerrainGen()
    path = str(Path(__file__).parent.resolve())
    img = t.gen_rand_ground_truth(0, 1, (300, 300))
    cv2.imwrite(path + '/cv_test.png', img)
    cv2.imshow("image", img)
    cv2.waitKey(0)
    
    