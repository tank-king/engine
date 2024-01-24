from typing import Union

import pygame
from pygame._sdl2 import video

from config import Config


class GPUTexture(video.Texture):
    def render(self, pos, scale, angle, flip=(0, 0), target: 'GPUTexture' = None):
        renderer: Renderer = self.renderer
        renderer.draw_texture(self, pos, scale, angle, flip, target)


class Texture(video.Image):
    pass


class BaseRenderer(video.Renderer):
    """
    Base Renderer class to be extended by other APIs
    """

    def draw_texture(self, texture: Union[GPUTexture, Texture], pos, scale, angle, flip=(0, 0),
                     target: GPUTexture = None):
        if isinstance(texture, GPUTexture):
            texture = Texture(texture)
        curr_target = self.target
        if target:
            self.target = target
        texture.angle = angle
        dst_rect = texture.get_rect().scale_by(scale)
        dst_rect.center = pos
        texture.flip_x, texture.flip_y = flip
        texture.draw(dstrect=dst_rect)
        self.target = curr_target

    def render(self):
        self.present()


class TextureManager:
    def __init__(self, renderer: 'Renderer'):
        self.renderer = renderer
        self.atlases = []

    def generate_atlases(self, count, width=1024, height=1024):
        s = pygame.Surface([width, height])
        return [GPUTexture.from_surface(self.renderer, s) for _ in range(count)]

    def load_image(self, path):
        return


class Renderer(BaseRenderer):
    """
    Class to handle window creation and associate a render with it
    """

    def __init__(self, size=None, headless=False, **kwargs):
        if not size:
            size = Config.Display.W, Config.Display.H
        defaults = {
            'resizable': Config.Display.RESIZABLE,
            'always_on_top': Config.Display.ALWAYS_ON_TOP,
            'borderless': Config.Display.BORDERLESS
        }
        for i, j in kwargs:
            defaults[i] = j
        self.headless = headless
        self.window = Window(Config.GameInfo.NAME, size, hidden=headless, **kwargs)
        super().__init__(self.window, vsync=Config.Display.VSYNC, target_texture=True)

        self.texture_manager = TextureManager(self)

    def render(self, flush=False):
        if flush or not self.headless:
            self.present()


Window = video.Window
Sprite = Texture
