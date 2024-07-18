import os
import imageio


import re

# Natural sorting function
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

# Directory containing the images
image_dir = '/home/kom018/refarm/src/multi_robot_rl/scripts/plots/r1_image'
# Path to save the output video
output_video = '/home/kom018/refarm/src/multi_robot_rl/scripts/plots/r1_image/robot1_image_sorted.mp4'

# Get list of image files
image_files = sorted([os.path.join(image_dir, img) for img in os.listdir(image_dir) if img.endswith('.png')], key=natural_sort_key)

# Define the frame rate (e.g., 30 frames per second)
frame_rate = 30

# Read images and write them to video
writer = imageio.get_writer(output_video, fps=frame_rate)
for image_file in image_files:
    image = imageio.imread(image_file)
    writer.append_data(image)
writer.close()

print(f"Video saved as {output_video}")

# Natural sorting function
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

# Directory containing the images
image_dir = '/home/kom018/refarm/src/multi_robot_rl/scripts/plots/r2_image'
# Path to save the output video
output_video = '/home/kom018/refarm/src/multi_robot_rl/scripts/plots/r2_image/robot2_image_sorted.mp4'

# Get list of image files
image_files = sorted([os.path.join(image_dir, img) for img in os.listdir(image_dir) if img.endswith('.png')], key=natural_sort_key)

# Define the frame rate (e.g., 30 frames per second)
frame_rate = 30

# Read images and write them to video
writer = imageio.get_writer(output_video, fps=frame_rate)
for image_file in image_files:
    image = imageio.imread(image_file)
    writer.append_data(image)
writer.close()

print(f"Video saved as {output_video}")
