from PIL import Image
import numpy as np

class TerrainGen():
    def load_im_from_arr(self, arr, path, name, file_type, grayscale=True):
        im = Image.fromarray(arr)
        if grayscale:
            im = im.convert("L") 
        im.save(path + name, file_type)
        return im
    
    def gen_rand_ground_truth(self, z_low, z_high, dimensions):
        if len(dimensions) != 2:
            print("Dimensions of ground truth must be of form: (x, y) (or any numpy equivalent)")
            return None
        gt = np.random.uniform(low=z_low, high=z_high, size=dimensions)
        return gt

    def gen_curve(self, xl, xh, yl, yh, num_points, fn, plot=False):
        x = np.linspace(xl, xh, num_points)
        y = np.linspace(yl, yh, num_points)
        x, y = np.meshgrid(x, y)
        fn = np.vectorize(fn)
        z = fn(x, y)
        # TODO : add plotting option
        return z
    
    def saddle_func(self, x, y):
        return np.square(x) - np.square(y)

    def hump_func(self, x, y):
        return (np.square(x) + np.square(y))

    
