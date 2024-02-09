from PenguinMol3D.materials import (
    phong_material as pm,
    pbr_material as pb
)


class BaseFactory:
    def __init__(self,
                 material_type: pm.PhongMaterial | pb.PBRMaterial = pb.PBRMaterial,
                 color_scale: float = 1.0):

        self._material_type = material_type
        self._color_scale = color_scale

    @property
    def material_type(self):
        return self._material_type

    @property
    def color_scale(self):
        return self._color_scale