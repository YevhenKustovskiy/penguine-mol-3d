from PenguinMol3D.materials.phong_material import PhongMaterial

"""
   This module contains presets of various materials. By manipulating with material shininess 
   and specular strength we can configure the reflectiveness of surface mimicking properties 
   of real world materials. This, however, has no impact on material color under different 
   types of lighting, which depends on the atom type.
"""

class BrassMaterial(PhongMaterial):
    def __init__(self, properties: dict = {}):
        PhongMaterial.__init__(self, properties)

        self.uniforms["specular_strength"].data = 1.
        self.uniforms["shininess"].data = 83.6922   #Phong 27.8974


class BronzeMaterial(PhongMaterial):
    def __init__(self, properties: dict = {}):
        PhongMaterial.__init__(self, properties)

        self.uniforms["specular_strength"].data = 1.
        self.uniforms["shininess"].data = 76.8       #Phong 25.6


class ChromeMaterial(PhongMaterial):
    def __init__(self, properties: dict = {}):
        PhongMaterial.__init__(self, properties)

        self.uniforms["specular_strength"].data = 1.
        self.uniforms["shininess"].data = 230.4      #Phong 76.8


class CopperMaterial(PhongMaterial):
    def __init__(self, properties: dict = {}):
        PhongMaterial.__init__(self, properties)

        self.uniforms["specular_strength"].data = 1.
        self.uniforms["shininess"].data = 38.4       #Phong 51.2


class GoldMaterial(PhongMaterial):
    def __init__(self, properties: dict = {}):
        PhongMaterial.__init__(self, properties)

        self.uniforms["specular_strength"].data = 1.
        self.uniforms["shininess"].data = 153.6      #Phong 51.2


class ObsidianMaterial(PhongMaterial):
    def __init__(self, properties: dict = {}):
        PhongMaterial.__init__(self, properties)

        self.uniforms["specular_strength"].data = 1.
        self.uniforms["shininess"].data = 115.2      #Phong 38.4


class PearlMaterial(PhongMaterial):
    def __init__(self, properties: dict = {}):
        PhongMaterial.__init__(self, properties)

        self.uniforms["specular_strength"].data = 1.
        self.uniforms["shininess"].data = 33.792     #Phong 11.264


class PlasticMaterial(PhongMaterial):
    def __init__(self, properties: dict = {}):
        PhongMaterial.__init__(self, properties)

        self.uniforms["specular_strength"].data = 1.
        self.uniforms["shininess"].data = 96.        #Phong 32.


class RubberMaterial(PhongMaterial):
    def __init__(self, properties: dict = {}):
        PhongMaterial.__init__(self, properties)

        self.uniforms["specular_strength"].data = 1.
        self.uniforms["shininess"].data = 30.         #Phong 10.



class Materials:
    Brass = BrassMaterial
    Bronze = BronzeMaterial
    Chrome = ChromeMaterial
    Copper = CopperMaterial
    Gold = GoldMaterial
    Obsidian = ObsidianMaterial
    Pearl = PearlMaterial
    Plastic = PlasticMaterial
    Rubber = RubberMaterial
