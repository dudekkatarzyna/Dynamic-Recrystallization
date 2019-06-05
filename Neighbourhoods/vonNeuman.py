import copy
import random

import numpy

from Utility import Colors


class vonNeuman:

    @staticmethod
    def przejscie_krystalizacja_vonNeumann(surface, mesh_height, mesh_width, border_condition, time):

        for i in range(mesh_height):
            for j in range(mesh_width):

                if surface[i][j].crystalised:
                    continue

                nbr = False
                lower = False

                for k in [-1, 0, 1]:
                    for l in [-1, 0, 1]:
                        if k == l or k == -l:
                            continue

                        if not border_condition:
                            if 0 > i + k >= mesh_height or 0 > j + i >= mesh_width:
                                continue

                        if surface[(i + k) % mesh_height][(j + l) % mesh_width].crystalised and \
                                surface[(i + k) % mesh_height][
                                    (j + l) % mesh_width].crystalised_in_step == time - 0.001:
                            nbr = True
                            color = surface[(i + k) % mesh_height][(j + l) % mesh_width].color

                        if surface[(i + k) % mesh_height][(j + l) % mesh_width].dislocation.real < surface[i][
                            j].dislocation.real:
                            lower = True
                        else:
                            lower = False

                if nbr and lower:
                    surface[i][j].crystalised = True
                    surface[i][j].dislocation = 0
                    surface[i][j].color = color

        pass

    @staticmethod
    def calculate_energy_vonNeumann(surface, embryo, mesh_height, mesh_width, periodic):
        x = embryo.x
        y = embryo.y

        different_ids = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == j or i == -j:
                    continue

                if x + i >= mesh_height or x + i < 0 or y + j >= mesh_width or y + j < 0:
                    if not periodic:
                        continue

                embryo.nbr_ids.add(surface[(x + i) % mesh_height][(y + j) % mesh_width].id)

                if surface[(x + i) % mesh_height][(y + j) % mesh_width].id != embryo.id:
                    different_ids += 1

        embryo.energy = different_ids
        return different_ids

    @staticmethod
    def calculate_next_step(surface, mesh_height, mesh_width, periodic):

        evaluate_surface = copy.deepcopy(surface)
        periodyczne = periodic
        for i in range(mesh_height):
            for j in range(mesh_width):

                neighbourhood = [0 for x in range(len(Colors.colors))]

                if evaluate_surface[i][j].id != 0:
                    continue

                if i == 0:
                    if j == 0:
                        neighbourhood[evaluate_surface[i + 1][j].id] += 1
                        neighbourhood[evaluate_surface[i][j + 1].id] += 1
                        if periodyczne:
                            neighbourhood[evaluate_surface[i][-1].id] += 1
                            neighbourhood[evaluate_surface[-1][j].id] += 1

                    elif j == mesh_width - 1:
                        neighbourhood[evaluate_surface[i][j - 1].id] += 1
                        neighbourhood[evaluate_surface[i + 1][j].id] += 1
                        if periodyczne:
                            neighbourhood[evaluate_surface[i][0].id] += 1
                            neighbourhood[evaluate_surface[-1][j].id] += 1
                    else:

                        neighbourhood[evaluate_surface[i + 1][j].id] += 1
                        neighbourhood[evaluate_surface[i][j + 1].id] += 1
                        neighbourhood[evaluate_surface[i][j - 1].id] += 1

                        if periodyczne:
                            neighbourhood[evaluate_surface[-1][j].id] += 1

                elif i == mesh_height - 1:

                    if j == 0:
                        neighbourhood[evaluate_surface[i][j + 1].id] += 1
                        neighbourhood[evaluate_surface[i - 1][j].id] += 1
                        if periodyczne:
                            neighbourhood[evaluate_surface[i][-1].id] += 1
                            neighbourhood[evaluate_surface[0][j].id] += 1

                    elif j == mesh_width - 1:
                        neighbourhood[evaluate_surface[i][j - 1].id] += 1
                        neighbourhood[evaluate_surface[i - 1][j].id] += 1
                        if periodyczne:
                            neighbourhood[evaluate_surface[i][0].id] += 1
                            neighbourhood[evaluate_surface[0][j].id] += 1

                    else:
                        neighbourhood[evaluate_surface[i][j - 1].id] += 1
                        neighbourhood[evaluate_surface[i - 1][j].id] += 1
                        neighbourhood[evaluate_surface[i][j + 1].id] += 1
                        if periodyczne:
                            neighbourhood[evaluate_surface[0][j].id] += 1

                else:
                    if j == 0:
                        neighbourhood[evaluate_surface[i][j + 1].id] += 1
                        neighbourhood[evaluate_surface[i + 1][j].id] += 1
                        neighbourhood[evaluate_surface[i - 1][j].id] += 1
                        if periodyczne:
                            neighbourhood[evaluate_surface[i][-1].id] += 1

                    elif j == mesh_width - 1:
                        neighbourhood[evaluate_surface[i][j - 1].id] += 1
                        neighbourhood[evaluate_surface[i + 1][j].id] += 1
                        neighbourhood[evaluate_surface[i - 1][j].id] += 1
                        if periodyczne:
                            neighbourhood[evaluate_surface[i][0].id] += 1

                    else:

                        neighbourhood[evaluate_surface[i][j + 1].id] += 1
                        neighbourhood[evaluate_surface[i + 1][j].id] += 1
                        neighbourhood[evaluate_surface[i - 1][j].id] += 1
                        neighbourhood[evaluate_surface[i][j - 1].id] += 1

                if numpy.any(neighbourhood[1:]):
                    max_value = max(neighbourhood[1:])
                    index = [i for i, j in enumerate(neighbourhood) if j == max_value]

                    choice = 0
                    while choice == 0:
                        choice = random.choice(index)

                    surface[i][j].id = choice
                    surface[i][j].color = Colors.colors[choice]

        return surface

    pass
