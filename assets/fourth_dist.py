import math
from heapq import nsmallest

def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def find_closest_coordinates(center_box1, box2_corners):
    distances = [(distance(center_box1, corner), corner) for corner in box2_corners]
    sorted_distances = sorted(distances, key=lambda x: x[0])
    
    return sorted_distances

# Example usage
center_box1 = (3, 3)
box2_corners = [(2, 2), (2, 6), (6, 2), (6, 6)]
closest_coordinates = find_closest_coordinates(center_box1, box2_corners)

b=[]
for i, (min_dist, closest_point) in enumerate(closest_coordinates, start=1):
    print(f"{i} closest point:", closest_point)
    print(f"Distance: {min_dist:.2f}")
    print()
    b.append(closest_point)

print(b)
