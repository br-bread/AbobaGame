import pygame.mixer

from settings import *
from core import BaseScene, BaseSprite
from sprites import DialogueSprite, Door
from tools import ImgEditor


class FirstStreetScene(BaseScene):
    def __init__(self, background, scene_collision_mask, music, background_pos=(0, 0)):
        super().__init__(background, scene_collision_mask, music, background_pos)
        self.name = 'first_street_scene'

        # Dialogue sprites
        self.scarecrow = DialogueSprite(
            'пугало',
            False,
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/scarecrow.png'), 4),
            (439, 226),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        self.signpost = DialogueSprite(
            'указатель',
            False,
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/signpost.png'), 4),
            (154, 323),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        self.basket = DialogueSprite(
            'корзинка для пикника',
            False,
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/basket.png'), 4),
            (206, 666),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        self.flowerbed = DialogueSprite(
            'клумба',
            False,
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/flowerbed.png'), 4),
            (593, 238),
            'magnifier',
            LAYERS['floor'],
            self.visible_sprites)

        self.window = DialogueSprite(
            'окно',
            False,
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/window.png'), 4),
            (996, 62),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        self.mail = DialogueSprite(
            'почтовый ящик',
            False,
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/mail.png'), 4),
            (832, 72),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        self.carpet = DialogueSprite(
            'коврик',
            False,
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/carpet.png'), 4),
            (888, 132),
            'magnifier',
            LAYERS['floor'],
            self.visible_sprites)

        # Other sprites
        # woods
        BaseSprite(
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/wood1.png'), 4),
            (1063, 402),
            LAYERS['main'],
            self.visible_sprites)

        BaseSprite(
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/wood2.png'), 4),
            (1062, 519),
            LAYERS['main'],
            self.visible_sprites)

        BaseSprite(
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/woods.png'), 4),
            (1230, 526),
            LAYERS['ceiling'],
            self.visible_sprites)
        # bench
        BaseSprite(
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/bench.png'), 4),
            (608, 336),
            LAYERS['main'],
            self.visible_sprites)
        # flowers
        BaseSprite(
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/flowers.png'), 4),
            (595, 202),
            LAYERS['ceiling'],
            self.visible_sprites)

        # lanterns
        coords = [(398, 346), (218, 590), (1110, 774)]
        for coord in coords:
            BaseSprite(
                ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/lantern.png'), 4),
                coord,
                LAYERS['main'],
                self.visible_sprites)
        # bushes
        coords = [(488, 344), (722, 350), (88, 646), (322, 592), (472, 606), (1310, 762), ]
        for i in range(len(coords)):
            BaseSprite(
                ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/bushes{i + 1}.png'), 4),
                coords[i],
                LAYERS['main'],
                self.visible_sprites)

        BaseSprite(
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/bushes7.png'), 4),
            (880, 832),
            LAYERS['ceiling'],
            self.visible_sprites)
        # Doors to next scene
        Door(
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/door.png'), 4),
            (888, 76),
            LAYERS['main'],
            self,
            'home_scene',
            (674, 750),
            'up_idle',
            self.visible_sprites)

    def run(self, delta_time, events):
        super().run(delta_time, events)
        if time['hours'] == 18 and time['minutes'] == 0 and not self.music_changing:
            self.change_music(pygame.mixer.Sound('..\\assets\\audio\\music\\street_night.mp3'))

        if time['hours'] == 9 and time['minutes'] == 0 and not self.music_changing:
            self.change_music(pygame.mixer.Sound('..\\assets\\audio\\music\\street_day.mp3'))
