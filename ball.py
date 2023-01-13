import pygame
from pygame.locals import *
import math

#controls the ball and its nonsence

#short lived. very stupid
class Ball:
    def __init__(self,VelX,VelY,StartX,StartY):
        self.VelX = VelX
        self.VelY = VelY
        self.X = StartX
        self.Y = StartY
    def move(self):
        #move the ball
        self.X += self.VelX
        self.Y += self.VelY
    def changeVel(self,newX,newY):
        #here for bounces
        self.VelX = newX
        self.VelY = newY
    def nextPositition(self):
        #calculate next pos
        return [(self.X+self.VelX),(self.Y+self.VelY)]
        
    

#the manager for all of the ballz

class BallManager:
    def __init__(self,StartX,StartY,FloorHight,BallSize):
        self.BallStartX = StartX
        self.BallStartY = StartY
        self.LowerLim = FloorHight
        self.BallSize = BallSize
        self.Sending = False
        self.ActiveBallz = []
    def drawStartingBall(self,surface):
        pygame.draw.circle(surface,(255,255,255),(self.BallStartX,self.BallStartY),self.BallSize)
    def resetBallz(self): #might not be used
        self.ActiveBallz = [] 
    def getStartVelocity(self,PixlsPerTick):
        mpos = pygame.mouse.get_pos() #direction to go
        #CHANGE SOON
        Sx = math.pow(mpos[0]-self.BallStartX,1)
        Sy = math.pow(mpos[1]-self.BallStartY,1)
        h = math.sqrt(Sx+Sy)
        Gx = math.acos((Sx/h))*PixlsPerTick
        Gy = math.asin((Sy/h))*PixlsPerTick
        return (Gx,Gy)
    def sendBallz(self,ballzCount,startX,StartY,clock,Vel:tuple,ballz:list):
        clockSpeed = 20 #number of ticks untill send next ball
        count = 0
        if clock%clockSpeed == 0:
            self.Sending = True
            ballz.append(Ball(Vel[0],Vel[1],startX,StartY))
            count += 1

        if count >= ballzCount:
            self.Sending = False
        
        return ballz

        


    