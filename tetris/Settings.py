import pygame

from SharedTypes import *

keymap = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'r_left': pygame.K_z, 'r_right': pygame.K_UP,
          'speed': pygame.K_DOWN, }

tilesize = 25

screen_field_offset = Point(tilesize, tilesize);

game_resolution = Point(10, 20)

game_screen_resolution = Point(game_resolution.x * tilesize, game_resolution.y * tilesize)

display_resolution = Point((game_resolution.x + 5) * tilesize, (game_resolution.y + 2) * tilesize)

fps = 60

game_tick = 0.2

skin1 = pygame.image.load('skin2.bmp')

texture1 = pygame.Surface(skin1.get_size())
texture1.fill([50, 50, 50])
texture1.blit(skin1, [0, 0], special_flags=pygame.BLEND_RGB_MULT)

color_palette = [(152, 49, 155)]  # t_figure
color_palette.append([192, 45, 12])  # z_figure
color_palette.append([40, 150, 90])  # s_figure
color_palette.append([243, 202, 64])  # o_figure
color_palette.append([36, 123, 160])  # j_figure
color_palette.append([206, 113, 59])  # l_figure
color_palette.append([13, 204, 211])  # i_figure

figure_queue_length = 5
