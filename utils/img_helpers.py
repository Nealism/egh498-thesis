import cv2

# constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (0, 0, 255)

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

def draw_bounding_box(img, pos, X, Y, colour=WHITE, thickness=3):
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
    cv2.rectangle(img, tl, br, colour, thickness)

def draw_dot(img, pos, radius=5, color=RED, thickness=-1):
    cv2.circle(img, pos, radius=radius, color=color, thickness=thickness)

def display_img(img, title="Terrain map"):
    cv2.imshow(title, img)
    cv2.waitKey(1)

