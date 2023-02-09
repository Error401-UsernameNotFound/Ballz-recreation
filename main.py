import sys
import pygame
from pygame.locals import *

from enum import Enum

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
PURPLE = (255,0,255)

# Set up the game variables
score = 1 #ball count
level = 1

#NBS
NBSS = []

# Set up the brick size and spacing
BRICK_WIDTH = 45
BRICK_HEIGHT = 45
BRICK_HSPACING = 12
BRICK_VSPACING = 10.5
BRICK_STARTHIGHT = 10
BRICK_OFFSET = 7
numbSent = 0

# Set up the bricks
bricks = []
BManager = BrickHandler(BRICK_STARTHIGHT,BRICK_WIDTH,BRICK_HEIGHT,BRICK_HSPACING,BRICK_VSPACING,BRICK_OFFSET)

#temp add bricks location
bricks,NBSS = BManager.spawnNew(score,bricks,NBSS)

#floor recangle
FLOOR_HIGHT = 130
floor = Rect(0,Screen_hight-FLOOR_HIGHT,Screen_Width,500)


#ballz
BALLSTARTX = 200
BALLSIZE = 7
BALLSTARTY = Screen_hight-FLOOR_HIGHT-BALLSIZE
START_BALL_EXISTS = True
BALLSPEED = 10
BALL_VELOCITY:tuple
START_UPDATED:bool

BALL_CLOCK = 0
BALLZ = [] 

BallM = BallManager(BALLSTARTX,BALLSTARTY,FLOOR_HIGHT,BALLSIZE)

BALLS_SENT = False
WAITING_FOR_BALLS = False
MAKENEWBRICKS = False

BallCount = 0

#hide mouse
pygame.mouse.set_visible(False)

#in play checks
inPlay = True


# Main game loop
while inPlay:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Update game state
    
    # Draw the screen
    screen.fill((100,100,100))

    #draw floor
    pygame.draw.rect(screen,(0,0,0),floor)
    
    # Draw the score
    score_text = font.render(f'Score: {level}', True, WHITE)
    screen.blit(score_text, (150, 600))

    #Draw the bricks
    BManager.drawBricks(screen,bricks,NBSS)
    
    #ball
    if START_BALL_EXISTS:
        BallM.drawStartingBall(screen)
    if not BALLS_SENT and pygame.mouse.get_pressed()[0] and not WAITING_FOR_BALLS:
        #activates on mouse press
        BALLS_SENT = True
        BALL_VELOCITY = BallM.getStartVelocity(BALLSPEED) 
        #reset state
        BALL_CLOCK = 0
        numbSent = 0
        START_UPDATED = False
    elif BALLS_SENT:
        #increse clock
        if numbSent < BallCount:
            BALLZ = BallM.sendBallz(BallCount,BALLSTARTX,BALLSTARTY,BALL_CLOCK,BALL_VELOCITY,BALLZ)
            if len(BALLZ) > 0:
                BALLZ, bricks, BallCount, NBSS = BallM.ballUpdate(BALLZ,(Screen_Width,Screen_hight),bricks,score,NBSS,BManager)
                BallM.drawBallz(screen,BALLZ)
            BALL_CLOCK += 1
            numbSent += 1
        else:
            #done sending now we wait for balz to come back down
            BALLS_SENT = False
            WAITING_FOR_BALLS = True
            START_BALL_EXISTS = False
    elif WAITING_FOR_BALLS:
        BALLZ, bricks, BallCount,NBSS = BallM.ballUpdate(BALLZ,(Screen_Width,Screen_hight),bricks,score,NBSS,BManager)
        BallM.drawBallz(screen,BALLZ)
        for i in BALLZ:
            if i.Y >= Screen_hight-FLOOR_HIGHT:
                if not START_UPDATED:
                    START_UPDATED = True
                    BALLSTARTX = i.X if  i.X < Screen_Width-(BALLSIZE+3) else Screen_Width-(BALLSIZE+3) #this solves the right side thing

                    #solve left side thing
                    BALLSTARTX = BALLSTARTX if i.X > (BALLSIZE+3) else (BALLSIZE+1)

                    BallM.BallStartX = BALLSTARTX

                BALLZ.remove(i)
        if len(BALLZ) == 0:
            WAITING_FOR_BALLS = False
            START_BALL_EXISTS = True
            MAKENEWBRICKS = True
    elif MAKENEWBRICKS:
        #make new bricks
        MAKENEWBRICKS = False
        level += 1
        bricks, NBSS = BManager.spawnNew(level,bricks,NBSS)
        for i in BManager.brickLocations.copy():
            if i == []:
                BManager.brickLocations.remove(i)
    
    

        
        

    #game ends if there are 8 layers of bricks
    if len(BManager.brickLocations) >= 8:
        print(BManager.brickLocations)
        inPlay = False
        #display final score 


    
    #mouse location
    pygame.draw.circle(screen,RED,pygame.mouse.get_pos(),4)

    #draw to screen and tick
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
