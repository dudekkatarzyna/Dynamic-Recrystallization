from math import sqrt
from random import randint

from Utility import Colors
from Utility.Embryo import Embryo


class Radius:
    x_list = []
    y_list = []

    @staticmethod
    def create_radius(newclass, drawing, radius, amount, mesh_width, mesh_height):
        if radius is '' or amount is '':
            return

        embryos = []

        for i in range(int(amount)):
            x = randint(0, mesh_height - 1)
            y = randint(0, mesh_width - 1)

            should_restart = True
            check = 0
            while should_restart:
                should_restart = False

                for j in range(len(Radius.x_list)):
                    space = sqrt(pow(Radius.x_list[j] - x, 2) + pow(Radius.y_list[j] - y, 2))
                    while space <= int(radius) and check < 10:
                        x = randint(0, mesh_height - 1)
                        y = randint(0, mesh_width - 1)
                        space = sqrt(pow(Radius.x_list[j] - x, 2) + pow(Radius.y_list[j] - y, 2))
                        check += 1
                        should_restart = True

                    if check == 10:
                        drawing.update_step(embryos)
                        newclass.print_no_embryos(len(embryos))
                        return

            Colors.colors[i + 1] = '%06X' % randint(0, 0xFFFFFF)
            embryos.append(Embryo(x, y, i + 1, Colors.colors[i + 1]))
            Radius.x_list.append(x)
            Radius.y_list.append(y)

        drawing.update_step(embryos)
