from math import floor
from random import randint

from kivy.core.window import Window

from Utility import Colors
from Utility.Embryo import Embryo


class User:

    @staticmethod
    def create_user_input(drawing, mesh_width, mesh_height, touch):
        if mesh_height > mesh_width:

            stepWidth = floor((0.52 * Window.width) / (mesh_height + 1))
            stepHeight = floor(0.9 * Window.height / (mesh_height + 1))

        else:
            stepWidth = floor((0.52 * Window.width) / (mesh_width + 1))
            stepHeight = floor(0.9 * Window.height / (mesh_width + 1))
        embryos = []

        if 0.4 * Window.width + stepWidth * mesh_width >= touch.x >= 0.4 * Window.width and 0.9 * Window.height >= touch.y >= 0.9 * Window.height - (
                stepHeight * mesh_width):
            Colors.colors[len(Colors.colors)] = '%06X' % randint(0, 0x0000FF)
            print(touch.x, touch.y)
            embryos.append(
                Embryo(int(mesh_width - int(
                    touch.y - (0.9 * Window.height - (stepHeight * mesh_height))) / stepHeight),
                       int((touch.x - 0.4 * Window.width) / stepWidth),
                       len(Colors.colors) - 1, Colors.colors[len(Colors.colors) - 1])

            )

        drawing.update_step(embryos)
