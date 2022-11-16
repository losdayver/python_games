import Figures
from Settings import *
from SharedTypes import *
import Draw

import pygame
import numpy
import random

# Pygame setup

pygame.init()
clock = pygame.time.Clock()

# Surfaces setup

screen = pygame.display.set_mode(display_resolution)
background_surf = pygame.Surface(display_resolution)
Draw.TileTexture(background_surf, tilesize, texture1)
print(screen.get_size())
field_surf = pygame.Surface(game_screen_resolution)
field_surf.fill((150, 150, 150))
blocks_surf = pygame.Surface(game_screen_resolution)
blocks_surf.set_colorkey((0, 0, 0))
Draw.drawGrid(field_surf, tilesize, game_resolution, (140, 140, 140), 1)

field_array = numpy.zeros(game_resolution)

game_score = 0
game_best_score = 0

# Figure setup

current_figure_position = [4, 0]

current_tick_state = fps * game_tick

list_of_figures = [Figures.t_figure]
list_of_figures.append(Figures.s_figure)
list_of_figures.append(Figures.z_figure)
list_of_figures.append(Figures.j_figure)
list_of_figures.append(Figures.l_figure)
list_of_figures.append(Figures.o_figure)
list_of_figures.append(Figures.i_figure)

current_figure = None

figure_queue = []

directional_key_pressed_flag = False
rotation_key_pressed_flag = False
ready_to_place_flag = False


# Collision detection

def placeFigure(fig, x, y):
    for block in fig.current_rotation:
        block_x = block % 4
        block_y = block // 4

        field_array[block_x + x, block_y + y] = 1

        start = Point((x + block_x) * tilesize, (y + block_y) * tilesize)

        pygame.draw.rect(blocks_surf, fig.color, (start.x, start.y, tilesize, tilesize))

        blocks_surf.blit(skin1, (start.x, start.y, tilesize, tilesize), special_flags=pygame.BLEND_RGB_MULT)


def checkBottomCollision(fig, x, y):
    for block in fig.current_rotation:
        block_x = block % 4
        block_y = block // 4

        if block_y + y >= game_resolution.y - 1:
            return True

        if field_array[block_x + x, block_y + y + 1] != 0:
            return True

    return False


def checkSideCollision(fig, x, y, side):
    for block in fig.current_rotation:
        block_x = block % 4
        block_y = block // 4

        if side == 'right':
            if x + block_x >= game_resolution.x - 1:
                return True
            elif field_array[x + block_x + 1, y + block_y] != 0:
                return True

        if side == 'left':
            if x + block_x <= 0:
                return True
            elif field_array[x + block_x - 1, y + block_y] != 0:
                return True

    return False


def checkRotationCollision(fig, x, y, side):
    if side == 'right':
        if len(fig.rotations) - 1 == fig.rotations.index(fig.current_rotation):
            rotation = fig.rotations[0]
        else:
            rotation = fig.rotations[fig.rotations.index(fig.current_rotation) + 1]
    elif side == 'left':
        rotation = fig.rotations[fig.rotations.index(fig.current_rotation) - 1]
    else:
        return False

    for block in rotation:
        block_x = block % 4
        block_y = block // 4

        if y + block_y > game_resolution.y - 1 or x + block_x > game_resolution.x - 1:
            return True

        if x + block_x < 0:
            return True

        if field_array[x + block_x, y + block_y] != 0:
            return True

    return False


def checkFullLines():
    global game_score

    for y in range(game_resolution.y):

        if numpy.sum(field_array.transpose()[y]) == 10:
            field_array[:, 1:y + 1] = field_array[:, :y]

            blocks_subsurf = pygame.transform.chop(blocks_surf, [0, y * tilesize, 0, 20 * tilesize])

            blocks_surf.fill([0, 0, 0], [0, 0, game_screen_resolution.x, (y + 1) * tilesize])

            blocks_surf.blit(blocks_subsurf, [0, tilesize])

            game_score += 10


# Operations

