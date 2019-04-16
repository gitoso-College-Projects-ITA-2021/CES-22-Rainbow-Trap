# Import Python libraries
import pygame
from pygame.locals import *

# Import local settings
from config import *


# Class for Main Character
class Kiko(pygame.sprite.Sprite):
    def __init__(self, size, color):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.size = size
        self.pos = (INITIAL_X, INITIAL_Y)
        self.move = STAY
        self.image = pygame.image.load("images/red.png")
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def change_dir(self, dir):
        self.move = dir

    def moving(self):
        if self.move == RIGHT:
            if (self.pos[0]+2*self.size <= SCREEN_WIDTH):
                self.pos = (self.pos[0]+self.size, INITIAL_Y)
        if self.move == LEFT:
            if (self.pos[0]-self.size >= 0):
                self.pos = (self.pos[0]-self.size, INITIAL_Y)

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
        if self.color == RED:
            self.image = pygame.image.load("images/red.png")
            self.rect = self.image.get_rect() 
            self.mask = pygame.mask.from_surface(self.image)
        elif self.color == GREEN:
            self.image = pygame.image.load("images/green.png")
            self.rect = self.image.get_rect() 
            self.mask = pygame.mask.from_surface(self.image)
        elif self.color == YELLOW:
            self.image = pygame.image.load("images/yellow.png")
            self.rect = self.image.get_rect() 
            self.mask = pygame.mask.from_surface(self.image)
        elif self.color == BLUE:
            self.image = pygame.image.load("images/blue.png")
            self.rect = self.image.get_rect() 
            self.mask = pygame.mask.from_surface(self.image)
        elif self.color == INDIGO:
            self.image = pygame.image.load("images/indigo.png")
            self.rect = self.image.get_rect() 
            self.mask = pygame.mask.from_surface(self.image)
        elif self.color == VIOLET:
            self.image = pygame.image.load("images/violet.png")
            self.rect = self.image.get_rect() 
            self.mask = pygame.mask.from_surface(self.image)
        elif self.color == ORANGE:
            self.image = pygame.image.load("images/orange.png")
            self.rect = self.image.get_rect() 
            self.mask = pygame.mask.from_surface(self.image)
        else:
            self.image = pygame.image.load("images/white.png")
            self.rect = self.image.get_rect() 
            self.mask = pygame.mask.from_surface(self.image)