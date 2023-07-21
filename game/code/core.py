import pygame
from math import sqrt
import settings
from tools import ImgEditor
from player import Player


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, img, pos, layer=settings.LAYERS['main'], *groups):
        super().__init__(*groups)
        self.image = img
        self.rect = self.image.get_rect(center=pos)
        self.game_layer = layer

    def is_mouse_on(self):
        pos_x = pygame.mouse.get_pos()[0]
        pos_y = pygame.mouse.get_pos()[1]
        if self.rect.x + self.rect[2] >= pos_x >= self.rect.x and self.rect.y + self.rect[3] >= pos_y >= self.rect.y:
            return True
        else:
            return False

    def get_distance(self, player_pos):
        # returns distance from player
        distance = sqrt((self.rect.centerx - player_pos.x) ** 2 + (self.rect.centery - player_pos.y) ** 2)
        return distance


class InteractiveSprite(BaseSprite):
    def __init__(self, img, pos, layer=settings.LAYERS['main'], *groups):
        super().__init__(img, pos, layer, *groups)
        self.cursor_image = None

    def is_accessible(self, distance):
        if distance <= settings.INTERACTION_DISTANCE:
            return True
        return False

    def update(self, dt, player_pos, *args, **kwargs):
        if self.is_mouse_on():
            if self.is_accessible(self.get_distance(player_pos)):
                img = ImgEditor.load_image(f'cursors/{self.cursor_image}')
            else:
                img = ImgEditor.load_image(f'cursors/inaccessible/{self.cursor_image}')
            settings.current_cursor = ImgEditor.enhance_image(img, 4)


class BaseScene:
    def __init__(self, background, scene_collision_mask, background_pos=(0, 0)):
        # sprite groups
        self.visible_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        # general
        self.screen = pygame.display.get_surface()
        self.player = Player(settings.CENTER, self.visible_sprites, self.collision_sprites)
        self.name = 'scene'
        self.collision_mask = scene_collision_mask
        self.background = BaseSprite(background, background_pos, settings.LAYERS['background'], self.visible_sprites)
        # animation
        self.appearing = True  # if appearing animation should be shown
        self.disappearing = False  # same
        self.speed = 500
        self.surface = pygame.Surface((settings.WIDTH, settings.HEIGHT))
        self.surface.fill('black')
        self.alpha = 255
        self.next_scene = None  # will be set when current scene is disappearing

    def disappear(self, next_scene):
        self.disappearing = True
        self.alpha = 0
        self.next_scene = next_scene

    def run(self, delta_time, events):
        self.visible_sprites.draw_sprites(self.player)
        if self.appearing:
            self.surface.set_alpha(self.alpha)
            self.screen.blit(self.surface, (0, 0))
            self.alpha -= self.speed * delta_time
            if self.alpha <= 0:
                self.appearing = False

        if self.disappearing:
            self.surface.set_alpha(self.alpha)
            self.screen.blit(self.surface, (0, 0))
            self.alpha += self.speed * delta_time
            if self.alpha >= 255:
                self.appearing = False
                settings.scene = self.next_scene

        # collision debug
        # self.screen.blit(self.collision_mask.to_surface(), (0, 0))
        # player_hitbox_mask = pygame.mask.Mask((self.player.hitbox.width, self.player.hitbox.height))
        # player_hitbox_mask.fill()
        # self.screen.blit(player_hitbox_mask.to_surface(), (self.player.pos[0], self.player.pos[1]))
        # pygame.draw.rect(self.screen, 'red', self.player.hitbox, 5)

        self.visible_sprites.update(delta_time, self.player.pos, events, self.screen, self.collision_mask)


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        # self.offset = [0, 0]

    def draw_sprites(self, player):
        # self.offset[0] = player.rect.centerx - settings.CENTER[0]
        # self.offset[1] = player.rect.centery - settings.CENTER[1]
        for layer in settings.LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda x: x.rect.centery):  # fake 3d effect
                if sprite.game_layer == layer:
                    self.screen.blit(sprite.image, sprite.rect)
