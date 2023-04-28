import content_access as content
import pygame
import math
import logic
import grphcs
import game

#variables
texture_b = pygame.image.load("textures/back.jpg")
WIDTH, HEIGHT = 640, 480
fps = 30
rays=128
screen = pygame.display.set_mode((WIDTH, HEIGHT))
texture_b = pygame.transform.scale(texture_b, (WIDTH, HEIGHT))

player = game.Player([96, 90], 0.4, 0.08, 5, math.pi/3)
level = game.Level()

g = grphcs.Graphics(WIDTH,HEIGHT,screen)
game.g = g
game.current_level = level

#init
pygame.init()
clock = pygame.time.Clock()
pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

#main cycle
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            running = False
            continue

    screen.blit(texture_b, (0, 0))

#controls
    player.keyboard_movement(pygame.key.get_pressed())

#logic
    collisions = logic.cast_multiple(player, level.layout, game.tile, 12, rays)
    #print(logic.cast_prop(player.coords, player.angle, level.layout, game.tile, 10))
    props=logic.cast_multiple_prop(player, level.layout, game.tile, 12, 16)
    g.draw_walls_textured(player, collisions, 20, (0,0,5), rays)
    print(props)

#drawing
    sctile = 8

    for y in range(len(level.layout)):
        for x in range(len(level.layout[y])):
            if level.layout[y][x]!="." and abs(player.coords[0]//game.tile-x)<5 and abs(player.coords[1]//game.tile-y)<5:
                pygame.draw.rect(screen, pygame.Color('green'), [x*sctile, y*sctile, sctile,sctile])
            else:
                pygame.draw.rect(screen, pygame.Color('black'), [x*sctile, y*sctile, sctile,sctile])

    pygame.draw.circle(screen, pygame.Color('gray'), (WIDTH//2, HEIGHT//2), 1)
    pygame.draw.circle(screen, pygame.Color('green'), [int(player.coords[0]/game.tile*sctile), int(player.coords[1]/game.tile*sctile)], 3)
    #screen.blit(content.gun, (WIDTH//2-100, HEIGHT-175))
    #if any(props):
        #g.draw_props(player,props)
    #print(rays)

#end

    pygame.mouse.set_pos((WIDTH//2, HEIGHT//2))
    pygame.display.flip()
    clock.tick(fps)