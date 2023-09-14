import settings
from core import BaseScene, BaseSprite
from sprites import DialogueSprite, Door
from tools import ImgEditor


class FirstStreetScene(BaseScene):
    def __init__(self, background, scene_collision_mask, music, background_pos=(0, 0)):
        super().__init__(background, scene_collision_mask, music, background_pos)
        self.name = 'first_street_scene'
        SCALE_K = settings.SCALE_K
        LAYERS = settings.LAYERS

        # Dialogue sprites
        self.scarecrow = DialogueSprite(
            'пугало',
            False,
            ImgEditor.load_image(f'{self.name}/scarecrow.png', SCALE_K),
            (109 * SCALE_K, 57 * SCALE_K),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        self.signpost = DialogueSprite(
            'указатель',
            False,
            ImgEditor.load_image(f'{self.name}/signpost.png', SCALE_K),
            (39 * SCALE_K, 81 * SCALE_K),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        self.basket = DialogueSprite(
            'корзинка для пикника',
            False,
            ImgEditor.load_image(f'{self.name}/basket.png', SCALE_K),
            (51 * SCALE_K, 166 * SCALE_K),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        self.flowerbed = DialogueSprite(
            'клумба',
            False,
            ImgEditor.load_image(f'{self.name}/flowerbed.png', SCALE_K),
            (148 * SCALE_K, 60 * SCALE_K),
            'magnifier',
            LAYERS['floor'],
            self.visible_sprites)

        self.window = DialogueSprite(
            'окно',
            False,
            ImgEditor.load_image(f'{self.name}/window.png', SCALE_K),
            (249 * SCALE_K, 16 * SCALE_K),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        self.mail = DialogueSprite(
            'почтовый ящик',
            False,
            ImgEditor.load_image(f'{self.name}/mail.png', SCALE_K),
            (208 * SCALE_K, 18 * SCALE_K),
            'magnifier',
            LAYERS['main'],
            self.visible_sprites)

        self.carpet = DialogueSprite(
            'коврик',
            False,
            ImgEditor.load_image(f'{self.name}/carpet.png', SCALE_K),
            (222 * SCALE_K, 33 * SCALE_K),
            'magnifier',
            LAYERS['floor'],
            self.visible_sprites)

        # Other sprites
        # woods
        BaseSprite(
            ImgEditor.load_image(f'{self.name}/wood1.png', SCALE_K),
            (266 * SCALE_K, 101 * SCALE_K),
            LAYERS['main'],
            self.visible_sprites)

        BaseSprite(
            ImgEditor.load_image(f'{self.name}/wood2.png', SCALE_K),
            (266 * SCALE_K, 130 * SCALE_K),
            LAYERS['main'],
            self.visible_sprites)

        BaseSprite(
            ImgEditor.load_image(f'{self.name}/woods.png', SCALE_K),
            (307 * SCALE_K, 137 * SCALE_K),
            LAYERS['ceiling'],
            self.visible_sprites)
        # bench
        BaseSprite(
            ImgEditor.load_image(f'{self.name}/bench.png', SCALE_K),
            (152 * SCALE_K, 84 * SCALE_K),
            LAYERS['main'],
            self.visible_sprites)
        # flowers
        BaseSprite(
            ImgEditor.load_image(f'{self.name}/flowers.png', SCALE_K),
            (149 * SCALE_K, 51 * SCALE_K),
            LAYERS['main'],
            self.visible_sprites)

        # lanterns
        coords = [(100 * SCALE_K, 87 * SCALE_K), (55 * SCALE_K, 148 * SCALE_K), (278 * SCALE_K, 194 * SCALE_K)]
        for coord in coords:
            BaseSprite(
                ImgEditor.load_image(f'{self.name}/lantern.png', SCALE_K),
                coord,
                LAYERS['main'],
                self.visible_sprites)
        # bushes
        coords = [(122 * SCALE_K, 86 * SCALE_K), (181 * SCALE_K, 88 * SCALE_K), (22 * SCALE_K, 162 * SCALE_K),
                  (81 * SCALE_K, 148 * SCALE_K), (118 * SCALE_K, 152 * SCALE_K), (328 * SCALE_K, 191 * SCALE_K), ]
        for i in range(len(coords)):
            BaseSprite(
                ImgEditor.load_image(f'{self.name}/bushes{i + 1}.png', SCALE_K),
                coords[i],
                LAYERS['main'],
                self.visible_sprites)

        BaseSprite(
            ImgEditor.load_image(f'{self.name}/bushes7.png', SCALE_K),
            (220 * SCALE_K, 208 * SCALE_K),
            LAYERS['ceiling'],
            self.visible_sprites)
        # Doors to next scene
        Door(
            ImgEditor.load_image(f'{self.name}/door.png', SCALE_K),
            (222 * SCALE_K, 19 * SCALE_K),
            LAYERS['main'],
            self,
            'home_scene',
            'home_day.mp3',
            (169 * SCALE_K, 188 * SCALE_K),
            'up_idle',
            self.visible_sprites)

    def run(self, delta_time, events):
        super().run(delta_time, events)
        if (settings.time['hours'] >= 18 or settings.time[
            'hours'] < 7) and settings.music_player.music_name != 'street_night.mp3':
            settings.music_player.change_music('street_night.mp3')

        elif 7 <= settings.time['hours'] < 18 and settings.music_player.music_name != 'street_day.mp3':
            settings.music_player.change_music('street_day.mp3')
