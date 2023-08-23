import pygame
from tools import ImgEditor
import settings


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites):
        super().__init__(group)

        # general
        self.image = pygame.Surface((19 * 4, 27 * 4))
        self.rect = self.image.get_rect(center=pos)
        self.game_layer = settings.LAYERS['main']

        # movement
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(pos)
        self.speed = 35 * settings.SCALE_K

        # collision
        self.hitbox = self.rect.copy().inflate((-40, -90))
        self.collision_sprites = collision_sprites

        # animation
        self.animations = {}
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

    def move(self, dt, scene_collision_mask):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # player hitbox mask for checking scene collision mask
        player_hitbox_mask = pygame.mask.Mask((self.hitbox.width, self.hitbox.height))
        player_hitbox_mask.fill()

        self.pos.x += self.direction.x * self.speed * dt
        if scene_collision_mask.overlap(player_hitbox_mask, (self.pos.x, self.pos.y)):  # collision with scene mask
            self.pos.x -= self.direction.x * self.speed * dt

        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx

        self.pos.y += self.direction.y * self.speed * dt
        if scene_collision_mask.overlap(player_hitbox_mask, (self.pos.x, self.pos.y)):  # collision with scene mask
            self.pos.y -= self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y) + 40
        self.rect.centery = self.hitbox.centery - 40

    # animation
    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0 and 'idle' not in self.status:
            self.status = self.status + '_idle'

    def import_frames(self):
        animation_sheet = ImgEditor.load_image('player_animation.png', settings.SCALE_K)
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

    def update(self, delta_time, player_pos, events, screen, scene_collision_mask, *args):
        if not settings.dialogue_run and not settings.window_opened:
            self.input()
        else:
            self.direction.xy = 0, 0
        self.get_status()
        self.animate(delta_time)
        self.move(delta_time, scene_collision_mask)
