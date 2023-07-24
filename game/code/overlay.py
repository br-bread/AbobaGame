import pygame
import settings


class Daytime:
    @staticmethod
    def run(screen, delta_time):
        hours = int(settings.time['hours'])
        if hours < 10:
            hours = '0' + str(hours)
        minutes = int(settings.time['minutes'])
        curr_time = str(hours) + ':' + str(minutes) + '0'
        time_surf = pygame.font.Font(settings.FONT, 65).render(curr_time, False, settings.TEXT_COLOR)
        screen.blit(time_surf, settings.TIME_COORDS)
