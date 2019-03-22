#!/usr/bin/python
# -*- coding: utf-8 -*-

# === Fazer um cabeçalho bonito aqui ===

# Import Python libraries
import pygame
import os
import sys
from pygame.locals import *
from random import randint

# Import local settings
from config import *


# Initialize game display
def initalize_display(argv):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_LENGTH))
    pygame.display.set_caption('Rainbow Trap')

    return screen


# Class for Maze generation
class Maze:
    def __init__(self, x_length, y_length):
        print('WIP')


# Class for Temporary grid used to generate maze before showing in the screen
class TempBlock:
    def new_grid(self):
        grid = []
        for i in range(self.y_length):
            grid_line = []
            for j in range(self.x_length):
                cell = MazeCell()
                if randint(0, 9) % 2 == 1:
                    cell.cell_state = INVALID
                grid_line.append(cell)
            grid.append(grid_line)
        return grid

    def __init__(self, cell_size, x_length, y_length):
        self.cell_size = cell_size
        self.x_length = x_length
        self.y_length = y_length
        self.grid = self.new_grid()

    def get_line(self):
        if self.grid:
            return self.grid.pop()
        else:
            self.grid = self.new_grid()
            return self.grid.pop()

    def get_grid(self):
        if self.grid:
            return self.grid
        else:
            self.grid = self.new_grid()
            return self.grid

    def renew_grid(self):
        self.grid = self.new_grid()


# Class for each maze cell used to generate the maze
class MazeCell:
    def __init__(self):
        self.cell_state = AVAIABLE


# Class for pool of possible objects to be inserted in the maze
class Pool:
    def __init__():
        print('')


# Class for Main Character
class Kiko:
    def __init__(self, size, color):
        self.color = color
        self.size = size
        self.skin = pygame.Surface((size, size))
        self.pos = (INITIAL_X, INITIAL_Y)
        self.move = STAY
        self.skin.fill(self.color)

    def change_dir(self, dir):
        self.move = dir

    def moving(self):
        if self.move == RIGHT:
            if (self.pos[0]+2*self.size <= SCREEN_WIDTH):
                self.pos = (self.pos[0]+self.size, INITIAL_Y)
        if self.move == LEFT:
            if (self.pos[0]-self.size >= 0):
                self.pos = (self.pos[0]-self.size, INITIAL_Y)

    def choose_color(self):
        if pygame.key.get_pressed()[K_a]:
            if pygame.key.get_pressed()[K_w]:
                self.change_color(VIOLET)
            elif pygame.key.get_pressed()[K_s]:
                self.change_color(INDIGO)
            else:
                self.change_color(BLUE)
        elif pygame.key.get_pressed()[K_d]:
            if pygame.key.get_pressed()[K_w]:
                self.change_color(ORANGE)
            elif pygame.key.get_pressed()[K_s]:
                self.change_color(WHITE)
            else:
                self.change_color(RED)
        elif pygame.key.get_pressed()[K_w]:
            self.change_color(YELLOW)
        else:
            self.change_color(GREEN)

    def change_color(self, color):
        self.color = color
        self.skin.fill(self.color)


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
        screen.blit(kiko.skin, kiko.pos)
        if not grid:
            grid = maze.get_grid()
        count_y = 200
        for line in grid:
            count_x = 0
            count_y = count_y + maze.cell_size
            for cell in line:
                maze_skin = pygame.Surface((maze.cell_size, maze.cell_size))
                maze_skin.fill(RED)
                if cell.cell_state == AVAIABLE:
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
