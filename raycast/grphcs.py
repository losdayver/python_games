import math
import pygame
import game
import logic
import content_access as content

class Graphics:
    def __init__(self, WIDTH, HEIGHT, surf):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.surf = surf

    def draw_walls_textured(self, player, list_of_collisions, fog_clip, fog_color, rays):
        def takedist(e):
            return e[2]

        list_of_collisions.sort(key=takedist)

        for col in list_of_collisions:
            try:
                xc = col[0]
                yc = col[1]
                r = col[2]
                orient = col[3]
                angle = col[4]

                d = 360*(player.fov/2*math.pi)/(2*math.tan(player.fov/2))
                h = ((d*game.tile/r)*game.tile_hscale)/math.cos(angle - player.angle)
                h = min((int(h), self.HEIGHT*3))

                c = 255*h/self.HEIGHT
                c-=fog_clip
                c = min([c, 255])
                c = max([c, 0])
                c=int(c)
                if orient==-1: c//=1.5
                c = (255-c)

                offset = 0

                if orient==1: offset = yc
                else: offset = xc

                offset = -(offset % game.tile)

                surf = pygame.Surface((1, game.tile))
                surf_d = pygame.Surface((1, game.tile)).convert_alpha()

                surf_d.fill((fog_color[0], fog_color[1], fog_color[2], c))
                surf.blit(game.tiles[col[5]], (offset, 0))
                surf.blit(surf_d, (0,0))

                display_c = pygame.transform.scale(surf , (self.WIDTH//rays, h))

                #pygame.draw.rect(screen, (c, c, c), [(WIDTH//rays)*i, (HEIGHT-h)//2, WIDTH//rays, h])
                self.surf.blit(display_c, ((self.WIDTH//rays)*col[6], (self.HEIGHT-h)//2))
            except:
                pass

    def draw_props(self, player, props):
        for p in props:
            angle=0
            r=math.dist(player.coords, (p[0]*game.tile+game.tile//2, p[1]*game.tile+game.tile//2))


            #angle=math.atan()

            d = 360*(player.fov/2*math.pi)/(2*math.tan(player.fov/2))
            h = ((d*game.tile/r)*game.tile_hscale)/math.cos(abs(player.angle))
            h = min((int(h), self.HEIGHT*3))

            image=content.barrel

            pygame.transform.scale(image, (h, h))
            self.surf.blit(image, (0,0))