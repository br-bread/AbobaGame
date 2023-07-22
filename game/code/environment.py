import pygame
import settings


class Sun:  # for changing light depending on daytime
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.full_surface = pygame.Surface((settings.WIDTH, settings.HEIGHT))
        self.speed = 1  # speed of light changing
        noon = [255, 255, 255]
        evening = [243, 172, 255]
        night = [121, 120, 249]
        self.time = [noon, evening, night]  # different colors of different times
        self.current_time = noon
        self.next_time = evening
        self.next_time_index = 2

    def display(self, delta_time):
        for j in range(3):
            if self.current_time[j] > self.next_time[j]:
                if self.current_time[j] - self.next_time[j] < 0.05:
                    self.current_time[j] = self.next_time[j]
                else:
                    self.current_time[j] -= self.speed * delta_time

            elif self.current_time[j] < self.next_time[j]:
                if self.next_time[j] - self.current_time[j] < 0.05:
                    self.current_time[j] = self.next_time[j]
                else:
                    self.current_time[j] += self.speed * delta_time

        # changing next_time
        if self.current_time == self.next_time:
            self.next_time_index += 1
            if self.next_time_index == len(self.time):
                self.next_time_index = 0
            self.next_time = self.time[self.next_time_index]

        self.full_surface.fill(self.current_time)
        self.screen.blit(self.full_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)


class Rain:
    pass
