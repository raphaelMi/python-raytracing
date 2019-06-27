from geometry import *

ball = Primitive([5, 0, -0.6], radius=0.3)
ball.is_light_source = False
ball.color = np.array([0.3, 0.1, 0.2])

lightsrc0 = Primitive(point_a=[5, 1, 1], radius=0.1)
lightsrc0.color = np.array([1, 1, 1])*700
lightsrc0.is_light_source = True

lightsrc1 = Primitive(point_a=[5, -1, 1], radius=0.1)
lightsrc1.color = np.array([1, 1, 1])*700
lightsrc1.is_light_source = True

bottom_wall = Primitive(point_a=[10, 0, -1], point_b=[0, -10, -1], point_c=[0, 10, -1])
bottom_wall.color = np.array([0.3, 0.2, 0.1])
left_wall = Primitive(point_a=[10, 0, -1], point_b=[0, -10, -1], point_c=[10, 0, 9])
left_wall.color = np.array([0.1, 0.2, 0.3])
right_wall = Primitive(point_a=[10, 0, -1], point_b=[0, 10, -1], point_c=[10, 0, 9])
right_wall.color = np.array([0.2, 0.3, 0.3])

test_scene = Scene({lightsrc0, lightsrc1, bottom_wall, left_wall, right_wall, ball})
