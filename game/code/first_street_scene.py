from settings import *
from core import BaseScene
from sprites import DialogueSprite, Door
from tools import ImgEditor


class FirstStreetScene(BaseScene):
    def __init__(self, background, scene_collision_mask, background_pos=(0, 0)):
        super().__init__(background, scene_collision_mask, background_pos)
        self.name = 'first_street_scene'

        self.scarecrow = DialogueSprite(
            'пугало',
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/scarecrow.png'), 4),
            (440, 225),
            LAYERS['main'],
            self.visible_sprites)

        self.signpost = DialogueSprite(
            'указатель',
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/signpost.png'), 4),
            (154, 323),
            LAYERS['main'],
            self.visible_sprites)

        self.basket = DialogueSprite(
            'корзинка для пикника',
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/basket.png'), 4),
            (206, 666),
            LAYERS['main'],
            self.visible_sprites)

        self.flowerbed = DialogueSprite(
            'клумба',
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/flowerbed.png'), 4),
            (593, 238),
            LAYERS['main'],
            self.visible_sprites)

        self.door = Door(
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/door.png'), 4),
            (888, 76),
            LAYERS['main'],
            'home_scene',
            self.visible_sprites)
