# Import Python libraries
import pygame
from pygame.locals import *
from random import randint

# Import local settings
from config import *

# Import classes
from pool import Pool


# Class for Maze generation
class Maze:
    def __init__(self, x_length, y_length):
        print('WIP')


# Class for Temporary grid used to generate maze before showing in the screen
class TempBlock:
    def __init__(self, cell_size, x_length, y_length):
        self.cell_size = cell_size
        self.x_length = x_length
        self.y_length = y_length
        self.pool = Pool()
        self.grid = self.new_grid()

    def new_grid(self):
        # Empty and avaiable grid
        grid = []
        for i in range(self.y_length):
            grid_line = []
            for j in range(self.x_length):
                cell = MazeCell()
                grid_line.append(cell)
            grid.append(grid_line)

        # Fill grid with obstacles
        invalid_count = 0
        obstacles_count = 0

        while invalid_count < 10 and obstacles_count < 3:
            x = randint(1, self.x_length - 1)
            y = randint(1, self.y_length - 1)

            if grid[x][y] and grid[x][y].cell_state == AVAIABLE:
                obstacle = self.pool.get_obstacle()
                x = x - 1
                y = y - 1

                i = 0
                for line in obstacle:
                    j = 0
                    for element in line:
                        if 0 <= x + i < len(grid):
                            if 0 <= y + j < len(grid[x + i]):
                                if grid[x + i][y + j].cell_state != INVALID:
                                    grid[x + i][y + j].cell_state = element
                        j = j + 1
                    i = i + 1
            else:
                invalid_count = invalid_count + 1

        # Fill last line with blank
        for element in grid[-1]:
            element.cell_state = INVALID
        return grid

    def renew_grid(self):
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


# Class for each maze cell used to generate the maze
class MazeCell:
    def __init__(self):
        self.cell_state = AVAIABLE
