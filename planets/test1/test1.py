import pygame
from variables import *
from methods import *
import math as m

pygame.init()
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
running = True

clock = pygame.time.Clock()

while running:
    keypress(pygame.key.get_pressed())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill((255,255,255))

    for y in range(len(level)):
        for x in range(len(level[y])):
            if (level[x][y]==1):
                pygame.draw.rect(screen, (0,0,0), [y*tilesize,x*tilesize,tilesize,tilesize])

    pygame.draw.circle(screen, (0, 255, 0), [p_x, p_y], 12);

    pygame.draw.line(screen, (0,255,0), [p_x, p_y], [p_x+m.cos(p_angle)*view_distance, p_y-m.sin(p_angle)*view_distance])

    pygame.display.update()

    clock.tick(60)

