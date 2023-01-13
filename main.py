#Goal use pygame to make a recreation of the ballz mobilegameimport sys

import sys
import pygame
from pygame.locals import *

from bricks import BrickHandler

from ball import BallManager

pygame.init()


Screen_Width = 400
Screen_hight = 625
screen = pygame.display.set_mode((Screen_Width,Screen_hight))
pygame.display.set_caption('Ballz')

# Set up the game font
font = pygame.font.Font(None, 36)

# Set up the game clock
clock = pygame.time.Clock()

# Set up the game colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255,0,0)

# Set up the game variables
score = 1
level = 1

# Set up the brick size and spacing
BRICK_WIDTH = 45
BRICK_HEIGHT = 45
BRICK_HSPACING = 12
BRICK_VSPACING = 10
BRICK_STARTHIGHT = 10
BRICK_OFFSET = 7

# Set up the bricks
bricks = []
BManager = BrickHandler(BRICK_STARTHIGHT,BRICK_WIDTH,BRICK_HEIGHT,BRICK_HSPACING,BRICK_VSPACING,BRICK_OFFSET)

#temp add bricks location
bricks = BManager.spawnNew(score,bricks)

#floor recangle
FLOOR_HIGHT = 130
floor = Rect(0,Screen_hight-FLOOR_HIGHT,Screen_Width,500)


#ballz
BALLSTARTX = 200
BALLSIZE = 7
BALLSTARTY = Screen_hight-FLOOR_HIGHT-BALLSIZE
START_BALL_EXISTS = True
BALLSPEED = 5
BALL_VELOCITY:tuple

BALL_CLOCK = 0
BALLZ = []
BALLX = BALLSTARTX + 0 #seperate variables

BallM = BallManager(BALLSTARTX,BALLSTARTY,FLOOR_HIGHT,BALLSIZE)

BALLS_SENT = False
WAITING_FOR_BALLS = False

#hide mouse
pygame.mouse.set_visible(False)

#in play checks
inPlay = True

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
    screen.fill((100,100,100))

    #draw floor
    pygame.draw.rect(screen,(0,0,0),floor)
    
    # Draw the score
    score_text = font.render(f'Score: {level}', True, WHITE)
    screen.blit(score_text, (150, 600))
    
    # Draw the game objects
    # (Draw the bricks, paddle, and ball here)
    
    #make new bricks

    # ***TEMP*** on right click to make bricks
    if pygame.mouse.get_pressed()[0] == True and inPlay:
        bricks = BManager.spawnNew(score,bricks)
        print(BManager.brickLocations)
        level += 1


    #Draw the bricks
    BManager.drawBricks(screen,bricks)
    
    #ball
    if START_BALL_EXISTS:
        BallM.drawStartingBall(screen)
    if not BALLS_SENT and pygame.mouse.get_pressed()[0] and not WAITING_FOR_BALLS:
        #activates on mouse press
        BALLS_SENT = True
        BALL_VELOCITY = BallM.getStartVelocity(BALLSPEED)
        #reset clock
        BALL_CLOCK = 0
    elif BALLS_SENT:
        #increse clock
        BALL_CLOCK += 1
        BALLZ = BallM.sendBallz(score,BALLX,BALLSTARTY,BALL_CLOCK,BALL_VELOCITY,BALLZ)
        print(BALLZ)
        
        

    #game ends if there are 7 layers of bricks
    if len(BManager.brickLocations) >= 8:
        inPlay = False
        #display final score 


    
    #mouse location
    pygame.draw.circle(screen,RED,pygame.mouse.get_pos(),4)

    #draw to screen and tick
    pygame.display.flip()
    clock.tick(60)
