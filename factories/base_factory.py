from PenguinMol3D.materials.materials import Materials

class BaseFactory:
    def __init__(self, material_type: str = "rubber"):
        self._material_type = None
        if material_type == "brass":
            self._material_type = Materials.Brass
        elif material_type == "bronze":
            self._material_type = Materials.Bronze
        elif material_type == "chrome":
            self._material_type = Materials.Chrome
        elif material_type == "copper":
            self._material_type = Materials.Copper
        elif material_type == "gold":
            self._material_type = Materials.Gold
        elif material_type == "obsidian":
            self._material_type = Materials.Obsidian
        elif material_type == "pearl":
            self._material_type = Materials.Pearl
        elif material_type == "plastic":
            self._material_type = Materials.Plastic
        elif material_type == "rubber":
            self._material_type = Materials.Rubber

    @property
    def material_type(self):
        return self._material_type