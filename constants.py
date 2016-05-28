#!/usr/bin/python
#-*- encoding:utf-8 -*-
screenBackground = (51, 51, 51)
gameBackground = (255, 255, 221)
gameBorderColor = (24, 124, 5)
fontColor = (251, 102, 10)
tipFontColor = (255, 255, 169)
screenSize = (800, 600)
gridWidth = 25
startX = 200
startY = 50
enemyGridWidth = gridWidth / 3

gridCountW, gridCountH = 14, 20
gameWidth = gridCountW * gridWidth
gameHeight = gridCountH * gridWidth
enemyZoneWidth = gridCountW * enemyGridWidth
enemyZoneHeight = gridCountH * enemyGridWidth

emptyGrid = [0, gameBackground]
gameOverPos = (startX + 2 * gridWidth, startY + gridCountH * gridWidth / 3)
nextGridsPos = ((startX + (gridCountW + 2) * gridWidth), startY + 2 *  gridWidth)
scorePos = (nextGridsPos[0] - 1 * gridWidth, nextGridsPos[1] + 5 * gridWidth)
enemyScorePos = (scorePos[0], scorePos[1] + 2 * gridWidth)
enemyGridsPos = (nextGridsPos[0], enemyScorePos[1] + 4 * gridWidth)

tipsPos = (startX, screenSize[1] - 1.7 * gridWidth)
#tips = ['up       -   turn', 'left     -  move left', 'right   - move right', 'space  - fall directly', 'down   - fast fall', 'Enter   - restart']
tips = ['UP - turn  LEFT - move left  RIGHT - move right', 'SPACE - fall directly  DOWN - fast fall  ENTER - restart']

gameTitle = 'Nancy Tetris'
face_left, face_right, face_up, face_down = 1, 3, 2, 0
startLevel = 0.9
game_win, game_fail, game_running = 1, -1, 0