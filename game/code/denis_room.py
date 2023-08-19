from core import BaseScene, BaseSprite
from sprites import InvisibleDoor, DialogueSprite
from settings import *


class DenisRoom(BaseScene):
    def __init__(self, background, scene_collision_mask, music, background_pos=(0, 0)):
        super().__init__(background, scene_collision_mask, music, background_pos)
        self.name = 'denis_room'

        InvisibleDoor(
            (880, 680),
            self,
            'home_upscene',
            (1050, 380),
            'down_idle',
            self.visible_sprites
        )

        DialogueSprite(
            'тапочки',
            False,
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/dinos.png'), 4),
            (788, 336),
            'magnifier',
            LAYERS['floor'],
            self.visible_sprites)

        DialogueSprite(
            'диплом',
            False,
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/diploma.png'), 4),
            (662, 418),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        DialogueSprite(
            'плакат',
            False,
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/dota.png'), 4),
            (904, 194),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        DialogueSprite(
            'тумбочка',
            False,
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/table.png'), 4),
            (902, 262),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        DialogueSprite(
            'носок',
            False,
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/sock.png'), 4),
            (1000, 368),
            'magnifier',
            LAYERS['floor'],
            self.visible_sprites)

        DialogueSprite(
            'носок',
            False,
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/sock.png'), 4),
            (928, 308),
            'magnifier',
            LAYERS['floor'],
            self.visible_sprites)

        DialogueSprite(
            'носок',
            False,
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/sock.png'), 4),
            (900, 520),
            'magnifier',
            LAYERS['floor'],
            self.visible_sprites)

        DialogueSprite(
            'носок',
            False,
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/sock.png'), 4),
            (560, 540),
            'magnifier',
            LAYERS['floor'],
            self.visible_sprites)

        BaseSprite(
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/sofa.png'), 4),
            (840, 464),
            LAYERS['main'],
            self.visible_sprites)

        BaseSprite(
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/ceiling.png'), 4),
            (876, 664),
            LAYERS['ceiling'],
            self.visible_sprites)
