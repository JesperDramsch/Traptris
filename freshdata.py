import threading
import game
from constants import *
import tetris

def sendMsg(socketName, message):
    try:
        socketName.sendall(message)
    except:
        game.game.gameResult = game_win
        socketName = None

class getgridsthreading(threading.Thread):
    def __init__(self, threadname, socketName):
        threading.Thread.__init__(self, name = threadname)
        self.socketName = socketName
    def run(self):
        while True:
            try:
                data = self.socketName.recv(5120)
                if not len(data):
                    continue
                game.game.enemyGrids = data
            except:
                game.game.gameResult = game_win
                socketName = None
            
        
class getscorethreading(threading.Thread):
    def __init__(self, threadname, socketName):
        threading.Thread.__init__(self, name = threadname)
        self.socketName = socketName
    def run(self):
        while True:
            try:
                data = self.socketName.recv(16)
                if not len(data):
                    continue
                if int(data) == -1:
                    game.game.gameResult = game_win
                elif int(data) == -9:
                    game.game.enemyReady = True
                else:
                    game.game.enemyScore = data
            except:
                game.game.gameResult = game_win
                socketName = None