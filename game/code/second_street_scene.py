import settings
from core import BaseScene, BaseSprite
from sprites import DialogueSprite, Door, InvisibleDoor
from tools import ImgEditor


class SecondStreetScene(BaseScene):
    def __init__(self, background, scene_collision_mask, music, background_pos=(0, 0)):
        super().__init__(background, scene_collision_mask, music, background_pos)
        self.name = 'second_street_scene'
        SCALE_K = settings.SCALE_K
        LAYERS = settings.LAYERS

        # doors
        InvisibleDoor(
            (1560, 428),
            self,
            'first_street_scene',
            self.music_name,
            (60, 410),
            'right_idle',
            'v',
            self.visible_sprites
        )

        # ceilings
        coords = [(164, 532), (798, 592), (1026, 158)]
        for i in range(len(coords)):
            BaseSprite(
                ImgEditor.load_image(f'{self.name}/top{i + 1}.png', SCALE_K),
                coords[i],
                LAYERS['ceiling'],
                self.visible_sprites)

        # bushes
        coords = [(1436, 750), (1202, 804), (932, 802), (1516, 832), (438, 722)]
        for i in range(len(coords)):
            BaseSprite(
                ImgEditor.load_image(f'{self.name}/bushes{i + 1}.png', SCALE_K),
                coords[i],
                LAYERS['main'],
                self.visible_sprites)

        BaseSprite(
            ImgEditor.load_image(f'{self.name}/bar.png', SCALE_K),
            (1002, 358),
            LAYERS['main'],
            self.visible_sprites)

        BaseSprite(
            ImgEditor.load_image(f'{self.name}/branches.png', SCALE_K),
            (338, 258),
            LAYERS['main'],
            self.visible_sprites)

        BaseSprite(
            ImgEditor.load_image(f'{self.name}/lantern.png', SCALE_K),
            (1446, 386),
            LAYERS['main'],
            self.visible_sprites)

        BaseSprite(
            ImgEditor.load_image(f'{self.name}/roots.png', SCALE_K),
            (814, 786),
            LAYERS['main'],
            self.visible_sprites)

        BaseSprite(
            ImgEditor.load_image(f'{self.name}/shop.png', SCALE_K),
            (158, 740),
            LAYERS['main'],
            self.visible_sprites)

        # dialogue sprites
        self.barrels = DialogueSprite(
            'бочки',
            False,
            ImgEditor.load_image(f'{self.name}/barrels.png', SCALE_K),
            (1342, 342),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        self.goods = DialogueSprite(
            'товары',
            False,
            ImgEditor.load_image(f'{self.name}/goods.png', SCALE_K),
            (328, 742),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        self.merchant = DialogueSprite(
            'торговец',
            True,
            ImgEditor.load_image(f'{self.name}/merchant.png', SCALE_K),
            (192, 708),
            'dialogue',
            LAYERS['main'],
            self.visible_sprites)

        self.j = DialogueSprite(
            'вывеска',
            False,
            ImgEditor.load_image(f'{self.name}/j.png', SCALE_K),
            (786, 264),
            'magnifier',
            LAYERS['ceiling'],
            self.visible_sprites)

    def run(self, delta_time, events):
        super().run(delta_time, events)
        if (settings.time['hours'] >= 18 or settings.time[
            'hours'] < 7) and settings.music_player.music_name != 'street_night.mp3':
            self.music_name = 'street_night.mp3'
            settings.music_player.change_music('street_night.mp3')

        elif 7 <= settings.time['hours'] < 18 and settings.music_player.music_name != 'street_day.mp3':
            self.music_name = 'street_day.mp3'
            settings.music_player.change_music('street_day.mp3')
