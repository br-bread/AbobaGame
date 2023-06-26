import pygame
from tools import ImgEditor
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites):
        super().__init__(group)

        # general
        self.image = pygame.Surface((19 * 4, 27 * 4))
        self.rect = self.image.get_rect(center=pos)
        self.game_layer = LAYERS['main']

        # movement
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(pos)
        self.speed = 140

        # collision
        self.hitbox = self.rect.copy().inflate((-40, -80))
        self.collision_sprites = collision_sprites

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

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if sprite.hitbox.colliderect(self.hitbox):
                if direction == 'h':
                    if self.direction.x > 0:  # right
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:  # left
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                    self.pos.x = self.hitbox.centerx
                elif direction == 'v':
                    if self.direction.y > 0:  # down
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:  # up
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery
                    self.pos.y = self.hitbox.centery

    def move(self, dt):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('h')

        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('v')

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
