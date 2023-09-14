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
            'home_day.mp3',
            (1050, 380),
            'down_idle',
            self.visible_sprites
        )

        DialogueSprite(
            'тапочки',
            False,
            ImgEditor.load_image(f'{self.name}/dinos.png', SCALE_K),
            (788, 336),
            'magnifier',
            LAYERS['floor'],
            self.visible_sprites)

        DialogueSprite(
            'диплом',
            False,
            ImgEditor.load_image(f'{self.name}/diploma.png', SCALE_K),
            (662, 418),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        DialogueSprite(
            'плакат',
            False,
            ImgEditor.load_image(f'{self.name}/dota.png', SCALE_K),
            (904, 194),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        DialogueSprite(
            'тумбочка',
            False,
            ImgEditor.load_image(f'{self.name}/table.png', SCALE_K),
            (902, 262),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        DialogueSprite(
            'носок',
            False,
            ImgEditor.load_image(f'{self.name}/sock.png', SCALE_K),
            (1000, 368),
            'magnifier',
            LAYERS['floor'],
            self.visible_sprites)

        DialogueSprite(
            'носок',
            False,
            ImgEditor.load_image(f'{self.name}/sock.png', SCALE_K),
            (928, 308),
            'magnifier',
            LAYERS['floor'],
            self.visible_sprites)

        DialogueSprite(
            'носок',
            False,
            ImgEditor.load_image(f'{self.name}/sock.png', SCALE_K),
            (900, 520),
            'magnifier',
            LAYERS['floor'],
            self.visible_sprites)

        DialogueSprite(
            'носок',
            False,
            ImgEditor.load_image(f'{self.name}/sock.png', SCALE_K),
            (560, 540),
            'magnifier',
            LAYERS['floor'],
            self.visible_sprites)

        BaseSprite(
            ImgEditor.load_image(f'{self.name}/sofa.png', SCALE_K),
            (840, 464),
            LAYERS['main'],
            self.visible_sprites)

        BaseSprite(
            ImgEditor.load_image(f'{self.name}/ceiling.png', SCALE_K),
            (876, 664),
            LAYERS['ceiling'],
            self.visible_sprites)
