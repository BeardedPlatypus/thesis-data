import json
import os
import random

import bpy
from pathlib import *

# ------------------------------------------------------------------------------
#  Conf
OBJ_PATH = Path("C:/Users/Monthy/Documents/projects/thesis/thesis-data-suite/scenes/pipers-alley/obj/")
GEO_PATH = Path("C:/Users/Monthy/Documents/projects/thesis/thesis-data-suite/scenes/pipers-alley/geo-json/")
LIGHT_PATH = Path("C:/Users/Monthy/Documents/projects/thesis/thesis-data-suite/scenes/pipers-alley/lights-json/")
SCENE_PATH = Path("C:/Users/Monthy/Documents/projects/thesis/thesis-data-suite/scenes/pipers-alley/scene-json/")


# ------------------------------------------------------------------------------
#  Scene
def build_scene_dic(pipeline_type: str,
                    viewport: tuple,
                    camera_eye: tuple,
                    camera_centre: tuple,
                    camera_up: tuple,
                    camera_fovy: float,
                    camera_aspect: float,
                    camera_clip: tuple,
                    camera_control: str,
                    camera_path: str,
                    camera_output_type: str,
                    camera_output_start: int,
                    camera_output_end: int,
                    camera_output_path: str,
                    exit_frame: int,
                    log_is_logging: bool,
                    log_output_path: str,
                    log_start: int,
                    log_end: int,
                    geometry: list,
                    lights: list,
                    tile_size: tuple):
    return { "pipeline": pipeline_type,
             "tile_size": { "x": tile_size[0],
                            "y": tile_size[1],
             },
             "viewport": { "width":  viewport[0],
                           "height": viewport[1] },
             "camera": { "eye": { "x": camera_eye[0],
                                  "y": camera_eye[1],
                                  "z": camera_eye[2] },
                         "center": { "x": camera_centre[0],
                                     "y": camera_centre[1],
                                     "z": camera_centre[2] },
                         "up": { "x": camera_up[0],
                                 "y": camera_up[1],
                                 "z": camera_up[2], },
                         "fovy": camera_fovy,
                         "aspect": camera_aspect,
                         "clip": { "near": camera_clip[0],
                                   "far": camera_clip[1] },
                         "control": camera_control,
                         "frames_path": camera_path,
                         "output": { "type": camera_output_type,
                                     "frames_start": camera_output_start,
                                     "frames_end": camera_output_end,
                                     "image_base_path": camera_output_path }},
             "exit_frame": exit_frame,
             "log": { "is_logging": log_is_logging,
                      "output_path": log_output_path,
                      "frame_start": log_start,
                      "frame_end": log_end },
             "geometry": geometry,
             "lights": lights }


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
    obj_count = { "Arch": 0,
                  "Barrel": 0,
                  "Building_01": 0,
                  "Building_02": 0,
                  "Building_03": 0,
                  "Building_04": 0,
                  "Building_05": 0,
                  "Building_06": 0,
                  "Building_07": 0,
                  "Building_08": 0,
                  "Building_09": 0,
                  "Building_10": 0,
                  "Building_11": 0,
                  "Cart1": 0,
                  "Cart2": 0,
                  "ClockTower": 0,
                  "Crate1": 0,
                  "Crate2": 0,
                  "Crate3": 0,
                  "crow": 0,
                  "Houses_far": 0,
                  "Planks1": 0,
                  "Planks2": 0,
                  "Planks3": 0,
                  "Planks4": 0,
                  "RoadUpper": 0,
                  "RoadLower": 0,
                  "RoadCover": 0,
                  "Seagull": 0,
                  "StreetLamp": 0,
                  "ThrashCan_closed": 0,
                  "ThrashCan_fallen": 0,
                  "ThrashCan_lid": 0,
                  "ThrashCan_open": 0,
                  "UtilityPole_close": 0,
                  "UtilityPole_far": 0,
                  "WaterHydrant": 0,
                  "WaterTower": 0 }

    obj_list = []
    objects = bpy.data.scenes[0].objects

    for obj in objects:
        if obj.type == 'EMPTY' and "::" in obj.name:
            obj_type, obj_name = obj.name.split("::")
            obj_name = obj_name.split(".")[0]

            if obj_type == 'obj' and obj_name in obj_count:
                obj_translation = obj.matrix_world.to_translation()
                obj_rotation = obj.matrix_world.to_euler()

                # transform into nTiled coordinate system
                obj_translation = (obj_translation[0], obj_translation[2], obj_translation[1])
                obj_rotation = (obj_rotation[0], obj_rotation[2], obj_rotation[1])
                
                print(obj_rotation)

                obj_list.append(Obj(mesh_id=obj_name,
                                    name=("{}.{}".format(obj_name, obj_count[obj_name])),
                                    rotation=obj_rotation,
                                    translation=obj_translation ))
                obj_count[obj_name] += 1

    print(obj_count)

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
    def __init__(self, anchor, number, size_width, size_depth):
        self._anchor = anchor
        self._x = bpy.data.scenes[0].objects["light::X.{}".format(number)]
        self._y = bpy.data.scenes[0].objects["light::Y.{}".format(number)]
        self._z = bpy.data.scenes[0].objects["light::Z.{}".format(number)]

        self._size_width = size_width
        self._size_depth = size_depth

    def get_origin(self):
        origin = self._anchor.matrix_world.to_translation()
        return (origin[0], origin[2], origin[1])

    @property
    def x(self):
        return self._x.matrix_world.to_translation()[0]

    @property
    def y(self):
        return self._y.matrix_world.to_translation()[2]

    @property
    def z(self):
        return self._z.matrix_world.to_translation()[1]

    @property
    def size_width(self):
        return self._size_width

    @property
    def size_depth(self):
        return self._size_depth


    def generate_lights(self, n_width, n_depth, n_height, radius):
        n_lights_width = self.size_width * n_width
        n_lights_depth = self.size_depth * n_depth
        n_lights_height = n_height

        origin = self.get_origin()
        size_width = abs(origin[2] - self.z)
        size_height = abs(origin[1] - self.y)
        size_depth = abs(origin[0] - self.x)


        spacing_width = size_width / (n_lights_width + 1)
        spacing_height = size_height / (n_lights_height + 1)
        spacing_depth = size_depth / (n_lights_depth + 1)

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

        for depth_i in range(1, n_lights_depth + 1):
            for height_i in range(1, n_lights_height + 1):
                for width_i in range(1, n_lights_width + 1):
                    colour = random_rgb_colour()
                    position = (depth_i * spacing_depth + origin[0],
                                height_i * spacing_height + origin[1],
                                width_i * spacing_width + origin[2] )

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
                and "_" in name):

                name, number = name.split(".")
                size, name = name.split("#")
                size_width, size_depth = size.split("_")

                if size_width == "Big":
                    size_width = 5
                elif size_width == "Small":
                    size_width = 1
                else:
                    raise Exception("width not recognised")

                size_depth = int(size_depth)


                light_spawners.append(LightSpawner(anchor=obj,
                                                   number=number,
                                                   size_width=size_width,
                                                   size_depth=size_depth))
    return light_spawners


def generate_lights(radius, n_width, n_height, n_depth):
    light_spawners = extract_light_spawners_from_blend()
    print("Number of light spawners generated: {}".format(len(light_spawners)))

    lights = []

    for spawner in light_spawners:
        lights +=  spawner.generate_lights(n_width,
                                           n_depth,
                                           n_height,
                                           radius)

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
        write_to_json(path= str(GEO_PATH / Path("{}.json".format(s))), data=json_dic)

    for x in range(1, 4):
        for z in range(1, 4):
            for y in range(1, 4):     
                lights = generate_lights(180.0, x, y, z)
                n_lights = len(lights)
                write_to_json(path=str(LIGHT_PATH / Path("{}#{}x_{}y_{}z.json".format(n_lights, x, y, z))), data=build_light_dic(lights))


#   for l in lights:
#       l.build_in_blender()
