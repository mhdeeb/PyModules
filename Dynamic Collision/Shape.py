from abc import ABC, abstractmethod

from pygame.surface import Surface, SurfaceType
from numpy import ndarray

from Vector import Vector2


class Shape(ABC):
    def __init__(self, points: ndarray[Vector2], velocity: Vector2, mass: float,
                 color: tuple[int, int, int] | str) -> None:
        self.points: ndarray[Vector2] = points
        self.color: tuple[int, int, int] | str = color
        self.velocity = velocity
        self.mass = mass

    @abstractmethod
    def draw(self, surface: Surface | SurfaceType) -> None:
        pass

    def move(self, dt: float) -> None:
        self.points += self.velocity * dt

    def momentum(self) -> Vector2:
        return self.velocity * self.mass

    def kinetic_energy(self) -> float:
        return 0.5 * self.mass * self.velocity.magnitude() ** 2
