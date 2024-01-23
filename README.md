# PenguineMol3D
PenguineMol3D is an open source Python3 package, which utilizes OpenGL python binding (https://pyopengl.sourceforge.net) for rendering of small compounds' 3D models. 

Initially, the RDKit Mol object is created from data in a file (e.g, MOL\SDF, MOL2 format) provided by user; the Mol object is further passed as an argument to the Mol3D class constructor, which generates a 3D model based on atom coordinates of the Mol object conformer. During the initialization stage (before running an event loop) user has to setup a scene by creating MolecularScene object and adding all necessary components like molecule and light sources as it is demonstrated in examples. As a drawing surface for rendering can be used any surface compatible with OpenGL; particularly, provided by such GUI libaries as GLFW (used in examples), PyGame, PyQt, PySide, wxPython, Tkinter + Togl widget, etc.

# Demostration of PenguineMol3D rendering
On the image below is demonstrated Penguinone (https://pubchem.ncbi.nlm.nih.gov/compound/12564106) rendered by PenguineMol3D:

![penguinone](https://github.com/YevhenKustovskiy/penguinemol3d/assets/136888021/12320171-5957-4ad7-b53e-c0246bc743cc)
