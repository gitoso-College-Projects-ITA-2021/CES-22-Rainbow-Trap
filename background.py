import pygame


class Background:
    """
    Esta classe representa o ator "Fundo" do jogo.
    """
    image = None

    def __init__(self):
        screen = pygame.display.get_surface()
        back = pygame.Surface(screen.get_size()).convert()
        back.fill((0, 0, 0))
        self.image = back
    # __init__()

    def update(self, dt):
        pass  # Ainda não faz nada
    # update()

    def draw(self, screen):
        screen.blit(self.image, (0, 0))
    # draw()
# Background
