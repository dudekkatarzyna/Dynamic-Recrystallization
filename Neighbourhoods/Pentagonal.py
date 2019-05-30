import copy
import random

import numpy

from Utility import Colors


class Pentagonal:

    @staticmethod
    def calculate_energy_pentagonal(surface, embryo, mesh_width, mesh_height, periodic):

        x = embryo.x
        y = embryo.y

        pent_type = random.choice(['left', 'right', 'up', 'down'])

        different_ids = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue

                if pent_type == 'left':
                    if (i == -1 and j == 1) or (i == 0 and j == 1) or (i == 1 and j == 1):
                        continue
                elif pent_type == 'right':
                    if (i == -1 and j == -1) or (i == 0 and j == -1) or (i == 1 and j == -1):
                        continue
                elif pent_type == 'up':
                    if (i == 1 and j == -1) or (i == 1 and j == 0) or (i == 1 and j == 1):
                        continue
                elif pent_type == 'down':
                    if (i == -1 and j == -1) or (i == -1 and j == 0) or (i == -1 and j == 1):
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

                neighbourhoods = [[1, 1, 0, 1, 1, 0, 1, 1, 0], [0, 1, 1, 0, 1, 1, 0, 1, 1], [0, 0, 0, 1, 1, 1, 1, 1, 1],
                                  [1, 1, 1, 1, 1, 1, 0, 0, 0]]

                lottery = random.choice(neighbourhoods)

                if i == 0:
                    if j == 0:
                        neighbourhood[evaluate_surface[i][j + 1].id] += lottery[5]
                        neighbourhood[evaluate_surface[i + 1][j + 1].id] += lottery[8]
                        neighbourhood[evaluate_surface[i + 1][j].id] += lottery[7]

                        if periodyczne:
                            neighbourhood[evaluate_surface[-1][-1].id] += lottery[0]
                            neighbourhood[evaluate_surface[i][-1].id] += lottery[3]
                            neighbourhood[evaluate_surface[i + 1][-1].id] += lottery[6]
                            neighbourhood[evaluate_surface[-1][j].id] += lottery[1]
                            neighbourhood[evaluate_surface[-1][j + 1].id] += lottery[2]


                    elif j == mesh_width - 1:

                        neighbourhood[evaluate_surface[i + 1][j].id] += lottery[5]
                        neighbourhood[evaluate_surface[i][j - 1].id] += lottery[1]
                        neighbourhood[evaluate_surface[i + 1][j - 1].id] += lottery[6]
                        if periodyczne:
                            neighbourhood[evaluate_surface[i][0].id] += lottery[3]
                            neighbourhood[evaluate_surface[-1][j].id] += lottery[1]
                            neighbourhood[evaluate_surface[-1][j - 1].id] += lottery[0]
                            neighbourhood[evaluate_surface[i + 1][0].id] += lottery[8]
                            neighbourhood[evaluate_surface[-1][0].id] += lottery[2]


                    else:

                        neighbourhood[evaluate_surface[i][j - 1].id] += lottery[3]
                        neighbourhood[evaluate_surface[i][j + 1].id] += lottery[5]
                        neighbourhood[evaluate_surface[i + 1][j - 1].id] += lottery[6]
                        neighbourhood[evaluate_surface[i + 1][j].id] += lottery[7]
                        neighbourhood[evaluate_surface[i + 1][j + 1].id] += lottery[8]
                        if periodyczne:
                            neighbourhood[evaluate_surface[-1][j].id] += lottery[1]
                            neighbourhood[evaluate_surface[-1][j - 1].id] += lottery[0]
                            neighbourhood[evaluate_surface[-1][j + 1].id] += lottery[2]


                elif i == mesh_height - 1:

                    if j == 0:
                        neighbourhood[evaluate_surface[i - 1][j + 1].id] += lottery[2]
                        neighbourhood[evaluate_surface[i - 1][j].id] += lottery[1]
                        neighbourhood[evaluate_surface[i][j + 1].id] += lottery[5]

                        if periodyczne:
                            neighbourhood[evaluate_surface[i - 1][j - 1].id] += lottery[0]
                            neighbourhood[evaluate_surface[i][j - 1].id] += lottery[4]
                            neighbourhood[evaluate_surface[0][j - 1].id] += lottery[6]
                            neighbourhood[evaluate_surface[0][j].id] += lottery[7]
                            neighbourhood[evaluate_surface[0][j + 1].id] += lottery[8]



                    elif j == mesh_width - 1:
                        neighbourhood[evaluate_surface[i][j - 1].id] += lottery[3]
                        neighbourhood[evaluate_surface[i - 1][j].id] += lottery[1]
                        neighbourhood[evaluate_surface[i - 1][j - 1].id] += lottery[0]
                        if periodyczne:
                            neighbourhood[evaluate_surface[i][j + 1].id] += lottery[5]
                            neighbourhood[evaluate_surface[i - 1][j + 1].id] += lottery[2]
                            neighbourhood[evaluate_surface[0][j + 1].id] += lottery[8]
                            neighbourhood[evaluate_surface[0][j].id] += lottery[7]
                            neighbourhood[evaluate_surface[0][j - 1].id] += lottery[6]

                    else:
                        neighbourhood[evaluate_surface[i][j - 1].id] += lottery[3]
                        neighbourhood[evaluate_surface[i - 1][j - 1].id] += lottery[0]
                        neighbourhood[evaluate_surface[i - 1][j].id] += lottery[1]
                        neighbourhood[evaluate_surface[i - 1][j + 1].id] += lottery[2]
                        neighbourhood[evaluate_surface[i][j + 1].id] += lottery[5]
                        if periodyczne:
                            neighbourhood[evaluate_surface[0][j].id] += lottery[7]
                            neighbourhood[evaluate_surface[0][j - 1].id] += lottery[6]
                            neighbourhood[evaluate_surface[0][j + 1].id] += lottery[8]

                else:
                    if j == 0:
                        neighbourhood[evaluate_surface[i][j + 1].id] += lottery[5]
                        neighbourhood[evaluate_surface[i + 1][j].id] += lottery[7]
                        neighbourhood[evaluate_surface[i + 1][j + 1].id] += lottery[8]
                        neighbourhood[evaluate_surface[i - 1][j].id] += lottery[1]
                        neighbourhood[evaluate_surface[i - 1][j + 1].id] += lottery[2]
                        if periodyczne:
                            neighbourhood[evaluate_surface[i - 1][-1].id] += lottery[0]
                            neighbourhood[evaluate_surface[i][-1].id] += lottery[3]
                            neighbourhood[evaluate_surface[i + 1][-1].id] += lottery[6]

                    elif j == mesh_width - 1:
                        neighbourhood[evaluate_surface[i][j - 1].id] += lottery[3]
                        neighbourhood[evaluate_surface[i + 1][j].id] += lottery[7]
                        neighbourhood[evaluate_surface[i + 1][j - 1].id] += lottery[6]
                        neighbourhood[evaluate_surface[i - 1][j].id] += lottery[1]
                        neighbourhood[evaluate_surface[i - 1][j - 1].id] += lottery[0]
                        if periodyczne:
                            neighbourhood[evaluate_surface[i][0].id] += lottery[5]
                            neighbourhood[evaluate_surface[i - 1][0].id] += lottery[2]
                            neighbourhood[evaluate_surface[i + 1][0].id] += lottery[8]

                    else:

                        neighbourhood[evaluate_surface[i][j + 1].id] += lottery[5]
                        neighbourhood[evaluate_surface[i][j - 1].id] += lottery[3]
                        neighbourhood[evaluate_surface[i + 1][j].id] += lottery[7]
                        neighbourhood[evaluate_surface[i + 1][j - 1].id] += lottery[6]
                        neighbourhood[evaluate_surface[i + 1][j + 1].id] += lottery[8]
                        neighbourhood[evaluate_surface[i - 1][j].id] += lottery[1]
                        neighbourhood[evaluate_surface[i - 1][j - 1].id] += lottery[0]
                        neighbourhood[evaluate_surface[i - 1][j + 1].id] += lottery[2]

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
