from PenguinMol3D.general.attribute import Attribute


class BaseGeometryGroup:
    def __init__(self):
        self._group_vertex_position = []
        self._group_vertex_color = []
        self._group_vertex_normal = []
        self._group_face_normal = []
        self._num_vertices = 0
        self._attributes = {}

    @property
    def attributes(self) -> dict:
        return self._attributes

    @property
    def num_vertices(self) -> int:
        return self._num_vertices

    def add_geometry(self, geometry):
        self._group_vertex_position.append(geometry.vertex_position)
        self._group_vertex_color.append(geometry.vertex_color)
        self._group_vertex_normal.append(geometry.vertex_normal)
        self._group_face_normal.append(geometry.face_normal)
        self._num_vertices += geometry.num_vertices

    def create_attributes(self):
        flat_vertex_position = []
        flat_vertex_color = []
        flat_vertex_normal = []
        flat_face_normal = []

        for bond_idx in range(len(self._group_vertex_position)):
            flat_vertex_position.extend(self._group_vertex_position[bond_idx])
            flat_vertex_color.extend(self._group_vertex_color[bond_idx])
            flat_vertex_normal.extend(self._group_vertex_normal[bond_idx])
            flat_face_normal.extend(self._group_face_normal[bond_idx])

        self._attributes["vertex_position"] = Attribute(flat_vertex_position, dtype="vec3")
        self._attributes["vertex_color"] = Attribute(flat_vertex_color, dtype="vec3")
        self._attributes["vertex_normal"] = Attribute(flat_vertex_normal, dtype="vec3")
        self._attributes["face_normal"] = Attribute(flat_face_normal, dtype="vec3")