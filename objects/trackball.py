import numpy as np

from PenguinMol3D.operations.matrix_operations import MatrixOperations
from PenguinMol3D.operations.vector_operations import VectorOperations


class Trackball:

    @staticmethod
    def canonicalize_coords(center: np.ndarray, scale: int, point: np.ndarray) -> np.ndarray:
        """Transforms mouse coordinates to canonical space"""
        px = (2 / scale) * (point[0] - center[0])
        py = -(2 / scale) * (point[1] - center[1])
        return np.array([px, py])

    @staticmethod
    def project_onto_sphere(radius: float, point_2d: np.ndarray) -> np.ndarray:
        """Projects an x,y pair onto a sphere of radius r OR a hyperbolic sheet
           if we are away from the center of the sphere.

           Calculates z-axis value based on input 2d point and returns 3d point
           """

        d = np.sqrt(np.dot(point_2d, point_2d))
        if d < radius * 0.70710678118654752440:
            z = np.sqrt(radius * radius - d * d)
            return np.array([point_2d[0], point_2d[1], z])
        else:
            t = radius / 1.41421356237309504880
            return np.array([point_2d[0], point_2d[1], t * t / d])

    @staticmethod
    def simulate_trackball(viewport_size: list[int],
                           curr_pos: list[float],
                           prev_pos: list[float]) -> np.ndarray:

        """ Projects the points onto the virtual trackball, then figures out
            the axis of rotation, which is the cross product of
            P1 P2 and O P1 (O is the center of the ball, 0,0,0)

            Note:  This is a deformed trackball-- is a trackball in the center,
            but is deformed into a hyperbolic sheet of rotation away from the
            center.  This particular function was chosen after trying out
            several variations.

            It is assumed that the arguments to this routine are in the range
            (-1.0 ... 1.0)"""

        # canonicalizes coordinates (-1.0 ... 1.0)
        center = np.array([(viewport_size[0] - 1) / 2, (viewport_size[1] - 1) / 2])
        scale = min(viewport_size[0], viewport_size[1])

        curr_pos = Trackball.canonicalize_coords(center, scale, np.array(curr_pos))
        prev_pos = Trackball.canonicalize_coords(center, scale, np.array(prev_pos))

        # trackball radius
        trackball_radius = 0.8

        # checks zero rotation
        zero_rotation = curr_pos[0] == prev_pos[0] and curr_pos[1] == prev_pos[1]
        if zero_rotation:
            return MatrixOperations.make_identity()

        # calculates 3d coordinates of two 2d points by their projection onto sphere
        curr_pos = Trackball.project_onto_sphere(trackball_radius, curr_pos)
        prev_pos = Trackball.project_onto_sphere(trackball_radius, prev_pos)

        # calculates axis ot rotation
        axis = np.cross(prev_pos, curr_pos)

        # calculates angle of rotation
        t = VectorOperations.calc_vector_length(curr_pos - prev_pos) / (2. * trackball_radius)
        if t >  1.: t =  1.
        if t < -1.: t = -1.
        angle = 2. * np.arcsin(t)

        # calculates quaternion
        quaternion = VectorOperations.calc_quaternion(axis, angle)

        # builds rotational matrix based on quaternion and returns it
        return MatrixOperations.rotate_quaternion(quaternion)


