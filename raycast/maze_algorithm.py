import random
import pygame

pygame.init()

#configure
tile = 5
dimensions = (100,100)
#configure

screen = pygame.display.set_mode((tile*dimensions[0], tile*dimensions[1]))

nodes = list()
stack = list()

color = pygame.Color('white')
color1 = pygame.Color('green')
color2 = pygame.Color('red')

nodes.append((1, random.randint(1, dimensions[1]+1)))
stack.append(nodes[0])

def test_empty(point):
    #right up left down
    vector = [False, False, False, False]

    if point[0]<dimensions[0] and not (point[0]+1, point[1]) in nodes:
        vector[0]=True
    if point[1]>1 and not (point[0], point[1]-1) in nodes:
        vector[1]=True
    if point[0]>1 and not (point[0]-1, point[1]) in nodes:
        vector[2]=True
    if point[1]<dimensions[1] and not (point[0], point[1]+1) in nodes:
        vector[3]=True

    return vector

def pick_turn(point):
    vector = test_empty(point)
    turns = list()
    turn_points = {1:(1,0), 2:(0,-1), 3:(-1,0), 4:(0,1)}

    for i in range(4):
        if vector[i]: turns.append(i+1)

    if any(turns):
        rand = random.choice(turns)
        new_point = (point[0]+turn_points[rand][0], point[1]+turn_points[rand][1])

        return new_point
    else:
        return None

def normalize(point):
    x = (point[0]-1)*tile+tile//2
    y = (point[1]-1)*tile+tile//2

    return (x,y)

while len(nodes)<dimensions[0]*dimensions[1]:
    point = pick_turn(stack[-1])

    if point!=None:
        #pygame.time.delay(20)
        nodes.append(point)
        stack.append(point)
    else:
        stack.pop()

    currentcolor=None

    if len(nodes)==2:
        currentcolor=color1
    elif len(nodes)<dimensions[0]*dimensions[1]:
        currentcolor=color
    else:
        currentcolor=color2

    pygame.draw.line(screen, currentcolor, normalize(stack[-2]), normalize(stack[-1]), int(tile/2))

    pygame.display.flip()

##for p in range(1, len(stack)):
##    pygame.draw.line(screen, currentcolor, normalize(stack[p]), normalize(stack[p-1]), 1)
##
##pygame.display.flip()