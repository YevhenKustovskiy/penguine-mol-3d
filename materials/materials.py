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
        self.uniforms["shininess"].data = 27.8974
        self.locate_uniforms()

class BronzeMaterial(PhongMaterial):
    def __init__(self, properties: dict = {}):
        PhongMaterial.__init__(self, properties)

        self.uniforms["specular_strength"].data = 1.
        self.uniforms["shininess"].data = 25.6
        self.locate_uniforms()

class ChromeMaterial(PhongMaterial):
    def __init__(self, properties: dict = {}):
        PhongMaterial.__init__(self, properties)

        self.uniforms["specular_strength"].data = 1.
        self.uniforms["shininess"].data = 76.8
        self.locate_uniforms()

class CopperMaterial(PhongMaterial):
    def __init__(self, properties: dict = {}):
        PhongMaterial.__init__(self, properties)

        self.uniforms["specular_strength"].data = 1.
        self.uniforms["shininess"].data = 12.8
        self.locate_uniforms()

class GoldMaterial(PhongMaterial):
    def __init__(self, properties: dict = {}):
        PhongMaterial.__init__(self, properties)

        self.uniforms["specular_strength"].data = 1.
        self.uniforms["shininess"].data = 51.2
        self.locate_uniforms()

class ObsidianMaterial(PhongMaterial):
    def __init__(self, properties: dict = {}):
        PhongMaterial.__init__(self, properties)

        self.uniforms["specular_strength"].data = 1.
        self.uniforms["shininess"].data = 38.4
        self.locate_uniforms()

class PearlMaterial(PhongMaterial):
    def __init__(self, properties: dict = {}):
        PhongMaterial.__init__(self, properties)

        self.uniforms["specular_strength"].data = 1.
        self.uniforms["shininess"].data = 11.264
        self.locate_uniforms()

class PlasticMaterial(PhongMaterial):
    def __init__(self, properties: dict = {}):
        PhongMaterial.__init__(self, properties)

        self.uniforms["specular_strength"].data = 1.
        self.uniforms["shininess"].data = 32.
        self.locate_uniforms()

class RubberMaterial(PhongMaterial):
    def __init__(self, properties: dict = {}):
        PhongMaterial.__init__(self, properties)

        self.uniforms["specular_strength"].data = 1.
        self.uniforms["shininess"].data = 10.
        self.locate_uniforms()


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
