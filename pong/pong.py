import pygame
from random import random, choice
from math import cos, sin, pi, atan

auto = True
th = 5

sw, sh = 800 // 2, 600 // 2

width = 7
length = 50
speed = 7
plt1 = list()
plt2 = list()

ballspdincrease = 1.01
ball = [0, 0]
ballv = [0, 0]
radius = 4

rndt = pi / 3

score = [0, 0]
bouncestreak = 0

colors = [(220, 190, 212), (244, 188, 184), (169, 212, 197), (255, 239, 231)]
maincolor = (255, 255, 255)
backcolor = (0, 0, 0)

screen = pygame.display.set_mode((sw, sh))
pygame.init()

clock = pygame.time.Clock()


def reset():
    updatecaption()
    global plt1, plt2, angle, ball, ballv, maincolor, ballspd, bouncestreak
    bouncestreak = 0
    plt1 = [0, (sh - length) // 2, length]
    plt2 = [sw - width, (sh - length) // 2, length]
    angle = random() * pi / 2
    angle = choice((angle + 3 / 4 * pi, angle - 1 / 4 * pi))
    ball = [sw // 2, sh // 2]
    ballspd = 7
    setvector(angle)
    maincolor = (255, 255, 255)
    pygame.time.delay(1000)


def setvector(angle):
    global ballv
    ballv[0] = cos(angle) * ballspd
    ballv[1] = sin(angle) * ballspd


def updatecaption():
    pygame.display.set_caption(f'Pong {score[0]} : {score[1]} Bounce streak: {bouncestreak} AUTO: {auto}')


reset()

while 1:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            quit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP] and plt2[1] > 0 and not auto:
        plt2[1] -= speed
    elif keys[pygame.K_DOWN] and plt2[1] < sh - plt1[2] and not auto:
        plt2[1] += speed

    if keys[pygame.K_w] and plt1[1] > 0 and not auto:
        plt1[1] -= speed
    elif keys[pygame.K_s] and plt1[1] < sh - plt1[2] and not auto:
        plt1[1] += speed

    if auto:
        if ball[0] > sw * 4 / 5 or ballv[0] > 0:
            if ball[1] > plt2[1] + plt2[2] // 2 + th and plt2[1] + plt2[2] < sh:
                plt2[1] += speed
            elif ball[1] < plt2[1] + plt2[2] // 2 - th and plt2[1] > 0:
                plt2[1] -= speed
        if ball[0] < sw // 5 or ballv[0] < 0:
            if ball[1] > plt1[1] + plt1[2] // 2 + th and plt1[1] + plt1[2] < sh:
                plt1[1] += speed
            elif ball[1] < plt1[1] + plt1[2] // 2 - th and plt1[1] > 0:
                plt1[1] -= speed

    pos = 0
    if ball[1] - radius <= 0:
        pos = 1
    elif ball[1] + radius >= sh:
        pos = -1
    if pos != 0:
        ##print('bounce')
        ballv[1] = -ballv[1]
        if pos == 1:
            ball[1] = radius
        else:
            ball[1] = sh - radius

    collided = False

    if 0 < ball[0] < sw:
        if plt1[1] <= ball[1] <= plt1[1] + plt1[2] and ball[0] - radius <= width + plt1[0]:
            ball[0] = width + radius + plt1[0] + 2
            collided = True
        elif plt2[1] <= ball[1] <= plt2[1] + plt2[2] and ball[0] + radius >= plt2[0]:
            ball[0] = plt2[0] - radius - 2
            collided = True
    else:
        ##print('oops')
        if ball[0] > sw // 2:
            score[0] += 1
        else:
            score[1] += 1
        updatecaption()
        reset()

    if collided:
        ##print('bounce')
        bouncestreak += 1
        updatecaption()
        angle = atan(ballv[1] / ballv[0])
        if angle > pi / 3:
            angle = pi / 3
        elif angle < -pi / 3:
            angle = -pi / 3
        angle += (random() - 0.5) * rndt

        if ballv[0] < 0:
            angle += pi

        ballspd *= ballspdincrease

        setvector(angle)
        ballv[0] = -ballv[0]
        maincolor = choice(colors)

    ball[0] += ballv[0]
    ball[1] += ballv[1]

    screen.fill(backcolor)
    pygame.draw.rect(screen, maincolor, (plt1[0], plt1[1], width, plt1[2]))
    pygame.draw.rect(screen, maincolor, (plt2[0], plt2[1], width, plt2[2]))
    pygame.draw.circle(screen, maincolor, ball, radius)
    pygame.draw.line(screen, maincolor, (sw // 2, 0), (sw // 2, sh), 2)
    pygame.display.flip()

    clock.tick(30)
