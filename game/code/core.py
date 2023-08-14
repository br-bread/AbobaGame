import pygame
from math import sqrt
import settings
from tools import ImgEditor
from player import Player
from overlay import Daytime, MenuWindow


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


class BaseAnimatedSprite(BaseSprite):
    def __init__(self, animation_sheet, pos, speed, columns, rows, layer=settings.LAYERS['main'], *groups):
        super().__init__(animation_sheet, pos, layer, *groups)
        self.animation = ImgEditor.cut_sheet(animation_sheet, columns, rows)
        self.animation_speed = speed
        self.frame = 0

    def animate(self, dt):
        self.frame += self.animation_speed * dt
        if self.frame >= len(self.animation):
            self.frame = 0

        self.image = self.animation[int(self.frame)]
        self.rect = self.image.get_rect()

    def update(self, delta_time, *args):
        self.animate(delta_time)


class InteractiveSprite(BaseSprite):
    def __init__(self, img, pos, layer=settings.LAYERS['main'], *groups):
        super().__init__(img, pos, layer, *groups)
        self.cursor_image = None

    def is_accessible(self, distance):
        if distance <= settings.INTERACTION_DISTANCE:
            return True
        return False

    def update(self, dt, events, player_pos, *args, **kwargs):
        if self.is_mouse_on() and not settings.window_opened:
            if self.is_accessible(self.get_distance(player_pos)):
                img = ImgEditor.load_image(f'cursors/{self.cursor_image}')
            else:
                img = ImgEditor.load_image(f'cursors/inaccessible/{self.cursor_image}')
            settings.current_cursor = ImgEditor.enhance_image(img, 4)


class BaseScene:
    def __init__(self, background, scene_collision_mask, music, background_pos=(0, 0)):
        # sprite groups
        self.visible_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        # general
        self.screen = pygame.display.get_surface()
        self.player = Player(settings.CENTER, self.visible_sprites, self.collision_sprites)
        self.name = 'scene'
        self.music = pygame.mixer.Sound(f'..\\assets\\audio\\music\\{music}')
        self.music_started = False
        self.collision_mask = scene_collision_mask
        self.background = BaseSprite(background, background_pos, settings.LAYERS['background'], self.visible_sprites)
        self.menu_window = MenuWindow()  # overlay
        # animation
        self.appearing = True  # if appearing animation should be shown
        self.disappearing = False  # same
        self.place_player = True  # to place player on scene at the appearing
        self.speed = 500
        self.surface = pygame.Surface((settings.WIDTH, settings.HEIGHT))
        self.surface.fill('black')
        self.alpha = 255
        self.next_scene = None  # will be set when current scene is disappearing

    def disappear(self, next_scene, player_pos, player_status):
        if self.alpha < 255:  # disappear method can be called even when scene has disappeared
            self.disappearing = True  # so this parameter will be set wrong (without this if statement)
        # set player pos in next scene
        settings.player_pos = player_pos
        settings.player_status = player_status
        self.next_scene = next_scene

    def run(self, delta_time, events):
        if not self.music_started:
            self.music.play(loops=-1)
            self.music_started = True
        if self.place_player:  # placing the player
            self.player.pos.x = settings.player_pos[0]
            self.player.pos.y = settings.player_pos[1]
            self.player.status = settings.player_status
            self.place_player = False
        self.visible_sprites.draw_sprites(self.player)
        if self.appearing:
            self.surface.set_alpha(self.alpha)
            self.screen.blit(self.surface, (0, 0))
            self.alpha -= self.speed * delta_time
            if self.alpha <= 0:
                self.appearing = False

        if self.disappearing:
            self.music.fadeout(1000)
            self.surface.set_alpha(self.alpha)
            self.screen.blit(self.surface, (0, 0))
            self.alpha += self.speed * delta_time
            if self.alpha >= 255:
                self.disappearing = False
                self.appearing = True  # set bool variables for next appearance of this scene
                self.place_player = True
                self.music_started = False
                settings.scene = self.next_scene

        Daytime.run(self.screen)
        settings.inventory.run(self.screen, delta_time, events)
        settings.journal.run(self.screen, delta_time, events)
        self.menu_window.run(self.screen, delta_time, events, self)

        # collision debug
        # self.screen.blit(self.collision_mask.to_surface(), (0, 0))
        # player_hitbox_mask = pygame.mask.Mask((self.player.hitbox.width, self.player.hitbox.height))
        # player_hitbox_mask.fill()
        # self.screen.blit(player_hitbox_mask.to_surface(), (self.player.pos[0], self.player.pos[1]))
        # pygame.draw.rect(self.screen, 'red', self.player.hitbox, 5)

        self.visible_sprites.update(delta_time, events, self.player.pos, self.screen, self.collision_mask)




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
