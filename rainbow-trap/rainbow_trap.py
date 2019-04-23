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


def game_intro(screen, best_score):

    intro = True

    while intro:

        myfont = pygame.font.SysFont('', 100)
        myfont2 = pygame.font.SysFont('', 50)
        myfont3 = pygame.font.SysFont('', 50)
        RT = myfont.render('Rainbow Trap', False, WHITE)
        PS = myfont2.render('Press ENTER to play', False, WHITE)
        BS = myfont3.render('Best score '+str(best_score), False, WHITE)
        screen.blit(RT, (200, SCREEN_SIZE // 2 - 100))
        screen.blit(PS, (200, SCREEN_SIZE // 2 + 100))
        screen.blit(BS, (200, SCREEN_SIZE // 2 + 200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    intro = False


def paused(screen):
    pause = True

    while pause:

        myfont = pygame.font.SysFont('', 150)
        PAUSE = myfont.render('Paused', False, WHITE)
        screen.blit(PAUSE, (SCREEN_SIZE // 2 - 200, SCREEN_SIZE // 2 - 75))
        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    pause = False


def difficulty_update(score, maze, speed):
    # Add color
    if((score // SCORE_LEVEL) == 2 and len(maze.colors) == 2):
        maze.add_color()
    if((score // SCORE_LEVEL) == 4 and len(maze.colors) == 3):
        maze.add_color()
    
    # Change speed
    if((score // SCORE_LEVEL) == 1 and speed == MAZE_SPEED):
        speed = speed + 1
    if((score // SCORE_LEVEL) == 3 and speed == MAZE_SPEED + 1):
        speed = speed + 1
    if((score // SCORE_LEVEL) == 5 and speed == MAZE_SPEED + 2):
        speed = speed + 1
    if((score // SCORE_LEVEL) == 6 and speed == MAZE_SPEED + 3):
        speed = speed + 1


# Main game flow
def main(argv):

    score = 0
    best_score = score

    while True:
        # Game initalization
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
        speed = MAZE_SPEED
        continue_game = True

        # Runs the intro
        game_intro(screen, best_score)
        score = 0
        difficulty_update(score, maze, speed)
        game = True

        # Main loop
        while game:
            # Sets FPS to 60
            clock.tick(60)

            # Update difficulty
            difficulty_update(score, maze, speed)

            # Score iterating
            score = score + 1
            myfont1 = pygame.font.SysFont('', 50)
            SCORE = myfont1.render('Score '+str(score), True, WHITE)

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
                    elif event.key in [K_a, K_w, K_s, K_d]:
                        kiko.choose_color()
                    if event.key == pygame.K_p:
                        paused(screen)

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
            for i in range(speed):
                if first_grid_line:
                    first_grid_line.pop(0)

            # Add kiko to the screen
            screen.blit(kiko.skin, kiko.pos)

            screen.blit(SCORE, (0, 0))

            # Update the display
            pygame.display.update()

            # Check if kiko did collide with maze walls
            for wall in walls:
                if kiko.rect.colliderect(wall):
                    best_score = score
                    game = False


# Calls main function if executed as a script
if __name__ == '__main__':
    main(sys.argv)
