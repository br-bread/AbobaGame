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

    def run(self, delta_time, events):
        super().run(delta_time, events)
        if (settings.time['hours'] >= 18 or settings.time[
            'hours'] < 7) and settings.music_player.music_name != 'street_night.mp3':
            self.music_name = 'street_night.mp3'
            settings.music_player.change_music('street_night.mp3')

        elif 7 <= settings.time['hours'] < 18 and settings.music_player.music_name != 'street_day.mp3':
            self.music_name = 'street_day.mp3'
            settings.music_player.change_music('street_day.mp3')
