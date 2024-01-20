import dis
import inspect
import time
from typing import Union

import pygame

clamp = pygame.math.clamp
Vec2 = Vector2 = Coordinate = Point = pygame.Vector2
lerp = pygame.math.lerp


def slerp(x, to, amt):
    amt = clamp(amt, -1, 1)
    return Point(x, x).slerp([to, to], amt).x


def map_value(value, from_min, from_max, to_min, to_max):
    clamped_value = max(min(value, from_max), from_min)
    mapped_value = (clamped_value - from_min) / (from_max - from_min) * (to_max - to_min) + to_min
    return mapped_value


class Color(pygame.Color):
    def blend(self, other: 'Color'):
        return self * other

    def blend_mul(self, other: 'Color'):
        self.r = int(clamp(self.r * other.r / 255, 0, 255))
        self.g = int(clamp(self.g * other.g / 255, 0, 255))
        self.b = int(clamp(self.b * other.b / 255, 0, 255))
        self.a = int(clamp(self.a * other.a / 255, 0, 255))
        return self

    def __mul__(self, other: Union[int, float, 'Color']):
        if isinstance(other, int) or isinstance(other, float):
            self.r = int(clamp(self.r * other, 0, 255))
            self.g = int(clamp(self.g * other, 0, 255))
            self.b = int(clamp(self.b * other, 0, 255))
            return self
        else:
            return super().__mul__(other)


class UtilTimer:
    def __init__(self, timeout=0.0, reset=True, callback=None):
        self.timeout = timeout
        self.timer = time.time()
        self.paused_timer = time.time()
        self.paused = False
        self._reset = reset
        self.callback = callback

    def reset(self):
        self.timer = time.time()

    def pause(self):
        self.paused = True
        self.paused_timer = time.time()

    def resume(self):
        self.paused = False
        self.timer -= time.time() - self.paused_timer

    @property
    def elapsed(self):
        if self.paused:
            return time.time() - self.timer - (time.time() - self.paused_timer)
        return time.time() - self.timer

    @property
    def tick(self):
        if self.elapsed > self.timeout:
            if self._reset:
                self.timer = time.time()  # reset timer
            if self.callback:
                self.callback()
            return True
        else:
            return False


# this class is based on the following answer
# https://stackoverflow.com/questions/16481156/find-out-into-how-many-values-a-return-value-will-be-unpacked
class Enum:
    def __init__(self, name=None, f=None):
        self.name = name
        self.f = f

    def __iter__(self):
        def expecting(offset=0):
            """Return how many values the caller is expecting"""
            f = inspect.currentframe().f_back.f_back
            i = f.f_lasti + offset
            bytecode = f.f_code.co_code
            instruction = bytecode[i]
            if instruction == dis.opmap['UNPACK_SEQUENCE']:
                return bytecode[i + 1]
            elif instruction == dis.opmap['POP_TOP']:
                return 0
            else:
                return 1

        c = expecting(offset=0)  # 0 because this is currently at unpack OP, otherwise use 3
        if self.name is None:
            r = range(c)
        else:
            if isinstance(self.name, int):
                r = range(self.name, self.name + c)
            elif isinstance(self.name, str):
                r = (f'{self.name}_{i}' for i in range(c))
            else:
                raise ValueError("Invalid argument to Enum")
        if self.f:
            yield from (self.f(i) for i in r)
        else:
            yield from r
