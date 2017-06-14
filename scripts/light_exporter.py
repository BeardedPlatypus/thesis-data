import os
import bpy

from enum import Enum


# -----------------------------------------------------------------------------
#  Supporting classes
class LightType(Enum):
    """
    Enum representing the different possible options for light types.
    """
    PointLight = 1


class Position(object):
    """
    Position class representing the position of a light
    """
    # -------------------------------------------------------------------------
    #  Constructor
    def __init__(self, x: float
                 , y: float
                 , z: float
                 ):
        self._x = x
        self._y = y
        self._z = z

    # -------------------------------------------------------------------------
    #  Properties
    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def z(self) -> float:
        return self._z


class Colour(object):
    """
    Colour class representing the colour of a light
    """
    # -------------------------------------------------------------------------
    #  Constructor
    def __init__(self, r: float
                 , g: float
                 , b: float
                 ):
        self._r = r
        self._g = g
        self._b = b

    @property
    def r(self) -> float:
        return self._r

    @property
    def g(self) -> float:
        return self._g

    @property
    def b(self) -> float:
        return self._b


class PointLight(object):
    # -------------------------------------------------------------------------
    #  Constructor
    def __init__(self
                , position: Position
                , intensity: Colour
                , radius: float
                ):
        self._position = position
        self._intensity = intensity
        self._radius = radius

    # -------------------------------------------------------------------------
    #  Properties
    @property
    def light_type(self) -> LightType:
        """
        :return: the light type of this Light
        """
        return LightType.PointLight

    @property
    def position(self) -> Position:
        """
        :return: the position of this light in world coordinates
        """
        return self._position

    @property
    def intensity(self):
        """
        :return: the intensity of this light in rgb colours ranging from [0..1]
        """
        return self._intensity

    @property
    def radius(self):
        """
        :return: the radius of the light volume of this
        """
        return self._radius


# -----------------------------------------------------------------------------
#  Json convert methods.
def json_light_array_start() -> str:
    return ( '{ "lights": [ ')


def json_light(l_ : PointLight,
               is_first: bool = False) -> str:
    result = ''
    if not is_first:
        result += '            , '

    # Position
    # -------------------------------------------------------------------------
    result += '{ "position": { "x": '
    result += str(l_.position.x)
    result += '\n'

    result += '                            , "y": '
    result += str(l_.position.y)
    result += '\n'

    result += '                            , "z": '
    result += str(l_.position.z)
    result += '\n'
    result += '                            }\n'

    # Intensity
    # -------------------------------------------------------------------------
    result += '              , "intensity": { "r": '
    result += str(l_.intensity.r)
    result += '\n'

    result += '                             , "g": '
    result += str(l_.intensity.g)
    result += '\n'

    result += '                             , "b": '
    result += str(l_.intensity.b)
    result += '\n'
    result += '                             }\n'

    # Radius
    # -------------------------------------------------------------------------
    result += '              , "radius": '
    result += str(l_.radius)
    result += '\n'
    result += '              }\n'

    return result


def json_light_array_end() -> str:
    return ( '            ]\n'
             '}\n')


# -----------------------------------------------------------------------------
#  LightManager class
class LightManager(object):
    def __init__(self):
        self._light_list = []

    def add_light(self, light: PointLight):
        self._light_list.append(light)

    def convert_to_json(self) -> str:
        json_str = json_light_array_start()

        if not self._light_list:
            json_str += '\n'
        else:
            json_str += json_light(self._light_list[0], is_first=True)
            for light in self._light_list[1:]:
                json_str += json_light(light)

        json_str += json_light_array_end()
        return json_str


def clamp(x: float, smallest: float, greatest: float):
        return max(smallest, min(x, greatest))

if __name__ == "__main__":
    # light manager
    light_manager = LightManager()

    # export lights currently in the scene
    only_selected = False
    # TODO this currently assumes only one scene, this could be done nicer with context
    objects = bpy.data.scenes[0].objects

    for obj in objects:
        if obj.type == 'LAMP' and (not only_selected or obj.selected):
            # swap y and z, because blender z matches opengl y
            pos = Position( obj.location[0]
                          , obj.location[2]
                          , obj.location[1]
                          )

            l = obj.data
            colour = Colour( clamp(l.energy * l.color[0], 0.0, 1.0)
                           , clamp(l.energy * l.color[1], 0.0, 1.0)
                           , clamp(l.energy * l.color[2], 0.0, 1.0)
                           )

            rad = l.distance

            light_manager.add_light(PointLight( pos
                                              , colour
                                              , rad
                                              ))

    # convert to json string and write the result to the specified document.
    lights_json = light_manager.convert_to_json()
    file_path = os.path.abspath(
        "C:/Users/Monthy/Documents/projects/thesis/thesis-data-suite/scenes/indoor-spaceship/lights/components_test_suite/BoxLights.json")

    with open(file_path, 'w') as output:
        output.write(lights_json)