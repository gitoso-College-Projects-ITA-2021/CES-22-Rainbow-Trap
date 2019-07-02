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


class Joystick():
    def __init__(self):
        pass
    
    def start(self):
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()

        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()


class Screen():
    def __init__(self):
        pass
    
    def start_screen(self, argv):
        screen = initalize_display(argv)

        return screen

    def start_maze(self):
        
        self.config()
        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP, JOYBUTTONDOWN, JOYBUTTONUP, JOYHATMOTION])
        kiko = Kiko(PLAYER_SIZE, RED)
        grid_x = SCREEN_WIDTH // SCALE_FACTOR
        grid_y = SCREEN_WIDTH // SCALE_FACTOR
        maze = Maze(SCREEN_WIDTH // grid_x, grid_x, grid_y)
        grid = maze.empty_grid()
        first_grid_line = ''
        maze.renew_grid()
        maze.restart_colors()

        return maze
    
    def config(self):
        clock = pygame.time.Clock()
        speed = MAZE_SPEED
        continue_game = True
        

class Music():
    def __init(self):
        pass
    
    def play(self):
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


class EventManager():
    def __init__(self):
        pass
    
    def setGameUp(self, maze, argv, scr):

        # Inicializes screen and its objects
        self.screen = Screen()
        scr = self.screen.start_screen(argv=argv)
        maze = self.screen.start_maze()

        # Sets the joystick up
        self.joystick = Joystick()
        self.joystick.start()

        # Loads and plays the game music
        self.music = Music()
        self.music.play()


class Game():
    def __init__(self, argv):
        self.screen = None
        self.maze = Maze()
        self.argv = argv
    
    def askEventManager(self):
        em = EventManager()
        em.setGameUp(maze=self.maze, argv=self.argv, scr=self.screen)


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
        # screen = initalize_display(argv)
        # pygame.joystick.init()
        # pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP, JOYBUTTONDOWN, JOYBUTTONUP, JOYHATMOTION])
        # clock = pygame.time.Clock()
        # kiko = Kiko(PLAYER_SIZE, RED)
        # grid_x = SCREEN_WIDTH // SCALE_FACTOR
        # grid_y = SCREEN_WIDTH // SCALE_FACTOR
        # maze = Maze(SCREEN_WIDTH // grid_x, grid_x, grid_y)
        # grid = maze.empty_grid()
        # first_grid_line = ''
        # maze.renew_grid()
        # speed = MAZE_SPEED
        # continue_game = True

        # # Restart Maze Colors
        # maze.restart_colors()

        # # Start Joystick
        # joystick_count = pygame.joystick.get_count()

        # for i in range(joystick_count):
        #     joystick = pygame.joystick.Joystick(i)
        #     joystick.init()

        # # Load Music
        # playlist = []
        # playlist.append('music/cake.mp3')
        # playlist.append('music/darude.mp3')
        # playlist.append('music/eminem.mp3')
        # playlist.append('music/feelgood.mp3')
        # playlist.append('music/fox.mp3')
        # playlist.append('music/mchammer.mp3')

        # # Shuffle the playlist
        # random.shuffle(playlist)

        # # Plays the music
        # pygame.mixer.init()
        # pygame.mixer.music.load(playlist.pop())
        # for song in playlist:
        #     pygame.mixer.music.queue(song)
        # pygame.mixer.music.play()

        g = Game(argv)
        g.askEventManager()

        # Runs the intro
        game_intro(g.screen, best_score)
        score = 0
        difficulty_update(score, g.maze)
        game_on = True

        # Main loop
        while game_on:
            # Sets FPS to 60
            clock.tick(60)

            # Update difficulty
            difficulty_update(score, g.maze)
            level = score // SCORE_LEVEL
            speed = MAZE_SPEED + level - len(g.maze.colors) + 2
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
                        paused(g.screen)

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
                            paused(g.screen)

            # Move the player
            kiko.moving()

            # Update and move the maze

            # Clear the screen
            g.screen.fill(BLACK)

            # Renew top lines if needed
            if not first_grid_line:
                first_grid_line = g.maze.convert_to_full_grid(grid[0])
                grid.pop(0)
                grid.append(g.maze.get_line())

            # Draw top lines of the maze (out of screen)
            count_y = -g.maze.cell_size
            for line in first_grid_line:
                count_x = 0
                for cell in line:
                    maze_skin = pygame.Surface((g.maze.cell_size, 1))
                    maze_skin.fill(RED)
                    if cell.state == WALL:
                        g.screen.blit(g.maze, (count_x, count_y))
                    count_x = count_x + g.maze.cell_size
                count_y = count_y + 1

            # Array that saves maze walls (for collision purposes)
            walls = []

            # Draw the rest of the maze (now count_y = 0)
            for line in grid:
                count_x = 0
                for cell in line:
                    maze_skin = pygame.Surface((g.maze.cell_size, g.maze.cell_size))
                    maze_skin.fill(cell.color)
                    if cell.state == WALL:
                        image_name = 'images/' + ''.join(cell.neighbors) + '_' + cell.get_color_string() + '.png'
                        if os.path.isfile(image_name):
                            image = pygame.image.load(image_name).convert_alpha()
                        else:
                            # Dummy image for things that are not done
                            image = pygame.image.load('images/4.png').convert_alpha()

                        if cell.color != kiko.color:
                            walls.append(pygame.Rect(((count_x, count_y)), (g.maze.cell_size, g.maze.cell_size)))
                        else:
                            image.fill((255, 255, 255, WALL_OPACITY), None, pygame.BLEND_RGBA_MULT)
                        g.screen.blit(image, (count_x, count_y))
                    count_x = count_x + g.maze.cell_size
                count_y = count_y + g.maze.cell_size

            # Move the labyrinth up (remove first lines and repeat loop)
            for i in range(speed):
                if first_grid_line:
                    first_grid_line.pop(0)

            # Add kiko to the screen
            g.screen.blit(kiko.skin, kiko.pos)

            # Print the Score
            g.screen.blit(SCORE, (0, 0))
            g.screen.blit(LEVEL, (300, 0))

            # Print the HUD
            wasd_hud = pygame.image.load('images/wasd_hud.png').convert_alpha()
            wasd_hud.fill((255, 255, 255, 190), None, pygame.BLEND_RGBA_MULT)
            g.screen.blit(wasd_hud, (0, 20))
            xbox_hud = pygame.image.load('images/xbox_hud.png').convert_alpha()
            xbox_hud.fill((255, 255, 255, 190), None, pygame.BLEND_RGBA_MULT)
            g.screen.blit(xbox_hud, (SCREEN_WIDTH - 100, 20))

            # Update the display
            pygame.display.update()

            # Check if kiko did collide with maze walls
            for wall in walls:
                if kiko.rect.colliderect(wall):
                    if score >= best_score:
                        best_score = score
                    game_on = False

# Calls main function if executed as a script
if __name__ == '__main__':
    main(sys.argv)