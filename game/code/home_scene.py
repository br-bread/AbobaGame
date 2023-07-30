from core import BaseScene
from sprites import InvisibleDoor


class HomeScene(BaseScene):
    def __init__(self, background, scene_collision_mask, background_pos=(0, 0)):
        super().__init__(background, scene_collision_mask, background_pos)
        self.name = 'home_scene'

        InvisibleDoor(
            (675, 850),
            self,
            'first_street_scene',
            (890, 100),
            'down_idle',
            self.visible_sprites
        )
