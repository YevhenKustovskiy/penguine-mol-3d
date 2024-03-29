# PenguinMol3D
PenguinMol3D is an open source Python3 package, which utilizes OpenGL python binding (https://pyopengl.sourceforge.net) for rendering of small compounds' 3D models. 
# Installation
**Using PyPI**
* pip install PenguinMol3D

**Manual installation**
* creat root folder and set it as current folder
* clone this repository
* move setup.py to root folder
* in root folder enter: pip install .

**Dependencies**
* numpy
* rdkit
* PyOpenGL
* PyOpenGL_accelerate
* glfw
* Pillow
  
NOTE: Although dependencies are installed with package, on Windows OS Microsoft C++ 14 Build Tools are required to install PyOpenGL_accelerate
# Usage

Initially, the RDKit Mol object is created from data in a file (e.g, MOL/SDF, MOL2 format) provided by user; the Mol object is further passed as an argument to the Mol3D class constructor, which generates a 3D model based on atom coordinates of the Mol object conformer. During the initialization stage (before running an event loop) user has to setup a scene by creating MolecularScene object and adding all necessary components like molecule and light sources as it is demonstrated in examples. As a drawing surface for rendering can be used any surface compatible with OpenGL; particularly, provided by such GUI libaries as GLFW (used in examples), PyGame, PyQt, PySide, wxPython, Tkinter + Togl widget, etc.

To check if package was installed correctly after installation enter:

**Windows OS:**

* python -m PenguinMol3D.glfw_surface_example

**Linux OS:**

* python3 -m PenguinMol3D.glfw_surface_example

PenguinMol3D currently supports two lighting models: Physically Based Lighting Model (default) and Blinn-Phong Lighting Model.
To see examples of this two models enter:

**Windows OS:**

* python -m PenguinMol3D.glfw_bpr_example
* python -m PenguinMol3D.glfw_pbr_example
* python -m PenguinMol3D.glfw_custom_material_example

**Linux OS:**

* python3 -m PenguinMol3D.glfw_bpr_example
* python3 -m PenguinMol3D.glfw_pbr_example
* python3 -m PenguinMol3D.glfw_custom_material_example

Main folder also contains script, which can be used for small molecule visualization with predefined scene, to run it enter:

**Windows OS:**

* python -m PenguinMol3D.display_molecule molecule_name.sdf

**Linux OS:**

* python3 -m PenguinMol3D.display_molecule molecule_name.sdf

# Demonstration
![demonstration4](https://github.com/YevhenKustovskiy/penguine-mol-3d/assets/136888021/61c5730e-50e1-49da-9b35-536a2adff283)

