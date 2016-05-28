#!/usr/bin/python
#-*- encoding:utf-8 -*-
from random import *
from constants import *

class shapeBase:
    """ Base Class of shape """
    "base class for shape"
    def __init__(self, status, faceDirection, posX, posY, color = (randint(0,255), randint(0,255), randint(0,255))):
        self.color = color
        self.status = status
        self.direction = faceDirection
        self.x = posX
        self.y = posY
        self.moveOver = False
        self.gameOver = False
        self.grids = []
        if not self.move(posX, posY, faceDirection):
            self.gameOver = True
        
    def moveleft(self):
        return self.move(self.x - 1, self.y, self.direction)
    def moveright(self):
        return self.move(self.x + 1, self.y, self.direction)
    def movedown(self):
        if self.move(self.x, self.y + 1, self.direction):
            return True
        #can't move up,then the move of the shape is over
        self.moveOver = True
        return False
    
    def move(self, endX, endY, newDirection):
        """move the shape from (startX, startY) to (endX, endY)"""
        newGrids = self.getGrids(newDirection, endX, endY) #get next grids
        if self.isMoveAble(newGrids):
            self.create(self.grids, 0) # clear current shape        
            self.create(newGrids) #create new shape
            self.grids = newGrids
            self.x = endX
            self.y = endY
            self.direction = newDirection
            return True
        return False
    def isMoveAble(self, newGrids):
        for (gx, gy) in newGrids:
            if not (gx in range(gridCountW) and gy in range(gridCountH)):
                return False
            if self.status[gx][gy][0] == 1:
                if not (gx, gy) in self.grids:
                    return False
        return True
    
    def turn(self):
        newDirection = self.direction + 1
        if newDirection == 4:
            newDirection = 0
        return self.move(self.x, self.y, newDirection)
        
    def create(self,  theGrids, fill = 1):
        for (gx, gy) in theGrids:
            self.status[gx][gy] = [fill, self.color]

    def getGrids(self, faceDirection, posX, posY):
        """create shapeT"""
        pass