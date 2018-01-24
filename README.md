# Thesis: Data repository

## Synopsis

This repository houses the input files and results generated for my master
thesis: Forward and Deferred Hashed Shading for Real-time Rendering of Many 
Lights. The input files are defined for [`nTiled`](https://github.com/BeardedPlatypus/nTiled),
my implementation of a real-time forward and deferred renderer, which implements
the Tiled and Clustered Shading light assignment algorithms. The majority of
the input files were generated through python scripts running inside blender,
which can be found in the scripts section.

## Motivation

All these files were generated as part of my master thesis of computer science.
The final thesis (in dutch) can be found in [this repository](https://github.com/BeardedPlatypus/thesis-latex).
The final paper (in english) can be found in [this repository](https://github.com/BeardedPlatypus/thesis-paper).

## Scene Suite

The following scenes are defined to evaluate the performance of the different
light assignment algorithms implemented in `nTiled`.
The input files of each scene are generated with the python scripts with 
their respective names. For each scene, the `.obj` files used in `nTiled`
can be found in the `obj` folder. Light definitions of different sizes
can be found in the `lights` folder. The original `blend` files are 
available on request, but are not stored here at this point, due to 
their size.

### Indoor Spaceship

(*[Indoor Spaceship](https://github.com/BeardedPlatypus/thesis-data/tree/master/scenes/spaceship-indoor)*)

The Indoor Spaceship scene consists of a set of corridors and junctions. This
models a (simple) average indoor game scene. 

### Piper's Alley

(*[Piper's Alley](https://github.com/BeardedPlatypus/thesis-data/tree/master/scenes/pipers-alley)*)

The piper's alley scene consists of a single long street, with buildings placed 
adjacent. The lights overlap in respect to the camera z-axis. This leads to a 
poor performance of the Tiled Shading algorithm.

### Ziggurat City

(*[Ziggurat City](https://github.com/BeardedPlatypus/thesis-data/tree/master/scenes/ziggurat-city)*)

The Ziggurat scene displays a large city with a high depth as well as detail 
located close to the camera. This models a (simple) outdoor game scene.

## Results

The results obtained with `nTiled` are stored in the 
[`data` folder](https://github.com/BeardedPlatypus/thesis-data/tree/master/data).
For all runs both execution time per frame, and total number of light 
calculations per frame are stored. The data is stored as a `json` object, where
for each frame the frame index and either execution time or number of light 
calculations is stored. The light assignment algorithm used can be identified 
by the folder name:

* `ns`: Naive Shading, all lights were evaluated per pixel.
* `ts`: Tiled Shading
* `cs`: Clustered Shading
* `hs`: Hashed Shading

The analysis is done with ipython notebook. For each of the data various 
graphs were plotted with seaborn. The ipython notebooks can be found in the
[`analysis`]() folder.

## Utilities

### Camera

In order to properly export paths to be used with the PathCameraControl in 
`nTiled`, the following two objects were defined.  

1. `components/CameraRig.blend`
2. `scripts/camera_path_exporter.py`

The script will act upon the `CameraRig` group defined in `CameraRig.blend`. 
For each frame the up vector, and, eye, and center locations will be calculated
based on the empties defined in `CameraRig`. 

The frames can be controlled with blender's timeline.

### Lights

In order to quickly define a large number of lights for a given volume,, 
the following objects were defined:  

1. `components/LightSpawner.blend`
2. `scripts/light_expporter.py`

In the `LightSpawner.blend` several components can be found which can
be used to define a cubic volume. For each direction a number 
of lights can be specified. The `light_exporter.py` script 
iterates over all the light spawner objects in the scene and 
generates uniformly spaced lights according to the ratios specified
in the volume. These lights are assigned random hues. Finally the
lights are exported to a `json` file to be used in `nTiled`.

## Folder Structure

The folders are structured in the following way:

* analysis
: ipython notebooks used for analysis
* components
: blender components used in `scripts`
    * `LightSpawner.blend`
    * `CameraRig.blend`
* data
: all generated results
* scenes
: all scene input files
    * indoor-spaceship
    : all files related to the Indoor Spaceship scene
    * pipers-alley
    : all files related to the Piper's Alley scene
    * ziggurat-city
    : all files related to the Ziggurat City scene
* scripts
    * `camera_path_exporter.py`
    * `light_exporter.py`

## See also

* [The repository of the software implementing the Hashed Shading algorithm.](https://github.com/BeardedPlatypus/nTiled)
* [The repository of the complete master thesis (in dutch).](https://github.com/BeardedPlatypus/thesis-latex)
* [The repository of the paper (in english).](https://github.com/BeardedPlatypus/thesis-paper)
