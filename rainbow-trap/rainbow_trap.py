#!/usr/bin/python
# -*- coding: utf-8 -*-

# === Fazer um cabeçalho bonito aqui ===

# Import Python libraries
import pygame
import os
import sys
from pygame.locals import *

# Import local settings
from config import *

# Import classes
from entities.kiko import Kiko
from entities.maze import *


# Initialize game display
def initalize_display(argv):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_LENGTH))
    pygame.display.set_caption('Rainbow Trap')
 
    return screen


# Main game flow
def main(argv):
    screen = initalize_display(argv)
    time = 0
    clock = pygame.time.Clock()
    kiko = Kiko(PLAYER_SIZE, RED)
    grid_x = SCREEN_WIDTH // FAT_X
    grid_y = SCREEN_LENGTH // FAT_Y
    maze = TempBlock(SCREEN_LENGTH // grid_x, grid_x, grid_y)
    grid = maze.get_grid()
    maze.renew_grid()
    continue_game = True

    while True:
        time = time + clock.tick(50)
        # If user closes the window, quit the game
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    kiko.change_dir(LEFT)
                elif event.key == K_RIGHT:
                    kiko.change_dir(RIGHT)
                if event.key in [K_a, K_w, K_s, K_d]:
                    kiko.choose_color()
            if event.type == KEYUP:
                if event.key == K_RIGHT and kiko.move == RIGHT:
                    if pygame.key.get_pressed()[K_LEFT]:
                        kiko.change_dir(LEFT)
                    else:
                        kiko.change_dir(STAY)
                if event.key == K_LEFT and kiko.move == LEFT:
                    if pygame.key.get_pressed()[K_RIGHT]:
                        kiko.change_dir(RIGHT)
                    else:
                        kiko.change_dir(STAY)

        kiko.moving()

        screen.fill((0, 0, 0))
        screen.blit(kiko.image, kiko.pos)
        if not grid:
            grid = maze.get_grid()
        count_y = 0
        for line in grid:
            count_x = 0
            count_y = count_y + maze.cell_size
            for cell in line:
                maze_skin = pygame.Surface((maze.cell_size, maze.cell_size))
                maze_skin.fill(WHITE)
                if cell.cell_state == WALL:
                    screen.blit(maze_skin, (count_x, count_y))
                count_x = count_x + maze.cell_size
        if time > 1000 / MAZE_SPEED:
            time = 0
            grid.pop(0)
            grid.append(maze.get_line())

        # Update the display
        pygame.display.update()

# Calls main function if executed as a script
if __name__ == '__main__':
    main(sys.argv)
