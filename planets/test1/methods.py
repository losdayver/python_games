import variables as v
import variables
import math as m
import pygame

def keypress(keys):
    if keys[pygame.K_a]:
        p_x-=v.p_speed
    elif keys[pygame.K_d]:
        p_x+=v.p_speed

    if keys[pygame.K_w]:
        p_y-=v.p_speed
    elif keys[pygame.K_s]:
        p_y+=v.p_speed

    if keys[pygame.K_LEFT]:
        p_angle+=v.rot_speed
    elif keys[pygame.K_RIGHT]:
        p_angle-=v.rot_speed

    if v.p_angle >= 2*m.pi:
        p_angle = 0
    elif v.p_angle < 0:
        p_angle = 2*m.pi+v.p_angle