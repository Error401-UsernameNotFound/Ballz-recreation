import sys
import pygame
from pygame.locals import *
# Set up the brick colors

BRICK_COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255)
]
BRICK_WIDTH = 50
BRICK_HEIGHT = 20
BRICK_SPACING = 10

class Brick:
    def __init__(self, x, y, hitpoints):
        self.x = x
        self.y = y
        self.hitpoints = hitpoints
        self.color = BRICK_COLORS[hitpoints - 1]

        self.BRICK_WIDTH = BRICK_WIDTH
        self.BRICK_HEIGHT = BRICK_HEIGHT
        self.BRICK_SPACING = BRICK_SPACING
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.BRICK_WIDTH, self.BRICK_HEIGHT))
