import numpy as np
from PenguinMol3D.operations.vector_operations import VectorOperations


class MatrixOperations:

    @staticmethod
    def make_identity() -> np.ndarray:
        return np.array([[1., 0., 0., 0.],
                         [0., 1., 0., 0.],
                         [0., 0., 1., 0.],
                         [0., 0., 0., 1.]],
                        dtype=np.float32)


    @staticmethod
    def make_look_at(position: np.ndarray,
                     target: np.ndarray) -> np.ndarray:
        world_up = [0., 1., 0.]
        forward = np.subtract(target, position)
        right = np.cross(forward, world_up)

        if np.linalg.norm(right) < 0.001:
            offset = np.array([0.001, 0, 0])
            right = np.cross(forward, world_up + offset)

        up = np.cross(right, forward)

        forward = np.divide(forward, np.linalg.norm(forward))
        right = np.divide(right, np.linalg.norm(right))
        up = np.divide(up, np.linalg.norm(up))

        return np.array([[right[0], up[0], -forward[0], position[0]],
                         [right[1], up[1], -forward[1], position[1]],
                         [right[2], up[2], -forward[2], position[2]],
                         [0., 0., 0., 1.]])

    @staticmethod
    def perspective(angle_of_view: int = 60,
                    aspect_ratio: int = 1,
                    near: float = 0.1,
                    far: int = 1000
                    ) -> np.ndarray:
        a = angle_of_view * np.pi / 180.
        d = 1. / np.tan(a / 2)
        r = aspect_ratio
        b = (far + near) / (near - far)
        c = 2 * far * near / (near - far)

        return np.array([[d / r, 0., 0., 0.],
                         [0., d, 0., 0.],
                         [0., 0., b, c],
                         [0., 0., -1., 0.]],
                        dtype=np.float32)

    @staticmethod
    def rotate_align(unit_vec1: np.ndarray, unit_vec2: np.ndarray) -> np.ndarray:
        axis = np.cross(unit_vec1, unit_vec2)
        cos_a = np.dot(unit_vec1, unit_vec2)
        k = 1.0 / 1.0 + cos_a

        return np.array([[axis[0] * axis[0] * k + cos_a,
                          axis[1] * axis[0] * k - axis[2],
                          axis[2] * axis[0] * k + axis[1],
                          0.],
                         [axis[0] * axis[1] * k + axis[2],
                          axis[1] * axis[1] * k + cos_a,
                          axis[2] * axis[1] * k - axis[0],
                          0.],
                         [axis[0] * axis[2] * k - axis[1],
                          axis[1] * axis[2] * k + axis[0],
                          axis[2] * axis[2] * k + cos_a,
                          0.],
                         [0., 0., 0., 1.]])
        """angle = np.arccos(np.dot(unit_vec1, unit_vec2))
        axis = np.cross(unit_vec1, unit_vec2)
        cos = np.cos(angle)
        sin = np.sin(angle)
        t = 1 - cos
        return np.array(  [[cos + axis[0] * axis[0] * t,
                            axis[0] * axis[1] * t - axis[2] * sin,
                            axis[0] * axis[2] * t + axis[1] * sin,
                            0.],
                           [axis[1] * axis[0] * t + axis[2] * sin,
                            cos + (axis[1] * axis[1]) * t,
                            axis[1] * axis[2] * t - axis[0] * sin,
                            0.],
                           [axis[2] * axis[0] * t - axis[1] * sin,
                            axis[2] * axis[1] * t + axis[0] * sin,
                            cos + axis[2] * axis[2] * t,
                            0.],
                           [0., 0., 0., 1.]])"""

    @staticmethod
    def rotate_align_rodrigues(unit_vec1: np.ndarray, unit_vec2: np.ndarray) -> np.ndarray:
        angle = np.arccos(np.dot(unit_vec1, unit_vec2))
        axis = np.cross(unit_vec1, unit_vec2)
        cos = np.cos(angle)
        sin = np.sin(angle)
        t = 1 - cos

        identity = MatrixOperations.make_identity()
        skew = np.array([[ 0.,      -axis[2],  axis[1], 0.],
                         [ axis[2],  0.,      -axis[0], 0.],
                         [-axis[1],  axis[0],  0.     , 0.],
                         [ 0.,       0.,       0.,      1.]])

        return identity + skew + (t * np.dot(skew, skew))

    @staticmethod
    def rotate_align_quaternion(unit_vec1: np.ndarray, unit_vec2: np.ndarray) -> np.ndarray:
        angle = np.arccos(np.dot(unit_vec1, unit_vec2))
        axis = np.cross(unit_vec1, unit_vec2)

        # calculating quaternion
        q = VectorOperations.normalize_quaternion([axis[0] * np.sin(angle / 2),
                                                   axis[1] * np.sin(angle / 2),
                                                   axis[2] * np.sin(angle / 2),
                                                   np.cos(angle/2)])
        qx = q[0]
        qy = q[1]
        qz = q[2]
        qw = q[3]

        #return rotation matrix

        return np.array([[1. - 2. * (qy * qy + qz * qz),
                          2.      * (qx * qy - qz * qw),
                          2.      * (qz * qx + qy * qw),
                          0.],
                         [2.      * (qx * qy + qz * qw),
                          1. - 2. * (qz * qz + qx * qx),
                          2.      * (qy * qz - qx * qw),
                          0.],
                         [2.      * (qz * qx - qy * qw),
                          2.      * (qy * qz + qx * qw),
                          1. - 2. * (qy * qy + qx * qx),
                          0.],
                         [0., 0., 0., 1.]])

    @staticmethod
    def rotate_quaternion(q: np.ndarray | list[float]) -> np.ndarray:
        qx = q[0]
        qy = q[1]
        qz = q[2]
        qw = q[3]

        return np.array([[1. - 2. * (qy * qy + qz * qz),
                          2.      * (qx * qy - qz * qw),
                          2.      * (qz * qx + qy * qw),
                          0.],
                         [2.      * (qx * qy + qz * qw),
                          1. - 2. * (qz * qz + qx * qx),
                          2.      * (qy * qz - qx * qw),
                          0.],
                         [2.      * (qz * qx - qy * qw),
                          2.      * (qy * qz + qx * qw),
                          1. - 2. * (qy * qy + qx * qx),
                          0.],
                         [0., 0., 0., 1.]])


    @staticmethod
    def rotate_x(angle: int) -> np.ndarray:
        c = np.cos(angle)
        s = np.sin(angle)
        return np.array([[1., 0., 0., 0.],
                         [0., c, -s,  0.],
                         [0., s,  c,  0.],
                         [0., 0., 0., 1.]],
                        dtype=np.float32)

    @staticmethod
    def rotate_y(angle: int) -> np.ndarray:
        c = np.cos(angle)
        s = np.sin(angle)
        return np.array([[c,  0., s,  0.],
                         [0., 1., 0., 0.],
                         [-s, 0., c,  0.],
                         [0., 0., 0., 1.]],
                        dtype=np.float32)

    @staticmethod
    def rotate_z(angle: int) -> np.ndarray:
        c = np.cos(angle)
        s = np.sin(angle)
        return np.array([[c, -s,  0., 0.],
                         [s,  c,  0., 0.],
                         [0., 0., 1., 0.],
                         [0., 0., 0., 1.]],
                        dtype=np.float32)

    @staticmethod
    def rotate_axis(axis: np.ndarray, angle: float) -> np.ndarray:
        cos = np.cos(angle)
        sin = np.sin(angle)
        t = 1 - cos
        return np.array([[cos + axis[0] * axis[0] * t,
                          axis[0] * axis[1] * t - axis[2] * sin,
                          axis[0] * axis[2] * t + axis[1] * sin,
                          0.],
                         [axis[1] * axis[0] * t + axis[2] * sin,
                          cos + (axis[1] * axis[1]) * t,
                          axis[1] * axis[2] * t - axis[0] * sin,
                          0.],
                         [axis[2] * axis[0] * t - axis[1] * sin,
                          axis[2] * axis[1] * t + axis[0] * sin,
                          cos + axis[2] * axis[2] * t,
                          0.],
                         [0., 0., 0., 1.]])


    @staticmethod
    def scale(s) -> np.ndarray:
        return np.array([[s,  0., 0., 0.],
                         [0., s,  0., 0.],
                         [0., 0., s,  0.],
                         [0., 0., 0., 1.]],
                        dtype=np.float32)


    @staticmethod
    def scale_nonunifrom(sx: float, sy: float, sz: float) -> np.ndarray:
        return np.array([[sx, 0., 0., 0.],
                         [0., sy, 0., 0.],
                         [0., 0., sz, 0.],
                         [0., 0., 0., 1.]],
                        dtype=np.float32)

    @staticmethod
    def translate(x: float,
                  y: float,
                  z: float
                  ) -> np.ndarray:
        return np.array([[1., 0., 0., x],
                         [0., 1., 0., y],
                         [0., 0., 1., z],
                         [0., 0., 0., 1.]],
                        dtype=np.float32)




