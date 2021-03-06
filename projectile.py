# -*- coding: utf-8 -*-

import os
import sys

# If we're on Windows, use the included compiled DLLs.
if sys.platform == "win32":
    os.environ["PYSDL2_DLL_PATH"] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'libs')

from sdl2 import *
import sdl2.ext

from const import WindowSize

RESOURCES = sdl2.ext.Resources(__file__, 'resources')


class Facing:
    LEFT_DOWN = 0
    DOWN = 1
    RIGHT_DOWN = 2
    RIGHT = 3
    RIGHT_UP = 4
    UP = 5
    LEFT_UP = 6
    LEFT = 7
    COUNT = 8


class Projectile:
    def __init__(self, renderer):
        self.renderer = renderer

        self.sprite_size = 64

        self.projectile_sprites = RESOURCES.get_path("player_standing.png")

        self.factory = sdl2.ext.SpriteFactory(
            sdl2.ext.TEXTURE,
            renderer=self.renderer
        )

        self.sprite_sheet = self.factory.from_image(self.projectile_sprites)

        self.facing = Facing.LEFT_DOWN
        self.last_facing = self.facing

        self.frame_index = 0

    def update(self, facing, elapsed_time):

        self.facing = facing

        self.frame_index += 1

        if self.facing != self.last_facing:
            self.frame_index = 0

        if self.frame_index == (self.sprite_sheet.size[0] / self.sprite_size):
            self.frame_index = 0

        self.last_facing = self.facing

    def draw(self):

        renderer = self.renderer.renderer
        facing = self.facing
        frame_index = self.frame_index

        sprite = self.sprite_sheet
        sprite_size = self.sprite_size

        src_rect = SDL_Rect()

        src_rect.x = frame_index * sprite_size
        src_rect.y = facing * sprite_size
        src_rect.w = sprite_size
        src_rect.h = sprite_size

        dest_rect = SDL_Rect()

        dest_rect.x = int((WindowSize.WIDTH / 2) - (sprite_size / 2))
        dest_rect.y = int((WindowSize.HEIGHT / 2) - (sprite_size / 2))
        dest_rect.w = sprite_size
        dest_rect.h = sprite_size

        render.SDL_RenderCopy(renderer, sprite.texture, src_rect, dest_rect)

