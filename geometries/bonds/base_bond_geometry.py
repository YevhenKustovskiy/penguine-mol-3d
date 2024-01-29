from PenguinMol3D.geometries.base_continuous_geometry import BaseContinuousGeometry
from PenguinMol3D.operations.circle_operations import ParametricCircle
from PenguinMol3D.operations.pipe_operations import ParametricPipe
from PenguinMol3D.operations.vector_operations import VectorOperations


class BaseBond(ParametricPipe, BaseContinuousGeometry):
    def __init__(self,
                 path_points: list[list[float]],
                 path_colors: list[list[float]],
                 contour_radius: float = 0.35,
                 contour_steps: int = 32):

        contour_points = ParametricCircle.build_circle(contour_radius,
                                                       contour_steps)

        ParametricPipe.__init__(self, path_points, contour_points)
        BaseContinuousGeometry.__init__(self)

        for c_idx in range(len(self.contours) - 1):
            contour1 = self.contours[c_idx]
            contour2 = self.contours[c_idx + 1]
            normals1 = self.normals[c_idx]
            normals2 = self.normals[c_idx + 1]
            contour_color1 = path_colors[c_idx]
            contour_color2 = path_colors[c_idx + 1]

            for v_idx in range(contour_steps):
                c0v0 = contour1[v_idx]
                c1v0 = contour2[v_idx]
                vn0 = normals1[v_idx]
                vn1 = normals1[v_idx]

                sv_idx = v_idx + 1
                if sv_idx == contour_steps:
                    c0v1 = contour1[0]
                    c1v1 = contour2[0]
                    vn2 = normals1[0]
                    vn3 = normals2[0]
                else:
                    c0v1 = contour1[sv_idx]
                    c1v1 = contour2[sv_idx]
                    vn2 = normals1[sv_idx]
                    vn3 = normals2[sv_idx]

                self.vertex_position.extend([c0v0, c0v1, c1v1,
                                              c0v0, c1v1, c1v0])
                self.vertex_color.extend([contour_color1,
                                           contour_color1,
                                           contour_color2,
                                           contour_color1,
                                           contour_color2,
                                           contour_color2])
                self.vertex_normal.extend([vn0, vn2, vn3, vn0, vn3, vn1])

                fn0 = VectorOperations.calc_normal(c0v0, c1v1, c0v1)
                fn1 = VectorOperations.calc_normal(c0v0, c1v0, c1v1)
                self.face_normal.extend([fn0, fn0, fn0, fn1, fn1, fn1])

        self.num_vertices = len(self._vertex_position)


