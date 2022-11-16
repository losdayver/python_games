import pygame as pg
import numpy as np
import ctypes

class Game:
    def __init__(self, dimensions, surf, tile=36, players=('Черные', 'Белые'), pegclrs=None):
        if pegclrs is None:
            pegclrs = [(15, 15, 15), (220, 220, 220)]
        self.restart = False
        self.ended = False

        self.players = players
        self.backclr = (220, 210, 170)
        self.pegclrs = pegclrs
        self.lineclr = (80, 80, 0)
        self.ackclr = (163, 153, 101)

        self.tile = tile
        self.dim = dimensions
        self.pegs = np.zeros(self.dim)
        self.turn = False

        self.sw, self.sh = (self.dim[0] + 1) * self.tile, (self.dim[1] + 1) * self.tile
        self.surf = surf
        self.surf = pg.display.set_mode((self.sw, self.sh))

        self.surf.fill(self.backclr)

        for y in range(1, self.dim[1] + 1):
            pg.draw.line(self.surf, self.lineclr, (self.tile, y * self.tile), (self.dim[0] * self.tile, y * self.tile), 1)

        for x in range(1, self.dim[0] + 1):
            pg.draw.line(self.surf, self.lineclr, (x * self.tile, self.tile), (x * self.tile, self.dim[1] * self.tile), 1)

        pg.display.flip()

    def placepeg(self, mouse):
        if self.ended:
            return self.win()

        x, y = int((mouse[0] - self.tile // 2) / (self.sw - self.tile) * self.dim[0]), int(
            (mouse[1] - self.tile // 2) / (self.sh - self.tile) * self.dim[1])

        if self.dim[0] > x >= 0 == self.pegs[x, y] and 0 <= y < self.dim[1]:
            if self.turn:
                self.pegs[x, y] = 1
            else:
                self.pegs[x, y] = 2

            x1, y1 = (x + 1) * self.tile, (y + 1) * self.tile
            pg.draw.circle(self.surf, (self.backclr[0] // 1.6, self.backclr[1] // 1.6, self.backclr[2] // 1.6),
                           (x1 + self.tile // 12, y1 + self.tile // 7), self.tile // 2.2)
            pg.draw.circle(self.surf, self.pegclrs[self.turn], (x1, y1), self.tile // 2.2)
            self.turn = not self.turn
            pg.display.flip()

            self.testwin((x, y))

    def win(self):
        self.ended = True
        w = f'Игрок \'{self.players[not self.turn]}\' победил!' + '\n\nНачать новую игру?'
        m = ctypes.windll.user32.MessageBoxW(0, w, "Конец игры", 4)
        if m == 6: self.restart = True
        return False

    def testwin(self, pos):
        score = 1

        for c in (0, 1):
            score = 1
            for sign in (1, -1):
                for i in range(1, 5):
                    p = i * sign
                    if 0 <= pos[c] + p < self.dim[c] and self.turn + 1 == self.pegs[
                        pos[0] + p * (not bool(c)), pos[1] + p * bool(c)]:
                        score += 1
                        if score >= 5:
                            self.win()
                            return True
                    else:
                        break

        for c in (1, -1):
            score = 1
            for sign in (1, -1):
                for i in range(1, 5):
                    p = i * sign
                    x, y = pos[0] + p * c, pos[1] + p
                    bounds = 0 <= x < self.dim[0] and 0 <= y < self.dim[1]
                    if bounds and self.turn + 1 == self.pegs[x, y]:
                        score += 1
                        if score >= 5:
                            self.win()
                            return True
                    else:
                        break


dimensions = (15, 15)
screen = None
g = Game(dimensions, screen)

clock = pg.time.Clock()
fps = 60


def changecaption():
    pg.display.set_caption(f'Гомоку {g.dim[0]}x{g.dim[1]} ходяит игрок \'{g.players[g.turn]}\'')


icon = pg.Surface((32, 32))
pg.draw.circle(icon, (255, 255, 255), (16, 16), 12)
pg.display.set_icon(icon)
pg.init()

changecaption()
while 1:
    mouse = pg.mouse.get_pos()

    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            quit()
        if e.type == pg.MOUSEBUTTONDOWN:
            g.placepeg(mouse)
            changecaption()

        if g.restart:
            g = Game(dimensions, screen)
            changecaption()

    clock.tick(fps)
