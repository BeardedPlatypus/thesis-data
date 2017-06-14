import json
import os
import random

import bpy
from pathlib import *

import math

# ------------------------------------------------------------------------------
#  Conf
OBJ_PATH = Path("C:/Users/Monthy/Documents/projects/thesis/thesis-data-suite/scenes/spaceship-indoor/obj/")
GEO_PATH = Path("C:/Users/Monthy/Documents/projects/thesis/thesis-data-suite/scenes/spaceship-indoor/geometry/")
LIGHT_PATH = Path("C:/Users/Monthy/Documents/projects/thesis/thesis-data-suite/scenes/spaceship-indoor/lights/")


# ------------------------------------------------------------------------------
#  Geometry
class Mesh(object):
    def __init__(self, mesh_id, path):
        self._mesh_id = mesh_id
        self._path = path

    @property
    def mesh_id(self):
        return self._mesh_id

    @property
    def path(self):
        return self._path

    def to_json_dic(self):
        return { "id": self.mesh_id,
                 "path": self.path }


class Obj(object):
    def __init__(self, mesh_id, name, rotation, translation):
        self._mesh_id = mesh_id
        self._name = name
        self._rotation = rotation
        self._translation = translation

    @property
    def mesh_id(self):
        return self._mesh_id

    @property
    def name(self):
        return self._name

    @property
    def rotation(self):
        return self._rotation

    @property
    def translation(self):
        return self._translation

    def to_json_dic(self, shader_id):
        return { "mesh_id": self.mesh_id,
                 "name": self.name,
                 "shader_id": shader_id,
                 "rotation": { "x": self.rotation[0],
                               "y": self.rotation[1],
                               "z": self.rotation[2] },
                 "translation": { "x": self.translation[0],
                                  "y": self.translation[1],
                                  "z": self.translation[2] * -1.0 }}


def build_geo_dic(shader_id: str,
                  meshes: list,
                  objects: list):
    json_meshes = list(m.to_json_dic() for m in meshes)
    json_objects = list(o.to_json_dic(shader_id) for o in objects)

    return { "meshes": json_meshes,
             "objects": json_objects }


def extract_geometry_from_blend():
    obj_count ={ 'Box'            : 0
               , 'CornerLeft'     : 0
               , 'CornerRight'    : 0
               , 'CorridorSmall'  : 0
               , 'CorridorWide'   : 0
               , 'Junction-4'     : 0
               , 'Junction-T-stw' : 0
               , 'Junction-T-wts' : 0
               , 'PanelA'         : 0
               , 'PanelB'         : 0
               , 'PanelC'         : 0
               , 'PanelD'         : 0
               , 'PanelE'         : 0
               , 'PanelF'         : 0
               , 'PanelG'         : 0
               }

    panels = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

    obj_list = []
    objects = bpy.data.scenes[0].objects

    for obj in objects:
        if obj.type == 'EMPTY' and "::" in obj.name:
            obj_type, obj_name = obj.name.split("::")
            obj_name = obj_name.split(".")[0]

            if obj_type == 'Panel':
                obj_type = 'Panel{}'.format(panels[random.randrange(7)])

            if obj_type == 'obj' and obj_name in obj_count:
                obj_translation = obj.matrix_world.to_translation()
                obj_rotation = obj.matrix_world.to_euler()

                # transform into nTiled coordinate system
                obj_translation = (obj_translation[0], obj_translation[2], obj_translation[1])
                obj_rotation = (obj_rotation[0], obj_rotation[2], obj_rotation[1])

                obj_list.append(Obj(mesh_id=obj_name,
                                    name=("{}.{}".format(obj_name, obj_count[obj_name])),
                                    rotation=obj_rotation,
                                    translation=obj_translation ))
                obj_count[obj_name] += 1

    mesh_list = []
    for key in obj_count:
        if obj_count[key] > 0:
            mesh_list.append(Mesh(key, str(OBJ_PATH / Path("{}.obj".format(key)))))

    return (mesh_list, obj_list)


