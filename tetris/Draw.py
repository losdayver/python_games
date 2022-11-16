from SharedTypes import *

import pygame


def drawGrid(draw_surface, tile_size, resolution, line_color, line_width):
    for x in range(resolution.x):
        pygame.draw.line(draw_surface, line_color, [x * tile_size, 0], [x * tile_size, tile_size * 20], line_width)
    for y in range(resolution.y):
        pygame.draw.line(draw_surface, line_color, [0, tile_size * y], [tile_size * 10, tile_size * y], line_width)


def drawFigure(draw_surface, tile_size, figure, location, offset=Point(0, 0), skin=None, rotation=None):
    if rotation == None: rotation = figure.current_rotation

    for block in rotation:
        block_x = block % 4
        block_y = block // 4

        start = Point(offset.x + (location.x + block_x) * tile_size,
                      offset.y + (location.y + block_y) * tile_size)

        pygame.draw.rect(draw_surface, figure.color, (start.x, start.y, tile_size, tile_size))

        if skin != None:
            draw_surface.blit(skin, (start.x, start.y, tile_size, tile_size), special_flags=pygame.BLEND_RGB_MULT)


def TileTexture(draw_surface : pygame.Surface, tile_size, texture):
    for y in range(draw_surface.get_size()[1] // tile_size):
        for x in range(draw_surface.get_size()[0] // tile_size):
            draw_surface.blit(texture, [x * tile_size, y * tile_size])

