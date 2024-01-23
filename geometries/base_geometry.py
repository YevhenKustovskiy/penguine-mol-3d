import numpy as np


class BaseGeometry:
    def __init__(self):
        self._vertex_color = []
        self._vertex_position = []
        self._vertex_normal = []
        self._face_normal = []
        self._num_vertices = 0

    @property
    def vertex_position(self) -> list:
        return self._vertex_position

    @vertex_position.setter
    def vertex_position(self, new_vertex_position: list):
        self._vertex_position = new_vertex_position

    @property
    def vertex_color(self) -> list:
        return self._vertex_color

    @vertex_color.setter
    def vertex_color(self, new_vertex_color: list):
        self._vertex_color = new_vertex_color

    @property
    def vertex_normal(self) -> list:
        return self._vertex_normal

    @vertex_normal.setter
    def vertex_normal(self, new_vertex_normal: list):
        self._vertex_normal = new_vertex_normal

    @property
    def face_normal(self) -> list:
        return self._face_normal

    @face_normal.setter
    def face_normal(self, new_face_normal: list):
        self._face_normal = new_face_normal

    @property
    def num_vertices(self) -> int:
        return self._num_vertices

    @num_vertices.setter
    def num_vertices(self, new_num_vertices: int):
        self._num_vertices = new_num_vertices

    def apply_transform(self,
                        matrix: np.ndarray):

        rotation_matrix = np.array([matrix[0][0:3],
                                    matrix[1][0:3],
                                    matrix[2][0:3]])
        new_positions = []
        new_vertex_normal_data = []
        new_face_normal_data = []
        for idx in range(len(self.vertex_position)):
            new_pos = self.vertex_position[idx].copy()
            new_pos.append(1)
            new_normal = self.vertex_normal[idx].copy()
            #new_normal_face = self.face_normal[idx].copy()

            new_pos = matrix @ new_pos
            new_pos = list(new_pos[0:3])
            new_normal = rotation_matrix @ new_normal
            #new_normal_face = rotation_matrix @ new_normal_face

            new_positions.append(new_pos)
            new_vertex_normal_data.append(new_normal)
            #new_face_normal_data.append(new_normal_face)

        self.vertex_position = new_positions
        self.vertex_normal = new_vertex_normal_data
        self.face_normal = new_face_normal_data

    def merge(self, other_bond):
        self.vertex_position += other_bond.vertex_position
        self.vertex_color += other_bond.vertex_color
        self.vertex_normal += other_bond.vertex_normal
        self.face_normal += other_bond.face_normal
        self.num_vertices += other_bond.num_vertices