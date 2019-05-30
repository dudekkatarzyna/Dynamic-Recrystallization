import math
from random import randint, choice, choices

from Neighbourhoods.Hex import Hex
from Neighbourhoods.Moore import Moore
from Neighbourhoods.Pentagonal import Pentagonal
from Neighbourhoods.WithRadius import WithRadius
from Neighbourhoods.vonNeuman import vonNeuman
from Utility import Colors


def calculate_energy(surface, embryo, mesh_height, mesh_width, periodic, neighbourhood, hex_type, radius):
    if neighbourhood == 'von Neumann':
        return vonNeuman.calculate_energy_vonNeumann(surface, embryo, mesh_height, mesh_width, periodic)
    elif neighbourhood == 'Moore':
        return Moore.calculate_energy_Moore(surface, embryo, mesh_width, mesh_height, periodic)
    elif neighbourhood == 'pentagonal':
        return Pentagonal.calculate_energy_pentagonal(surface, embryo, mesh_width, mesh_height, periodic)
    elif neighbourhood == 'with radius':
        return WithRadius.calculate_energy_withRadius(surface, embryo, mesh_width, mesh_height, radius, periodic)
    elif neighbourhood == 'hexagonal':
        return Hex.calculate_energy_hex(surface, embryo, mesh_width, mesh_height, periodic, hex_type)


class Algorithm:

    @staticmethod
    def iteration(drawing, surface, mesh_width, mesh_height, periodic, neighbourhood, kt, hex_type, radius):

        already_checked = []
        while len(already_checked) != mesh_height * mesh_width:

            x = randint(0, mesh_height - 1)
            y = randint(0, mesh_width - 1)
            possible = [x, y]
            while possible in already_checked:
                x = randint(0, mesh_height - 1)
                y = randint(0, mesh_width - 1)

                possible = [x, y]

            already_checked.append([x, y])

            current_energy = calculate_energy(surface, surface[x][y], mesh_height, mesh_width,
                                              periodic, neighbourhood,
                                              hex_type, radius)

            old_id = surface[x][y].id
            old_color = surface[x][y].color

            choose_nbr = choice(tuple(surface[x][y].nbr_ids))
            new_id = choose_nbr
            new_color = Colors.colors[new_id]

            surface[x][y].id = new_id
            surface[x][y].color = new_color
            new_energy = calculate_energy(surface, surface[x][y], mesh_height, mesh_width, periodic,
                                          neighbourhood,
                                          hex_type, radius)

            if new_energy - current_energy > 0:
                exp = math.exp(-(new_energy - current_energy) / kt)

                if choices([True, False], [exp, (1 - exp)]):
                    surface[x][y].id = old_id
                    surface[x][y].color = old_color
                    surface[x][y].energy = current_energy

            drawing.draw_point(surface[x][y].x, surface[x][y].y, surface[x][y].color)

        return
