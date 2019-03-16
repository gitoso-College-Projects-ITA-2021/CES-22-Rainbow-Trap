#!/usr/bin/python
# -*- coding: utf-8 -*-

# === Fazer um cabeçalho bonito aqui ===

# Import Python libraries
import pygame
import os
import sys
from pygame.locals import *

# Define colors
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,225)
YELLOW = (255,255,0)

# Define directions
STAY = 0
RIGHT = 1
LEFT = 2

# Initialize game display
def initalize_display(argv):
    pygame.init()
    screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption('Rainbow Trap')
    return screen

# Class for Main Character
class Kiko:
    def __init__(self,size,color):
        self.color = color
        self.size = size
        self.skin = pygame.Surface((size,size))
        self.pos = (495,50)
        self.move = STAY
        self.skin.fill(self.color)

    def change_dir(self,dir):
        self.move = dir

    def moving(self):
        if self.move == RIGHT:
            if (self.pos[0]+2*self.size <= 1000):
                self.pos = (self.pos[0]+self.size,50)
        if self.move == LEFT:
            if (self.pos[0]-self.size >= 0):
                self.pos = (self.pos[0]-self.size,50)
    
    def change_color(self,color):
        self.color = color
        self.skin.fill(self.color)

# Main game flow
def main(argv):
    screen = initalize_display(argv)

    clock = pygame.time.Clock()
    kiko = Kiko(10,RED)

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
                if event.key == K_a:
                    kiko.change_color(RED)
                if event.key == K_s:
                    kiko.change_color(GREEN)
                if event.key == K_d:
                    kiko.change_color(BLUE)
                if event.key == K_w:
                    kiko.change_color(YELLOW)
            if event.type == KEYUP:
                if event.key in [K_RIGHT,K_LEFT]:
                    kiko.change_dir(STAY)

        kiko.moving()

        screen.fill((0,0,0))
        screen.blit(kiko.skin,kiko.pos)

        # Update the display
        pygame.display.update()

# Calls main function if executed as a script
if __name__ == '__main__':
    main(sys.argv)
