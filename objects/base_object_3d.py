import numpy as np

from PenguinMol3D.operations.matrix_operations import MatrixOperations


class BaseObject3D:
    def __init__(self):
        self._transform = MatrixOperations.make_identity()
        self._parent = None
        self._children = []

    @property
    def children(self) -> list:
        return self._children

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    def apply_transform(self,
                        matrix: np.ndarray,
                        local_coord: bool = True
                        ):
        if local_coord:
            self._transform = self._transform @ matrix
        else:
            self._transform = matrix @ self._transform

    def add_child(self, child):
        self._children.append(child)
        child.parent = self

    def get_descendants(self) -> list:
        descendants = []
        nodes_to_process = [self]
        while len(nodes_to_process)>0:
            node = nodes_to_process.pop(0)
            descendants.append(node)
            nodes_to_process = node.children + nodes_to_process
        return descendants

    def get_direction(self) -> list[list]:
        forward = np.array([0.,0.,-1])
        return list(self.get_rotation_transform() @ forward)

    def get_rotation_transform(self) -> np.ndarray:
        return np.array([self._transform[0][0:3],
                         self._transform[1][0:3],
                         self._transform[2][0:3]])

    def get_world_transform(self) -> np.ndarray:
        if self._parent == None:
            return self._transform
        else:
            return self._parent.get_world_transform() @ self._transform

    def get_world_position(self) -> list[float]:
        world_transform = self.get_world_transform()
        return [world_transform.item((0, 3)),
                world_transform.item((1, 3)),
                world_transform.item((2, 3))]

    def get_position(self) -> list[float]:
        return [self._transform.item((0, 3)),
                self._transform.item((1, 3)),
                self._transform.item((2, 3))]

    def look_at(self, target_position: np.ndarray):
        self._transform = MatrixOperations.make_look_at(self.get_world_position(),
                                                        target_position)

    def remove_child(self, child):
        self._children.remove(child)
        child.parent = None

    def rotate_x(self,
                 angle: int | float,
                 local_coord: bool = True):
        m = MatrixOperations.rotate_x(angle)
        self.apply_transform(m, local_coord)

    def rotate_y(self,
                 angle: int | float,
                 local_coord: bool = True):
        m = MatrixOperations.rotate_y(angle)
        self.apply_transform(m, local_coord)

    def rotate_z(self,
                 angle: int | float,
                 local_coord: bool = True):
        m = MatrixOperations.rotate_z(angle)
        self.apply_transform(m, local_coord)

    def set_direction(self, direction):
        position = self.get_position()
        target_position = [position[0] + direction[0],
                           position[1] + direction[1],
                           position[2] + direction[2]]
        self.look_at(target_position)


    def set_position(self, position: list[float]):
        self._transform.itemset((0, 3), position[0])
        self._transform.itemset((1, 3), position[1])
        self._transform.itemset((2, 3), position[2])

    def set_world_transform(self, transform: np.ndarray):
        self._transform = transform

    def scale(self,
              s,
              local_coord: bool = True):
        m = MatrixOperations.scale(s)
        self.apply_transform(m, local_coord)

    def translate(self,
                  x: float,
                  y: float,
                  z: float,
                  local_coord: bool = True):
        m = MatrixOperations.translate(x, y, z)
        self.apply_transform(m, local_coord)