# ------------------------------------------------------------------------------
#  Lights
class Light(object):
    def __init__(self, position, intensity, radius):
        self._position = position
        self._intensity = intensity
        self._radius = radius

    @property
    def position(self):
        return self._position

    @property
    def intensity(self):
        return self._intensity

    @property
    def radius(self):
        return self._radius

    def to_json_dic(self):
        return { "position": { "x": float(self.position[0]),
                               "y": float(self.position[1]),
                               "z": float(self.position[2]) * -1.0 },
                 "intensity": { "r": float(self.intensity[0]),
                                "g": float(self.intensity[1]),
                                "b": float(self.intensity[2]) },
                 "radius": float(self.radius) }

    def build_in_blender(self):
        position = (self.position[0], self.position[2], self.position[1])
        bpy.ops.mesh.primitive_uv_sphere_add(size=self.radius,
                                             view_align=False,
                                             enter_editmode=False,
                                             location=position,
                                             layers=(False,
                                                     False,
                                                     False,
                                                     False,
                                                     False,
                                                     False,
                                                     False,
                                                     False,
                                                     False,
                                                     False,
                                                     False,
                                                     False,
                                                     False,
                                                     False,
                                                     False,
                                                     False,
                                                     False,
                                                     False,
                                                     False,
                                                     True))
        ob = bpy.context.object
        bpy.ops.object.shade_smooth()

        ob.name = "LightSphere"


def hsv_to_rgb(hsv : tuple):
    # Check pre conditions
    if (len(hsv) != 3 ):
        return (0.0, 0.0, 0.0)

    if (hsv[0] is None or not isinstance(hsv[0], float)):
        return (0.0, 0.0, 0.0)

    # Convert value
    hue = hsv[0] % 360.0
    saturation = hsv[1]
    value = hsv[2]

    chroma = hue * saturation

    h_sec = hue / 60.0
    intermediate = chroma * ( 1 - abs((h_sec % 2) - 1))

    # calculate second r_1, g_1, b_1
    if h_sec < 1.0:
        rgb_1 = ( chroma, intermediate, 0.0)
    elif h_sec < 2.0:
        rgb_1 = ( intermediate, chroma, 0.0)
    elif h_sec < 3.0:
        rgb_1 = ( 0.0, chroma, intermediate )
    elif h_sec < 4.0:
        rgb_1 = ( 0.0, intermediate, chroma, )
    elif h_sec < 5.0:
        rgb_1 = ( intermediate, 0.0, chroma )
    else:
        rgb_1 = ( chroma, 0.0, intermediate )

    m = value - chroma
    return ( rgb_1[0] + m, rgb_1[1] + m, rgb_1[2] + m )


class LightSpawner(object):
    def __init__(self, anchor, number, size_x, size_y, size_z, t):
        self._anchor = anchor
        self._x = bpy.data.scenes[0].objects["light::X.{}".format(number)]
        self._y = bpy.data.scenes[0].objects["light::Y.{}".format(number)]
        self._z = bpy.data.scenes[0].objects["light::Z.{}".format(number)]

        self._size_x = size_x
        self._size_y = size_y
        self._size_z = size_z

        self._t = t

    @property
    def origin(self):
        origin = self._anchor.matrix_world.to_translation()
        return (origin[0], origin[2], origin[1])

    @property
    def x_empty(self):
        x = self._x.matrix_world.to_translation()
        return (x[0], x[2], x[1])

    @property
    def y_empty(self):
        y = self._y.matrix_world.to_translation()
        return (y[0], y[2], y[1])

    @property
    def z_empty(self):
        z = self._z.matrix_world.to_translation()
        return (z[0], z[2], z[1])

    @property
    def x_axis(self):
        origin = self.origin
        x_empty = self.x_empty
        return (x_empty[0] - origin[0], x_empty[1] - origin[1], x_empty[2] - origin[2])

    @property
    def y_axis(self):
        origin = self.origin
        y_empty = self.y_empty
        return (y_empty[0] - origin[0], y_empty[1] - origin[1], y_empty[2] - origin[2])

    @property
    def z_axis(self):
        origin = self.origin
        z_empty = self.z_empty
        return (z_empty[0] - origin[0], z_empty[1] - origin[1], z_empty[2] - origin[2])

    @property
    def size_x(self):
        return self._size_x

    @property
    def size_y(self):
        return self._size_y

    @property
    def size_z(self):
        return self._size_z

    @property
    def t(self):
        return self._t

    def generate_lights(self, n_x, n_y, n_z, radius):
        origin = self.origin

        n_lights_x = self.size_x * n_x
        n_lights_y = self.size_y * n_y
        n_lights_z = self.size_z * n_z

        x_axis = self.x_axis
        y_axis = self.y_axis
        z_axis = self.z_axis

        def calculate_length(axis):
            return math.sqrt(axis[0] * axis[0] + axis[1] * axis[1] + axis[2] * axis[2])

        len_x = calculate_length(x_axis)
        len_y = calculate_length(y_axis)
        len_z = calculate_length(z_axis)


        spacing_x = len_x / (n_lights_x + 1)
        spacing_y = len_y / (n_lights_y + 1)
        spacing_z = len_z / (n_lights_z + 1)

        norm_x_axis = (x_axis[0] / len_x, x_axis[1] / len_x, x_axis[2] / len_x)
        norm_y_axis = (y_axis[0] / len_y, y_axis[1] / len_y, y_axis[2] / len_y)
        norm_z_axis = (z_axis[0] / len_z, z_axis[1] / len_z, z_axis[2] / len_z)

        def random_rgb_colour():
            colour = [0.0, 0.0, 0.0]

            colour_options = [ (0, 1),
                               (0, 2),
                               (1, 0),
                               (1, 2),
                               (2, 0),
                               (2, 1) ]
            colour_def = colour_options[random.randint(0,5)]
            colour[colour_def[0]] = 1.0
            colour[colour_def[1]] = random.random()

            return (colour[0], colour[1], colour[2])

        lights = []

        for x_i in range(1, n_lights_x + 1):
            for y_i in range(1, n_lights_y + 1):
                for z_i in range(1, n_lights_z + 1):
                    colour = random_rgb_colour()
                    position = (
                        x_i * norm_x_axis[0] * spacing_x + y_i * norm_y_axis[0] * spacing_y + z_i * norm_z_axis[0] * spacing_z + origin[0],
                        x_i * norm_x_axis[1] * spacing_x + y_i * norm_y_axis[1] * spacing_y + z_i * norm_z_axis[1] * spacing_z + origin[1],
                        x_i * norm_x_axis[2] * spacing_x + y_i * norm_y_axis[2] * spacing_y + z_i * norm_z_axis[2] * spacing_z + origin[2])

                    lights.append(Light(position, colour, radius))
        return lights


