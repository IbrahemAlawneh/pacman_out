import sys
import pygame


class MainScreen:
    def __init__(self, surface):
        self.surface = surface


pygame.init()
sr = pygame.display.set_mode((800,800),pygame.RESIZABLE)
pygame.display.set_caption("Pac-man")

#jst for test cuz the main surface we well get it from pac-man.py

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
    sc = MainScreen(sr)

