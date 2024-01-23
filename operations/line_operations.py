import numpy as np


class ParametricLine:

    def __init__(self, direction: np.ndarray, point: np.ndarray):
        """class to construct a line with parametric form"""

        self.direction = direction
        self.point = np.array(point)

    def __repr__(self) -> str:
        return f"ParametricLine (start: {self.point}, " \
               f"direction: {self.direction})"

    @classmethod
    def from_points(cls, p1: list[float], p2: list[float]):
        point = np.array(p1)
        direction = np.array(p2) - p1
        return cls(direction, point)


    def get_normalized_direction(self) -> np.ndarray:
        """returns unit vector representing line direction"""
        return self.direction / np.linalg.norm(self.direction)


    def get_intersection(self, line) -> np.ndarray:
        """returns the intersection point with the other line
           or NaN if lines are parallel"""

        d2 = line.direction
        p2 = line.point

        d3 = np.cross(p2 - self.point, d2)
        d4 = np.cross(self.direction, d2)

        dot = np.dot(d4, d4)
        if not dot.any():
            return np.array([np.nan, np.nan, np.nan])

        alpha = np.dot(d3, d4) / dot

        return self.point + (alpha * self.direction)


    def is_intersected(self, line) -> bool:
        """determine if this line intersects with the other line"""
        vector = np.cross(self.direction,
                          line.direction)
        if not vector.any():
            return False
        return True