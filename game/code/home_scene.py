from core import BaseScene, BaseSprite
from sprites import InvisibleDoor, DialogueSprite
from tools import ImgEditor
import settings


class HomeScene(BaseScene):
    def __init__(self, background, scene_collision_mask, music, background_pos=(0, 0)):
        super().__init__(background, scene_collision_mask, music, background_pos)
        self.name = 'home_scene'

        self.artem = DialogueSprite(
            'Артём',
            True,
            ImgEditor.load_image(f'{self.name}/artem.png', settings.SCALE_K),
            (946, 480),
            'dialogue',
            settings.LAYERS['main'],
            self.visible_sprites)

        DialogueSprite(
            'Боб',
            False,
            ImgEditor.load_image(f'{self.name}/bob.png', settings.SCALE_K),
            (674, 216),
            'magnifier',
            settings.LAYERS['main'],
            self.visible_sprites)

        DialogueSprite(
            'коробка из-под роллов',
            False,
            ImgEditor.load_image(f'{self.name}/box.png', settings.SCALE_K),
            (209, 452),
            'magnifier',
            settings.LAYERS['main'],
            self.visible_sprites)

        DialogueSprite(
            'консервы',
            False,
            ImgEditor.load_image(f'{self.name}/cans.png', settings.SCALE_K),
            (220, 508),
            'magnifier',
            settings.LAYERS['main'],
            self.visible_sprites)

        BaseSprite(
            ImgEditor.load_image(f'{self.name}/chair.png', settings.SCALE_K),
            (548, 488),
            settings.LAYERS['main'],
            self.visible_sprites)

        BaseSprite(
            ImgEditor.load_image(f'{self.name}/chair.png', settings.SCALE_K),
            (768, 498),
            settings.LAYERS['main'],
            self.visible_sprites)

        DialogueSprite(
            'сундук',
            False,
            ImgEditor.load_image(f'{self.name}/chest.png', settings.SCALE_K),
            (1362, 526),
            'magnifier',
            settings.LAYERS['main'],
            self.visible_sprites)

        DialogueSprite(
            'барабанная установка',
            False,
            ImgEditor.load_image(f'{self.name}/drums.png', settings.SCALE_K),
            (1264, 708),
            'magnifier',
            settings.LAYERS['main'],
            self.visible_sprites)

        BaseSprite(
            ImgEditor.load_image(f'{self.name}/plates.png', settings.SCALE_K),
            (1332, 644),
            settings.LAYERS['ceiling'],
            self.visible_sprites)

        DialogueSprite(
            'холодильник',
            False,
            ImgEditor.load_image(f'{self.name}/fridge.png', settings.SCALE_K),
            (304, 516),
            'magnifier',
            settings.LAYERS['main'],
            self.visible_sprites)

        DialogueSprite(
            'записки',
            False,
            ImgEditor.load_image(f'{self.name}/notes.png', settings.SCALE_K),
            (478, 478),
            'magnifier',
            settings.LAYERS['main'],
            self.visible_sprites)

        BaseSprite(
            ImgEditor.load_image(f'{self.name}/table.png', settings.SCALE_K),
            (654, 482),
            settings.LAYERS['main'],
            self.visible_sprites)

        DialogueSprite(
            'салат',
            False,
            ImgEditor.load_image(f'{self.name}/salad.png', settings.SCALE_K),
            (640, 466),
            'magnifier',
            settings.LAYERS['main'],
            self.visible_sprites)

        DialogueSprite(
            'коробка с чаем',
            False,
            ImgEditor.load_image(f'{self.name}/tea.png', settings.SCALE_K),
            (210, 562),
            'magnifier',
            settings.LAYERS['main'],
            self.visible_sprites)

        BaseSprite(
            ImgEditor.load_image(f'{self.name}/ceiling.png', settings.SCALE_K),
            (1158, 324),
            settings.LAYERS['ceiling'],
            self.visible_sprites)

        BaseSprite(
            ImgEditor.load_image(f'{self.name}/ceiling1.png', settings.SCALE_K),
            (682, 834),
            settings.LAYERS['ceiling'],
            self.visible_sprites)

        InvisibleDoor(
            (675, 850),
            self,
            'first_street_scene',
            (890, 100),
            'down_idle',
            self.visible_sprites
        )

        InvisibleDoor(
            (1150, 330),
            self,
            'home_upscene',
            (985, 470),
            'up_idle',
            self.visible_sprites
        )
