import numpy as np
from PenguinMol3D.operations.line_operations import ParametricLine


class ParametricPlane:

    def __init__(self,
                 point: list[float],
                 normal: list[float] = [0., 0., 1.]):
        """class for a 3D plane with normal vector (a,b,c) and a point (x0,y0,z0)
           ax + by + cz + d = 0,  where d = -(ax0 + by0 + cz0)"""

        self.p = np.array(point)
        self.normal = np.array(normal)
        self.normal_length = float(np.sqrt(np.dot(self.normal, self.normal)))
        self.d = -float(np.dot(self.normal, self.p))
        self.distance = -self.d / self.normal_length

    @classmethod
    def from_three_points(cls,
                          p1: list[float],
                          p2: list[float],
                          p3: list[float]):

        AB = np.array(p2) - np.array(p1)
        AC = np.array(p3) - np.array(p1)
        normal = np.cross(AB, AC)
        return cls(p1, normal)


    def get_distance(self, point: list[float]) -> np.ndarray:
        """compute the shortest distance from a given point p2 to the plane defined by normal and p1
           Note: The distance is signed. If the distance is negative, the point is in
           opposite side of the plane.

           D = (a * Px + b * Py + c * Pz + d) / sqrt(a*a + b*b + c*c)
           """

        dot = np.dot(self.normal, point)
        return (dot + self.d) / self.normal_length

    def normalize(self):
        """normalize by dividing each coefficient by the length of normal"""
        length_inv = 1. / self.normal_length
        self.normal *= length_inv
        self.normal_length = 1.
        self.d *= length_inv
        self.distance = -self.d

    def get_intersection_line(self, line: ParametricLine) -> np.ndarray:
        """find the intersect point, substitute a point on the line to the plane equation,
           then solve for alpha a point on a line: (x0 + x*t, y0 + y*t, z0 + z*t)
           plane: a*X + b*Y + c*Z + d = 0

           a*(x0 + x*t) + b*(y0 + y*t) + c*(z0 + z*t) + d = 0
           a*x0 + a*x*t + b*y0 + b*y*t + c*z0 + c*z*t + d = 0
           (a*x + b*x + c*x)*t = -(a*x0 + b*y0 + c*z0 + d)

           t = -(a*x0 + b*y0 + c*z0 + d) / (a*x + b*x + c*x)"""

        dot1 = np.dot(self.normal, line.point)
        dot2 = np.dot(self.normal, line.direction)

        if not dot2.any():
            return np.array([np.nan, np.nan, np.nan])

        t = -(dot1 + self.d) / dot2

        return line.point + (line.direction * t)

    def get_intersection_plane(self, plane) -> ParametricLine:
        """find the intersection line of 2 planes
           P1: N1 dot p + d1 = 0 (a1*X + b1*Y + c1*Z + d1 = 0)
           P2: N2 dot p + d2 = 0 (a2*X + b2*Y + c2*Z + d2 = 0)

           L: p0 + a*V where
           V is the direction vector of intersection line = (a1,b1,c1) x (a2,b2,c2)
           p0 is a point, which is on the L and both P1 and P2 as well

           p0 can be found by solving a linear system of 3 planes
           P1: N1 dot p + d1 = 0     (given)
           P2: N2 dot p + d2 = 0     (given)
           P3: V dot p = 0           (chosen where d3=0)

           Use the formula for intersecting 3 planes to find p0;
           p0 = ((-d1*N2 + d2*N1) x V) / V dot V"""

        direction = np.cross(self.normal, plane.normal)
        if not direction.any():
            return ParametricLine(np.array([np.nan, np.nan, np.nan]),
                                  np.array([np.nan, np.nan, np.nan]))

        dot = np.dot(direction, direction)
        n1 = plane.d * self.normal
        n2 = -self.d * plane.normal
        p = np.cross((n1 + n2), direction) / dot

        return ParametricLine(direction, p)

    def is_intersected_line(self, line: ParametricLine) -> bool:
        """determine if it intersects with the line"""
        dot = np.dot(self.normal, line.direction)

        if not dot.any():
            return False
        return True

    def is_intersected_plane(self, plane) -> bool:
        """determine if it intersects with the other plane"""
        cross = np.cross(self.normal, plane.normal)

        if not cross.any():
            return False
        return True


