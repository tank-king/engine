import pygame.event

from utils import Point
from video import Renderer


class BaseStructure:
    def update(self, events: list[pygame.event.Event], dt: float = 1.0):
        pass

    def draw(self):
        pass
