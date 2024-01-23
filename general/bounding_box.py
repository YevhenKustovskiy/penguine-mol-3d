import numpy as np

class BoundingBox:
    """Container for spatial information"""
    def __init__(self,
                 xmin: float,
                 xmax: float,
                 ymin: float,
                 ymax: float,
                 zmin: float,
                 zmax: float):

        self._x_center_factor = (xmax + xmin) / 2
        self._y_center_factor = (ymax + ymin) / 2
        self._z_center_factor = (zmax + zmin) / 2

        self._width = abs(xmin - xmax)
        self._height = abs(ymin - ymax)
        self._depth = abs(zmin - zmax)

        self._center = [np.median([xmin / self._x_center_factor, xmax / self._x_center_factor]),
                        np.median([ymin / self._y_center_factor, ymax / self._y_center_factor]),
                        np.median([zmin / self._z_center_factor, zmax / self._z_center_factor])]

    @property
    def x_center_factor(self) -> float:
        return self._x_center_factor

    @property
    def y_center_factor(self) -> float:
        return self._y_center_factor

    @property
    def z_center_factor(self) -> float:
        return self._z_center_factor


    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self._height

    @property
    def depth(self) -> float:
        return self._depth


    @property
    def center(self) -> list[float]:
        return self._center


