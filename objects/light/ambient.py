from PenguinMol3D.objects.light.base_light import BaseLight


class Ambient(BaseLight):
    def __init__(self, color: list[float] = [1., 1., 1.]):
        BaseLight.__init__(self,light_type=BaseLight.AMBIENT)
        self.color = color
