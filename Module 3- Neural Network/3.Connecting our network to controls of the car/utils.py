# if t is 0, it returns A
# if t is 1, it returns B
# if t is between 1 and 0,say 0.5, it is going to move half (0.5) away from A.
def lerp(a, b, t):
        return a + (b - a) * t


def get_intersection(A, B, C, D):
    t_top = (D['x'] - C['x']) * (A['y'] - C['y']) - (D['y'] - C['y']) * (A['x'] - C['x'])
    u_top = (C['y'] - A['y']) * (A['x'] - B['x']) - (C['x'] - A['x']) * (A['y'] - B['y'])
    bottom = (D['y'] - C['y']) * (B['x'] - A['x']) - (D['x'] - C['x']) * (B['y'] - A['y'])

    if bottom != 0:
        t = t_top / bottom
        u = u_top / bottom
        if 0 <= t <= 1 and 0 <= u <= 1:
            intersection_x = lerp(A['x'], B['x'], t)
            intersection_y = lerp(A['y'], B['y'], t)
            return {'x': intersection_x, 'y': intersection_y, 'offset': t}

    return None

def polys_intersect(poly1, poly2):
    for i in range(len(poly1)):
        for j in range(len(poly2)):
            p1 = poly1[i]
            p2 = poly1[(i + 1) % len(poly1)]
            q1 = poly2[j]
            q2 = poly2[(j + 1) % len(poly2)]

            touch = get_intersection(p1, p2, q1, q2)
            if touch:
                return True
    
    return False
