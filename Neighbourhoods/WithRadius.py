import copy
import random

from Utility import Colors


class WithRadius:

    @staticmethod
    def przejscie_krystalizacja_withRadius():
        pass

    @staticmethod
    def calculate_energy_withRadius(surface, embryo, mesh_width, mesh_height, radius, periodic):

        different_ids = 0
        for i in range(-int(radius), int(radius) + 1):
            if embryo.x + i < 0 or embryo.x + i >= mesh_height:
                if not periodic:
                    continue

            for j in range(-int(radius), int(radius) + 1):
                if i == 0 and j == 0:
                    continue
                if embryo.y + j < 0 or embryo.y + j >= mesh_width:
                    if not periodic:
                        continue

                x = embryo.y + 0.25 * surface[embryo.x][embryo.y].center_point_x
                y = embryo.x + 0.25 * surface[embryo.x][embryo.y].center_point_y

                dest_x = y + j + 0.25 * surface[
                    (x + i) % mesh_height][(y + j) % mesh_width].center_point_x
                dest_y = x + i + 0.25 * surface[
                    (x + i) % mesh_height][(y + j) % mesh_width].center_point_y

                if pow(x - dest_x, 2) + pow(y - dest_y, 2) <= pow(int(radius), 2):
                    embryo.nbr_ids.add(surface[(x + i) % mesh_height][(y + j) % mesh_width].id)

                    if surface[(x + i) % mesh_height][(y + j) % mesh_width].id != embryo.id:
                        different_ids += 1

        embryo.energy = different_ids
        return different_ids

    @staticmethod
    def calculate_next_step(surface, mesh_height, mesh_width, periodic, radius):

        if radius == '':
            return
        evaluate_surface = copy.deepcopy(surface)

        for index_y in range(mesh_width):
            for index_x in range(mesh_height):

                potential_nbr = []

                for i in range(-int(radius), int(radius) + 1):
                    if index_x + i < 0 or index_x + i >= mesh_height:
                        if not periodic:
                            continue

                    for j in range(-int(radius), int(radius) + 1):
                        if i == 0 and j == 0:
                            continue
                        if index_y + j < 0 or index_y + j >= mesh_width:
                            if not periodic:
                                continue

                        x = index_y + 0.25 * evaluate_surface[index_x][
                            index_y].center_point_x
                        y = index_x + 0.25 * evaluate_surface[index_x][
                            index_y].center_point_y

                        dest_x = index_y + j + 0.25 * evaluate_surface[
                            (index_x + i) % mesh_height][(index_y + j) % mesh_width].center_point_x
                        dest_y = index_x + i + 0.25 * evaluate_surface[
                            (index_x + i) % mesh_height][(index_y + j) % mesh_width].center_point_y

                        if pow(x - dest_x, 2) + pow(y - dest_y, 2) <= pow(int(radius), 2):
                            potential_nbr.append(
                                evaluate_surface[(index_x + i) % mesh_height][(index_y + j) % mesh_width])

                neighbourhood = [0 for z in range(len(Colors.colors))]

                for nbr in potential_nbr:
                    neighbourhood[nbr.id] += 1

                if any(neighbourhood[1:]):
                    max_value = max(neighbourhood[1:])
                    index = [i for i, j in enumerate(neighbourhood) if j == max_value]

                    choice = 0
                    while choice == 0:
                        choice = random.choice(index)

                    surface[index_x][index_y].id = choice
                    surface[index_x][index_y].color = Colors.colors[choice]

        return surface
