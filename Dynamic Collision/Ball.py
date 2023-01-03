from math import pi

from numpy import array
from pygame.surface import Surface, SurfaceType
from pygame.draw import circle, aaline

from Shape import Shape
from Vector import Vector2


class Ball(Shape):
    def __init__(self, center: Vector2, radius: int, color: tuple[int, int, int] | str) -> None:
        super().__init__(array([center, center + Vector2(radius, 0)]), Vector2(), 1, color)
        self.radius: int = radius

    def move(self, dt: float) -> None:
        super().move(dt)
        self.points[1].translate(-self.points[0]).rotate(2 * pi * self.velocity.x * dt / self.radius).translate(
            self.points[0])

    def draw(self, surface: Surface | SurfaceType) -> None:
        circle(surface, self.color, self.points[0].to_tuple(), self.radius)
        aaline(surface, "black", self.points[0].to_tuple(), self.points[1].to_tuple())
