import pygame
from random import choice
from math import sqrt
import settings
from tools import ImgEditor, blit_text
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
        # text

        # going through the text to find out if some parts are too long
        new_texts = []
        for i in range(len(texts)):
            text = texts[i][texts[i].find('_') + 1:]
            kind = texts[i][:texts[i].find('_')]
            if len(text) > settings.MAX_DIALOGUE_LENGTH:
                part = kind + '_'
                for word in text.split():
                    if len(part) - len(kind) + len(word) <= settings.MAX_DIALOGUE_LENGTH:
                        part += word + ' '
                    else:
                        new_texts.append(part)
                        print(len(part))
                        i += 1
                        part = kind + '_' + word + ' '
                new_texts.append(part)
            else:
                new_texts.append(texts[i])

        self.texts = new_texts[:]

        self.font = pygame.font.Font(settings.FONT, 65)
        self.text = ''

        img = ImgEditor.load_image(f'empty.png')
        self.dialogue = BaseSprite(img, settings.DIALOGUE_POS, settings.LAYERS['dialogue'], group)
        self.stage = 0
        self.is_shown = False
        self.kind = ''  # base dialogue or someone's
        self.speed = 800  # appearing&disappearing animation speed
        # for text animation
        self.text_frame = 0
        self.text_speed = 23

    def run(self, is_mouse_on):
        if not self.is_shown and is_mouse_on:
            self.is_shown = True
            self.stage = 0
        elif self.is_shown:
            self.stage += 1
            self.text_frame = 0
            if self.stage == len(self.texts):
                # end of the dialogue
                self.is_shown = False
                self.text = ''

        if self.is_shown:
            text = self.texts[self.stage]
            self.kind = text[:text.find('_')]
            img = ImgEditor.enhance_image(ImgEditor.load_image(f'/dialogues/{self.kind}_dialogue.png'), 4)
            self.text = text[text.find('_') + 1:]
            self.dialogue.image = img
            self.dialogue.rect = self.dialogue.image.get_rect(center=(settings.DIALOGUE_POS[0], 1000))

    def animate(self, delta_time, screen):
        if self.stage == 0:  # appearing
            if self.dialogue.rect.centery > settings.DIALOGUE_POS[1]:
                self.dialogue.rect.centery -= self.speed * delta_time
        elif self.stage == len(self.texts):  # disappearing
            if self.dialogue.rect.centery < 1000:
                self.dialogue.rect.centery += self.speed * delta_time
        else:
            self.dialogue.rect.centery = settings.DIALOGUE_POS[1]

        # text
        if self.kind != 'base':
            pos = (600, 90 + self.dialogue.rect.y)
        else:
            pos = (475, 110 + self.dialogue.rect.y)
        text = self.text[:int(self.text_frame)]
        if self.text_frame < len(self.text):
            self.text_frame += self.text_speed * delta_time
        blit_text(screen, pos, 1210, text, self.font, settings.TEXT_COLOR, (True, (self.kind == 'base')))


class InteractiveSprite(BaseSprite):
    def __init__(self, name, img, pos, layer=settings.LAYERS['main'], *groups):
        super().__init__(img, pos, layer, *groups)
        # general
        self.name = name
        self.cursor_image = 'magnifier_cursor.png'
        # dialogue
        description = choice([f"base_Это {name}.", f"base_Это просто {name}.", f"base_Выглядит как {name}.",
                              f"base_Это {name}, ничего интересного.", f"base_{name.capitalize()}."])
        self.dialogue = Dialogue(groups[0], description, *settings.DIALOGUES[name])

    def is_accessible(self, distance):
        if distance <= settings.INTERACTION_DISTANCE:
            return True
        return False

    def update(self, dt, player_pos, events, screen, *args, **kwargs):
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
        self.dialogue.animate(dt, screen)


class BaseScene:
    def __init__(self, background, background_pos=(0, 0)):
        # sprite groups
        self.visible_sprites = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        # general
        self.screen = pygame.display.get_surface()
        self.player = Player(settings.CENTER, self.visible_sprites)
        self.name = 'scene'
        self.background = BaseSprite(background, background_pos, settings.LAYERS['background'])

    def run(self, delta_time, events):
        self.screen.blit(self.background.image, self.background.rect)
        self.visible_sprites.draw_sprites()
        self.visible_sprites.update(delta_time, self.player.pos, events, self.screen)


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.screen = pygame.display.get_surface()

    def draw_sprites(self):
        for layer in settings.LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda x: x.rect.centery):  # fake 3d effect
                if sprite.game_layer == layer:
                    self.screen.blit(sprite.image, sprite.rect)
