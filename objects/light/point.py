from PenguinMol3D.objects.light.base_light import BaseLight


class Point(BaseLight):
    def __init__(self,
                 color: list[float] = [1., 1., 1.],
                 position: list[float] = [1., 1., 1.],
                 attenuation: list[float] = [1., 0., 0., 1.]):
        BaseLight.__init__(self, light_type=BaseLight.POINT)
        self.color = color
        self.set_position(position)
        self.attenuation = attenuation