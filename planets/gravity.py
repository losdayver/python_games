import pygame
import math
import space
import random as rng
import copy

clip = 300

WIDTH, HEIGHT = 1366, 768
fps=30

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

G = 0.0006

planets = list()

mouse_coords = [0,0]

mousedown = False
mousepressed = False
mouse = [0,0]
tick=0

#planets.append(space.Planet([WIDTH//2,HEIGHT//2], 35, [0,0]))
#planets.append(space.Planet([WIDTH//2+260,HEIGHT//2], 7, [0,-9.5]))
#planets.append(space.Planet([WIDTH//2+140,HEIGHT//2], 5, [0,-9.5]))


planet_to_create = space.Planet(0,0,0)
a_divide = 30
tail_precision = 4


planets_to_destroy = list()

while True:

    mouse = list(pygame.mouse.get_pos())

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            planet_to_create = space.Planet(mouse, rng.randint(2,20), [0,0])

            mousepressed = True
            mousedown = True
            mouse_coords = pygame.mouse.get_pos()

            #planets.append(space.Planet(list(pygame.mouse.get_pos()), rng.randint(2,20), [rng.uniform(-1.3,1.3), rng.uniform(-1.5,1.5)]))
        elif event.type == pygame.MOUSEBUTTONUP:
            mousepressed = False
            mousedown = False

            planet_to_create_copy = copy.deepcopy(planet_to_create)
            dx = (mouse_coords[0]-mouse[0])
            dy = (mouse_coords[1]-mouse[1])

            if dx**2+dy**2>4:
                planet_to_create_copy.vector = [dx/a_divide, dy/a_divide]
            else:
                planet_to_create_copy.vector = [0,0]
            planets.append(planet_to_create_copy)

        if event.type == pygame.QUIT:
            exit()

    key = pygame.key.get_pressed()
    if key[pygame.K_UP] and planet_to_create.radius<100:
        planet_to_create.radius+=1
    elif key[pygame.K_DOWN] and planet_to_create.radius>2:
        planet_to_create.radius-=1

    screen.fill((0,0,0))

    for p in planets:
        x = p.coords[0]
        y = p.coords[1]

        if tick%tail_precision==0:
            p.lines.append([x,y])

        planets_copy = planets.copy()
        planets_copy.remove(p)

        for p1 in planets_copy:
            r = math.dist(p.coords, p1.coords)+0.001

            F = G*(p.mass*p1.mass)/(r**1)
            a = F/p.mass


            if p.radius+p1.radius>r:

                #a=-abs(p.radius-p1.radius)*a
                a=-a*p1.radius*0.5


            dx = p1.coords[0] - p.coords[0]
            dy = p1.coords[1] - p.coords[1]

            ax = (a*dx)/r
            ay = (a*dy)/r

            p.vector[0]+=ax
            p.vector[1]+=ay

        p.coords[0]+=p.vector[0]
        p.coords[1]+=p.vector[1]

        x=p.coords[0]
        y=p.coords[1]

        #pygame.draw.aalines(screen, (0,255,0), False, p.lines)

        for l in p.lines[1:]:
            i=p.lines.index(l)
            c = int(255/len(p.lines)*i)
            pygame.draw.line(screen, (0,c,0), p.lines[i], p.lines[i-1])

        if any(p.lines):
           pygame.draw.line(screen, (0,255,0), p.coords, p.lines[-1])

        tail_l = 1000//tail_precision

        if len(p.lines)>=tail_l:
            del p.lines[0 : len(p.lines)-tail_l]


        if ((p.coords[0]>WIDTH+clip+p.radius) or (p.coords[1]>HEIGHT+clip+p.radius) or (p.coords[0]<-p.radius-clip) or (p.coords[1]<-p.radius-clip)) and not(p in planets_to_destroy):
            planets_to_destroy.append(p)


        for i in planets_to_destroy:
            planets.remove(i)

        planets_to_destroy.clear()


    for i in planets:
        pygame.draw.circle(screen, (0,255,0), i.coords, i.radius)

    if mousedown:
        pygame.draw.line(screen, (0,255,0), mouse_coords, mouse)
        pygame.draw.circle(screen, (0,255,0), mouse_coords, planet_to_create.radius)

    tick+=1
    pygame.display.flip()
    clock.tick(fps)

