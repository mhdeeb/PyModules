import numpy as np
from pygame import *

init()
window = display.set_mode((1000, 1000))


def make_polygon(point: np.array, radius: float, vertices: int):
    return np.array(
        [radius * np.array([np.cos(theta), np.sin(theta)]) + point for theta in
         np.arange(0, 2 * np.pi, 2 * np.pi / vertices)])


clock = time.Clock()
running = True
n = 0
while running:
    window.fill('white')
    draw.aalines(window, 'black', True, make_polygon(np.array([500, 500]), 400, n+2))
    for e in event.get():
        if e.type == QUIT:
            running = False
    display.update()
    clock.tick(1)
    n += 1
    n = n % 10
quit()
