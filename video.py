from typing import Union

from pygame._sdl2 import video

from config import Config


class Texture(video.Texture):
    def render(self, pos, scale, angle, flip=(0, 0), target: 'Texture' = None):
        renderer: Renderer = self.renderer
        renderer.draw_texture(self, pos, scale, angle, flip, target)


class Image(video.Image):
    pass


class BaseRenderer(video.Renderer):
    """
    Base Renderer class to be extended by other APIs
    """

    def draw_texture(self, texture: Union[Texture, Image], pos, scale, angle, flip=(0, 0), target: Texture = None):
        if isinstance(texture, Texture):
            texture = Image(texture)
        curr_target = self.target
        if target:
            self.target = target
        texture.angle = angle
        dst_rect = texture.get_rect().scale_by(scale)
        dst_rect.center = pos
        texture.flip_x, texture.flip_y = flip
        texture.draw(dstrect=dst_rect)
        self.target = curr_target


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

    def render(self, flush=False):
        if flush or not self.headless:
            self.present()


Window = video.Window
Sprite = Image
