#!/usr/bin/python
#-*- encoding:utf-8 -*-
from game import *
import pygame
from pygame.locals import *
import time
import sys
import socket

host = ''
client = 'localhost'
port = 54321

def startgame(scoreSocket = None, gridSocket = None):
    newgame = game(scoreSocket, gridSocket)
    newgame.startGame()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if scoreSocket <> None:
                        freshdata.sendMsg(scoreSocket, '-9')
                    game.iAmReady = True
        if (scoreSocket == None or gridSocket == None) and game.iAmReady:
            newgame.startGame()
        elif game.iAmReady and game.enemyReady:
            newgame.startGame()
        time.sleep(0.010)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == 'server':
            serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            serverSocket.bind((host, port))
            serverSocket.listen(1)
            print 'Waiting...'
            scoreSocket, clientaddr = serverSocket.accept()
            while True:
                print 'Connected from :', clientaddr
                data = scoreSocket.recv(16)
                if data == 'nancy':
                    scoreSocket.sendall('start')
                    break
            while True:
                gridSocket, gridclientaddr = serverSocket.accept()
                if clientaddr[0] == gridclientaddr[0]:
                    break
            startgame(scoreSocket, gridSocket)
        else:
            scoreSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host = sys.argv[1]
            print 'connect to ', host
            scoreSocket.connect((host, port))
            scoreSocket.sendall('nancy')
            while True:
                buf = scoreSocket.recv(16)
                if buf == 'start':
                    break
            gridSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            gridSocket.connect((host, port))
            startgame(scoreSocket, gridSocket)
    else:
        startgame()