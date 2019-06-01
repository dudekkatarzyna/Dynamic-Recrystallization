from random import randint

from Utility import Colors
from Utility.Embryo import Embryo


class RandomCase:

    @staticmethod
    def create_random(drawing, amount, mesh_width, mesh_height):
        if amount is '':
            return

        x_list = []
        y_list = []
        embryos = []

        for i in range(int(amount)):
            x = randint(0, mesh_height - 1)
            y = randint(0, mesh_width - 1)

            if x in x_list and y in y_list:
                x = randint(0, mesh_height - 1)
                y = randint(0, mesh_width - 1)

            Colors.colors[i + 1] = '%06X' % randint(0, 0x0000FF)
            embryos.append(Embryo(x, y, i + 1, Colors.colors[i + 1]))
            x_list.append(x)
            y_list.append(y)

        drawing.create_mesh()
        drawing.update_step(embryos)

