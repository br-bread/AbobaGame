import pygame
from settings import *
from core import BaseScene, InteractiveSprite
from player import Player
from tools import ImgEditor


class FirstStreetScene(BaseScene):
    def __init__(self, background, background_pos=(0, 0)):
        super().__init__(background, background_pos)
        self.name = 'first_street_scene'

        self.sprite = InteractiveSprite(
            'пугало',
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/scarecrow.png'), 4),
            (440, 225),
            LAYERS['main'],
            self.visible_sprites)
