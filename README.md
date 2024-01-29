# PenguineMol3D

PenguineMol3D is an open source Python3 package, which utilizes OpenGL python binding (https://pyopengl.sourceforge.net) for rendering of small compounds' 3D models. 
# Installation

**Basic installation**

Project page on PyPI: https://pypi.org/project/PenguinMol3D/
* pip install PenguinMol3D

**Manual installation**
1. Create root directory
2. Clone the repository to root directory
3. Move setup.py from the repository to root directory
4. Open terminal and set current working directory to root directory
5. pip install .
   
**Dependencies**

* numpy
* rdkit
* PyOpenGL
* PyOpenGL_accelerate
* glfw
* Pillow

NOTE: Although dependencies are installed with package, on Windows OS Microsoft C++ 14 Build Tools are required to install PyOpenGL_accelerate

To check if package was installed correctly after installation enter:

**Windows OS:**

* python -m PenguinMol3D.glfw_surface_example
* python -m PenguinMol3D.glfw_screenshot_example
* python -m PenguinMol3D.glfw_transformations_example

**Linux OS:**

* python3 -m PenguinMol3D.glfw_surface_example
* python3 -m PenguinMol3D.glfw_screenshot_example
* python3 -m PenguinMol3D.glfw_transformations_example

Main folder also contains script, which can be used for small molecule visualization with predefined scene, to run it enter:

**Windows OS:**

* python -m PenguinMol3D.display_molecule molecule_name.sdf

**Linux OS:**

* python3 -m PenguinMol3D.display_molecule molecule_name.sdf

# Usage

Initially, the RDKit Mol object is created from data in a file (e.g, MOL\SDF, MOL2 format) provided by user; the Mol object is further passed as an argument to the Mol3D class constructor, which generates a 3D model based on atom coordinates of the Mol object conformer. During the initialization stage (before running an event loop) user has to setup a scene by creating MolecularScene object and adding all necessary components like molecule and light sources as it is demonstrated in examples. As a drawing surface for rendering can be used any surface compatible with OpenGL; particularly, provided by such GUI libaries as GLFW (used in examples), PyGame, PyQt, PySide, wxPython, Tkinter + Togl widget, etc.

# Demonstration

![demonstration](https://github.com/YevhenKustovskiy/penguine-mol-3d/assets/136888021/2800b85c-95e7-4fff-98e3-297178e0ba1d)

