import pygame
import numpy as np
import time

from pygame import mouse

pygame.init()

# size of the screen
width,  height = 800, 800

# create the screen
screen = pygame.display.set_mode((height,width))

# background color = almost black
bg = 25, 25, 25

# Paint the screen with the chosen background color
screen.fill(bg)


nxC, nyC = 75, 75

dimCW = width / nxC
dimCH = height / nyC

# Cell states. Lives = 1, Dead = 0
gameState = np.zeros((nxC, nyC))

pauseExec = True

while True:

    newGameState = np.copy(gameState)

    screen.fill(bg)

    time.sleep(0.1)

    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.KEYDOWN:
            pauseExec = not pauseExec

        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            cellX, cellY = round(np.floor(posX / dimCW)), round(np.floor(posY / dimCH))
            newGameState[cellX, cellY] = not mouseClick[2]

    for y in range ( 0, nyC):

        for x in range( 0, nxC):

            if not pauseExec:
                n_neigh = gameState[ (x-1)  % nxC,  (y-1)   % nyC] + \
                        gameState[ (x)    % nxC,  (y-1)   % nyC] + \
                        gameState[ (x+1)  % nxC,  (y-1)   % nyC] + \
                        gameState[ (x-1)  % nxC,  (y)     % nyC] + \
                        gameState[ (x+1)  % nxC,  (y)     % nyC] + \
                        gameState[ (x-1)  % nxC,  (y+1)   % nyC] + \
                        gameState[ (x)    % nxC,  (y+1)   % nyC] + \
                        gameState[ (x+1)  % nxC,  (y+1)   % nyC]

                # Rule 1: A dead cell with 3 alive neighboors, "revive"
                if gameState[x,y] == 0 and n_neigh == 3:
                    newGameState[x,y] = 1

                # Rule 2: An alive cell with less than 2 or more than 3 alive neighboors cells, "die"
                elif gameState[x,y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x,y] = 0

            poly = [((x)    * dimCW, y      * dimCH),
                    ((x+1)  * dimCW, y      * dimCH),
                    ((x+1)  * dimCW, (y+1)  * dimCH),
                    ((x)    * dimCW, (y+1)  * dimCH)]
    
            if gameState[x,y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    gameState = np.copy(newGameState)

    pygame.display.flip()
