from core import BaseScene, BaseSprite
from sprites import InvisibleDoor, DialogueSprite
from settings import *


class KsushaRoom(BaseScene):
    def __init__(self, background, scene_collision_mask, music, background_pos=(0, 0)):
        super().__init__(background, scene_collision_mask, music, background_pos)
        self.name = 'ksusha_room'

        self.ksusha = DialogueSprite(
            'Ксюша',
            True,
            ImgEditor.load_image(f'{self.name}/ksusha.png', SCALE_K),
            (1039, 500),
            'dialogue',
            LAYERS['main'],
            self.visible_sprites)

        InvisibleDoor(
            (796, 660),
            self,
            'home_upscene',
            'home_day.mp3',
            (452, 360),
            'down_idle',
            'h',
            self.visible_sprites
        )

        BaseSprite(
            ImgEditor.load_image(f'{self.name}/ceiling.png', SCALE_K),
            (800, 652),
            LAYERS['ceiling'],
            self.visible_sprites)

        DialogueSprite(
            'забавный плакат',
            False,
            ImgEditor.load_image(f'{self.name}/astarion.png', SCALE_K),
            (1084, 298),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        DialogueSprite(
            'необычный плакат',
            False,
            ImgEditor.load_image(f'{self.name}/gale.png', SCALE_K),
            (1012, 266),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        DialogueSprite(
            'пыльная тумбочка',
            False,
            ImgEditor.load_image(f'{self.name}/table.png', SCALE_K),
            (602, 370),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        DialogueSprite(
            'гитара',
            False,
            ImgEditor.load_image(f'{self.name}/guitar.png', SCALE_K),
            (770, 305),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        DialogueSprite(
            'барабанные палочки',
            False,
            ImgEditor.load_image(f'{self.name}/sticks.png', SCALE_K),
            (872, 366),
            'magnifier',
            LAYERS['floor'],
            self.visible_sprites)

        DialogueSprite(
            'ковёр',
            False,
            ImgEditor.load_image(f'{self.name}/carpet.png', SCALE_K),
            (818, 510),
            'magnifier',
            LAYERS['floor'],
            self.visible_sprites)

        DialogueSprite(
            'помятый диплом',
            False,
            ImgEditor.load_image(f'{self.name}/diploma.png', SCALE_K),
            (830, 266),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)
