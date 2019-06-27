from geometry import *

ball_light = Primitive([5, 1, 0.5], radius=1)
ball_light.is_light_source = False
ball_light.color = np.array([0.5, 1, 1])

green_triangle = Primitive(point_a=[5, 0, 0], point_b=[6, -2, 3], point_c=[5, -2, -1])
green_triangle.color = np.array([0.5, 1, 0.5])*140
green_triangle.is_light_source = True

test_scene = Scene({ball_light, green_triangle})

test_scene.camera.point = (15, 0, 0.5)
