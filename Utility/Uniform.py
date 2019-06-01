from math import floor
from random import randint

from Utility import Colors
from Utility.Embryo import Embryo


class Uniform:
    @staticmethod
    def create_uniform(drawing, row, column, mesh_width, mesh_height):
        if row is '':
            return

        embryos = []

        spacing_row = floor(mesh_width / int(row))
        spacing_column = floor(mesh_height / int(column))

        i = 0
        x = int((mesh_width - (spacing_row * (int(row) - 1) + 1)) / 2) - spacing_row
        y = int((mesh_height - (spacing_column * (int(column) - 1) + 1)) / 2) - spacing_column

        while x + spacing_row < mesh_width:
            x += spacing_row
            y = int((mesh_height - (spacing_column * (int(column) - 1) + 1)) / 2) - spacing_column
            while y + spacing_column < mesh_height:
                y += spacing_column

                Colors.colors[i + 1] = '%06X' % randint(0, 0x0000FF)
                embryos.append(Embryo(x, y, i + 1, Colors.colors[i + 1]))
                i += 1
        drawing.update_step(embryos)
