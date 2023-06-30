from settings import *
from core import BaseScene, InteractiveSprite
from tools import ImgEditor


class FirstStreetScene(BaseScene):
    def __init__(self, background, scene_collision_mask, background_pos=(0, 0)):
        super().__init__(background, scene_collision_mask, background_pos)
        self.name = 'first_street_scene'

        self.sprite = InteractiveSprite(
            'пугало',
            ImgEditor.enhance_image(ImgEditor.load_image(f'{self.name}/scarecrow.png'), 4),
            (440, 225),
            LAYERS['main'],
            self.visible_sprites, self.collision_sprites)
        self.sprite.hitbox = self.sprite.rect.copy().inflate(-self.sprite.rect.width * 0.4, -self.sprite.rect.height * 0.9)
        self.sprite.hitbox.y += 50
