from core import BaseScene
from sprites import InvisibleDoor


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
