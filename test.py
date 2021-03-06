from geometry import *
import random

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

bounding_sphere = Primitive([5,0,0], radius=1.25)

sphere1 = Primitive([5,0.75,0],radius=0.1)
sphere2 = Primitive([5,-0.75,0],radius=0.1)
sphere3 = Primitive([5,0.75,0.75],radius=0.1)
sphere4 = Primitive([5,-0.75,0.75],radius=0.1)
sphere5 = Primitive([5,-0.75,-0.75],radius=0.1)
sphere6 = Primitive([5,0.75,-0.75],radius=0.1)

sphere1.color = [random.random(),random.random(),random.random()]
sphere2.color = [random.random(),random.random(),random.random()]
sphere3.color = [random.random(),random.random(),random.random()]
sphere4.color = [random.random(),random.random(),random.random()]
sphere5.color = [random.random(),random.random(),random.random()]
sphere6.color = [random.random(),random.random(),random.random()]

test_scene_0 = Scene({None:{light_src0, light_src1, bottom_wall, left_wall, right_wall}, bounding_sphere:{ball,sphere1, sphere2, sphere3, sphere4, sphere5, sphere6}})

ball2 = Primitive([8, 0, -0.6], radius=2)
ball2.is_light_source = False
ball2.color = np.array([0.3, 0.1, 0.2])
ball2.specular = 32
ball2.shininess = 0.5

test_scene_1 = Scene({None:{ball2, light_src0}})

triag0 = Primitive(point_a=[7, -2, -3], point_b=[7, -2, 7], point_c=[2, -2, 2])
triag0.color = np.array([1, 0, 0])
triag1 = Primitive(point_a=[7, -2, -3], point_b=[7, -2, 7], point_c=[12, -2, 2])
triag1.color = np.array([0, 1, 1])

ball5 = Primitive([7, 0, 0], radius=0.6)
ball5.is_reflective = True

light_src3 = Primitive(point_a=[0, 10, 17], radius=5)
light_src3.color = np.array([1, 1, 1]) * 50000
light_src3.is_light_source = True

test_scene_2 = Scene({None:{light_src3, ball5, triag0, triag1}})