# Import Python libraries
import pygame
from pygame.locals import *
from random import randint

# Import local settings
from config import *

# Import classes
from entities.pool import Pool


# Class for Maze generation
class Maze:
    __instance = None
    def __init__(self, cell_size=0, x_length=0, y_length=0):
        self.colors_pool = [RED, GREEN, BLUE, YELLOW]
        self.cell_size = cell_size
        self.x_length = x_length
        self.y_length = y_length
        self.pool = Pool()
        self.colors = self.new_colors()
        self.inv_count = INVALID_COUNT
        self.obst_count = OBSTACLES_COUNT
        self.grid = self.new_grid()
        if Maze.__instance != None:
            raise Exception("This class must is a Singleton")
        else:
            Maze.__instance = self
    
    def restart_colors(self):
        self.colors_pool = [RED, GREEN, BLUE, YELLOW]
        self.colors = self.new_colors()
        
    def new_colors(self):
        random_c_1 = self.colors_pool.pop(randint(0, len(self.colors_pool) - 1))
        random_c_2 = self.colors_pool.pop(randint(0, len(self.colors_pool) - 1))
        return [random_c_1, random_c_2]

    def add_color(self):
        if len(self.colors_pool) != 0:
            self.colors.append(self.colors_pool.pop(randint(0, len(self.colors_pool) - 1)))

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

        while invalid_count < self.inv_count and obstacles_count < self.obst_count:
            x = randint(0, self.x_length - 1)
            y = randint(0, self.y_length - 1)

            if grid[x][y] and grid[x][y].state == AVAIABLE:
                obstacle = self.pool.get_obstacle()
                color = self.colors[randint(0, len(self.colors) - 1)]
                x = x - 1
                y = y - 1

                i = 0
                for line in obstacle:
                    j = 0
                    for element in line:
                        if 0 <= x + i < len(grid):
                            if 0 <= y + j < len(grid[x + i]):
                                if grid[x + i][y + j].state != INVALID:
                                    grid[x + i][y + j].state = element
                                    grid[x + i][y + j].color = color
                        j = j + 1
                    i = i + 1
            else:
                invalid_count = invalid_count + 1

        # Select correct sprites for each wall
        for i in range(0, self.y_length):
            for j in range(0, self.x_length):
                    if grid[i][j].state == WALL:
                        # TOP
                        if i - 1 >= 0:
                            if grid[i - 1][j].state == WALL:
                                grid[i][j].neighbors[0] = 'W'
                            else:
                                grid[i][j].neighbors[0] = 'X'

                        # RIGHT
                        if j + 1 <= self.x_length - 1:
                            if grid[i][j + 1].state == WALL:
                                grid[i][j].neighbors[1] = 'W'
                            else:
                                grid[i][j].neighbors[1] = 'X'

                        # BOTTOM
                        if i + 1 <= self.y_length - 1:
                            if grid[i + 1][j].state == WALL:
                                grid[i][j].neighbors[2] = 'W'
                            else:
                                grid[i][j].neighbors[2] = 'X'

                        # LEFT
                        if j - 1 >= 0:
                            if grid[i][j - 1].state == WALL:
                                grid[i][j].neighbors[3] = 'W'
                            else:
                                grid[i][j].neighbors[3] = 'X'

        # Fill last line with blank
        for element in grid[-1]:
            element.state = INVALID

        # # Colors rest of the grid
        # count = 0
        # color = colors[randint(0, len(colors) - 1)]
        # for line in grid:
        #     if count > COLOR_LINE_SIZE:
        #         color = colors[randint(0, len(colors) - 1)]
        #         count = 0
        #     for element in line:
        #         element.color = color
        #     count = count + 1

        # Return the grid
        return grid

    def empty_grid(self):
        # Empty and avaiable grid
        grid = []
        for i in range(self.y_length):
            grid_line = []
            for j in range(self.x_length):
                cell = MazeCell()
                grid_line.append(cell)
            grid.append(grid_line)
        return grid

    def renew_grid(self):
        self.grid = self.new_grid()

    def get_line(self):
        if self.grid:
            return self.grid.pop(0)
        else:
            self.grid = self.new_grid()
            return self.grid.pop(0)

    def get_grid(self):
        if self.grid:
            return self.grid
        else:
            self.grid = self.new_grid()
            return self.grid

    def get_empty_grid(self):
        self.grid = self.empty_grid()
        return self.grid

    def convert_to_full_grid(self, line):
        full_grid = []
        for i in range(self.cell_size):
            full_grid.append(line)
        return full_grid

    def pop_first_full_grid(self):
        temp_line = self.get_line()
        full_grid = []
        for i in range(self.cell_size):
            full_grid.append(temp_line)
        return full_grid


# Class for each maze cell used to generate the maze
class MazeCell:
    def __init__(self):
        self.state = AVAIABLE
        self.color = BLACK
        self.neighbors = ['X', 'X', 'X', 'X']  # W = WALL | X = NOT WALL | Order: Top, Right, Bottom, Left

    def get_color_string(self):
        if self.color == YELLOW:
            return 'yellow'
        elif self.color == RED:
            return 'red'
        elif self.color == GREEN:
            return 'green'
        elif self.color == BLUE:
            return 'blue'
        else:
            return ''
