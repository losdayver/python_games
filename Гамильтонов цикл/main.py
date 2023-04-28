import pygame
import random

random.seed(3)

pygame.init()
SCREEN = pygame.display.set_mode((800, 600))

class Vertex:
    num_vertices = 0
    list_vertices = []
    def __init__(self, adjecent_vertices:list = []):
        self.coords = random.randint(0, SCREEN.get_width()), \
                      random.randint(0, SCREEN.get_height())

        self.id = Vertex.num_vertices
        Vertex.num_vertices += 1

        self.adjecent_vertices = adjecent_vertices[:]
        self.visited = False

        Vertex.list_vertices.append(self)

    def set_con(self, vertices):
        self.adjecent_vertices = vertices[:]

v0 = Vertex()
v1 = Vertex()
v2 = Vertex()
v3 = Vertex()
v4 = Vertex()
v5 = Vertex()

v0.set_con((v1, v3, v4))
v1.set_con((v0, v2, v4))
v2.set_con((v1, v3, v5))
v3.set_con((v0, v2, v5))
v4.set_con((v0, v1, v5))
v5.set_con((v2, v3, v4))

hamilton_stack = []
def propagate(from_v:Vertex = v1):
    global hamilton_stack

    # Проверяю является ли текущая вершина последней
    if len(hamilton_stack) == Vertex.num_vertices - 1 and \
        hamilton_stack[-1] not in from_v.adjecent_vertices:
            return

    # Отмечаю вершину как посещенную и добавляю ее в "стэк"
    from_v.visited = True
    hamilton_stack.append(from_v)

    # Перебераем соединенные вершины, входи в рекурсию если вершина не посещена
    for vertex in from_v.adjecent_vertices:
        if not vertex.visited:
            propagate(vertex)

    # Если стэк заполнен - выходим из текущего шага рекурсии
    if len(hamilton_stack) == Vertex.num_vertices:
        return

    # Если зашли в тупик и стэк не заполнен (цикл не гамильтонов или не завершен)
    # отмечаем вершину как не посещенную и удаляем из стэка
    from_v.visited = False
    hamilton_stack.pop()

propagate(v2)

for vertex in hamilton_stack:
    print(vertex.id)

SCREEN.fill((255,255,255))

font1 = pygame.font.SysFont('arial', 10, False, False)

for vertex in Vertex.list_vertices:
    text = font1.render(str(vertex.id), False, (0,0,255))

    pygame.draw.circle(
        surface=SCREEN,
        color=(0,0,255),
        center=vertex.coords,
        radius=10)

    for other in vertex.adjecent_vertices:
        pygame.draw.line(surface=SCREEN,
                         color=(0,0,255),
                         start_pos=vertex.coords,
                         end_pos=other.coords,
                         width=2)

prev_vertex = hamilton_stack[0]
for vertex in hamilton_stack[1:]:
    pygame.draw.line(surface=SCREEN,
                     color=(255, 0, 0),
                     start_pos=vertex.coords,
                     end_pos=prev_vertex.coords,
                     width=2)

    prev_vertex = vertex

pygame.draw.line(surface=SCREEN,
                     color=(255, 0, 0),
                     start_pos=hamilton_stack[0].coords,
                     end_pos=hamilton_stack[-1].coords,
                     width=2)

pygame.display.flip()

while 1:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            quit()



















