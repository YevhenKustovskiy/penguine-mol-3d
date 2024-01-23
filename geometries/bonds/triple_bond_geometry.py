from geometries.bonds.base_bond_geometry import BaseBond


class TripleBondGeometry(BaseBond):
    def __init__(self,
                 path_points: list[list[float]],
                 path_colors: list[list[float]]):

        BaseBond.__init__(self,
                          path_points,
                          path_colors,
                          contour_radius=0.075,
                          contour_steps=32)