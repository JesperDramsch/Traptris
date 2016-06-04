#!/usr/bin/env python2
#-*- coding: utf-8 -*-

# NOTE FOR WINDOWS USERS:
# You can download a "exefied" version of this game at:
# http://kch42.de/progs/tetris_py_exefied.zip
# If a DLL is missing or something like this, write an E-Mail (kevin@kch42.de)
# or leave a comment on this gist.

# Very simple tetris implementation
# 
# Control keys:
#       Down - Drop stone faster
# Left/Right - Move stone
#         Up - Rotate Stone clockwise
#     Escape - Quit game
#          P - Pause game
#     Return - Instant drop
#
# Have fun!

# Copyright (c) 2010 "Kevin Chabowski"<kevin@kch42.de>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from random import randrange as rand
import pygame, sys
from numpy import count_nonzero as countnz
from numpy import multiply as mp
from collections import deque
# The configuration
cell_size =    18
cols =        10
rows =        22
maxfps =     30
kitchen = 15
file = 'music.mp3'

colors = [(  255,   255,   255)]*12

# Define the shapes of the single parts
tetris_shapes = [
    [[1, 1, 1],
     [0, 1, 0]],
    
    [[0, 1, 1],
     [1, 1, 0]],
    
    [[1, 1, 0],
     [0, 1, 1]],
    
    [[1, 0, 0],
     [1, 1, 1]],
    
    [[0, 0, 1],
     [1, 1, 1]],
    
    [[1, 1, 1, 1]],
    
    [[1, 1],
     [1, 1]]
]


def rotate_clockwise(shape):
    return [ [ shape[y][x]
            for y in range(len(shape)) ]
        for x in range(len(shape[0]) - 1, -1, -1) ]

def check_collision(board, shape, offset):
    off_x, off_y = offset
    for cy, row in enumerate(shape):
        for cx, cell in enumerate(row):
            try:
                if cell and board[ cy + off_y ][ cx + off_x ]:
                    return True
            except IndexError:
                return True
    return False

def remove_row(board, row, subsurface, lines):
    subsurface[(rows*2-1)-lines] = board[row]
    del board[row]
    return [[0 for i in range(cols)]] + board
    
def join_matrixes(mat1, mat2, mat2_off):
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            mat1[cy+off_y-1    ][cx+off_x] += val
    return mat1

def weighted_choice(choices):
   total = sum(w for c, w in choices)
   r = rand(0, total+1)
   upto = 0
   for c, w in choices:
      if upto + w >= r:
         return c
      upto += w
   assert False, "Shouldn't get here"

def color_vec(matrix):
    for key in matrix:
        colors[matrix[key]["val"]]=matrix[key]["color"]

def new_board():
    board = [ [ 0 for x in range(cols) ]
            for y in range(rows) ]
    board += [[ 1 for x in range(cols)]]
    return board
 
def new_sub():
    board = [ [0 for x in range(cols) ]
            for y in range(rows*2) ]
    return board

