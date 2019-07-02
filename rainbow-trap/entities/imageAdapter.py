# Import Python libraries
import pygame


class ImageAdapter():
    def __init__(self, filename):
        self.image = pygame.image.load(filename).convert_alpha()

    def setOpacity(self, opacity):
        self.image.fill((255, 255, 255, opacity), None, pygame.BLEND_RGBA_MULT)

    def blit(self, screen, positionTuple):
        screen.blit(self.image, positionTuple)