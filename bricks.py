import pygame
from pygame.locals import *

#Game Constents
numberOfBricksPerRow = 6
numberOfRowsAllowed = 8

class brick():
    def __init__(self,size:float,isTri:bool,location:int,rotation:int,HitPoints:int) -> None:
        self.size = size
        self.isTri= isTri
        self.location = location
        self.rotation = rotation
        self.hitPoints = HitPoints
        self.truePosition = (0,0)
        self.VSpaceBetweenBricks = 0

    def moveDown(self) -> bool:
        self.location += numberOfBricksPerRow
        if self.location/8 > numberOfRowsAllowed:
            #beyond allowed limit
            return True
        return False
    
    #need to get offsets from game
    def SetPosition(self,startHOffset:int,startVOffset:int,HSpaceBetweenBricks:int,VSpaceBetweenBricks:int):
        self.VSpaceBetweenBricks = HSpaceBetweenBricks
        self.truePosition = ((self.location%numberOfBricksPerRow)*(self.size+HSpaceBetweenBricks)+startHOffset,(self.size+VSpaceBetweenBricks)+startVOffset)

    def UpdatePosition(self):
        self.truePosition[1] += self.VSpaceBetweenBricks + self.size

    def draw(self,screen,color):
        if not self.isTri:
            pygame.draw.rect(screen,color,pygame.Rect(self.truePosition[0]-self.size,self.truePosition[1]-self.size,self.size,self.size))
        else:
            #draw right triangle
            #see the note document
            x = self.truePosition[0]
            y = self.truePosition[1]
            p1 = (x+(self.size/2),y-(self.size/2))
            p2 = (x+(self.size/2),y+(self.size/2))
            p3 = (x-(self.size/2),y-(self.size/2))
            p4 = (x-(self.size/2),y+(self.size/2))
            #deside what to use
            match self.rotation:
                case 0:
                    pygame.draw.polygon(screen,color,[p1,p2,p3])
                case 1:
                    pygame.draw.polygon(screen,color,[p2,p3,p4])
                case 2:
                    pygame.draw.polygon(screen,color,[p3,p4,p1])
                case 3:
                    pygame.draw.polygon(screen,color,[p4,p1,p2])

    def setRotation(self,newRot):
        #rotation goes from 0-3
        self.rotation = newRot%4