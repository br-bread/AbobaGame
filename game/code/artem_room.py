from core import BaseScene, BaseSprite
from sprites import InvisibleDoor, DialogueSprite
from settings import *


class ArtemRoom(BaseScene):
    def __init__(self, background, scene_collision_mask, music, background_pos=(0, 0)):
        super().__init__(background, scene_collision_mask, music, background_pos)
        self.name = 'artem_room'

        InvisibleDoor(
            (796, 710),
            self,
            'home_upscene',
            'home_day.mp3',
            (668, 360),
            'down_idle',
            'h',
            self.visible_sprites
        )

        DialogueSprite(
            'плакат',
            False,
            ImgEditor.load_image(f'{self.name}/rick.png', SCALE_K),
            (740, 314),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        DialogueSprite(
            'тумбочка',
            False,
            ImgEditor.load_image(f'{self.name}/table.png', SCALE_K),
            (742, 390),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        DialogueSprite(
            'диплом',
            False,
            ImgEditor.load_image(f'{self.name}/diploma.png', SCALE_K),
            (674, 298),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        self.socks = [DialogueSprite(
            'носок',
            False,
            ImgEditor.load_image(f'{self.name}/sock.png', SCALE_K),
            (850, 570),
            'magnifier',
            LAYERS['floor'],
            self.visible_sprites, id=5),

            DialogueSprite(
                'носок',
                False,
                ImgEditor.load_image(f'{self.name}/sock.png', SCALE_K),
                (800, 470),
                'magnifier',
                LAYERS['floor'],
                self.visible_sprites, id=6),

            DialogueSprite(
                'носок',
                False,
                ImgEditor.load_image(f'{self.name}/sock.png', SCALE_K),
                (980, 410),
                'magnifier',
                LAYERS['floor'],
                self.visible_sprites, id=7)]

        BaseSprite(
            ImgEditor.load_image(f'{self.name}/computer.png', SCALE_K),
            (680, 548),
            LAYERS['main'],
            self.visible_sprites)

        BaseSprite(
            ImgEditor.load_image(f'{self.name}/trash.png', SCALE_K),
            (782, 568),
            LAYERS['main'],
            self.visible_sprites)

        BaseSprite(
            ImgEditor.load_image(f'{self.name}/ceiling.png', SCALE_K),
            (792, 708),
            LAYERS['ceiling'],
            self.visible_sprites)
