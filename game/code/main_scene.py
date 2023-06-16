import pygame
from settings import *
from player import Player


# main_scene contains all objects, events and interactions,
# which will be always displayed (except main menu scene)
class MainScene:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.visible_sprites = pygame.sprite.Group()
        self.player = Player(CENTER, self.visible_sprites)

    def run(self, delta_time):
        self.visible_sprites.draw(self.screen)
        self.visible_sprites.update(delta_time)
