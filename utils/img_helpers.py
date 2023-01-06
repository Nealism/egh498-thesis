import cv2

# constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (0, 0, 255)

def top_left_bot_right(i, j, n, m):
    """
    Returns the top left and bottom right positions of an nxm sub-section
    centred at (i, j)
    """
    min_row = i - n // 2
    min_col = j - m // 2
    max_row = i + n // 2 + 1 if n % 2 == 1 else i + m // 2
    max_col = j + m // 2 + 1 if m % 2 == 1 else j + m // 2
    return (min_row, min_col), (max_row - 1, max_col - 1)

def draw_bounding_box(img, pos, n, m, colour=WHITE, thickness=3):
    """
    Draws a bounding box of dimensions nxm onto the given image 

    NOTE: this is used to show the robot's height map FOV on the map
    in real time

    Params:
        pos - (i,j) image position of box's centre
        n,m - dimensions of bounding box (pixels)
    """
    tl, br = top_left_bot_right(pos[0], pos[1], n, m)
    # draw rectangle on copy to preserve the original
    cv2.rectangle(img, tl, br, colour, thickness)

def draw_dot(img, pos, radius=5, color=RED, thickness=-1):
    cv2.circle(img, pos, radius=radius, color=color, thickness=thickness)

def display_img(img, title="Terrain map"):
    cv2.imshow(title, img)
    cv2.waitKey(1)

