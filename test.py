from geometry import *

ball_light = Primitive([0, 5, 2], radius=0.2)
ball_light.is_light_source = True
ball_light.color = np.array([1, 1, 1])*500

red_triangle = Primitive(point_a=[5, 0, 0], point_b=[0, 5, 0], point_c=[0, 0, 5])
red_triangle.color = np.array([0.5, 0.2, 0.2])
red_triangle.is_light_source = False

blue_triangle = Primitive(point_a=[5, 0, 0], point_b=[0, 0, 5], point_c=[0, 5, 5])
blue_triangle.color = np.array([0.2, 0.2, 0.5])
blue_triangle.is_light_source = False

test_scene = Scene({ball_light, blue_triangle, red_triangle})

test_scene.camera.point = (1, 1, 1)
