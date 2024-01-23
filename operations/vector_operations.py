import numpy as np

class VectorOperations:

    @staticmethod
    def calc_midpoint(vec1: list[float], vec2: list[float]) -> list[float]:
        return [(vec1[0] + vec2[0]) / 2,
                (vec1[1] + vec2[1]) / 2,
                (vec1[2] + vec2[2]) / 2]

    @staticmethod
    def calc_normal(p0:  list[float], p1:  list[float], p2:  list[float]) -> np.ndarray:
        v1 = np.array(p1) - np.array(p0)
        v2 = np.array(p2) - np.array(p0)
        normal = np.cross(v1, v2)
        return normal / np.linalg.norm(normal)

    @staticmethod
    def calc_quaternion(axis: np.ndarray | list[float], angle: float) -> np.ndarray:
        axis = axis / np.linalg.norm(axis)
        q = VectorOperations.normalize_quaternion([axis[0] * np.sin(angle / 2),
                                                   axis[1] * np.sin(angle / 2),
                                                   axis[2] * np.sin(angle / 2),
                                                   np.cos(angle / 2)])
        return q

    @staticmethod
    def calc_unit_vector(vec1: np.ndarray, vec2: np.ndarray) -> np.ndarray:
        diff = vec1 - vec2
        return diff / np.linalg.norm(diff)

    @staticmethod
    def calc_vector_length(vec: np.ndarray | list[float]) -> float:
        return float(np.sqrt(np.dot(vec, vec)))

    @staticmethod
    def convert_3x1_to_4x1(vec: np.ndarray | list[float]) -> np.ndarray:
        return np.array([vec[0], vec[1], vec[2], 1.])

    @staticmethod
    def convert_4x1_to_3x1(vec: np.ndarray | list[float]) -> np.ndarray:
        return np.array([vec[0], vec[1], vec[2]])

    @staticmethod
    def normalize_quaternion(vec: np.ndarray | list[float]) -> np.ndarray:
        return vec / np.dot(vec, vec)

    @staticmethod
    def rotate_align_rodrigues(vec1: np.ndarray, vec2: np.ndarray) -> np.ndarray:
        angle = np.arccos(np.dot(vec1, vec2))
        axis = np.cross(vec1, vec2)
        cos_a = np.cos(angle)
        sin_a = np.sin(angle)
        t = 1 - cos_a

        return vec1 * cos_a + np.cross(axis, vec1) * sin_a + axis * (axis * vec1) * t




