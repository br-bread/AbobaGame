from core import BaseScene, BaseSprite
from sprites import InvisibleDoor, DialogueSprite
from settings import *


class BarUpScene(BaseScene):
    def __init__(self, background, scene_collision_mask, music, background_pos=(0, 0)):
        super().__init__(background, scene_collision_mask, music, background_pos)
        self.name = 'bar_upscene'

        InvisibleDoor(
            (480, 330),
            self,
            'bar_scene',
            'bar.mp3',
            (485, 400),
            'down_idle',
            'h',
            self.visible_sprites
        )

        DialogueSprite(
            'Яна',
            True,
            ImgEditor.load_image(f'{self.name}/yana.png', SCALE_K),
            (590, 410),
            'dialogue',
            LAYERS['main'],
            self.visible_sprites)

        coords = [(532, 616), (536, 684), (888, 568), (924, 680), (948, 564), (988, 676)]
        for i in range(len(coords)):
            BaseSprite(
                ImgEditor.load_image(f'{self.name}/chair.png', SCALE_K),
                coords[i],
                LAYERS['main'],
                self.visible_sprites)

        BaseSprite(
            ImgEditor.load_image(f'{self.name}/table.png', SCALE_K),
            (466, 600),
            LAYERS['ceiling'],
            self.visible_sprites)

        BaseSprite(
            ImgEditor.load_image(f'{self.name}/table1.png', SCALE_K),
            (940, 586),
            LAYERS['ceiling'],
            self.visible_sprites)

        self.sofa = DialogueSprite(
            'диван',
            False,
            ImgEditor.load_image(f'{self.name}/sofa.png', SCALE_K),
            (708, 540),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

