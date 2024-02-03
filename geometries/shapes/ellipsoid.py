import numpy as np
from PenguinMol3D.geometries.base_parametric_geometry import BaseParametricGeometry


class Ellipsoid(BaseParametricGeometry):
    def __init__(self,
                 width: int = 1,
                 height: int = 1,
                 depth: int = 1,
                 radius_segments: int = 32,
                 height_segments: int = 32,
                 colors: list[list] = [[1., 0., 0.],
                                       [0., 1., 0.],
                                       [0., 0., 1.],
                                       [0., 1., 1.],
                                       [1., 0., 1.],
                                       [1., 1., 0.]]
                 ):

        def s(u,v):
            return [ width/2 * np.sin(u) * np.cos(v),
                    height/2 * np.sin(v),
                     depth/2 * np.cos(u) * np.cos(v)]

        BaseParametricGeometry.__init__(self,
                                        0,
                                        2 * np.pi,
                                        radius_segments,
                                        -np.pi / 2,
                                        np.pi / 2,
                                        height_segments,
                                        s,
                                        colors)