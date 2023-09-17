from core import BaseScene, BaseSprite
from sprites import InvisibleDoor, DialogueSprite, Door
import settings
from tools import ImgEditor


class HomeUpScene(BaseScene):
    def __init__(self, background, scene_collision_mask, music, background_pos=(0, 0)):
        super().__init__(background, scene_collision_mask, music, background_pos)
        self.name = 'home_upscene'

        InvisibleDoor(
            (990, 560),
            self,
            'home_scene',
            self.music_name,
            (1155, 410),
            'down_idle',
            'h',
            self.visible_sprites
        )

        self.doorD = Door(
            ImgEditor.load_image(f'{self.name}/doorD.png', settings.SCALE_K),
            (1052, 340),
            settings.LAYERS['main'],
            self,
            'denis_room',
            'denis.mp3',
            (880, 590),
            'up_idle')

        self.doorA = Door(
            ImgEditor.load_image(f'{self.name}/doorA.png', settings.SCALE_K),
            (668, 340),
            settings.LAYERS['main'],
            self,
            'artem_room',
            'artem.mp3',
            (810, 610),
            'up_idle')

        self.ksusha = DialogueSprite(
            'Ксюша',
            True,
            ImgEditor.load_image(f'{self.name}/ksusha.png', settings.SCALE_K),
            (439, 500),
            'dialogue',
            settings.LAYERS['main'],
            self.visible_sprites)

        DialogueSprite(
            'фикус',
            False,
            ImgEditor.load_image(f'{self.name}/plant.png', settings.SCALE_K),
            (1138, 346),
            'magnifier',
            settings.LAYERS['main'],
            self.visible_sprites)

        DialogueSprite(
            'книги',
            False,
            ImgEditor.load_image(f'{self.name}/books.png', settings.SCALE_K),
            (878, 344),
            'magnifier',
            settings.LAYERS['main'],
            self.visible_sprites)

        DialogueSprite(
            'вязаный Почита',
            False,
            ImgEditor.load_image(f'{self.name}/pochita.png', settings.SCALE_K),
            (936, 278),
            'magnifier',
            settings.LAYERS['main'],
            self.visible_sprites)

        # doors (sprites)
        self.roomD = DialogueSprite(
            'комната Дениса',
            False,
            ImgEditor.load_image(f'{self.name}/doorD.png', settings.SCALE_K),
            (1052, 340),
            'magnifier',
            settings.LAYERS['main'],
            self.visible_sprites)

        DialogueSprite(
            'комната Ксюши',
            False,
            ImgEditor.load_image(f'{self.name}/doorK.png', settings.SCALE_K),
            (456, 340),
            'magnifier',
            settings.LAYERS['main'],
            self.visible_sprites)

        self.roomA = DialogueSprite(
            'комната Артёма',
            False,
            ImgEditor.load_image(f'{self.name}/doorA.png', settings.SCALE_K),
            (668, 340),
            'magnifier',
            settings.LAYERS['main'],
            self.visible_sprites)

        # ceiling sprites
        BaseSprite(
            ImgEditor.load_image(f'{self.name}/railings.png', settings.SCALE_K),
            (598, 608),
            settings.LAYERS['ceiling'],
            self.visible_sprites)

        BaseSprite(
            ImgEditor.load_image(f'{self.name}/ceiling.png', settings.SCALE_K),
            (982, 566),
            settings.LAYERS['ceiling'],
            self.visible_sprites)

    def run(self, delta_time, events):
        super().run(delta_time, events)
        if settings.player == 'artem':
            inventory = settings.inventory.artem_items
        else:
            inventory = settings.inventory.denis_items

        if 'keyA' in inventory.keys() and inventory['keyA'].count == 1:
            self.roomA.kill()
            self.doorA.add(self.visible_sprites)

        if 'keyD' in inventory.keys() and inventory['keyD'].count == 1:
            self.roomD.kill()
            self.doorD.add(self.visible_sprites)
