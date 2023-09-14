import pygame


class MusicPlayer:
    def __init__(self):
        self.music_name = ''
        self.new_name = ''
        self.music = None
        self.is_changing = False
        self.fading_time = 0

    def run(self, dt):
        if self.is_changing:
            self.fading_time += dt
        if self.fading_time >= 0.7:
            self.fading_time = 0
            self.is_changing = False
            self.set_music(self.new_name)

    def play(self):
        self.music.play(loops=-1)

    def set_music(self, new_name):
        self.is_changing = False
        self.music_name = new_name
        self.music = pygame.mixer.Sound(f'..\\assets\\audio\\music\\{self.music_name}')
        self.play()
        self.music.set_volume(0.5)

    def change_music(self, new_name):
        if new_name != self.music_name:
            self.is_changing = True
            self.new_name = new_name
            self.fadeout()

    def stop_music(self):
        self.music.stop()

    def fadeout(self):
        self.music.fadeout(1000)
