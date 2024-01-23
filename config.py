from pygame._sdl2.video import SCALEQUALITY_NEAREST


class Config:
    class Display:
        W = WIDTH = 1000
        H = HEIGHT = 800
        TARGET_FPS = 60
        FPS = 240
        CLEAR_COLOR = (0, 0, 0, 255)
        VSYNC = True
        RESIZABLE = True
        ALWAYS_ON_TOP = False
        BORDERLESS = False

    class Debug:
        pass

    class Texture:
        DEFAULT_SCALE_QUALITY = SCALEQUALITY_NEAREST
        TEXTURE_ATLAS_MAX_DIMENSION = 1024

    class GameInfo:
        NAME = 'Untitled Game'
        VERSION = [0, 0, 0, 0]
