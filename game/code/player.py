import pygame
from tools import ImgEditor
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        # general
        self.image = pygame.Surface((19 * 4, 27 * 4))
        self.rect = self.image.get_rect(center=pos)
        self.game_layer = LAYERS['main']

        # movement
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(pos)
        self.speed = 140

        # animation
        self.import_frames()
        self.status = 'down'
        self.frame = 0
        self.animation_speed = 6.5

    # movement
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0

    def move(self, dt):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    # animation
    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0 and not 'idle' in self.status:
            self.status = self.status + "_idle"

    def import_frames(self):
        animation_sheet = ImgEditor.enhance_image(ImgEditor.load_image("player_animation.png"), 4)
        frames = ImgEditor.cut_sheet(animation_sheet, 4, 4)
        self.animations = {
            'down': frames[:4],
            'up': frames[4:8],
            'right': frames[8:12],
            'left': frames[12:],
            'down_idle': [frames[0]],
            'up_idle': [frames[4]],
            'right_idle': [frames[8]],
            'left_idle': [frames[12]]}

    def animate(self, dt):
        animation = self.animations[self.status]

        self.frame += self.animation_speed * dt
        if self.frame >= len(animation):
            self.frame = 0

        self.image = animation[int(self.frame)]
        self.rect = self.image.get_rect()

    def update(self, delta_time, *args):
        self.input()
        self.get_status()
        self.animate(delta_time)
        self.move(delta_time)
