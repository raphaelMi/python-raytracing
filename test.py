from geometry import *

ball = Primitive([5, 0, 0], radius=0.6)
ball.is_light_source = False
ball.color = np.array([0.2, 0.1, 0.1])
ball.specular = 32
ball.shininess = 0.07

light_src0 = Primitive(point_a=[0, 10, 17], radius=0.1)
light_src0.color = np.array([1, 1, 1]) * 50000
light_src0.is_light_source = True

light_src1 = Primitive(point_a=[0, -10, 17], radius=0.1)
light_src1.color = np.array([1, 1, 1]) * 100000
light_src1.is_light_source = True

bottom_wall = Primitive(point_a=[10, 0, -1], point_b=[0, -10, -1], point_c=[0, 10, -1])
bottom_wall.color = np.array([0.3, 0.2, 0.1])
left_wall = Primitive(point_a=[10, 0, -1], point_b=[0, -10, -1], point_c=[10, 0, 9])
left_wall.color = np.array([0.1, 0.2, 0.3])
right_wall = Primitive(point_a=[10, 0, -1], point_b=[0, 10, -1], point_c=[10, 0, 9])
right_wall.color = np.array([0.2, 0.3, 0.3])

test_scene_0 = Scene({light_src0, light_src1, bottom_wall, left_wall, right_wall, ball})

ball2 = Primitive([8, 0, -0.6], radius=2)
ball2.is_light_source = False
ball2.color = np.array([0.3, 0.1, 0.2])
ball2.specular = 32
ball2.shininess = 0.5

test_scene_1 = Scene({ball2, light_src0})
