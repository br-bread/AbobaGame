from core import BaseAnimatedSprite, BaseSprite
from overlay import Button
from tools import ImgEditor
import settings
import pygame
import sys


class Menu:

    def __init__(self):
        # sprite groups
        self.visible_sprites = pygame.sprite.Group()
        # general
        self.screen = pygame.display.get_surface()
        self.name = 'menu'
        self.music = pygame.mixer.Sound(f'..\\assets\\audio\\music\\menu.mp3')
        self.music_started = False
        # animation
        self.appearing = True  # if appearing animation should be shown
        self.disappearing = False  # same
        self.speed = 500  # speed of appearing/disappearing
        self.surface = pygame.Surface((settings.WIDTH, settings.HEIGHT))  # black surface
        self.surface.fill('black')
        self.alpha = 255
        self.next_scene = None  # will be set when current scene is disappearing
        # background
        BaseAnimatedSprite(ImgEditor.enhance_image(ImgEditor.load_image('menu/menu_animation.png'), 4), settings.CENTER,
                           3, 4, 4, settings.LAYERS['main'], self.visible_sprites)
        # buttons
        self.begin = Button(ImgEditor.enhance_image(ImgEditor.load_image('menu/begin.png'), 6), (300, 500),
                            self.visible_sprites)
        self.exit = Button(ImgEditor.enhance_image(ImgEditor.load_image('menu/exit.png'), 6), (300, 700),
                           self.visible_sprites)
        self.authors = Button(ImgEditor.enhance_image(ImgEditor.load_image('menu/authors.png'), 6), (300, 600),
                              self.visible_sprites)
        # authors view
        self.authors_background = BaseSprite(
            ImgEditor.enhance_image(ImgEditor.load_image('menu/authors_window.png'), 4),
            (1000, 1500), settings.LAYERS['main'], self.visible_sprites)
        self.back = Button(ImgEditor.enhance_image(ImgEditor.load_image('menu/back.png'), 4), (300, 1500),
                           self.visible_sprites)
        self.authors_list = [('Ксюша Цыканова', (675, 230)), ('Ксюша Цыканова', (675, 310)),
                             ('Ксюша Цыканова', (675, 390)),
                             ('Animal Crossing', (673, 470)), ('Ксюша Цыканова', (675, 550)),
                             ('Артём Суханов, Денис Криштопа', (590, 630))]
        self.font = pygame.font.Font(settings.FONT, 47)

    def disappear(self, next_scene, player_pos, player_status):
        if self.alpha < 255:  # disappear method can be called even when scene has disappeared
            self.disappearing = True  # so this parameter will be set wrong (without this if statement)
        # set player pos in next scene
        settings.player_pos = player_pos
        settings.player_status = player_status
        self.next_scene = next_scene

    def run(self, delta_time, events):
        if not self.music_started:
            self.music.play(loops=-1)
            self.music_started = True
        self.visible_sprites.draw(self.screen)
        if self.appearing:
            self.surface.set_alpha(self.alpha)
            self.screen.blit(self.surface, (0, 0))
            self.alpha -= self.speed * delta_time
            if self.alpha <= 0:
                self.appearing = False

        if self.disappearing:
            self.music.fadeout(1000)
            self.surface.set_alpha(self.alpha)
            self.screen.blit(self.surface, (0, 0))
            self.alpha += self.speed * delta_time
            if self.alpha >= 255:
                self.disappearing = False
                self.appearing = True  # set bool variables for next appearance of this scene
                self.music_started = False
                settings.scene = self.next_scene

        self.visible_sprites.update(delta_time, events)

        if not settings.window_opened:
            if self.begin.is_clicked:
                self.begin.change_image(ImgEditor.enhance_image(ImgEditor.load_image('menu/continue.png'), 6))
                self.disappear('first_street_scene', settings.CENTER, 'down_idle')
            if self.exit.is_clicked:
                pygame.quit()
                sys.exit()
            if self.authors.is_clicked:
                settings.window_opened = True
                self.authors_background.rect.center = settings.CENTER
                self.back.rect.center = (517, 200)
                self.begin.rect.center = (300, 1500)
                self.exit.rect.center = (300, 1700)
                self.authors.rect.center = (300, 1600)
        else:
            if self.back.is_clicked:
                settings.window_opened = False
                self.authors_background.rect.center = (400, 1500)
                self.back.rect.center = (150, 1260)
                self.begin.rect.center = (300, 500)
                self.exit.rect.center = (300, 700)
                self.authors.rect.center = (300, 600)

            for author in self.authors_list:
                self.screen.blit(self.font.render(author[0], False, settings.TEXT_COLOR),
                                 author[1])
