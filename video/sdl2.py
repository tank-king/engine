from typing import Union

from pygame._sdl2 import video


class Texture(video.Texture):
    pass


class Image(video.Image):
    pass


class Renderer(video.Renderer):
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


Window = video.Window
Sprite = Image
