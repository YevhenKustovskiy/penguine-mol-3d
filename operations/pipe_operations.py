import numpy as np

from PenguinMol3D.operations.line_operations import ParametricLine
from PenguinMol3D.operations.matrix_operations import MatrixOperations
from PenguinMol3D.operations.plane_operations import ParametricPlane
from PenguinMol3D.operations.vector_operations import VectorOperations


class ParametricPipe:
    def __init__(self,
                 path_points: list[list[float]],
                 contour_points: list[list[float]]):

        self._path = path_points
        self._contour = contour_points
        self._contours = []
        self._normals = []
        self._generate_contours()

    @property
    def path(self) -> list[list[float]]:
        return self._path

    @path.setter
    def path(self, path: list[list[float]]):
        self._path = path
        self._generate_contours()

    @property
    def contour(self) -> list[list[float]]:
        return self._contour

    @contour.setter
    def contour(self, contour: list[list[float]]):
        self._generate_contours()
        self._contour = contour

    @property
    def contours(self) -> list[list[list[float]]]:
        return self._contours

    @property
    def normals(self) -> list[list[list[float]]]:
        return self._normals

    def _compute_contour_normal(self, path_idx: int) -> list[np.ndarray]:
        """return normal vectors at the current path point"""

        contour = np.array(self._contours[path_idx])
        center = np.array(self._path[path_idx])

        contour_normal = []
        for i in range(len(contour)):
            normal = VectorOperations.calc_unit_vector(contour[i], center)
            contour_normal.append(normal)

        return contour_normal

    def _generate_contours(self):
        """build countour vertex and normal list on each path point"""
        self._contours.clear()
        self._normals.clear()

        if len(self._path) < 1:
            return

        self._transform_first_contour()
        self._contours.append(self._contour)
        self._normals.append(self._compute_contour_normal(0))

        count = len(self._path)
        for i in range(1, count):
            self._contours.append(self._project_contour(i - 1, i))
            self._normals.append(self._compute_contour_normal(i))
        #print(self._contours)

    def _project_contour(self, from_idx: int, to_idx: int):
        """project a contour to a plane at the path point"""
        dir1 = np.array(self._path[to_idx]) \
               - np.array(self._path[from_idx])
        dir2 = None
        if to_idx == len(self._path) - 1:
            dir2 = dir1
        else:
            dir2 = np.array(self._path[to_idx + 1]) \
                   - np.array(self._path[to_idx])

        normal = dir1 + dir2
        plane = ParametricPlane(self._path[to_idx], normal)

        from_contour = self._contours[from_idx]

        to_contour = []
        for i in range(len(from_contour)):
            line = ParametricLine(dir1, from_contour[i])
            to_contour.append(plane.get_intersection_line(line))

        return to_contour

    def _transform_first_contour(self):
        path_count = len(self._path)
        contour_count = len(self._contour)

        transform = MatrixOperations.make_identity()
        p1 = np.array(self._path[0])
        p2 = np.array(self._path[1])
        if path_count:
            transform = transform @ MatrixOperations.translate(p1[0], p1[1], p1[2])

            if path_count > 1:
                transform = MatrixOperations.make_look_at(p1, p2)

            for i in range(contour_count):
                vector = self._contour[i]
                vector.append(1)
                self._contour[i] = np.dot(transform, vector)[:3]


    def add_path_point(self, point: list[float]):
        self._path.append(point)

        count = len(self._path)
        if count == 1:
            self._transform_first_contour()
            self._normals.append(self._compute_contour_normal(0))

        elif count == 2:
            self._contours.append(self._project_contour(0, 1))
            self._normals.append(self._compute_contour_normal(1))
        else:
            dummy = []
            self._contours.append(dummy)
            self._normals.append(dummy)

            self._contours[count - 2] = self._project_contour(count - 3, count - 2)
            self._normals[count - 2] = self._compute_contour_normal(count - 2)

            self._contours[count - 1] = self._project_contour(count - 2, count - 1)
            self._normals[count - 1] = self._compute_contour_normal(count - 1)










