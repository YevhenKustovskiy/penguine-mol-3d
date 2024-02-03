import numpy as np
from PenguinMol3D.general.attribute import Attribute


class BaseSingularGeometry:
    def __init__(self):
        self._attributes = {}
        self._num_vertices = None

    @property
    def attributes(self) -> dict:
        return self._attributes

    @property
    def num_vertices(self) -> int:
        return self._num_vertices

    @num_vertices.setter
    def num_vertices(self, num_vertices: int):
        self._num_vertices = num_vertices

    def add_attribute(self,
                      data: int|float|list,
                      dtype: str,
                      name: str):
        self._attributes[name] = Attribute(data, dtype)

    def count_vertices(self):
        attrib = list(self._attributes.values())[0]
        self._num_vertices = len(attrib.data)

    def apply_transform(self,
                        matrix: np.ndarray,
                        name: str = "vertex_position"):

        old_positions = self._attributes[name].data
        old_vertex_normal_data = self._attributes["vertex_normal"].data
        old_face_normal_data = self._attributes["face_normal"].data

        rotation_matrix = np.array([matrix[0][0:3],
                                    matrix[1][0:3],
                                    matrix[2][0:3]])

        new_positions          = []
        new_vertex_normal_data = []
        new_face_normal_data   = []
        for idx in range(len(old_positions)):
            new_pos         = old_positions[idx].copy()
            new_pos.append(1)
            new_normal      = old_vertex_normal_data[idx].copy()
            new_normal_face = old_face_normal_data[idx].copy()

            new_pos = matrix @ new_pos
            new_pos = list(new_pos[0:3])
            new_normal = rotation_matrix @ new_normal
            new_normal_face = rotation_matrix @ new_normal_face

            new_positions.append(new_pos)
            new_vertex_normal_data.append(new_normal)
            new_face_normal_data.append(new_normal_face)

        self._attributes[name].data = new_positions
        self._attributes["vertex_normal"].data = new_vertex_normal_data
        self._attributes["face_normal"].data = new_face_normal_data

        self._attributes[name].upload_data()

    def merge(self, other_geometry):
        for name, attribute in self._attributes.items():
            attribute.data += other_geometry.attributes[name].data
            attribute.upload_data()

        self.num_vertices += other_geometry.num_vertices