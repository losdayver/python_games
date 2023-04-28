import pygame
import random as rng

keys_to_direction={'right':(1,0), 'up':(0,-1), 'left':(-1,0), 'down':(0,1)}
keys={'right':pygame.K_RIGHT, 'up':pygame.K_UP, 'left':pygame.K_LEFT, 'down':pygame.K_DOWN}
dw,dh=512,512
l=3
tile=32
dimensions=(dw//tile,dh//tile)
direction=(0,1)
food=(rng.randint(1,dw//tile-1), rng.randint(1,dh//tile-1))
last_direction=direction
stack=list()

for i in range(l):
    stack.append((5+i,5))

def normalize(point):
    x=point[0]*tile+tile//2
    y=point[1]*tile+tile//2

    return (x,y)

def move(d):
    global last_direction
    global l
    global food

    x=last_direction[0]
    y=last_direction[1]
    if last_direction!=d and (last_direction[0]!=-d[0] and last_direction[1]!=-d[1]):
        x=d[0]
        y=d[1]
        last_direction=d

    point=(x+stack[-1][0],y+stack[-1][1])

    if food==point:
        l+=1
        food=(rng.randint(1,dw//tile-1), rng.randint(1,dh//tile-1))

    if point in stack or not(-1<point[0]<dimensions[0]) or not(-1<point[1]<dimensions[1]):
        pygame.quit()
        exit()


    stack.append(point)

screen = pygame.display.set_mode((dw,dh))
pygame.init()

fps=120
timer=fps
clock=pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill((0,0,0))

    keys_pressed=pygame.key.get_pressed()

    if keys_pressed[keys['right']]:
        direction=keys_to_direction['right']
    elif keys_pressed[keys['up']]:
        direction=keys_to_direction['up']
    elif keys_pressed[keys['left']]:
        direction=keys_to_direction['left']
    elif keys_pressed[keys['down']]:
        direction=keys_to_direction['down']

    if timer%30==0:
        move(direction)

        if len(stack)>l:
            stack.pop(0)

    pygame.draw.circle(screen, (255,0,0), normalize(food), tile//3)

    for i in range(1,len(stack)):
        pygame.draw.line(screen, (0,int((255/len(stack))*i),150), normalize(stack[i-1]), normalize(stack[i]), tile//2)

    pygame.display.flip()
    clock.tick(fps)

    if timer>1: timer-=1
    else: timer=fps