import cv2
import numpy as np

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (0, 0, 255)
GREEN = (0, 255, 0)

# minimum image size can display
MIN_IMG_DIM = (250, 250)

def top_left_bot_right(x, y, X, Y):
    """
    Returns the top left and bottom right positions of an X x Y sub-section
    centred at (x,y)
    """
    min_x = x - X // 2
    min_y = y - Y // 2
    max_x = x + X // 2 + 1 if X % 2 == 1 else x + X // 2
    max_y = y + Y // 2 + 1 if Y % 2 == 1 else y + Y // 2
    return (min_x, min_y), (max_x - 1, max_y - 1)

def draw_arrow(img, pos, angle, color=RED, length=20):
    end_x = pos[0] + int(np.rint(length * np.cos(-angle)))
    end_y = pos[1] + int(np.rint(length * np.sin(-angle)))
    end = (end_x, end_y)
    thickness = 2
    cv2.arrowedLine(img, pos, end, color, thickness)

def draw_bounding_box(img, pos, X, Y, colour=WHITE):
    """
    Draws a bounding box of dimensions nxm onto the given image 

    NOTE: this is used to show the robot's height map FOV on the map
    in real time

    Params:
        pos - (x,y) image position of box's centre
        X,Y - dimensions of bounding box (pixels)
    """
    tl, br = top_left_bot_right(pos[0], pos[1], X, Y)
    # draw rectangle on copy to preserve the original
    thickness = max(2, img.shape[0] // 100)
    cv2.rectangle(img, tl, br, colour, thickness)

def draw_dot(img, pos, color=RED):
    """
    Draw a dot at specified position in the image 
    """
    radius = max(2, img.shape[0] // 100)
    thickness = -1
    cv2.circle(img, pos, radius=radius, color=color, thickness=thickness)

def display_img(img, title="Terrain map"):
    """
    Display the image for 1 millisecond

    NOTE: we resize the img to a visible dimension if needed

    """
    if img.shape[0] < MIN_IMG_DIM[0] or img.shape[1] < MIN_IMG_DIM[1]:
        img = cv2.resize(img, MIN_IMG_DIM)
    cv2.imshow(title, img)
    cv2.waitKey(1)

