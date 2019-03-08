import pygame
from pygame.locals import *
from background import Background


class Game:
    screen = None
    screen_size = None
    run = True
    background = None

    def __init__(self, size, fullscreen):
        """
        Esta é a função que inicializa o pygame, define a resolução da tela,
        caption, e disabilitamos o mouse dentro desta.
        """
        actors = {}
        pygame.init()
        flags = DOUBLEBUF
        if fullscreen:
            flags |= FULLSCREEN
        self.screen = pygame.display.set_mode(size, flags)
        self.screen_size = self.screen.get_size()

        pygame.mouse.set_visible(0)
        pygame.display.set_caption('Título da Janela')
    # init()

    def handle_events(self):
        """
        Trata o evento e toma a ação necessária.
        """
        for event in pygame.event.get():
            t = event.type
            if t in (KEYDOWN, KEYUP):
                k = event.key

            if t == QUIT:
                self.run = False

            elif t == KEYDOWN:
                if k == K_ESCAPE:
                    self.run = False
    # handle_events()

    def actors_update(self, dt):
        self.background.update(dt)
    # actors_update()

    def actors_draw(self):
        self.background.draw(self.screen)
    # actors_draw()

    def loop(self):
        """
        Laço principal
        """
        # Criamos o fundo
        self.background = Background()

        # Inicializamos o relogio e o dt que vai limitar o valor de
        # frames por segundo do jogo
        clock = pygame.time.Clock()
        dt = 16

        # assim iniciamos o loop principal do programa
        while self.run:
            clock.tick(1000 / dt)

            # Handle Input Events
            self.handle_events()

            # Atualiza Elementos
            self.actors_update(dt)

            # Desenhe para o back buffer
            self.actors_draw()

            # ao fim do desenho temos que trocar o front buffer e o back buffer
            pygame.display.flip()

            print("FPS: %0.2f" % clock.get_fps())
        # while self.run
    # loop()
# Game
