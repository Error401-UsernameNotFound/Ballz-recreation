import pygame
from pygame.locals import *
from random import randint



class BrickHandler:
    def __init__(self,startHight,width,hight,HSpacing,VSpacing,HOffset):
        self.startHight = startHight
        self.width = width
        self.hight = hight
        self.HSpacing = HSpacing
        self.VSpacing = VSpacing
        self.HOffset = HOffset

        self.brickLocations = []

    def spawnNew(self,level,bricks:list,NBSS:list):
        new = []

        #set up random block spawn placement
        locations = [0,1,2,3,4,5,6]
        rLoc = []
        for _ in range(randint(1,3)): # selcect a random amount to remove
            rLoc.append(locations.pop(randint(0,len(locations)-1)))

        #record brick locations
        #adds to the start of the brick locations list
        self.brickLocations.reverse()
        self.brickLocations.append(locations)
        self.brickLocations.reverse()

        #new bricks
        for loc in locations:
            #number is the position relitive to the number of spaces
            #position is the center
            x = loc*(self.width + self.HSpacing) + self.HOffset
            y = self.hight + self.VSpacing + self.startHight
            m = 2 if randint(1,5) == 1 else 1
            new.append(Brick(x,y,level*m,self.width,self.hight,self.HSpacing))

        #move all other bricks down
        for i in bricks:
            i.y += (self.VSpacing + self.hight)
        
        #move NBS DOWN
        for i in NBSS:
            i.positionY += (self.VSpacing + self.hight)
        #pick a removed location and add the NBS there
        rX = (rLoc[randint(0,len(rLoc)-1)])*(self.width + self.HSpacing) + self.HOffset
        rY = self.hight + self.VSpacing + self.startHight
        NBSS.append(NBS(15,rX,rY))
        #add new bricks
        for i in new:
            bricks.append(i)
        return bricks, NBSS

    def drawBricks(self,surface,bricks,NBSS):
        for i in bricks:
            font = pygame.font.Font(None, 36)
            pygame.draw.rect(surface, i.color, (i.x, i.y, i.BRICK_WIDTH, i.BRICK_HEIGHT))
            surface.blit(font.render(f'{i.hitpoints}', True, (255, 255, 255)), (i.x + (i.BRICK_WIDTH-33), i.y + (i.BRICK_HEIGHT/4)))
        for i in NBSS:
            i.draw(surface)
    
    
    def damage(self,bricks:list,brickID,locX,locY):
        bricks[brickID].hitpoints -= 1
        bricks[brickID].updateColor()
        if bricks[brickID].hitpoints <= 0:
            bricks.pop(brickID)
            if len(self.brickLocations[locY]) > 1:
                self.brickLocations[locY].pop(locX)
            else:
                self.brickLocations.pop(locY)
        return bricks

    def collectNBS(self,NBSS:list,bCords:tuple,ballCount):
        for i in NBSS:
            if abs(i.positionX-bCords[0]) <= 20 and abs(i.positionY-bCords[1]) <= 20:
                NBSS.remove(i)
                ballCount += 1
        return NBSS,ballCount
    
    def findID(self,bricks,blocX,blocY):
        id = -1
        c = 0
        for i in range(len(self.brickLocations)):
            for b in range(len(self.brickLocations[i])):
                scanedBrick = bricks[c]
                BX = int((scanedBrick.x)/(400/7)) #ten to put it in a the box. i think thats the problem
                BY = int((scanedBrick.y+51)/(445/8)) #51 is there because of offset
                if BX == blocX and BY == blocY:
                    #found the block in the position
                    id = c
                    #exit
                    return (id,b,i)
                else:#not found
                    c += 1
        return (id,0,0) #gona be -1
                

                
            



class Brick:
    def __init__(self, x, y, hitpoints,width,hight,spacing):
        self.x = x
        self.y = y
        self.hitpoints = hitpoints
        self.color = (255,0,0)
        self.updateColor()

        self.BRICK_WIDTH = width
        self.BRICK_HEIGHT = hight
        self.BRICK_SPACING = spacing
        self.right = x+width
        self.bottom = y+hight

    def updateColor(self):
        hp = self.hitpoints%60 +1 #reset every 60s
        mP = (hp%20)*(20/255) #multiplyer
        if hp < 21:
            self.color = (255-mP,0+mP,0)
        elif hp < 41:
            self.color = (0,255-mP,0+mP)
        elif hp < 61:
            self.color = (0+mP,0,255-mP)
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.BRICK_WIDTH, self.BRICK_HEIGHT))
    
    def collidepoint(self,x,y):
        L = self.x
        T = self.y
        rec = pygame.rect.Rect(L,T,self.BRICK_WIDTH,self.BRICK_HEIGHT)
        return rec.collidepoint(x,y)


class NBS:
    def __init__(self,size,X,Y):
        self.size = size
        self.positionX = X + 22
        self.positionY = Y + 22
        self.WHITE = (255,255,255)
    def draw(self,screen):
        pygame.draw.circle(screen,self.WHITE,(self.positionX,self.positionY),self.size) #back circle
        pygame.draw.circle(screen,(100,100,100),(self.positionX,self.positionY),self.size-5) #"see through" part
        pygame.draw.circle(screen,self.WHITE,(self.positionX,self.positionY),self.size-10) #front circle

