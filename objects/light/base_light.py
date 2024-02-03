from PenguinMol3D.objects.base_object_3d import BaseObject3D


class BaseLight(BaseObject3D):
    AMBIENT = 1
    DIRECTIONAL = 2
    POINT = 3
    def __init__(self, light_type: int = 0):
        BaseObject3D.__init__(self)
        self._light_type  = light_type
        self._color       = [1., 1., 1.]
        self._attenuation = [1., 0., 0.]

    @property
    def light_type(self) -> int:
        return self._light_type

    @light_type.setter
    def light_type(self, light_type: int):
        self._light_type = light_type

    @property
    def color(self) -> list[float]:
        return self._color

    @color.setter
    def color(self, color: list[float]):
        self._color = color

    @property
    def attenuation(self) -> list[float]:
        return self._attenuation

    @attenuation.setter
    def attenuation(self, attenuation: list[float]):
        self._attenuation = attenuation
