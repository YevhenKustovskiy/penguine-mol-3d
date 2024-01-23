from math import acos, cos, sin


class ParametricCircle:

    @staticmethod
    def build_circle(radius: float, steps: int) -> list[list[float]]:

        pi2 = acos(-1) * 2.
        points = []
        for step in range(steps):
            a = pi2 / steps * step
            x = radius * cos(a)
            y = radius * sin(a)
            points.append([x, y, 0.])

        return points


