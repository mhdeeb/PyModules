from math import sin, cos
from typing import Any, Callable


class Vector2:
    def __init__(self, x: float = 0, y: float = 0):
        self.x: float = x
        self.y: float = y

    def __str__(self):
        return f"({self.x:.2f}, {self.y:.2f})"

    def __repr__(self):
        return "Vector2" + self.__str__()

    def __eq__(self, other: 'Vector2') -> bool:
        if isinstance(other, Vector2):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __iter__(self):
        yield self.x
        yield self.y

    def __getitem__(self, key: int) -> float:
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("index out of range")

    def operate(self, other: Any, operation: Callable) -> 'Vector2':
        if isinstance(other, Vector2):
            return Vector2(operation(self.x, other.x), operation(self.y, other.y))
        elif (isinstance(other, tuple) or isinstance(other, list)) and len(other) == 2:
            return Vector2(operation(self.x, other[0]), operation(self.y, other[1]))
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2(operation(self.x, other), operation(self.y, other))
        else:
            raise TypeError(f"unsupported operand type(s): 'Vector2' and '{type(other)}'")

    def __add__(self, other: Any) -> 'Vector2':
        return self.operate(other, lambda x, y: x + y)

    def __sub__(self, other: Any) -> 'Vector2':
        return self.operate(other, lambda x, y: x - y)

    def __neg__(self) -> 'Vector2':
        return Vector2(-self.x, -self.y)

    def __mul__(self, other: Any) -> 'Vector2':
        return self.operate(other, lambda x, y: x * y)

    def __truediv__(self, other: Any) -> 'Vector2':
        return self.operate(other, lambda x, y: x / y)

    def __format__(self, format_spec):
        return f"({self.x:{format_spec}},{self.y:{format_spec}})"

    def magnitude(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def translate(self, vector: 'Vector2') -> 'Vector2':
        self.x += vector.x
        self.y += vector.y
        return self

    def scale(self, vector: 'Vector2') -> 'Vector2':
        self.x *= vector.x
        self.y *= vector.y
        return self

    def rotate(self, angle: float) -> 'Vector2':
        temp_x = self.x
        self.x = temp_x * cos(angle) - self.y * sin(angle)
        self.y = temp_x * sin(angle) + self.y * cos(angle)
        return self

    def to_tuple(self) -> tuple[float, float]:
        return self.x, self.y
