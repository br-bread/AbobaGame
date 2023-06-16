import pygame
from settings import *
from player import Player


# main_level contains all objects, events and interactions,
# which will be always displayed (except main menu scene)
class MainScene:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()
        self.player = Player((300, 300), self.all_sprites)

    def run(self, delta_time):
        self.all_sprites.draw(self.screen)
        self.all_sprites.update(delta_time)