class TetrisApp(object):
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(250,25)
        self.width = cell_size*(2*cols+2)
        self.height = cell_size*rows
        self.rlim = cell_size*cols
        
        self.default_font =  pygame.font.Font(
            pygame.font.get_default_font(), 12)
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.event.set_blocked(pygame.MOUSEMOTION) # We do not need
                                                     # mouse movement
                                                     # events, so we
                                                     # block them.
        self.next_stone = tetris_shapes[rand(len(tetris_shapes))]
                
        self.init_game()
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(loops=-1)

    def new_stone(self):
        self.stone = self.next_stone[:]
        self.stoneprop = weighted_choice([(self.rocktypes["source"],5),(self.rocktypes["sand_l"],2),(self.rocktypes["sand_h"],2),(self.rocktypes["seal"],2)]) if self.lines <= int(self.lines/7)+1 else weighted_choice([(self.rocktypes["sand_l"],3),(self.rocktypes["sand_h"],3),(self.rocktypes["seal"],3)])
        self.next_stone = mp(self.stoneprop["val"],tetris_shapes[weighted_choice([(0,10),(1,12),(2,12),(3,11),(4,11),(5,8),(6,9)])])
        self.stone_x = int(cols / 2 - len(self.stone[0])/2)
        self.stone_y = 0
        self.stonerand = [rand(-1,2),rand(1,4),rand(-3,6)]
        if check_collision(self.board,
                           self.stone,
                           (self.stone_x, self.stone_y)):
            self.gameover = True
    
    def init_game(self):
        self.board = new_board()
        self.subsurface = new_sub()
        self.oil = new_sub()
        self.oilblocks = 0
        self.level = 1
        self.spill = 0
        self.migmax = 0
        self.trappedblocks = 0
        self.score = 0
        self.lines = 0     
        self.directions = [0]*(rows*2)
        self.rocktypes = {
            "source": {
                "val": 1,
                "name": "Black Shale",
                "perm": 0,
                "pore": 10,
                "toc": 20,
                "color":(150,150,150)},
            "sand_h": {
                "val": 2,
                "name": "Sandstone",
                "perm": 1,
                "pore": 20,
                "toc": 1,
                "color":(250,233,0)},
            "sand_l": {
                "val": 3,
                "name": "Sandstone",
                "perm": 2,
                "pore": 30,
                "toc": 1,
                "color":(241,228,0)},
            "seal": {
                "val": 4,
                "name": "Clay",
                "perm": -2,
                "pore": 40,
                "toc": 4,
                "color":(200,96,60)},
            "oil": {
                "val": 5,
                "name": "Oil",
                "color":(0,0,0)}}
        self.bg_colors = {
            "lightgrey" : { 
                "val": 8,
                "color": (235, 235, 235)},
            "midgrey" : { 
                "val": 9,
                "color": (220, 220, 220)},
            "darkgrey" : { 
                "val": 10,
                "color": (35, 35, 35)}
        }
        color_vec(self.bg_colors)        
        color_vec(self.rocktypes)
        self.bground_grid = [[ self.bg_colors["midgrey"]["val"] if x%2==y%2 else self.bg_colors["lightgrey"]["val"] for x in range(cols)] for y in range(rows)]
        self.subsurf_grid = [[ self.bg_colors["midgrey"]["val"] if x%2==y%2 else self.bg_colors["lightgrey"]["val"] for x in range(cols)] for y in range(rows*2)]
        self.new_stone()
        self.stoneprop = self.rocktypes["source"]
        self.spill_point = int(cols/2)
        self.victory = False
        self.runoil = False
        self.slowmig = 0
        pygame.time.set_timer(pygame.USEREVENT+1, 1000)
    
    def disp_msg(self, msg, topleft): 
        x,y = topleft
        for line in msg.splitlines():
            self.screen.blit(
                self.default_font.render(
                    line,
                    False,
                    (255,255,255),
                    (0,0,0)),
                (x,y))
            y+=14
    
    def center_msg(self, msg):
        for i, line in enumerate(msg.splitlines()):
            msg_image =  self.default_font.render(line, False,
                (255,255,255), (0,0,0))
        
            msgim_center_x, msgim_center_y = msg_image.get_size()
            msgim_center_x //= 2
            msgim_center_y //= 2
        
            self.screen.blit(msg_image, (
              self.width // 2-msgim_center_x,
              self.height // 4-msgim_center_y+i*11))
    
    def draw_matrix(self, matrix, offset):
        off_x, off_y  = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(
                        self.screen,
                        colors[val],
                        pygame.Rect(
                            (off_x+x) *
                              cell_size,
                            (off_y+y) *
                              cell_size, 
                            cell_size,
                            cell_size),0)

    def draw_sub(self, matrix, offset):
        off_x, off_y  = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(
                        self.screen,
                        colors[val],
                        pygame.Rect(
                            (off_x) *
                              cell_size + x * cell_size/2,
                            (off_y) *
                              cell_size + y  * cell_size/2, 
                            cell_size/2,
                            cell_size/2),0)
    
    def add_cl_lines(self, n):
        linescores = [0, 40, 100, 300, 1200]
        self.lines += n
        self.score += linescores[n] * self.level
        if self.lines >= self.level*6:
            self.level += 1
            newdelay = 1000-50*(self.level-1)
            newdelay = 100 if newdelay < 100 else newdelay
            pygame.time.set_timer(pygame.USEREVENT+1, newdelay)
    
    def move(self, delta_x):
        if not self.gameover and not self.paused:
            new_x = self.stone_x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > cols - len(self.stone[0]):
                new_x = cols - len(self.stone[0])
            if not check_collision(self.board,
                                   self.stone,
                                   (new_x, self.stone_y)):
                self.stone_x = new_x
    def quit(self):
        self.center_msg("Exiting...")
        pygame.display.update()
        sys.exit()
    
    def drop(self, manual):
        if not self.gameover and not self.paused:
            self.score += 1 if manual else 0
            self.stone_y += 1
            if check_collision(self.board,
                               self.stone,
                               (self.stone_x, self.stone_y)):
                self.board = join_matrixes(
                  self.board,
                  self.stone,
                  (self.stone_x, self.stone_y))
                self.new_stone()
                while True:
                    for i, row in enumerate(self.board[:-1]):
                        if 0 not in row:
                            self.board = remove_row(
                              self.board, i, self.subsurface, self.lines)
                            self.add_cl_lines(1)
                            break
                    else:
                        break
                
                return True
        return False
    
    def insta_drop(self):
        if not self.gameover and not self.paused:
            while(not self.drop(True)):
                pass
    
    def rotate_stone(self):
        if not self.gameover and not self.paused:
            new_stone = rotate_clockwise(self.stone)
            if not check_collision(self.board,
                                   new_stone,
                                   (self.stone_x, self.stone_y)):
                self.stone = new_stone
    
    def toggle_pause(self):
        self.paused = not self.paused
    
    def start_game(self):
        if self.gameover:
            self.init_game()
            self.gameover = False
            
    def oil_create(self,matrix):
        oil = mp(matrix,0)        
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val == 1:
                    oil[y][x] = self.rocktypes["oil"]["val"]
                    self.oilblocks += 1
        return oil
#        self.subsurface += mp((self.subsurface == 1),3)
        
    def oil_migrate(self,submatrix,oilmatrix):
        self.trappedblocks = 0
        for y, row in reversed(list(enumerate(oilmatrix))) if self.spill == 0 else enumerate(oilmatrix):
            for x, val in enumerate(row):
                if val == self.rocktypes["oil"]["val"]:
                    if submatrix[y-1][x] == 0:
                        height = 9
                        if self.spill == 0:
                            self.spill_point = x
                            self.spill = 1
                        if y > height and self.spill_point == x:
                            oilmatrix[y-1][x] = 1
                            oilmatrix[y][x] = 1
                        elif y <= 1:
                            self.gameover = True
                            self.trappedblocks = countnz(oilmatrix[-self.lines+1:])
                            return oilmatrix
                        elif not x == 0 and not x == cols-1  and y <= height:
                            oilmatrix[y-1][x+1] = 1
                            oilmatrix[y-1][x-1] = 1
                        elif not x == cols-1   and y <= height:
                            oilmatrix[y-1][x+1] = 1
                        elif not x == 0   and y <= height:
                            oilmatrix[y-1][x-1] = 1
                        else:
                            oilmatrix[y][x] = 1
                       #self.gameover = True
                        #
# Success, Upward migration                    
                    elif submatrix[y-1][x] < self.rocktypes["seal"]["val"] and oilmatrix[y-1][x] == 0:
                        oilmatrix[y-1][x] = 1
                        oilmatrix[y][x] = 0
                        self.migmax = 0
# Success, left or right
                    elif not x==0 and not x==cols-1 and submatrix[y][x-1] < self.rocktypes["seal"]["val"] and submatrix[y][x+1] < self.rocktypes["seal"]["val"] and oilmatrix[y][x-1] == 0 and oilmatrix[y][x+1] == 0:
                        if self.directions[y] == 0:
                            self.directions[y] = int(2*(rand(0,2)-0.5))
                        oilmatrix[y][x+self.directions[y]] = 1
                        oilmatrix[y][x] = 0
                        self.migmax += 1
# Success, left
                    elif not x==0 and submatrix[y][x-1] < self.rocktypes["seal"]["val"] and oilmatrix[y][x-1] == 0:
                        oilmatrix[y][x-1] = 1
                        oilmatrix[y][x] = 0
                        self.migmax += 1
                        self.directions[y] = -1
# Success, right
                    elif not x==cols-1 and submatrix[y][x+1] < self.rocktypes["seal"]["val"] and oilmatrix[y][x+1] == 0:
                        oilmatrix[y][x+1] = 1
                        oilmatrix[y][x] = 0
                        self.migmax += 1
                        self.directions[y] = 1
                    else:
                        self.trappedblocks += 1 
                        oilmatrix[y][x] = 1 
                        if self.trappedblocks >= self.oilblocks:
                            self.gameover = True
                            self.victory = True
        oilmatrix = mp(self.rocktypes["oil"]["val"],oilmatrix)
        self.draw_sub(oilmatrix,(cols*1.5 + 1,0))
        return oilmatrix
    
    def run(self):
        key_actions = {
            'ESCAPE':    self.quit,
            'LEFT':        lambda:self.move(-1),
            'RIGHT':    lambda:self.move(+1),
            'DOWN':        lambda:self.drop(True),
            'UP':        self.rotate_stone,
            'p':        self.toggle_pause,
            's':        self.toggle_pause,
            'SPACE':    self.start_game,
            'RETURN':    self.insta_drop
        }
        
        # TEST for migration paths
        
        kitchen = 18
        self.subsurface = self.subsurface[:-kitchen]
        self.subsurface += [ [self.rocktypes["seal"]["val"] if (x==5 and y%4) or (x>=5 and not (y)%4)  else self.rocktypes["sand_h"]["val"] for x in range(cols) ]
            for y in range(4) ] #trap
        self.subsurface += [ [self.rocktypes["seal"]["val"] if (x<=6 and y%4==1) or (x>=3 and (y)%4==3)  else self.rocktypes["sand_h"]["val"] for x in range(cols) ]
            for y in range(8) ] #parcour
        self.subsurface += [ [self.rocktypes["sand_h"]["val"] if x%2==y%2 else self.rocktypes["sand_l"]["val"] for x in range(cols) ]
            for y in range(3) ] #sand
        self.subsurface += [ [self.rocktypes["source"]["val"] if x%2==y%2 else self.rocktypes["sand_h"]["val"] for x in range(cols) ]
            for y in range(2) ] #source
        self.subsurface += [ [self.rocktypes["source"]["val"] for x in range(cols) ]
            for y in range(1) ] #source
        self.lines = kitchen
        
        self.gameover = False
        self.paused = True
                
        
        dont_burn_my_cpu = pygame.time.Clock()
        while 1:
            self.screen.fill((0,0,0))
            if self.gameover and self.victory:
                self.center_msg("""Victory!\nGet drilling! You trapped: %d barrels\n
Your boring tetris score is: %d \n
Press space to beat that score""" % (self.oilblocks*1000000, self.score))
            elif self.gameover and self.trappedblocks > 0:
                self.center_msg("""Game Over!\nYou did not Trap It all \n but %d barrel are safe!
Press space to try again""" % (self.trappedblocks*1000000))
            elif self.gameover:
                self.center_msg("""Game Over!\nYou did not Trap It \n
Press space to try again""")
            else:
                if self.paused:
                    self.center_msg("""Welcome to Traptris!\n
The tetris game with a geo-twist.\n\n Form lines to build your subsurface.\n Build up the source rock.\n Form a seal.\n Bury the rock to get it cooking! \n\n Press "S" to Play!\n
. . . \n\nPaused""")
                else:
                    pygame.draw.line(self.screen,
                        (255,255,255),
                        (self.rlim+1, 0),
                        (self.rlim+1, self.height-1))
# Mid column
                    self.disp_msg("Next:", (
                        self.rlim+cell_size, 2))
                    self.disp_msg("Rock Type: \n%s\n\nTOC: %d%%\n\nPerm.: %3.2fmD\n\nPorosity: %d%%\n\nScore: %d\n\nLevel: %d\
                        \nLines: %d" % (self.stoneprop["name"], self.stoneprop["toc"]+self.stonerand[0], self.stonerand[1]*10**self.stoneprop["perm"], self.stonerand[2]+self.stoneprop["pore"], self.score, self.level, self.lines),
                        (self.rlim+cell_size, cell_size*5))
                    self.draw_matrix(self.next_stone,
                        (cols+1,2))
                    self.draw_matrix(self.bground_grid, (0,0))
                    self.draw_matrix(self.board, (0,0))
                    self.draw_sub(self.subsurf_grid, (cols*1.5 + 1,0))
                    self.draw_sub(self.subsurface, (cols*1.5 + 1,0))
                    self.draw_matrix(self.stone,
                        (self.stone_x, self.stone_y))                    
                        
# If in kitchen migrate
                    if self.lines >= kitchen and self.runoil == False:
                        self.runoil = True
                        self.oil = self.oil_create(self.subsurface)
                        self.oilblocks = countnz(self.oil)
                        self.disp_msg("Oil done cooking! \nMigration starting right now!", (
                        cols*1.5+2, 2))
                        self.draw_sub(self.oil,(cols*1.5 + 1,0))
                    elif self.lines == kitchen-2 or self.lines == kitchen-1:
                        self.disp_msg("Oil cooking! \nMigration starting soon!", (
                        cols*1.5+2, 2))
                        
                    elif self.lines >= kitchen:
                        self.slowmig +=1
                        if self.slowmig == 5:
                            self.slowmig = 0
                            self.oil = self.oil_migrate(self.subsurface,self.oil)
                            if self.migmax >= countnz(self.oil)*10+1:
                                self.gameover = True
                                self.victory = True
                        self.draw_sub(self.oil,(cols*1.5 + 1,0))
                        
                        

            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT+1:
                    self.drop(False)
                elif event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    for key in key_actions:
                        if event.key == eval("pygame.K_"
                        +key):
                            key_actions[key]()
                    
            dont_burn_my_cpu.tick(maxfps)

if __name__ == '__main__':
    App = TetrisApp()
    App.run()
