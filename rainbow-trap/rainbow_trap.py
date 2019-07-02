#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import Python libraries
import pygame
import os
import sys
import random
from pygame.locals import *

# Import local settings
from config import *

# Import classes
from entities.kiko import Kiko
from entities.maze import *
from entities.controller import Controller
from entities.imageAdapter import ImageAdapter


# Initialize game display
def initalize_display(argv):
    pygame.init()
    flags = DOUBLEBUF  # (Enhance performance)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH), flags)
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
        PS = myfont2.render('Press ENTER or START to play', False, WHITE)
        BS = myfont3.render('Best score '+str(best_score), False, WHITE)
        screen.blit(RT, (200, SCREEN_HEIGTH // 2 - 100))
        screen.blit(PS, (200, SCREEN_HEIGTH // 2 + 100))
        screen.blit(BS, (200, SCREEN_HEIGTH // 2 + 200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    intro = False
            if event.type == JOYBUTTONDOWN:
                if event.button == B_START:
                    intro = False


def paused(screen):
    pause = True

    while pause:

        myfont = pygame.font.SysFont('', 150)
        PAUSE = myfont.render('Paused', False, WHITE)
        screen.blit(PAUSE, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGTH // 2 - 75))
        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    pause = False
            if event.type == JOYBUTTONDOWN:
                if event.button == B_START:
                    pause = False


def difficulty_update(score, maze):

    level = score // SCORE_LEVEL

    if(level == 2):
        if(len(maze.colors) == 2):
            maze.add_color()

    if(level == 4):
        if(len(maze.colors) == 3):
            maze.add_color()

    maze.inv_count = INVALID_COUNT*level*5 + INVALID_COUNT
    if(maze.inv_count > COUNT_MAX):
        maze.inv_count = COUNT_MAX

    maze.obst_count = OBSTACLES_COUNT*level*5 + OBSTACLES_COUNT
    if(maze.obst_count > COUNT_MAX):
        maze.obst_count = COUNT_MAX


# Main game flow
def main(argv):
    score = 0
    best_score = score

    while True:
        # Game initalization
        screen = initalize_display(argv)
        pygame.joystick.init()
        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP, JOYBUTTONDOWN, JOYBUTTONUP, JOYHATMOTION])
        clock = pygame.time.Clock()
        kiko = Kiko(PLAYER_SIZE, RED)
        grid_x = SCREEN_WIDTH // SCALE_FACTOR
        grid_y = SCREEN_WIDTH // SCALE_FACTOR
        maze = Maze(SCREEN_WIDTH // grid_x, grid_x, grid_y)
        grid = maze.empty_grid()
        first_grid_line = ''
        maze.renew_grid()
        speed = MAZE_SPEED
        continue_game = True

        # Restart Maze Colors
        maze.restart_colors()

        # Start Joystick
        joystick_count = pygame.joystick.get_count()

        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()

        # Load Music
        playlist = []
        playlist.append('music/cake.mp3')
        playlist.append('music/darude.mp3')
        playlist.append('music/eminem.mp3')
        playlist.append('music/feelgood.mp3')
        playlist.append('music/fox.mp3')
        playlist.append('music/mchammer.mp3')

        # Shuffle the playlist
        random.shuffle(playlist)

        # Plays the music
        pygame.mixer.init()
        pygame.mixer.music.load(playlist.pop())
        for song in playlist:
            pygame.mixer.music.queue(song)
        pygame.mixer.music.play()

        # Runs the intro
        game_intro(screen, best_score)
        score = 0
        difficulty_update(score, maze)
        game = True

        # Main loop
        while game:
            # Sets FPS to 60
            clock.tick(60)

            # Update difficulty
            difficulty_update(score, maze)
            level = score // SCORE_LEVEL
            speed = MAZE_SPEED + level - len(maze.colors) + 2
            if(speed > MAX_MAZE_SPEED):
                speed = MAX_MAZE_SPEED

            # Score iterating
            score = score + 1
            level = score // SCORE_LEVEL
            myfont1 = pygame.font.SysFont('', 50)
            SCORE = myfont1.render('Score '+str(score), True, WHITE)
            LEVEL = myfont1.render('Level '+str(level), True, WHITE)

            print(speed)

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
                    elif event.key == pygame.K_p:
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
                # Event: Button pressed (Controller)
                if event.type == JOYHATMOTION:
                    if event.value[0] == -1:
                        kiko.change_dir(LEFT)
                    elif event.value[0] == 1:
                        kiko.change_dir(RIGHT)
                    else:
                        kiko.change_dir(STAY)
                if event.type == JOYBUTTONDOWN:
                    if event.button in [0, 1, 2, 3]:
                        kiko.choose_color()
                    elif event.button == B_START:
                            paused(screen)

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
                    if cell.state == WALL:
                        image_name = 'images/' + ''.join(cell.neighbors) + '_' + cell.get_color_string() + '.png'
                        if os.path.isfile(image_name):
                            image = ImageAdapter(image_name)
                        if cell.color != kiko.color:
                            walls.append(pygame.Rect(((count_x, count_y)), (maze.cell_size, maze.cell_size)))
                        else:
                            image.setOpacity(WALL_OPACITY)
                        image.blit(screen, (count_x, count_y))
                    count_x = count_x + maze.cell_size
                count_y = count_y + maze.cell_size

            # Move the labyrinth up (remove first lines and repeat loop)
            for i in range(speed):
                if first_grid_line:
                    first_grid_line.pop(0)

            # Add kiko to the screen
            screen.blit(kiko.skin, kiko.pos)

            # Print the Score
            screen.blit(SCORE, (0, 0))
            screen.blit(LEVEL, (300, 0))

            # Print the HUD
            # wasd_hud = pygame.image.load('images/wasd_hud.png').convert_alpha()
            # wasd_hud.fill((255, 255, 255, 190), None, pygame.BLEND_RGBA_MULT)
            # screen.blit(wasd_hud, (0, 20))
            wasd_hud = ImageAdapter('images/wasd_hud.png')
            wasd_hud.setOpacity(190)
            wasd_hud.blit(screen, (0, 20))

            # xbox_hud = pygame.image.load('images/xbox_hud.png').convert_alpha()
            # xbox_hud.fill((255, 255, 255, 190), None, pygame.BLEND_RGBA_MULT)
            # screen.blit(xbox_hud, (SCREEN_WIDTH - 100, 20))
            xbox_hud = ImageAdapter('images/xbox_hud.png')
            xbox_hud.setOpacity(190)
            xbox_hud.blit(screen, (SCREEN_WIDTH - 100, 20))

            # Update the display
            pygame.display.update()

            # Check if kiko did collide with maze walls
            for wall in walls:
                if kiko.rect.colliderect(wall):
                    if score >= best_score:
                        best_score = score
                    game = False

# Calls main function if executed as a script
if __name__ == '__main__':
    main(sys.argv)
