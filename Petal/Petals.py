import pygame
from math import *
import colorsys
import numpy as np

width = 1980
height = 1080
radius = 400
sin_freq = 1
cos_freq = 50
window = pygame.display.set_mode((width, height))
pygame.display.iconify()
window.fill('black')
petal = [[radius * sin((sin_freq + 1) * theta) * cos(theta * (cos_freq - 1)),
          radius * sin(sin_freq * theta) * sin(theta * cos_freq)] for theta in
         np.arange(0, 2 * pi + 0.000001, pi * 0.000001)]
[pygame.draw.aaline(window, [round(i * 255) for i in
                           colorsys.hsv_to_rgb(sqrt(petal[i][0] ** 2 + petal[i][1] ** 2) % 360 / 360, 1, 1)],
                  [petal[i][0] + width / 2, petal[i][1] + height / 2],
                  [petal[i + 1][0] + width / 2, petal[i + 1][1] + height / 2], 2) for i in range(len(petal) - 1)]
pygame.image.save(window, 'petal.png')
pygame.quit()
