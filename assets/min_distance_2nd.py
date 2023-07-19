def intersection(line_start, line_end, rectangle_corners):
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

            if 0 <= t1 <= 1 and 0 <= t2 <= 1:
                intersection_point = (x1 + t1 * (x2 - x1), y1 + t1 * (y2 - y1))
                intersections.append(intersection_point)

    return intersections


line_start = (0, 0)
line_end = (5, 9)
rectangle_corners = [(2, 2), (2, 4), (4, 4), (4, 2)]

result = intersection(line_start, line_end, rectangle_corners)
print(result)
