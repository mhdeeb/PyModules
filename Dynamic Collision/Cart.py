from numpy import array
from pygame.draw import lines
from pygame.surface import Surface, SurfaceType

from Shape import Shape
from Vector import Vector2
from Ball import Ball


class Cart(Shape):
    def __init__(self, origin: Vector2, width: int, height: int, color: tuple[int, int, int] | str) -> None:
        super().__init__(array([origin + Vector2(-width / 2, -height),
                                origin + Vector2(-width / 2, 0),
                                origin + Vector2(width / 2, 0),
                                origin + Vector2(width / 2, -height)]), Vector2(), 1, color)
        self.width: int = width
        self.height: int = height
        self.color = color
        self.ball1 = Ball(self.points[1] + Vector2(50, 20), 20, (0, 255, 0))
        self.ball2 = Ball(self.points[2] + Vector2(-50, 20), 20, (0, 255, 0))

    def move(self, dt: float) -> None:
        super().move(dt)
        self.ball1.velocity = self.velocity
        self.ball2.velocity = self.velocity
        self.ball1.move(dt)
        self.ball2.move(dt)

    def draw(self, surface: Surface | SurfaceType) -> None:
        self.ball1.draw(surface)
        self.ball2.draw(surface)
        lines(surface, self.color, False, (
            self.points[0].to_tuple(),
            self.points[1].to_tuple(),
            self.points[2].to_tuple(),
            self.points[3].to_tuple()
        ), 2)
