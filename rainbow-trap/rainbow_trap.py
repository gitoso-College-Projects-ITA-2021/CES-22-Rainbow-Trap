#!/usr/bin/python
# -*- coding: utf-8 -*-

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
    flags = DOUBLEBUF  # (Enhance performance)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_LENGTH), flags)
    screen.set_alpha(None) # (Enhance performance)
    pygame.display.set_caption('Rainbow Trap')

    return screen

# Main game flow
def main(argv):
    ## Game initalization
    screen = initalize_display(argv)
    pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
    clock = pygame.time.Clock()
    kiko = Kiko(PLAYER_SIZE, RED)
    grid_x = SCREEN_WIDTH // FAT_X
    grid_y = SCREEN_LENGTH // FAT_Y
    maze = TempBlock(SCREEN_LENGTH // grid_x, grid_x, grid_y)
    grid = maze.empty_grid()
    first_grid_line = ''
    maze.renew_grid()
    continue_game = True

    ## Main loop
    while True:
        ## Sets FPS to 60
        clock.tick(60)

        ## Event handling
        for event in pygame.event.get():
            # Event: Quit Game
            if event.type == QUIT:
                pygame.quit()
            # Event: Key pressed
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    kiko.change_dir(LEFT)
                elif event.key == K_RIGHT:
                    kiko.change_dir(RIGHT)
                if event.key in [K_a, K_w, K_s, K_d]:
                    kiko.choose_color()
            # Event: Key rekeased
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

        ## Move the player
        kiko.moving()

        ## Update and move the maze

        # Clear the screen
        screen.fill((0, 0, 0))

        # Add kiko to the screen
        screen.blit(kiko.image, kiko.pos)

        # Renew top lines if needed
        if not first_grid_line:
            first_grid_line = maze.convert_to_full_grid(grid[0])
            grid.pop(0)
            grid.append(maze.get_line())

        # Draw top lines of the maze
        count_y = 0
        for line in first_grid_line:
            count_x = 0
            for cell in line:
                maze_skin = pygame.Surface((maze.cell_size, 1))
                maze_skin.fill(WHITE)
                if cell.cell_state == WALL:
                    screen.blit(maze_skin, (count_x, count_y))
                count_x = count_x + maze.cell_size
            count_y = count_y + 1
        
        # Draw the rest of the maze
        for line in grid:
            count_x = 0
            for cell in line:
                maze_skin = pygame.Surface((maze.cell_size, maze.cell_size))
                maze_skin.fill(WHITE)
                if cell.cell_state == WALL:
                    screen.blit(maze_skin, (count_x, count_y))
                count_x = count_x + maze.cell_size
            count_y = count_y + maze.cell_size

        # Move the labyrinth up (remove first lines and repeat loop)
        for i in range(MAZE_SPEED):
            if(first_grid_line):
                first_grid_line.pop(0)
        
        ## Update the display
        pygame.display.update()

# Calls main function if executed as a script
if __name__ == '__main__':
    main(sys.argv)
