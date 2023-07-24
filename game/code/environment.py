import pygame
import settings


class Sun:  # for changing light and daytime
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.full_surface = pygame.Surface((settings.WIDTH, settings.HEIGHT))
        self.speed = 15  # speed of light changing
        # 434 color steps during the whole day, and 144 time steps (24*6)
        noon = [255, 255, 255]  # 100 (255 - 155)
        evening = [255, 155, 213]  # 159 (255 - 96)   434 total
        night = [96, 80, 185]  # 175 (255 - 80)
        self.time = [noon, evening, night]  # different colors of different times
        self.current_time = noon[:]
        self.next_time = evening[:]
        self.next_time_index = 1
        # for self.step color steps there is one time step (+10 min)
        self.step = 434 // 144  # 3
        self.last_time = noon[:]  # color which was <=10min ago

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

            for i in range(3):
                if abs(self.current_time[i] - self.last_time[i]) >= self.step:
                    self.last_time = self.current_time[:]
                    settings.time['minutes'] += 1
                    if settings.time['hours'] == 11 and settings.time['minutes'] == 6:
                        self.current_time = self.time[0][:]
                    break

        # changing next_time
        if self.current_time == self.next_time:
            self.next_time_index += 1
            if self.next_time_index == len(self.time):
                self.next_time_index = 0
            self.next_time = self.time[self.next_time_index][:]
        if settings.time['minutes'] >= 6:
            settings.time['hours'] += 1
            settings.time['minutes'] = 0
        if settings.time['hours'] == 24:
            settings.time['hours'] = 0

        self.full_surface.fill(self.current_time)
        self.screen.blit(self.full_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)


class Rain:
    pass
