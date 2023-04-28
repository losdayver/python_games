import pygame
import numpy as np
import random as rnd

tile = 10
pw, ph = 50, 50
screen = pygame.display.set_mode((pw * tile, ph * tile))
fps = 30

clock = pygame.time.Clock()
pygame.init()

marks = np.zeros((pw, ph))
cells = []

for y in range(ph):
    for x in range(pw):
        if rnd.random() < 0.5: cells.append((x, y))


def makemarks(c):
    for x in range(c[0] - 1, c[0] + 2):
        for y in range(c[1] - 1, c[1] + 2):
            if 0 <= x < pw and 0 <= y < ph and not (x - c[0] == y - c[1] == 0):
                marks[x, y] += 1


while 1:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            quit()

    screen.fill((0, 0, 0))

    for c in cells:
        pygame.draw.rect(screen, (255, 255, 0), (c[0] * tile, c[1] * tile, tile, tile))
        makemarks(c)

    for x in range(pw):
        for y in range(ph):
            l = marks[x, y]

            if (x, y) in cells:
                if not 2 <= l <= 3: cells.remove((x, y))
            elif l == 3:
                cells.append((x, y))

    marks *= 0

    pygame.display.flip()
    clock.tick(fps)
