from core import BaseAnimatedSprite
from tools import ImgEditor
import settings
import pygame


class Menu:

    def __init__(self):
        # sprite groups
        self.visible_sprites = pygame.sprite.Group()
        # general
        self.screen = pygame.display.get_surface()
        self.name = 'menu'
        # animation
        self.appearing = True  # if appearing animation should be shown
        self.disappearing = False  # same
        self.speed = 500  # speed of appearing/disappearing
        self.surface = pygame.Surface((settings.WIDTH, settings.HEIGHT))
        self.surface.fill('black')
        self.alpha = 255
        self.next_scene = None  # will be set when current scene is disappearing
        # background
        BaseAnimatedSprite(ImgEditor.enhance_image(ImgEditor.load_image('menu/menu_animation.png'), 4), settings.CENTER,
                           3, 4, 4, settings.LAYERS['main'], self.visible_sprites)

    def disappear(self, next_scene, player_pos, player_status):
        if self.alpha < 255:  # disappear method can be called even when scene has disappeared
            self.disappearing = True  # so this parameter will be set wrong (without this if statement)
        # set player pos in next scene
        settings.player_pos = player_pos
        settings.player_status = player_status
        self.next_scene = next_scene

    def run(self, delta_time, events):
        self.visible_sprites.draw(self.screen)
        if self.appearing:
            self.surface.set_alpha(self.alpha)
            self.screen.blit(self.surface, (0, 0))
            self.alpha -= self.speed * delta_time
            if self.alpha <= 0:
                self.appearing = False

        if self.disappearing:
            self.surface.set_alpha(self.alpha)
            self.screen.blit(self.surface, (0, 0))
            self.alpha += self.speed * delta_time
            if self.alpha >= 255:
                self.disappearing = False
                self.appearing = True  # set bool variables for next appearance of this scene
                settings.scene = self.next_scene

        self.visible_sprites.update(delta_time)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.disappear('first_street_scene', settings.CENTER, 'down_idle')
