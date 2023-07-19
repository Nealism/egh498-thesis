import math

def intersection(line_start, line_end, rectangle_corners):
    int=False
    x1, y1 = line_start
    x2, y2 = line_end

    intersections = []

    for i in range(4):
        x3, y3 = rectangle_corners[i]
        x4, y4 = rectangle_corners[(i + 1) % 4]

        denominator = ((x4 - x3) * (y1 - y2)) - ((x1 - x2) * (y4 - y3))

        if denominator != 0:
            t1 = ((x1 - x3) * (y4 - y3) - (y1 - y3) * (x4 - x3)) / denominator
            t2 = ((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator
            print(t1,t2)

            if 0 <= t1 <= 1 and 0 <= t2 <= 1:
                int=True
                intersection_point = (x1 + t1 * (x2 - x1), y1 + t1 * (y2 - y1))
                
                intersections.append(intersection_point)

    return intersections, int


line_start = (0, 0)
line_end = (4, 5)
rectangle_corners = [(2, 9), (2, 4), (4, 9), (4, 2)]

result = intersection(line_start, line_end, rectangle_corners)
print(result)


def smallest_rectangle(intersection_points):
    if len(intersection_points) < 2:
        return None

    x_coords, y_coords = zip(*intersection_points)
    min_x = min(x_coords)
    max_x = max(x_coords)
    min_y = min(y_coords)
    max_y = max(y_coords)

    return [(min_x, min_y), (min_x, max_y), (max_x, max_y), (max_x, min_y)]

# Example usage:
line_start = (0, 0)
line_end = (5, 5)
rectangle_corners = [(2, 2), (2, 4), (4, 4), (4, 2)]

intersections = intersection(line_start, line_end, rectangle_corners)
smallest_rect_coords = smallest_rectangle(intersections)

print(smallest_rect_coords)


