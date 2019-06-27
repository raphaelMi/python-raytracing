from geometry import *

ball = Primitive([6, 1, 0.5], radius=1)
ball.is_light_source = False
ball.color = np.array([1, 0.5, 0.5])

green_triangle = Primitive(point_a=[5, 0, 0], radius=0.1)
green_triangle.color = np.array([1, 1, 1]) * 1400
green_triangle.is_light_source = True

bottom_wall = Primitive(point_a=[10, 0, -1], point_b=[0, -10, -1], point_c=[0, 10, -1])
bottom_wall.color = np.array([0.3, 0.2, 0.1])
left_wall = Primitive(point_a=[10, 0, -1], point_b=[0, -10, -1], point_c=[10, 0, 9])
left_wall.color = np.array([0.1, 0.3, 0.2])
right_wall = Primitive(point_a=[10, 0, -1], point_b=[0, 10, -1], point_c=[10, 0, 9])
right_wall.color = np.array([0.2, 0.3, 0.3])

test_scene = Scene({ball, green_triangle, bottom_wall, left_wall, right_wall})
