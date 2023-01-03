import pygame
from math import *
import colorsys
from numpy import array, arange, ndarray, sin, cos, transpose
from numpy.linalg import norm

from Utilities.file_utilities import uniquify_file_path


def funcx(theta: ndarray) -> ndarray:
    return radius * sin((sin_freq + 1) * theta) * cos(theta * (cos_freq - 1)) + width / 2


def funcy(theta: ndarray) -> ndarray:
    return radius * sin(sin_freq * theta) * sin(theta * cos_freq) + height / 2


def color_func(start: ndarray[2], end: ndarray[2]) -> ndarray:
    return array([round(i * 255) for i in colorsys.hsv_to_rgb(norm((start + end - size) / 2) % 360 / 360, 1, 1)])


if __name__ == '__main__':
    height = 1080
    aspect_ratio = 16 / 9
    width = int(height * aspect_ratio)
    size = array([width, height])
    name = uniquify_file_path("petal.png")
    background = "black"

    radius = 400
    sin_freq = 1
    cos_freq = 50
    dTheta = 0.0001
    solid = False

    foreground = "white"

    window = pygame.display.set_mode(size)
    pygame.display.iconify()
    window.fill(background)

    theta = arange(0, 2 * pi + dTheta, pi * dTheta)
    petal = transpose([funcx(theta), funcy(theta)])

    if solid:
        pygame.draw.aalines(window, foreground, False, petal)
    else:
        [pygame.draw.aaline(window, color_func(petal[i], petal[i + 1]), petal[i], petal[i + 1])
         for i in range(len(petal) - 1)]

    pygame.image.save(window, name)

    pygame.quit()
