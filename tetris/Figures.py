import Settings

class Figure:
    def __init__(self, color, rot1):
        self.color = color
        self.rotations = [rot1]
        self.current_rotation = rot1

    def RotateLeft(self):
        self.current_rotation = self.rotations[self.rotations.index(self.current_rotation) - 1]

    def RotateRight(self):
        index = self.rotations.index(self.current_rotation) + 1;
        if index > len(self.rotations) - 1: index = 0
        self.current_rotation = self.rotations[index]

    def CancelRotation(self):
        self.current_rotation = self.rotations[0]


t_figure = Figure(Settings.color_palette[0], (1, 4, 5, 6))
t_figure.rotations.append((1, 5, 6, 9))
t_figure.rotations.append((4, 5, 6, 9))
t_figure.rotations.append((1, 4, 5, 9))

z_figure = Figure(Settings.color_palette[1], (0, 1, 5, 6))
z_figure.rotations.append((2, 5, 6, 9))
z_figure.rotations.append((4, 5, 9, 10))
z_figure.rotations.append((1, 4, 5, 8))

s_figure = Figure(Settings.color_palette[2], (1, 2, 4, 5))
s_figure.rotations.append((1, 5, 6, 10))
s_figure.rotations.append((5, 6, 8, 9))
s_figure.rotations.append((0, 4, 5, 9))

o_figure = Figure(Settings.color_palette[3], (0, 1, 4, 5))

j_figure = Figure(Settings.color_palette[4], (2, 4, 5, 6))
j_figure.rotations.append((1, 5, 9, 10))
j_figure.rotations.append((4, 5, 6, 8))
j_figure.rotations.append((0, 1, 5, 9))

l_figure = Figure(Settings.color_palette[5], (0, 4, 5, 6))
l_figure.rotations.append((1, 2, 5, 9))
l_figure.rotations.append((4, 5, 6, 10))
l_figure.rotations.append((1, 5, 8, 9))

i_figure = Figure(Settings.color_palette[6], (4, 5, 6, 7))
i_figure.rotations.append((2, 6, 10, 14))
i_figure.rotations.append((8, 9, 10, 11))
i_figure.rotations.append((1, 5, 9, 13))
