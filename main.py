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
    pygame.display.set_caption('Rainbow Trap')
    pygame.display.set_mode((1024, 720))


# Main game flow
def main(argv):
    initalize_display(argv)

    while True:
        # If user closes the window, quit the game
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

        # Update the display
        pygame.display.update()

# Calls main function if executed as a script
if __name__ == '__main__':
    main(sys.argv)
