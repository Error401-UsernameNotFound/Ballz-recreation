#Goal use pygame to make a recreation of the ballz mobilegameimport sys

import sys
import pygame
from pygame.locals import *

from bricks import Brick

pygame.init()


width = 400
hight = 625
screen = pygame.display.set_mode((width,hight))
pygame.display.set_caption('Balz')

# Set up the game font
font = pygame.font.Font(None, 36)

# Set up the game clock
clock = pygame.time.Clock()

# Set up the game colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up the game variables
score = 1


# Set up the brick size and spacing
BRICK_WIDTH = 50
BRICK_HEIGHT = 20
BRICK_SPACING = 10

# Set up the bricks
bricks = []
for i in range(10):
    for j in range(5):
        brick = Brick(i * (BRICK_WIDTH + BRICK_SPACING), j * (BRICK_HEIGHT + BRICK_SPACING), j + 1)
        bricks.append(brick)


# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Update game state
    # (Update the game variables and objects here)
    
    # Draw the screen
    screen.fill(BLACK)
    
    # Draw the score
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Draw the game objects
    # (Draw the bricks, paddle, and ball here)
    
    # Draw the bricks
    for brick in bricks:
        brick.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)