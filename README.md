# python-raytracing
A raytracer built in python

This raytracing program is capable of rendering triangles and spheres.

Features:
* Colors
* Multicore optimisation
* Spherical bounding volumes for quicker intersection testing
* Reflective surfaces and specular highlights
* Polygons and planes are able to be rendered with triangles
* Diffuse lighting for more realistic renders
* Antialiasing
* Custom resolutions and field-of-view
* Customizable iteration depth for iterative raytracing
* Custom background colors

For testing purposes a small resolution (160x90) should be used. Use as many threads as there are virtual processor cores for optimal rendering speed. Enabling Antialiasing will render 4 times as many pixels, making the computation slower.


Needed modules are Pillow (https://pillow.readthedocs.io/en/stable/), numpy and matplotlib.
