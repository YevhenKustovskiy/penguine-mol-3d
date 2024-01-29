from PenguinMol3D.geometries.shapes.ellipsoid import Ellipsoid


class Sphere(Ellipsoid):
    def __init__(self,
                 radius: int = 1,
                 radius_segments: int = 4,
                 height_segments: int = 2,
                 colors: list[list] = [[1., 0., 0.],
                                       [0., 1., 0.],
                                       [0., 0., 1.],
                                       [0., 1., 1.],
                                       [1., 0., 1.],
                                       [1., 1., 0.]]
                 ):

        Ellipsoid.__init__(self,
                           2 * radius,
                           2 * radius,
                           2 * radius,
                           radius_segments,
                           height_segments,
                           colors)