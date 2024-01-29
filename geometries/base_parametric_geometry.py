import numpy as np

from PenguinMol3D.geometries.base_singular_geometry import BaseSingularGeometry


class BaseParametricGeometry(BaseSingularGeometry):
    def __init__(self,
                 u_start: int|float,
                 u_end: int|float,
                 u_resolution: int|float,
                 v_start: int|float,
                 v_end: int|float,
                 v_resolution: int|float,
                 surface_function: int|float,
                 colors: list[list] = [[1., 0., 0.],
                                       [0., 1., 0.],
                                       [0., 0., 1.],
                                       [0., 1., 1.],
                                       [1., 0., 1.],
                                       [1., 1., 0.]]):

        BaseSingularGeometry.__init__(self)

        delta_u = (u_end - u_start) / u_resolution
        delta_v = (v_end - v_start) / v_resolution

        uv_space = []
        vertex_normals = []
        for u_idx in range(u_resolution + 1):
            v_array, v_normal_array = [], []
            for v_idx in range(v_resolution + 1):
                u = u_start + u_idx * delta_u
                v = v_start + v_idx * delta_v
                v_array.append(surface_function(u,v))

                P0 = surface_function(u, v)
                P1 = surface_function(u + 0.0001, v)
                P2 = surface_function(u, v + 0.0001)
                v_normal_array.append(self._calc_normal(P0, P1, P2))
            uv_space.append(v_array)
            vertex_normals.append(v_normal_array)


        vertex_positions   = []
        vertex_colors      = []
        vertex_normal_data = []
        face_normal_data   = []

        for x_idx in range(u_resolution):
            for y_idx in range(v_resolution):
                V0 = uv_space[x_idx + 0][y_idx + 0]
                V1 = uv_space[x_idx + 1][y_idx + 0]
                V2 = uv_space[x_idx + 0][y_idx + 1]
                V3 = uv_space[x_idx + 1][y_idx + 1]
                vertex_positions += [V0.copy(), V1.copy(), V3.copy(),
                              V0.copy(), V3.copy(), V2.copy()]

                vertex_colors    += colors

                n0 = vertex_normals[x_idx + 0][y_idx + 0]
                n1 = vertex_normals[x_idx + 1][y_idx + 0]
                n2 = vertex_normals[x_idx + 0][y_idx + 1]
                n3 = vertex_normals[x_idx + 1][y_idx + 1]

                vertex_normal_data += [n0,n1,n3,n0,n3,n2]

                fn0 = self._calc_normal(n0,n1,n3)
                fn1 = self._calc_normal(n0,n3,n2)
                face_normal_data += [fn0, fn0, fn0, fn1, fn1, fn1]


        self.add_attribute(vertex_positions, "vec3", "vertex_position")
        self.add_attribute(vertex_colors,    "vec3", "vertex_color")
        self.add_attribute(vertex_normal_data, "vec3", "vertex_normal")
        self.add_attribute(face_normal_data, "vec3", "face_normal")
        self.count_vertices()

    def _calc_normal(self, P0, P1, P2) -> np.ndarray:
        v1 = np.array(P1) - np.array(P0)
        v2 = np.array(P2) - np.array(P0)
        normal = np.cross(v1, v2)
        normal /= np.linalg.norm(normal)
        return normal