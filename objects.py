import pygame

from base import BaseStructure
from utils import Point


class BaseObject(BaseStructure):
    """
    All x, y, z values are considered as relative by default
    For reference, absolute position can be accessed
    """
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x, self.y = x, y
        self.alive = True
        self.z = z  # for sorting
        self.parent: BaseObject | None = None

    def destroy(self):
        self.alive = False

    @staticmethod
    def post_event(event, **kwargs):
        pygame.event.post(pygame.event.Event(event, kwargs))

    @property
    def pos(self):
        return Point(self.x, self.y)

    @pos.setter
    def pos(self, value):
        self.x, self.y = value

    @property
    def absolute(self):
        if self.parent:
            return self.parent.absolute + self.pos
        else:
            return self.pos

    @property
    def rect(self) -> pygame.Rect:
        raise NotImplementedError

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def move_to(self, x, y):
        dx, dy = x - self.x, y - self.y
        self.move(dx, dy)
