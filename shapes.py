#!/usr/bin/env python
#coding=utf-8
from shapebase import *

class shapeZ(shapeBase):
    """ shape Z """
    @staticmethod
    def getGrids(faceDirection, posX, posY):
        resGrids = []
        #face down up
        if faceDirection == face_down or faceDirection == face_up:
            resGrids.append((posX, posY + 1))
            resGrids.append((posX, posY + 2))
            resGrids.append((posX + 1, posY))
            resGrids.append((posX + 1, posY + 1))
        else:
            resGrids.append((posX, posY))
            resGrids.append((posX + 1, posY))
            resGrids.append((posX + 1, posY + 1))
            resGrids.append((posX + 2, posY + 1))
        return resGrids

class shapeZ2(shapeBase):
    """ shape Z2 """
    @staticmethod
    def getGrids(faceDirection, posX, posY):
        resGrids = []
        #face down up
        if faceDirection == face_down or faceDirection == face_up:
            resGrids.append((posX + 1, posY))
            resGrids.append((posX + 1, posY + 1))
            resGrids.append((posX + 2, posY + 1))
            resGrids.append((posX + 2, posY + 2))
        else:
            resGrids.append((posX, posY + 1))
            resGrids.append((posX + 1, posY))
            resGrids.append((posX + 1, posY + 1))
            resGrids.append((posX + 2, posY))
        return resGrids

class shapeI(shapeBase):
    """ shape I """
    @staticmethod
    def getGrids(faceDirection, posX, posY):
        resGrids = []
        #face down up
        if faceDirection == face_down or faceDirection == face_up:
            resGrids.append((posX + 1, posY))
            resGrids.append((posX + 1, posY + 1))
            resGrids.append((posX + 1, posY + 2))
            resGrids.append((posX + 1, posY + 3))
        else:
            resGrids.append((posX, posY + 1))
            resGrids.append((posX + 1, posY + 1))
            resGrids.append((posX + 2, posY + 1))
            resGrids.append((posX + 3, posY + 1))
        return resGrids

class shapeT(shapeBase):
    """ shape T """
    @staticmethod
    def getGrids(faceDirection, posX, posY):
        resGrids = []
        #face down
        if faceDirection == face_down:
            resGrids.append((posX, posY + 1))
            resGrids.append((posX + 1, posY + 1))
            resGrids.append((posX + 1, posY + 2))
            resGrids.append((posX + 2, posY + 1))
        #face left
        if faceDirection == face_left:
            resGrids.append((posX, posY + 1))
            resGrids.append((posX + 1, posY))
            resGrids.append((posX + 1, posY + 1))
            resGrids.append((posX + 1, posY + 2))
        #face up
        if faceDirection == face_up:
            resGrids.append((posX, posY + 1))
            resGrids.append((posX + 1, posY))
            resGrids.append((posX + 1, posY + 1))
            resGrids.append((posX + 2, posY + 1))
        #face right
        if faceDirection == face_right:
            resGrids.append((posX + 1, posY))
            resGrids.append((posX + 1, posY + 1))
            resGrids.append((posX + 1, posY + 2))
            resGrids.append((posX + 2, posY + 1))
        return resGrids
    
class shapeL(shapeBase):
    """ shape L """
    @staticmethod
    def getGrids(faceDirection, posX, posY):
        resGrids = []
        #face down
        if faceDirection == face_down:
            resGrids.append((posX + 1, posY))
            resGrids.append((posX + 1, posY + 1))
            resGrids.append((posX + 1, posY + 2))
            resGrids.append((posX + 2, posY))
        #face left
        if faceDirection == face_left:
            resGrids.append((posX, posY + 1))
            resGrids.append((posX + 1, posY + 1))
            resGrids.append((posX + 2, posY + 1))
            resGrids.append((posX + 2, posY + 2))
        #face up
        if faceDirection == face_up:
            resGrids.append((posX, posY + 2))
            resGrids.append((posX + 1, posY))
            resGrids.append((posX + 1, posY + 1))
            resGrids.append((posX + 1, posY + 2))
        #face right
        if faceDirection == face_right:
            resGrids.append((posX, posY))
            resGrids.append((posX, posY + 1))
            resGrids.append((posX + 1, posY + 1))
            resGrids.append((posX + 2, posY + 1))
        return resGrids

class shapeL2(shapeBase):
    """ shape L2 """
    @staticmethod
    def getGrids(faceDirection, posX, posY):
        resGrids = []
        #face down
        if faceDirection == face_down:
            resGrids.append((posX, posY))
            resGrids.append((posX + 1, posY))
            resGrids.append((posX + 1, posY + 1))
            resGrids.append((posX + 1, posY + 2))
        #face left
        if faceDirection == face_left:
            resGrids.append((posX, posY + 1))
            resGrids.append((posX + 1, posY + 1))
            resGrids.append((posX + 2, posY + 1))
            resGrids.append((posX + 2, posY))
        #face up
        if faceDirection == face_up:
            resGrids.append((posX + 1, posY))
            resGrids.append((posX + 1, posY + 1))
            resGrids.append((posX + 1, posY + 2))
            resGrids.append((posX + 2, posY + 2))
        #face right
        if faceDirection == face_right:
            resGrids.append((posX, posY + 1))
            resGrids.append((posX, posY + 2))
            resGrids.append((posX + 1, posY + 1))
            resGrids.append((posX + 2, posY + 1))
        return resGrids

class shapeO(shapeBase):
    """ shape O"""
    @staticmethod
    def getGrids(faceDirection, posX, posY):
        resGrids = []
        resGrids.append((posX, posY))
        resGrids.append((posX, posY + 1))
        resGrids.append((posX + 1, posY))
        resGrids.append((posX + 1, posY + 1))
        return resGrids