def resetGame():
    global current_figure, field_array

    current_figure.CancelRotation()
    current_figure = random.choice(list_of_figures)

    current_figure_position[1] = 0
    current_figure_position[0] = 4

    game_score = 0

    blocks_surf.fill([0, 0, 0])

    field_array *= 0


def checkKeyPress():
    global directional_key_pressed_flag, rotation_key_pressed_flag, current_tick_state, ready_to_place_flag

    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[keymap['right']] and not directional_key_pressed_flag \
            and not checkSideCollision(current_figure, current_figure_position[0], current_figure_position[1], 'right'):
        current_figure_position[0] += 1
        directional_key_pressed_flag = True
        ready_to_place_flag = False
    elif keys_pressed[keymap['left']] and not directional_key_pressed_flag \
            and not checkSideCollision(current_figure, current_figure_position[0], current_figure_position[1], 'left'):
        current_figure_position[0] -= 1
        directional_key_pressed_flag = True
        ready_to_place_flag = False

    if not keys_pressed[keymap['left']] and not keys_pressed[keymap['right']]:
        directional_key_pressed_flag = False

    if keys_pressed[keymap['r_left']] and not rotation_key_pressed_flag \
            and not checkRotationCollision(current_figure, current_figure_position[0], current_figure_position[1],
                                           'left'):
        current_figure.RotateLeft()
        rotation_key_pressed_flag = True
        ready_to_place_flag = False

    if keys_pressed[keymap['r_right']] and not rotation_key_pressed_flag \
            and not checkRotationCollision(current_figure, current_figure_position[0], current_figure_position[1],
                                           'right'):
        current_figure.RotateRight()
        rotation_key_pressed_flag = True
        ready_to_place_flag = False

    if not keys_pressed[keymap['r_left']] and not keys_pressed[keymap['r_right']]:
        rotation_key_pressed_flag = False

    if keys_pressed[keymap['speed']]: current_tick_state /= 10


def resetFigureQueue():
    global figure_queue

    figure_queue = [random.choice(list_of_figures)]

    for i in range(figure_queue_length - 1):
        figure_queue.append(random.choice(list_of_figures))


def cycleFigures():
    figure = figure_queue[0]

    figure_queue.pop(0)

    figure_queue.append(random.choice(list_of_figures))

    return figure


resetFigureQueue()

current_figure = figure_queue[0]

while 1:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            quit()

    checkKeyPress()

    if game_score > game_best_score:
        game_best_score = game_score

    if numpy.sum(field_array.transpose()[0]) != 0:
        resetGame()

    screen.blit(background_surf, [0, 0])

    screen.blit(field_surf, screen_field_offset)
    screen.blit(blocks_surf, screen_field_offset)

    Draw.drawFigure(screen, tilesize, current_figure, Point(current_figure_position[0], current_figure_position[1]),
                    screen_field_offset,
                    skin1)

    for f, i in zip(figure_queue, range(len(figure_queue))):
        Draw.drawFigure(screen, tilesize // 2, f, Point(0, i * 4),
                        Point(screen_field_offset.x + game_screen_resolution.x + tilesize + 5, tilesize),
                        rotation=f.rotations[0])

    collision_flag = checkBottomCollision(current_figure, current_figure_position[0], current_figure_position[1])

    current_tick_state -= 1
    if current_tick_state <= 0:

        current_tick_state = fps * game_tick

        if collision_flag:

            if not ready_to_place_flag:
                ready_to_place_flag = True
                continue

            placeFigure(current_figure, current_figure_position[0], current_figure_position[1])
            ready_to_place_flag = False

            checkFullLines()

            current_figure.CancelRotation()
            current_figure = cycleFigures()

            current_figure_position[1] = 0
            current_figure_position[0] = 4

            game_score += 1
        else:
            current_figure_position[1] += 1

        pygame.display.set_caption('Tetris. Score: ' + str(game_score) + '. Best: ' + str(game_best_score))

    pygame.display.flip()
    clock.tick(fps)
