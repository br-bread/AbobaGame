from core import BaseScene, BaseSprite
from sprites import InvisibleDoor, DialogueSprite
from tools import ImgEditor
from settings import *


class HomeUpScene(BaseScene):
    def __init__(self, background, scene_collision_mask, background_pos=(0, 0)):
        super().__init__(background, scene_collision_mask, background_pos)
        self.name = 'home_upscene'

        InvisibleDoor(
            (990, 560),
            self,
            'home_scene',
            (1155, 410),
            'down_idle',
            self.visible_sprites
        )

        self.ksusha = DialogueSprite(
            'Ксюша',
            True,
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/ksusha.png'), 4),
            (439, 500),
            'dialogue',
            LAYERS['main'],
            self.visible_sprites)

        DialogueSprite(
            'фикус',
            False,
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/plant.png'), 4),
            (1138, 346),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        DialogueSprite(
            'книги',
            False,
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/books.png'), 4),
            (878, 344),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        DialogueSprite(
            'вязаный Почита',
            False,
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/pochita.png'), 4),
            (936, 278),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        # doors (sprites)
        DialogueSprite(
            'комната Ксюши',
            False,
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/doorK.png'), 4),
            (456, 340),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        DialogueSprite(
            'комната Артёма',
            False,
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/doorA.png'), 4),
            (668, 340),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        # ceiling sprites
        BaseSprite(
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/railings.png'), 4),
            (598, 608),
            LAYERS['ceiling'],
            self.visible_sprites)

        BaseSprite(
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/ceiling.png'), 4),
            (982, 566),
            LAYERS['ceiling'],
            self.visible_sprites)
