from PenguinMol3D.objects.light.base_light import BaseLight


class Directional(BaseLight):
    def __init__(self,
                 color: list[float]     = [1.,  1., 1.],
                 direction: list[float] = [0., -1., 0.]):

        BaseLight.__init__(self, light_type=BaseLight.DIRECTIONAL)
        self.color = color
        self.set_direction(direction)
