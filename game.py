#!/usr/bin/env python
#coding=utf-8

import time
import pygame
from pygame.locals import *
from sys import exit
from shapes import *
from constants import *
import freshdata
import threading

class game(object):
    enemyScore = 0
    enemyGrids= ''
    gameResult = game_running
    enemyReady = False
    iAmReady = False
    def __init__(self,  scoreSocket = None, gridsSocket = None):
        self.scoreSocket = scoreSocket
        self.gridsSocket = gridsSocket
        self.shapeList = [shapeT, shapeZ, shapeZ2 ,shapeI, shapeL2, shapeL, shapeO]
        self.initpygame()
        self.startgetgridsthread()
        self.startgetscorethread()
    
    def startgetgridsthread(self):
        if self.gridsSocket <> None:
            self.getgridsThread = freshdata.getgridsthreading('getGrids', self.gridsSocket)
            self.getgridsThread.setDaemon(True)
            self.getgridsThread.start()
    def startgetscorethread(self):
        if self.scoreSocket <> None:
            self.getScoreThread = freshdata.getscorethreading('getScore', self.scoreSocket)
            self.getScoreThread.setDaemon(True)
            self.getScoreThread.start()
    def initpygame(self):
        pygame.init()
        icon = pygame.image.load("bm.png")
        pygame.display.set_icon(icon)
        pygame.event.set_allowed([KEYDOWN])
        #KEYDOWN repeat enable
        pygame.key.set_repeat(300, 20)
        self.screen = pygame.display.set_mode(screenSize, 0, 32)
        pygame.display.set_caption(gameTitle)
        self.my_font = pygame.font.SysFont("arial", 23)
        self.my_font_tip = pygame.font.SysFont("arial", 15)
        self.my_font_gameover = pygame.font.SysFont("arial", 75)

    def display(self, getMyGrids = False):
        """Display the screen by the array of stutas"""
        # draw the game zone
        self.screen.fill(screenBackground)
        pygame.draw.rect(self.screen, gameBorderColor, ((startX - 2, startY - 2), (gameWidth + 4, gameHeight + 4)))
        pygame.draw.rect(self.screen, gameBackground, ((startX, startY), (gameWidth, gameHeight)))
        
        #draw tips
        tipX, tipY = tipsPos[0], tipsPos[1]
        for tip in tips:
            tip_text = self.my_font_tip.render(tip, True, tipFontColor)
            self.screen.blit(tip_text, (tipX, tipY))
            tipY += 0.8 * gridWidth
        
        #draw the player's score
        text_Score = self.my_font.render('Nancy Score: ' + str(self.yourScore), True, fontColor)
        self.screen.blit(text_Score, scorePos)
        #draw the competitor's score 
        if self.scoreSocket <> None:
            enemy_text_Score = self.my_font.render("Enemy's Score:" + str(game.enemyScore), True, fontColor)
            self.screen.blit(enemy_text_Score, enemyScorePos)
        self.myGrids = ''
        #draw the player's game zone
        for i in range(gridCountW):
            for j in range(gridCountH):
                if self.status[i][j][0] == 1:
                    pygame.draw.rect(self.screen, gameBackground, 
                                    ((startX + i * gridWidth, startY + j * gridWidth),
                                     (gridWidth, gridWidth)))
                    pygame.draw.rect(self.screen, self.status[i][j][1],
                                    ((startX + i * gridWidth + 1, startY + j * gridWidth + 1),
                                     (gridWidth - 2, gridWidth - 2)))
                    if getMyGrids:
                        self.myGrids += str(i) + ',' + str(j) + ',' + str(self.status[i][j][1][0]) + ',' + \
                            str(self.status[i][j][1][1]) + ',' + str(self.status[i][j][1][2]) + ';'
        #draw the competitor's game zone
        if self.gridsSocket <> None:
            pygame.draw.rect(self.screen, gameBorderColor, ((enemyGridsPos[0] - 2, enemyGridsPos[1] - 2),
                                                            (enemyZoneWidth + 4, enemyZoneHeight + 4)))
            pygame.draw.rect(self.screen, gameBackground, ((enemyGridsPos[0], enemyGridsPos[1]), (enemyZoneWidth, enemyZoneHeight)))
            gridList = game.enemyGrids.rstrip(';').split(';')
            for grid in gridList:
                gridItems = grid.split(',')
                if len(gridItems) <> 5:
                    break
                pygame.draw.rect(self.screen, gameBackground,
                                 ((enemyGridsPos[0] + int(gridItems[0]) * enemyGridWidth, 
                                   enemyGridsPos[1] + int(gridItems[1]) * enemyGridWidth),
                                  (enemyGridWidth, enemyGridWidth)))
                pygame.draw.rect(self.screen, (int(gridItems[2]), int(gridItems[3]), int(gridItems[4])),
                                 ((enemyGridsPos[0] + int(gridItems[0]) * enemyGridWidth + 1.0/3, 
                                   enemyGridsPos[1] + int(gridItems[1]) * enemyGridWidth + 1.0/3),
                                  (enemyGridWidth - 2.0/3, enemyGridWidth - 2.0/3)))
        #display next shape
        nextGrids = self.nextShape.getGrids(face_down, 0, 0)
        for i in range(4):
            for j in range(4):
                if (i, j) in nextGrids:
                    pygame.draw.rect(self.screen, screenBackground, 
                                     ((nextGridsPos[0] + i * gridWidth, nextGridsPos[1] + j * gridWidth), 
                                      (gridWidth, gridWidth)))
                    pygame.draw.rect(self.screen, self.nextShapeColor, 
                                     ((nextGridsPos[0] + i * gridWidth + 1, nextGridsPos[1] + j * gridWidth + 1), 
                                      (gridWidth - 2, gridWidth - 2)))
        if game.gameResult == game_fail:
            text_gameOver = self.my_font_gameover.render("You Lost!", True, (255, 0, 0))
            self.screen.blit(text_gameOver, gameOverPos)
        elif game.gameResult == game_win:
            text_gameOver = self.my_font_gameover.render("You Win!", True, (0, 0, 255))
            self.screen.blit(text_gameOver, gameOverPos)
        pygame.display.update()
                    
    def isFullLine(self, y):
        if y >= gridCountH:
            return False
        ls = [x for x in range(gridCountW) if self.status[x][y][0] == 0]
        return ls == []
    
    def getLevel(self):
        self.level =  startLevel - 0.01 * (self.yourScore / 1000)
    
    def clearOneLine(self, startY):
        self.yourScore += 100
        self.getLevel()
        for x in range(gridCountW):
            for y in range(startY, 0, -1):
                self.status[x][y] = self.status[x][y - 1]
            self.status[x][0] = emptyGrid
    
    def dropByLine(self, shape):
        """dorp all by the line count cleared"""
        fullLines = filter(self.isFullLine, range(shape.y, shape.y + 4))
        if len(fullLines) >= 3:
            self.yourScore += (len(fullLines) - 2) * 100
        clearLines = (len(fullLines) > 0)
        while fullLines <> []:
            fullY = fullLines.pop()
            self.clearOneLine(fullY)
            fullLines = filter(self.isFullLine, range(0, fullY + 1))
        if clearLines and self.scoreSocket <> None:
            freshdata.sendMsg(self.scoreSocket, str(self.yourScore))
        if self.gridsSocket <> None:
            self.display(getMyGrids = True)
            freshdata.sendMsg(self.gridsSocket, self.myGrids)
        else:
            self.display()
    
    def fetchNextShape(self):
        self.nextShape = choice(self.shapeList)
        self.nextShapeColor = (randint(0,255), randint(0,255), randint(0,255))
    
    def initsettings(self):
        """init game Environment"""
        game.gameResult = game_running
        game.enemyGrids = ''
        game.enemyScore = 0
        game.enemyReady = False
        game.iAmReady = False
        self.yourScore = 0
        self.getLevel()
        self.status = [[[0,gameBackground] for col in range(gridCountH)] for row in range(gridCountW)]
        self.myGrids = ''
        self.fetchNextShape()
        self.display()
    def startGame(self):
        """start a game"""
        self.initsettings()
        while game.gameResult == game_running:
            sp = self.nextShape(self.status, face_down, (gridCountW - 1) / 2, 0, self.nextShapeColor)
            self.fetchNextShape()
            if sp.gameOver:
                game.gameResult = game_fail
                if self.scoreSocket <> None:
                    freshdata.sendMsg(self.scoreSocket, '-1')
                self.display()
                break
            timeFlag = time.time()
            while (game.gameResult == game_running) and (not sp.moveOver):
                for event in pygame.event.get():
                    if event.type == QUIT:
                        exit()
                    elif event.type == KEYDOWN:
                        if event.key == K_LEFT:
                            sp.moveleft()
                        if event.key == K_RIGHT:
                            sp.moveright()
                        elif event.key == K_UP:
                            sp.turn()
                        elif event.key == K_DOWN:
                            sp.movedown()
                        elif event.key == K_SPACE:
                            while sp.movedown():
                                self.display()
                                #time.sleep(0.001)
                if time.time() - timeFlag >= self.level:
                    timeFlag = time.time()
                    sp.movedown()
                self.display()
                time.sleep(0.010)
            #when shapeBlock is over, check the status
            self.dropByLine(sp)