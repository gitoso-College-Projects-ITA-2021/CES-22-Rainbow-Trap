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
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE), flags)
    screen.set_alpha(None)  # (Enhance performance)
    pygame.display.set_caption('Rainbow Trap')

    return screen


# Main game flow
def main(argv):
    # Game initalization
    pygame.init()
    screen = initalize_display(argv)
    pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
    clock = pygame.time.Clock()
    kiko = Kiko(PLAYER_SIZE, RED)
    grid_x = SCREEN_SIZE // SCALE_FACTOR
    grid_y = SCREEN_SIZE // SCALE_FACTOR
    maze = Maze(SCREEN_SIZE // grid_x, grid_x, grid_y)
    grid = maze.empty_grid()
    first_grid_line = ''
    maze.renew_grid()
    continue_game = True

    # Main loop
    while True:
        # Sets FPS to 60
        clock.tick(60)

        # Event handling
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

        # Move the player
        kiko.moving()

        # Update and move the maze

        # Clear the screen
        screen.fill(BLACK)

        # Renew top lines if needed
        if not first_grid_line:
            first_grid_line = maze.convert_to_full_grid(grid[0])
            grid.pop(0)
            grid.append(maze.get_line())

        # Draw top lines of the maze (out of screen)
        count_y = -maze.cell_size
        for line in first_grid_line:
            count_x = 0
            for cell in line:
                maze_skin = pygame.Surface((maze.cell_size, 1))
                maze_skin.fill(RED)
                if cell.state == WALL:
                    screen.blit(maze_skin, (count_x, count_y))
                count_x = count_x + maze.cell_size
            count_y = count_y + 1

        # Array that saves maze walls (for collision purposes)
        walls = []

        # Draw the rest of the maze (now count_y = 0)
        for line in grid:
            count_x = 0
            for cell in line:
                maze_skin = pygame.Surface((maze.cell_size, maze.cell_size))
                maze_skin.fill(cell.color)
                # # Fill maze with color
                # if cell.color == kiko.color:
                #     walls.append(pygame.Rect(((count_x, count_y)), (maze.cell_size, maze.cell_size)))
                #     maze_skin.set_alpha(255)
                # else:
                #     maze_skin.set_alpha(50)
                # screen.blit(maze_skin, (count_x, count_y))
                # If maze wall fill with sprite
                if cell.state == WALL:
                    image_name = 'images/' + ''.join(cell.neighbors) + '_' + cell.get_color_string() + '.png'
                    if os.path.isfile(image_name):
                        image = pygame.image.load(image_name).convert_alpha()
                    else:
                        # Dummy image for things that are not done
                        image = pygame.image.load('images/4.png').convert_alpha()

                    if cell.color != kiko.color:
                        walls.append(pygame.Rect(((count_x, count_y)), (maze.cell_size, maze.cell_size)))
                    else:
                        image.fill((255, 255, 255, WALL_OPACITY), None, pygame.BLEND_RGBA_MULT)
                    screen.blit(image, (count_x, count_y))
                count_x = count_x + maze.cell_size
            count_y = count_y + maze.cell_size

        # Move the labyrinth up (remove first lines and repeat loop)
        for i in range(MAZE_SPEED):
            if first_grid_line:
                first_grid_line.pop(0)

        # Add kiko to the screen
        screen.blit(kiko.skin, kiko.pos)

        # Update the display
        pygame.display.update()

        # Check if kiko did collide with maze walls
        for wall in walls:
            if kiko.rect.colliderect(wall):
                pygame.quit()


# Calls main function if executed as a script
if __name__ == '__main__':
    main(sys.argv)
