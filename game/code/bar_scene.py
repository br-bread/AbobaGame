import pygame
from core import BaseScene, BaseSprite
from sprites import InvisibleDoor, DialogueSprite
from tools import ImgEditor
import settings


class BarScene(BaseScene):
    def __init__(self, background, scene_collision_mask, music, background_pos=(0, 0)):
        super().__init__(background, scene_collision_mask, music, background_pos)
        self.name = 'bar_scene'
        SCALE_K = settings.SCALE_K
        LAYERS = settings.LAYERS

        # chairs
        coords = [(500, 512), (560, 508), (536, 624), (600, 620), (852, 594), (844, 648), (984, 588), (988, 656)]
        for i in range(len(coords)):
            BaseSprite(
                ImgEditor.load_image(f'{self.name}/chair.png', SCALE_K),
                coords[i],
                LAYERS['main'],
                self.visible_sprites)

        self.jazz = DialogueSprite(
            'постер',
            False,
            ImgEditor.load_image(f'{self.name}/jazz.png', SCALE_K),
            (588, 358),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        self.tablet = DialogueSprite(
            'табличка',
            False,
            ImgEditor.load_image(f'{self.name}/tablet.png', SCALE_K),
            (478, 398),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        # table
        BaseSprite(
            ImgEditor.load_image(f'{self.name}/table.png', settings.SCALE_K),
            (552, 530),
            settings.LAYERS['ceiling'],
            self.visible_sprites)
        BaseSprite(
            ImgEditor.load_image(f'{self.name}/table1.png', settings.SCALE_K),
            (918, 567),
            settings.LAYERS['ceiling'],
            self.visible_sprites)

        # characters
        DialogueSprite(
            'Джесс',
            True,
            ImgEditor.load_image(f'{self.name}/jess.png', settings.SCALE_K),
            (766, 327),
            'dialogue',
            settings.LAYERS['main'],
            self.visible_sprites)
        DialogueSprite(
            'Джефф',
            True,
            ImgEditor.load_image(f'{self.name}/jeff.png', settings.SCALE_K),
            (1006, 470),
            'dialogue',
            settings.LAYERS['main'],
            self.visible_sprites)
        DialogueSprite(
            'Джек',
            True,
            ImgEditor.load_image(f'{self.name}/jack.png', SCALE_K),
            (984, 560),
            'dialogue',
            LAYERS['ceiling'],
            self.visible_sprites)

        # doors
        self.upstairs = InvisibleDoor(
            (480, 280),
            self,
            'bar_upscene',
            'bar.mp3',
            (485, 430),
            'down_idle',
            'h'
        )
        InvisibleDoor(
            (740, 770),
            self,
            'second_street_scene',
            'street_day.mp3',
            (1005, 400),
            'down_idle',
            'h',
            self.visible_sprites
        )
        BaseSprite(
            ImgEditor.load_image(f'{self.name}/ceiling.png', settings.SCALE_K),
            (476, 244),
            settings.LAYERS['ceiling'],
            self.visible_sprites)
        BaseSprite(
            ImgEditor.load_image(f'{self.name}/ceiling1.png', settings.SCALE_K),
            (744, 790),
            settings.LAYERS['ceiling'],
            self.visible_sprites)

    def run(self, delta_time, events):
        super().run(delta_time, events)
        if settings.finished_quests == 1 + 1:
            self.collision_mask = pygame.mask.from_surface(
                ImgEditor.load_image('bar_scene/collisions1.png', settings.SCALE_K))
            self.background.image = ImgEditor.load_image('/backgrounds/bar_scene1.png', settings.SCALE_K)
            self.tablet.kill()
            self.upstairs.add(self.visible_sprites)
