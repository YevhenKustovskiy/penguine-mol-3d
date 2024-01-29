import numpy as np

from PenguinMol3D.objects.base_object_3d import BaseObject3D
from PenguinMol3D.operations.matrix_operations import MatrixOperations


class Camera(BaseObject3D):
    def __init__(self,
                 angle_of_view: int = 60,
                 aspect_ratio: int = 1,
                 near: float = 0.1,
                 far: int = 1000):
        BaseObject3D.__init__(self)

        self._angle = angle_of_view
        self._projection = MatrixOperations.perspective\
            (angle_of_view, aspect_ratio, near, far)
        self._view = MatrixOperations.make_identity()

    @property
    def angle(self) -> float:
        return self._angle

    @angle.setter
    def angle(self, angle: float):
        self._angle = angle
    @property
    def projection(self) -> np.ndarray:
        return self._projection

    @property
    def view(self) -> np.ndarray:
        return self._view

    def update_view(self):
        self._view = np.linalg.inv(self.get_world_transform())

    def set_bb_based_position(self, box):
        """Set camera position based on the object spatial information and current angle of view"""
        distance = box.height / np.tan(np.deg2rad(self._angle)/2)
        self.set_position([box.center[0]-1, box.center[1]-1, distance])

