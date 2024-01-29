from PenguinMol3D.geometries.shapes.sphere import Sphere


class BaseAtomGeometry(Sphere):

    def __init__(self,
                 radius: int = 1,
                 radius_segments: int = 32,
                 height_segments: int = 16):

        Sphere.__init__(self,
                        radius=radius,
                        radius_segments=radius_segments,
                        height_segments=height_segments)


