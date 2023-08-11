from core import BaseScene
from sprites import InvisibleDoor, DialogueSprite
from tools import ImgEditor
import settings


class HomeScene(BaseScene):
    def __init__(self, background, scene_collision_mask, background_pos=(0, 0)):
        super().__init__(background, scene_collision_mask, background_pos)
        self.name = 'home_scene'

        self.artem = DialogueSprite(
            'Артём',
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/artem.png'), 4),
            (946, 480),
            'dialogue',
            settings.LAYERS['main'],
            self.visible_sprites)

        InvisibleDoor(
            (675, 850),
            self,
            'first_street_scene',
            (890, 100),
            'down_idle',
            self.visible_sprites
        )
