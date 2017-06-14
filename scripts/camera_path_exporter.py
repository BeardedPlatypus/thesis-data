import bpy
import json


class CameraRig(object):
    # Constructor
    # ------------------------------------------------------------------
    def __init__(self, eye="EyeHandle",
                       center="CenterHandle",
                       up="UpHandle"):
        self._eye    = bpy.data.objects[eye]
        self._center = bpy.data.objects[center]
        self._up     = bpy.data.objects[up]

    # Properties
    # ------------------------------------------------------------------
    @property
    def eye_location(self):
        return self._eye.matrix_world.to_translation()

    @property
    def center_location(self):
        return self._center.matrix_world.to_translation()

    @property
    def up_vector(self):
        return ( self._up.matrix_world.to_translation() -
                 self.eye_location )


def to_path(camera : CameraRig ) -> list:
    scene = bpy.data.scenes[0]

    frames = []
    for i in range(scene.frame_start, scene.frame_end + 1):
        scene.frame_set(i)

        up     = camera.up_vector
        eye    = camera.eye_location
        center = camera.center_location

        frame_data = { "up"     : { "x": up.x,
                                    "y": up.z,
                                    "z": up.y * -1.0 } ,
                       "eye"    : { "x": eye.x,
                                    "y": eye.z,
                                    "z": eye.y * -1.0 },
                       "center" : { "x": center.x,
                                    "y": center.z,
                                    "z": center.y * -1.0 }}
        frames.append(frame_data)
    return frames


if __name__ == "__main__":
    path = "C:/Users/Monthy/Documents/projects/thesis/thesis-data-suite/scenes/ziggurat-city/camera/camera.json"

    camera_rig = CameraRig()
    frames = to_path(camera_rig)

    json_dic = { "frames" : frames }

    json_string = json.dumps(json_dic, sort_keys=True, indent=2)
    with open(path, 'w') as f:
        f.write(json_string)

