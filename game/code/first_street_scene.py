import pygame
from settings import *
from core import BaseScene, BaseSprite


class FirstStreetScene(BaseScene):
    def __init__(self, background, background_pos=(0, 0)):
        super().__init__(background, background_pos)

