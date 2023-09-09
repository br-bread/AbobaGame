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
        BaseAnimatedSprite(ImgEditor.load_image('menu/menu_animation.png', settings.SCALE_K), settings.CENTER,
                           3, 4, 4, settings.LAYERS['main'], self.visible_sprites)
        # buttons
        self.begin = Button(ImgEditor.load_image('menu/begin.png', settings.BIGGER_SCALE),
                            (75 * settings.SCALE_K, 125 * settings.SCALE_K),
                            self.visible_sprites)
        self.exit = Button(ImgEditor.load_image('menu/exit.png', settings.BIGGER_SCALE),
                           (75 * settings.SCALE_K, 175 * settings.SCALE_K),
                           self.visible_sprites)
        self.authors = Button(ImgEditor.load_image('menu/authors.png', settings.BIGGER_SCALE),
                              (75 * settings.SCALE_K, 150 * settings.SCALE_K),
                              self.visible_sprites)
        # authors view
        self.authors_is_opened = False
        self.authors_background = BaseSprite(ImgEditor.load_image('menu/authors_window.png', settings.SCALE_K),
                                             (250 * settings.SCALE_K, 375 * settings.SCALE_K), settings.LAYERS['main'],
                                             self.visible_sprites)
        self.back = Button(ImgEditor.load_image('menu/back.png', settings.SCALE_K),
                           (75 * settings.SCALE_K, 375 * settings.SCALE_K),
                           self.visible_sprites)
        self.authors_list = [('Ксюша Цыканова', (169 * settings.SCALE_K, 58 * settings.SCALE_K)),
                             ('Ксюша Цыканова', (169 * settings.SCALE_K, 78 * settings.SCALE_K)),
                             ('Ксюша Цыканова', (169 * settings.SCALE_K, 98 * settings.SCALE_K)),
                             ('Animal Crossing', (168 * settings.SCALE_K, 118 * settings.SCALE_K)),
                             ('Ксюша Цыканова', (169 * settings.SCALE_K, 138 * settings.SCALE_K)),
                             ('Артём Суханов, Денис Криштопа', (148 * settings.SCALE_K, 158 * settings.SCALE_K))]
        self.font = pygame.font.Font(settings.FONT, 11 * settings.SCALE_K)
        # character choice view
        self.character_choice = CharacterChoice()

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
        self.character_choice.run(self.screen, delta_time, events, self)

        if not settings.window_opened:
            if self.begin.is_clicked:
                self.begin.change_image(ImgEditor.load_image('menu/continue.png', settings.BIGGER_SCALE))
                self.character_choice.is_opened = True
            if self.exit.is_clicked:
                pygame.quit()
                sys.exit()
            if self.authors.is_clicked:
                settings.window_opened = True
                self.authors_is_opened = True
                self.authors_background.rect.center = settings.CENTER
                self.back.rect.center = (129 * settings.SCALE_K, 50 * settings.SCALE_K)
                self.begin.rect.center = (75 * settings.SCALE_K, 375 * settings.SCALE_K)
                self.exit.rect.center = (75 * settings.SCALE_K, 375 * settings.SCALE_K)
                self.authors.rect.center = (75 * settings.SCALE_K, 375 * settings.SCALE_K)
        elif self.authors_is_opened:
            if self.back.is_clicked:
                settings.window_opened = False
                self.authors_background.rect.center = (250 * settings.SCALE_K, 375 * settings.SCALE_K)
                self.back.rect.center = (75 * settings.SCALE_K, 375 * settings.SCALE_K)
                self.begin.rect.center = (75 * settings.SCALE_K, 125 * settings.SCALE_K)
                self.exit.rect.center = (75 * settings.SCALE_K, 175 * settings.SCALE_K)
                self.authors.rect.center = (75 * settings.SCALE_K, 150 * settings.SCALE_K)

            for author in self.authors_list:
                self.screen.blit(self.font.render(author[0], False, settings.TEXT_COLOR),
                                 author[1])


class CharacterChoice:
    def __init__(self):
        self.is_opened = False
        self.background = ImgEditor.load_image('menu/character_window.png', settings.SCALE_K, colorkey=-1)
        self.group = pygame.sprite.Group()

        # characters
        self.denis = BaseAnimatedSprite(ImgEditor.load_image('menu/denis_animation.png', settings.SCALE_K), (670, 450),
                                        5, 4, 1, settings.LAYERS['main'],
                                        self.group)
        self.artem = BaseAnimatedSprite(ImgEditor.load_image('menu/artem_animation.png', settings.SCALE_K), (850, 450),
                                        5, 4, 1, settings.LAYERS['main'],
                                        self.group)
        self.denis.is_animated = False
        self.denis_is_pressed = False
        self.artem.is_animated = False
        self.artem_is_pressed = False

        self.button_sound = pygame.mixer.Sound('..\\assets\\audio\\button.mp3')

    def run(self, screen, dt, events, scene):
        if self.is_opened:
            screen.blit(self.background,
                        (settings.CENTER[0] - self.background.get_width() // 2,
                         settings.CENTER[1] - self.background.get_height() // 2))
            settings.window_opened = True

            if self.denis.is_mouse_on():
                self.denis.is_animated = True
                settings.current_cursor = ImgEditor.load_image(f'cursors/pointer_cursor.png', settings.SCALE_K - 2)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN and not self.denis_is_pressed:
                        self.denis_is_pressed = True
                        self.button_sound.play()
                    if event.type == pygame.MOUSEBUTTONUP and self.denis_is_pressed:
                        settings.player = 'denis'
                        settings.window_opened = False
                        self.is_opened = False
                        scene.disappear(settings.previous_scene, settings.player_pos, 'down_idle')

            else:
                self.denis.image = self.denis.animation[0]
                self.denis.is_animated = False

            if self.artem.is_mouse_on():
                self.artem.is_animated = True
                settings.current_cursor = ImgEditor.load_image(f'cursors/pointer_cursor.png', settings.SCALE_K - 2)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN and not self.artem_is_pressed:
                        self.artem_is_pressed = True
                        self.button_sound.play()
                    if event.type == pygame.MOUSEBUTTONUP and self.artem_is_pressed:
                        settings.player = 'artem'
                        settings.window_opened = False
                        self.is_opened = False
                        scene.disappear(settings.previous_scene, settings.player_pos, 'down_idle')

            else:
                self.artem.image = self.artem.animation[0]
                self.artem.is_animated = False

            self.group.draw(screen)
            self.group.update(dt)
