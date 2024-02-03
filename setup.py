import os
import setuptools

with open(os.path.join("PenguinMol3D", "README.md"), "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "PenguinMol3D",
    version = "0.1.1",
    author = "Yevhen Kustovskiy",
    author_email = "ykustovskiy@gmail.com",
    description = "3D visualization of small compounds",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    project_urls = {
        "Homepage": "https://github.com/YevhenKustovskiy/penguinemol3d",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    packages = [
    "PenguinMol3D", 
    "PenguinMol3D.factories",
    "PenguinMol3D.general",
    "PenguinMol3D.geometries",
    "PenguinMol3D.geometries.atoms",
    "PenguinMol3D.geometries.bonds",
    "PenguinMol3D.geometries.shapes",
    "PenguinMol3D.materials",
    "PenguinMol3D.materials.shaders",
    "PenguinMol3D.objects",
    "PenguinMol3D.objects.light",
    "PenguinMol3D.operations"
    ],
    package_data={
      "PenguinMol3D": ["*.txt", "*.sdf", "*.md"],
      "PenguinMol3D.materials.shaders": ["*.vert", "*.frag"]
    },
    include_package_data=True,
    install_requires=[
    "numpy", 
    "rdkit", 
    "PyOpenGL", 
    "PyOpenGL_accelerate", 
    "glfw",
    "Pillow"
    ],
    python_requires = ">=3.10"
)