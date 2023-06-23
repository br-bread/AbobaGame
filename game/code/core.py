import pygame
from random import choice
from math import sqrt
import settings
from tools import ImgEditor
from player import Player


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, img, pos, layer=settings.LAYERS['main'], *groups):
        super().__init__(*groups)
        self.image = img
        self.rect = self.image.get_rect(center=pos)
        self.game_layer = layer

    def is_mouse_on(self):
        pos_x = pygame.mouse.get_pos()[0]
        pos_y = pygame.mouse.get_pos()[1]
        if self.rect.x + self.rect[2] >= pos_x >= self.rect.x and self.rect.y + self.rect[3] >= pos_y >= self.rect.y:
            return True
        else:
            return False

    def get_distance(self, player_pos):
        # returns distance from player
        distance = sqrt((self.rect.centerx - player_pos.x) ** 2 + (self.rect.centery - player_pos.y) ** 2)
        return distance


class Dialogue:
    def __init__(self, group, *texts):
        self.texts = texts
        img = ImgEditor.load_image(f'empty.png')
        self.dialogue = BaseSprite(img, settings.DIALOGUE_POS, settings.LAYERS['dialogue'], group)
        self.stage = 0
        self.is_shown = False

    def run(self, is_mouse_on):
        if not self.is_shown and is_mouse_on:
            self.is_shown = True
        else:
            self.stage += 1
            if self.stage == len(self.texts):
                self.is_shown = False
                self.stage = 0
                img = ImgEditor.load_image(f'empty.png')
                self.dialogue.image = img
                self.dialogue.rect = self.dialogue.image.get_rect(center=settings.DIALOGUE_POS)

        if self.is_shown:
            text = self.texts[self.stage]
            kind = text[:text.find('_')]
            img = ImgEditor.enhance_image(ImgEditor.load_image(f'/dialogues/{kind}_dialogue.png'), 4)
            self.dialogue.image = img
            self.dialogue.rect = self.dialogue.image.get_rect(center=settings.DIALOGUE_POS)
            # appearing animation (if self.stage == 0)
            # text animation


class InteractiveSprite(BaseSprite):
    def __init__(self, name, img, pos, layer=settings.LAYERS['main'], *groups):
        super().__init__(img, pos, layer, *groups)
        self.name = name
        self.cursor_image = 'magnifier_cursor.png'
        # dialogue
        description = choice([f"base_Это {name}.", f"base_Это просто {name}.", f"base_Выглядит как {name}.",
                              f"base_Это {name}, ничего интересного.", f"base_{name.capitalize()}."])
        self.dialogue = Dialogue(groups[0], description)

    def is_accessible(self, distance):
        if distance <= settings.INTERACTION_DISTANCE:
            return True
        return False

    def update(self, dt, player_pos, events, *args, **kwargs):
        if self.is_mouse_on():
            if self.is_accessible(self.get_distance(player_pos)):
                img = ImgEditor.load_image(f'cursors/{self.cursor_image}')
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.dialogue.run(is_mouse_on=True)
            else:
                img = ImgEditor.load_image(f'cursors/inaccessible/{self.cursor_image}')
            settings.current_cursor = ImgEditor.enhance_image(img, 4)
        else:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.dialogue.run(is_mouse_on=False)


class BaseScene:
    def __init__(self, background, background_pos=(0, 0)):
        # sprite groups
        self.visible_sprites = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.screen = pygame.display.get_surface()
        self.player = Player(settings.CENTER, self.visible_sprites)
        self.name = 'scene'

        self.background = BaseSprite(background, background_pos, settings.LAYERS['background'])

    def run(self, delta_time, events):
        self.screen.blit(self.background.image, self.background.rect)
        self.visible_sprites.draw_sprites()
        self.visible_sprites.update(delta_time, self.player.pos, events)


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.screen = pygame.display.get_surface()

    def draw_sprites(self):
        for layer in settings.LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda x: x.rect.centery):
                if sprite.game_layer == layer:
                    self.screen.blit(sprite.image, sprite.rect)
