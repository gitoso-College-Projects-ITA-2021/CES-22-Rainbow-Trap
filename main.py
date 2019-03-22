#!/usr/bin/python
# -*- coding: utf-8 -*-

# === Fazer um cabeçalho bonito aqui ===

# Import Python libraries
import pygame
import os
import sys
from pygame.locals import *


# Initialize game display
def initalize_display(argv):
    pygame.init()
    screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption('Rainbow Trap')

    return screen


# Class for Maze generation
class Maze:
    def __init__():
        print('')


# Class for Temporary grid used to generate maze before showing in the screen
class TempBlock:
    def __init__():
        print('')


# Class for each maze cell used to generate the maze
class MazeCell:
    def __init__():
        print('')


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
        self.pos = (495, 50)
        self.move = STAY
        self.skin.fill(self.color)

    def change_dir(self, dir):
        self.move = dir

    def moving(self):
        if self.move == RIGHT:
            if (self.pos[0]+2*self.size <= 1000):
                self.pos = (self.pos[0]+self.size, 50)
        if self.move == LEFT:
            if (self.pos[0]-self.size >= 0):
                self.pos = (self.pos[0]-self.size, 50)

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

    clock = pygame.time.Clock()
    kiko = Kiko(10, RED)

    while True:
        clock.tick(50)
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

        # Update the display
        pygame.display.update()

# Calls main function if executed as a script
if __name__ == '__main__':
    main(sys.argv)
