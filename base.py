import pygame.event

from utils import Point


class BaseStructure:
    def update(self, events: list[pygame.event.Event], dt: float = 1.0):
        pass

    def draw(self, pos: Point, scale: float = 1.0, angle: float = 0.0):
        pass
