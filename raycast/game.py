import content_access as content

import math
import pygame
import logic
import grphcs

tile = 32
tile_hscale = 1.5

g = None
current_level = None

sensitivity = 0.002

tiles = {'1':content.texture1, '2':content.texture2, '3':content.texture3, '4':content.texture4}
props = {'o':content.barrel}

class Instance:
    def __init__(self, coords):
        self.coords = list()
        self.coords = [coords[0], coords[1]]

class Player(Instance):
    def __init__(self, coords, angle, rot_vel, vel, fov):
        super().__init__(coords)

        self.angle = angle
        self.rot_vel = rot_vel
        self.vel = vel
        self.controls = {
            'turn_left':pygame.K_LEFT,
            'str_right':pygame.K_d,
            'str_left':pygame.K_a,
            'turn_right':pygame.K_RIGHT,
            'forward':pygame.K_w,
            'backward':pygame.K_s,
            'action':pygame.K_e
            }
        self.fov = fov

    def check_collide(self, coords):
        x=int(coords[0]/tile)
        y=int(coords[1]/tile)

        if current_level.layout[y][x] != '.': return True
        return False

    def go(self, angle, vel):
        y=math.sin(angle)*vel
        x=math.cos(angle)*vel

        bound=3

        if not self.check_collide((self.coords[0]+x*bound,self.coords[1]-y*bound)):
            self.coords[1]-=y
            self.coords[0]+=x

    def keyboard_movement(self, keys):
        if keys[self.controls['turn_left']]:
            self.angle+=self.rot_vel
        if keys[self.controls['turn_right']]:
            self.angle-=self.rot_vel

        if keys[self.controls['forward']]:
            self.go(self.angle, self.vel)
        if keys[self.controls['backward']]:
            self.go(self.angle, -self.vel)

        if keys[self.controls['str_left']]:
            self.go(self.angle+math.pi/2, self.vel*0.4)
        if keys[self.controls['str_right']]:
            self.go(self.angle-math.pi/2, self.vel*0.4)

        self.angle-=(pygame.mouse.get_pos()[0]-g.WIDTH//2)*sensitivity

        self.angle = logic.normalize_angle(self.angle)

class Prop(Instance):
    def __init__(self, x, y, symbol, sprite):
        super().__init__((x,y))

        self.sprite = sprite

class Level:
    def __init__(self):
        self.layout = level = [
                      "11314111211121213111",
                      "1o.....2...........1",
                      "1.....o2..2..2o.2..1",
                      "113..112...........2",
                      "1....3....2..2..2..1",
                      "1....1..........2..1",
                      "1....21.141311..2..4",
                      "311.11..1....1.....1",
                      "1...4..o2....1..2..1",
                      "4...1...1....1..2..1",
                      "3.111.......o1.....2",
                      "1...2...4....1..2..2",
                      "111.1133113121..2..1",
                      "1....1.............1",
                      "3....2..1114241..231",
                      "3....2..3..........3",
                      "3....1..3..........4",
                      "3.......1..........1",
                      "31111122311121111111",
                      ]



##class Tile:
##    def __init__(self, texture, id, symbol):
##        self.texture = texture
##        self.id = id
##        self.symbol = symbol