def build_light_dic(lights):
    return { "lights": list(l.to_json_dic() for l in lights) }


def extract_light_spawners_from_blend():
    # Obtain light generators
    objects = bpy.data.scenes[0].objects

    light_spawners = []
    for obj in objects:
        if obj.type == "EMPTY" and "::" in obj.name:
            ty, name = obj.name.split("::")

            if (ty == "light" and
                "Anchor" in name
                and "." in name
                and "#" in name
                and "_" in name
                and "$" in name):

                name, number = name.split(".")
                t, name = name.split('$')
                size, name = name.split("#")
                n_x, n_y, n_z = size.split("_")

                light_spawners.append(LightSpawner(anchor=obj,
                                                   number=number,
                                                   size_x=int(n_x),
                                                   size_y=int(n_y),
                                                   size_z=int(n_z),
                                                   t=t))
    return light_spawners


def generate_lights(size_dic, n_width, n_height, n_depth):
    light_spawners = extract_light_spawners_from_blend()
    print("Number of light spawners generated: {}".format(len(light_spawners)))

    lights = []

    for spawner in light_spawners:
        lights +=  spawner.generate_lights(n_width,
                                           n_depth,
                                           n_height,
                                           size_dic[spawner.t])

    return lights


# ------------------------------------------------------------------------------
#  misc
def write_to_json(path, data):
    with open(path, 'w') as f:
        f.write(json.dumps(data, indent=2))





# ------------------------------------------------------------------------------
#  Main
if __name__ == "__main__":
    meshes, objects = extract_geometry_from_blend()

    shaders = [ "forward_attenuated",
                "forward_tiled",
                "forward_clustered",
                "forward_hashed",
                "deferred_attenuated",
                "deferred_tiled",
                "deferred_clustered",
                "deferred_hashed" ]

    for s in shaders:
        json_dic = build_geo_dic(s, meshes, objects)
        write_to_json(path= str(GEO_PATH / Path("{}.json".format(s))),
                      data=json_dic)

    for x in range(1, 4):
        for z in range(1, 4):
            for y in range(1, 4):
                lights = generate_lights({"small": 16.0, "big": 23.0}, x, y, z)
                n_lights = len(lights)
                write_to_json(path=str(LIGHT_PATH / Path("{}#{}x_{}y_{}z.json".format(n_lights, x, y, z))),
                              data=build_light_dic(lights))


#   for l in lights:
#       l.build_in_blender()
