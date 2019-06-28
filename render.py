# This module is responsible for rendering a scene.

from geometry import *

MAX_RECURSION_DEPTH = 1
BACKGROUND_COLOR = np.array([0, 0, 0])
# evaluate flags
FLAG_DEFAULT = 0x00
FLAG_LIGHTS_ONLY = 0x01
FLAG_LIGHTS_SKIP = 0x02


class Ray:
    # ray has information about
    def __init__(self, point, vector):
        self.point = point
        self.vector = vector * (1 / np.linalg.norm(vector))

    def intersect(self, scene):
        # calculate the earliest intersection with a primitive of the scene

        nearest_dist = 10 ** 8 + 1
        nearest_prim = 0

        for prim in scene.primitives:
            # we use intersection testing algorithms from
            # http://www.iquilezles.org/www/articles/intersectors/intersectors.htm

            if prim.kind == KIND_SPHERE:

                origin_center = self.point - prim.points[0]
                b = np.dot(origin_center, self.vector)
                c = np.linalg.norm(origin_center) ** 2 - prim.radius ** 2
                h = b ** 2 - c
                if h >= 0.0:  # TODO check if this algorithm fails when ray origin is inside sphere
                    h = np.sqrt(h)
                    if nearest_dist > -b - h > 0 and not np.isclose(-b - h, 0):
                        nearest_dist = -b - h
                        nearest_prim = prim
                    if nearest_dist > -b + h > 0 and not np.isclose(-b + h, 0):
                        nearest_dist = -b + h
                        nearest_prim = prim

            elif prim.kind == KIND_TRIANGLE:

                v0v1 = prim.points[1] - prim.points[0]
                v0v2 = prim.points[2] - prim.points[0]
                rov0 = self.point - prim.points[0]

                n = np.cross(v0v1, v0v2)

                q = np.cross(rov0, self.vector)

                a = np.dot(self.vector, n)
                if not a == 0:
                    d = 1.0 / a

                    u = d * np.dot(-q, v0v2)
                    v = d * np.dot(q, v0v1)
                    t = d * np.dot(-n, rov0)

                    if 1.0 >= u >= 0.0 and 1.0 >= v >= 0.0 and (
                            u + v) <= 1.0 and nearest_dist > t > 0 and not np.isclose(t, 0):
                        nearest_dist = t
                        nearest_prim = prim
        if nearest_dist > 10 ** 8:  # no intersection
            return

        nearest_point = nearest_dist * self.vector + self.point
        normal = np.array([0.0, 0.0, 0.0])
        if nearest_prim.kind == KIND_SPHERE:
            normal = nearest_point - nearest_prim.points[0]
            normal = normal * (1 / np.linalg.norm(normal))
        elif nearest_prim.kind == KIND_TRIANGLE:
            normal = nearest_prim.normal

        return nearest_prim, nearest_point, nearest_dist, normal

    def evaluate(self, scene, recursion_depth, flag=FLAG_DEFAULT):
        # evaluates color and brightness of a given ray recursively for a set depth of recursion
        # [1.0, 1.0, 1.0] is white

        if recursion_depth > MAX_RECURSION_DEPTH:
            # rays die after exceeding depth of recursion
            return np.array([0.0, 0.0, 0.0])

        try:
            prim, coord, length, normal = self.intersect(scene)
        except TypeError:
            # if ray did not make any intersection, return
            return BACKGROUND_COLOR

        if prim.is_light_source:
            if flag & FLAG_LIGHTS_SKIP:
                return np.array([0.0, 0.0, 0.0])
            # if the ray hits a light source we can stop iterating
            return prim.color / (length+1) ** 2

        if flag & FLAG_LIGHTS_ONLY:
            return np.array([0.0, 0.0, 0.0])

        incoming_lightrays = []

        # diffuse lightrays heading to source
        for light_prim in scene.lights:
            if light_prim.kind == KIND_SPHERE:
                light_point = light_prim.points[0]
            elif light_prim.kind == KIND_TRIANGLE:
                light_point = sum(light_prim.points) / 3
            else:
                continue

            light_vector = light_point - coord
            c = Ray(coord, light_vector).evaluate(scene, MAX_RECURSION_DEPTH, flag=FLAG_LIGHTS_ONLY)
            c = c * np.abs(np.dot(normal, light_vector)) / (np.linalg.norm(light_vector) * np.linalg.norm(normal))
            # intensity has to be scaled down relative to the angle

            incoming_lightrays.append(c)

        # diffuse lightray in direction of normal (heuristic)
        # d = Ray(coord, normal).evaluate(scene, MAX_RECURSION_DEPTH, flag=FLAG_LIGHTS_SKIP)
        # incoming_lightrays.append(d)

        # diffuse lightray in random direction (introduces noise)
        delta = np.random.randn(3)
        delta /= np.linalg.norm(delta)
        diffuse_vector = normal + delta
        d = Ray(coord, diffuse_vector).evaluate(scene, MAX_RECURSION_DEPTH - 1, flag=FLAG_LIGHTS_SKIP)
        d = d * np.abs(np.dot(normal, diffuse_vector)) / (np.linalg.norm(diffuse_vector) * np.linalg.norm(normal))
        incoming_lightrays.append(d)

        result = np.multiply(sum(incoming_lightrays), prim.color)
        return result / (length+1) ** 2
        # if prim.shininess == 0.0:
        #    pass

        # TODO:
        # depending on the texture of the primitive, calculate more rays and combine result
        # light_reflection = Ray(coords, self.vector - 2*np.dot(self.vector,normal)*normal)
        #                       .evaluate(scene,recursion_depth+1)
        # light_source = Ray(coords, scene.light.coords - coords).eval...
        # light_diffuse = ...
        # light_refraction...
        # return np.quick_maths(light...)


def ray_iterator(camera, resolution, start_row, end_row, start_column, end_column):
    # this function enables iteration through every pixel on the FOV for the specified part to be rendered
    # yield ray,(x,y)...

    half_fov_width = np.tan(camera.fov_width_angle / 2)
    ratio = resolution[1] / resolution[0]
    half_fov_height = half_fov_width * ratio
    top_left = np.array([1, -half_fov_width, half_fov_height])
    down = np.array([0, 0, -2 * half_fov_height])
    right = np.array([0, 2 * half_fov_width, 0])

    for y in range(end_row - start_row + 1):
        for x in range(resolution[0] - start_column if y == 0 else (end_column + 1 if y == end_row else resolution[0])):
            yield Ray(camera.point,
                      top_left + x / resolution[0] * right + y /
                      resolution[1] * down), (x, y)


def render_scene(scene: Scene, **config):
    # Iterates through all pixels in viewport, traces rays and draws to bitmap. For the documentation of the config
    # parameters, look at main.py. The method is expected to return a 2D array containing the exact block as
    # requested. The size of the first and last column may vary - therefore take the parameters "firstColumn" and
    # "lastColumn" into account

    w = config["width"]
    h = config["height"]

    start_row = config["start_row"]
    start_column = config["start_column"]

    end_row = config["end_row"]
    end_column = config["end_column"]

    pixels = []

    for ray, pixel in ray_iterator(scene.camera, [w, h], start_row, end_row, start_column, end_column):
        color = np.uint8(np.clip(ray.evaluate(scene, 0) * 255, a_min=0, a_max=255))
        x = pixel[0]
        y = pixel[1]
        if len(pixels) <= y:
            pixels.append([])
        row = pixels[y]
        if (len(row)) <= x:
            row.append([])
        row[x] = color

    return pixels
