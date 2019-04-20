# Import Python libraries
import pygame
from pygame.locals import *

# Import local settings
from config import *


# Class for Main Character
class Kiko:
    def __init__(self, size, color):
        self.color = color
        self.size = size
        self.skin = pygame.Surface((size, size))
        self.pos = (INITIAL_X, INITIAL_Y)
        self.move = STAY
        self.skin.fill(self.color)
        self.rect = pygame.Rect(self.pos, (self.size, self.size))

    def change_dir(self, dir):
        self.move = dir

    def moving(self):
        if self.move == RIGHT:
            if (self.pos[0]+2*self.size <= SCREEN_SIZE):
                self.pos = (self.pos[0] + KIKO_SPEED, INITIAL_Y)
        if self.move == LEFT:
            if (self.pos[0]-self.size >= 0):
                self.pos = (self.pos[0] - KIKO_SPEED, INITIAL_Y)
        self.rect = pygame.Rect(self.pos, (self.size, self.size))

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

    def get_corners(self):
        return [self.pos, (self.pos[0] + self.size, self.pos[1]), (self.pos[0], self.pos[1] + self.size), (self.pos[0] + self.size, self.pos[1] + self.size)]