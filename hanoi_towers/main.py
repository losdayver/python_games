import pygame
import time
import threading

pygame.init()
SCREEN = pygame.display.set_mode(
    size=(600, 400)
)
pygame.display.set_caption('Ханойская башня Олег Жмелев')

N = 6
disk_size_multiplier_px = 150//N
disk_height_px = 100//N
rod1 = [N - n for n in range(N)]
rod2 = []
rod3 = []

rods = (rod1, rod2, rod3)

def hanoi_move(n = N, start = 0, end = 2):
    if n == 1:
        buffer = rods[start][-1]
        rods[start].pop()
        rods[end].append(buffer)
        draw()
        time.sleep(0.1)
        return

    other = 3 - (start+end)
    hanoi_move(n-1, start, other)
    hanoi_move(1, start, end)
    hanoi_move(n-1, other, end)

def draw():
    SCREEN.fill(
        color=(255,255,255)
    )

    pygame.draw.line(
        surface=SCREEN,
        color=(0,0,0),
        start_pos=(SCREEN.get_width()/4,SCREEN.get_height()*(1 - 1/5)),
        end_pos=(SCREEN.get_width()*(1-1/4), SCREEN.get_height()*(1 - 1/5)),
        width=10
    )

    for i in range(3):
        pygame.draw.line(
            surface=SCREEN,
            color=(0, 0, 0),
            start_pos=(SCREEN.get_width() * (1 - (1 + i) / 4), SCREEN.get_height() * (1 - 1 / 5)),
            end_pos=(SCREEN.get_width() * (1 - (1 + i) / 4), SCREEN.get_height()/ 3),
            width=10
        )

    for j, rod in enumerate(rods):
        for i, disk in enumerate(rod):
            rect = [SCREEN.get_width() * (1 - (3 - j) / 4) - disk * disk_size_multiplier_px / 2,
                      SCREEN.get_height() * (1 - 1 / 5) - disk_height_px * (i + 1),
                      disk_size_multiplier_px * disk, disk_height_px]

            pygame.draw.rect(
                surface=SCREEN,
                color=[0,255,255],
                rect=rect
            )

            pygame.draw.rect(
                surface=SCREEN,
                color=[0, 0, 0],
                rect=rect,
                width=2
            )
    pygame.display.flip()

thread1 = threading.Thread(target=hanoi_move)
thread1.start()

while 1:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            quit()
