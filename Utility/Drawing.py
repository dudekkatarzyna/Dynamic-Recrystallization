from math import floor

from kivy import utils
from kivy.core.window import Window
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle, Line

from Neighbourhoods.Hex import Hex
from Neighbourhoods.Pentagonal import Pentagonal
from Neighbourhoods.WithRadius import WithRadius
from Utility import Colors
from Utility.Embryo import Embryo
from Neighbourhoods.Moore import Moore
from Neighbourhoods.vonNeuman import vonNeuman


class Drawing:

    def __init__(self, wid, mesh_width, mesh_height):
        self.mesh_width = mesh_width
        self.mesh_height = mesh_height
        self.wid = wid
        self.surface = [[Embryo(x, y, 0, 0) for y in range(self.mesh_width)] for x in range(self.mesh_height)]

    def create_mesh(self):
        self.wid.canvas.clear()

        height = Window.height
        width = Window.width

        if self.mesh_height > self.mesh_width:

            stepWidth = floor((0.52 * width) / (self.mesh_height + 1))
            stepHeight = floor(0.9 * height / (self.mesh_height + 1))

        else:
            stepWidth = floor((0.52 * width) / (self.mesh_width + 1))
            stepHeight = floor(0.9 * height / (self.mesh_width + 1))

        with self.wid.canvas:
            Color(1., 1, 1)

            for index in range(0, self.mesh_height + 1):
                # poziome
                Line(points=[0.4 * width,
                             0.9 * height - stepHeight * index,
                             self.mesh_width * stepWidth + 0.4 * width,
                             0.9 * height - stepHeight * index],
                     width=1)

            for index in range(0, self.mesh_width + 1):
                # pionowe
                Line(points=[(self.mesh_width - index) * stepWidth + 0.4 * width,
                             0.9 * height,
                             (self.mesh_width - index) * stepWidth + 0.4 * width,
                             0.9 * height - (stepHeight * self.mesh_height)],
                     width=1)

        pass

    def draw_energy(self):
        for i in range(self.mesh_height):
            for j in range(self.mesh_width):
                if self.surface[i][j].energy != 0:
                    print(self.surface[i][j].energy)
                    if self.surface[i][j].energy <= 1:
                        self.draw_point(self.surface[i][j].x, self.surface[i][j].y, "1C1C18")
                    elif self.surface[i][j].energy <= 2:
                        self.draw_point(self.surface[i][j].x, self.surface[i][j].y, "1F1F1C")
                    elif self.surface[i][j].energy <= 3:
                        self.draw_point(self.surface[i][j].x, self.surface[i][j].y, "3F3F38")
                    elif self.surface[i][j].energy <= 4:
                        self.draw_point(self.surface[i][j].x, self.surface[i][j].y, "5F5F54")
                    elif self.surface[i][j].energy <= 5:
                        self.draw_point(self.surface[i][j].x, self.surface[i][j].y, "7F7F70")
                    elif self.surface[i][j].energy <= 6:
                        self.draw_point(self.surface[i][j].x, self.surface[i][j].y, "9F9F8C")
                    elif self.surface[i][j].energy <= 7:
                        self.draw_point(self.surface[i][j].x, self.surface[i][j].y, "BFBFA8")
                    elif self.surface[i][j].energy <= 8:
                        self.draw_point(self.surface[i][j].x, self.surface[i][j].y, "DFDFC4")
                    elif self.surface[i][j].energy <= 9:
                        self.draw_point(self.surface[i][j].x, self.surface[i][j].y, "FFFFE0")

                else:
                    self.draw_point(self.surface[i][j].x, self.surface[i][j].y, "000000")

    def update_step(self, embryos):

        for embryo in embryos:
            self.surface[embryo.x][embryo.y] = embryo
            self.draw_point(embryo.x, embryo.y, embryo.color)

    def draw_point(self, index_x, index_y, color):

        if self.mesh_height > self.mesh_width:

            stepWidth = floor((0.52 * Window.width) / (self.mesh_height + 1))
            stepHeight = floor(0.9 * Window.height / (self.mesh_height + 1))

        else:
            stepWidth = floor((0.52 * Window.width) / (self.mesh_width + 1))
            stepHeight = floor(0.9 * Window.height / (self.mesh_width + 1))

        with self.wid.canvas:
            color = utils.get_color_from_hex(color)
            Color(color[0], color[1], color[2], color[3])
            Rectangle(
                pos=(0.4 * Window.width + (stepWidth * index_y), 0.9 * Window.height - (stepHeight * (index_x + 1))),
                size=(stepWidth, stepWidth))

        return

    def draw_dislocations(self):

        count=0
        for i in range(self.mesh_height):
            for j in range(self.mesh_width):
                if self.surface[i][j].crystalised:
                    print("crystalized")
                    count+=1
                    self.draw_point(i, j, self.surface[i][j].color)
        print("ilosc",count)




    def draw_all_points(self):
        for i in range(self.mesh_height):
            for j in range(self.mesh_width):
                self.draw_point(self.surface[i][j].x, self.surface[i][j].y, self.surface[i][j].color)
                self.surface[i][j].drawn = True

    # noinspection PyArgumentList
    def draw_center_points(self, mesh_height, mesh_width):
        if self.mesh_height > self.mesh_width:

            stepWidth = floor((0.52 * Window.width) / (self.mesh_height + 1))
            stepHeight = floor(0.9 * Window.height / (self.mesh_height + 1))

        else:
            stepWidth = floor((0.52 * Window.width) / (self.mesh_width + 1))
            stepHeight = floor(0.9 * Window.height / (self.mesh_width + 1))

        with self.wid.canvas:
            Color(1, 0, 0, 1)
            for index_x in range(mesh_height):
                for index_y in range(mesh_width):
                    x = 0.4 * Window.width + (stepWidth * index_y) + 0.25 * stepHeight * self.surface[index_x][
                        index_y].center_point_x
                    y = 0.9 * Window.height - (stepHeight * (index_x + 1)) + 0.25 * stepWidth * self.surface[index_x][
                        index_y].center_point_y

                    Line(circle=(x, y, stepWidth / 15), close=True, background_color=(1, 0, 0, 1))

    def draw_animation(self, border_condition, neighbourhood_type, hex_type, with_radius):

        if neighbourhood_type == 'Moore':
            self.surface = Moore.calculate_next_step(self.surface, self.mesh_height, self.mesh_width, border_condition)
        elif neighbourhood_type == 'hexagonal':
            if hex_type is None:
                return False
            self.surface = Hex.calculate_next_step(self.surface, self.mesh_height, self.mesh_width, border_condition,
                                                   hex_type)
        elif neighbourhood_type == 'pentagonal':
            self.surface = Pentagonal.calculate_next_step(self.surface, self.mesh_height, self.mesh_width,
                                                          border_condition)
        elif neighbourhood_type == 'radius':
            if with_radius is None:
                return False
            self.surface = WithRadius.calculate_next_step(self.surface, self.mesh_height, self.mesh_width,
                                                          border_condition,
                                                          with_radius)
        elif neighbourhood_type == 'von Neumann':
            self.surface = vonNeuman.calculate_next_step(self.surface, self.mesh_height, self.mesh_width,
                                                         border_condition)
        else:
            return False

        # self.wid.canvas.clear()
        # self.create_mesh()

        count = 0
        for i in range(self.mesh_height):
            for j in range(self.mesh_width):
                if self.surface[i][j].id is not 0 and self.surface[i][j].drawn is False:
                    self.draw_point(self.surface[i][j].x, self.surface[i][j].y, self.surface[i][j].color)
                    self.surface[i][j].drawn = True

                else:
                    count += 1

        if count == self.mesh_height * self.mesh_width:
            return False
        else:
            return True
        # return keep_going
