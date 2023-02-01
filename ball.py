import pygame
from pygame.locals import *
import math
from bricks import BrickHandler as bHandel
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
        self.X = (self.X+self.VelX)
        self.Y = (self.Y+self.VelY)
        
    

#the manager for all of the ballz

class BallManager:
    def __init__(self,StartX,StartY,FloorHight,BallSize:int):
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
        Sx = (mpos[0]-self.BallStartX) #VX
        Sy = (mpos[1]-self.BallStartY) #VY
        h = math.sqrt((Sx*Sx)+(Sy*Sy))
        Gx = (Sx/h)*PixlsPerTick
        Gy = (Sy/h)*PixlsPerTick
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
    def ballUpdate(self,ballz,boarder,bricks:list,Bhandeler:bHandel):
        tballz = []
        for i in ballz:
            #calculate bounces off screen width hight
            if i.X + self.BallSize <= 0 or i.X + self.BallSize >= boarder[0]:
                #reflect x axis
                i.VelX *= -1
            if i.Y + self.BallSize <= 0 or i.Y + self.BallSize >= boarder[1]:
                #reflect y axis
                i.VelY *= -1

            #bounce off of bricks
            
            BLocX = int(i.X/(400/7))
            BLocY = int((i.Y+51)/(445/8)) #45 is there because of offset
            brickid, BrickX, BrickY = Bhandeler.findID(bricks,BLocX,BLocY) #is negitive - when no brick is found
            if brickid != -1:
                #collide with brick
                print("found id", brickid)
                #bounce
                brick = bricks[brickid]
                #damage block
                bricks = Bhandeler.damage(bricks,brickid,BrickX,BrickY)
                
                dx = i.X - (((brick.x - brick.right)/2) + brick.x)
                dy = i.Y - (((brick.y - brick.bottom)/2) + brick.y)
                i.VelX, i.VelY = self.bounce(dx,dy,(i.VelX, i.VelY))
            i.nextPositition()
            tballz.append(i)

        return tballz , bricks
    def drawBallz(self,surface,ballz):
        for i in ballz:
            pygame.draw.circle(surface,(255,255,255),(i.X,i.Y),self.BallSize)
    
    def bounce(self,dx,dy,ballV:tuple):
        v = pygame.math.Vector2(ballV[0], ballV[1])
        if abs(dx) > abs(dy):
            if (dx > 0 and v[0] < 0) or (dx < 0 and v[0] > 0):
                v.reflect_ip(pygame.math.Vector2(1, 0))
        else:
            if (dy > 0 and v[1] < 0) or (dy < 0 and v[1] > 0):
                v.reflect_ip(pygame.math.Vector2(0, 1))
        return v.x, v.y



        


    