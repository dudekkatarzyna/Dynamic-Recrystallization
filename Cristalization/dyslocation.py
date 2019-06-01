import copy
from math import exp
from random import random, choices, randint

from Smoothing.algorithm import calculate_energy


def ro(time_step):
    A = 86710969050178.5
    B = 9.41268203527779

    new_ro = (A / B) + (1 - (A / B)) * exp(-B * time_step)
    print(time_step, new_ro)
    return new_ro


def distribute_dislocations(surface, delta_ro, mesh_width, mesh_height, time):
    per_embryo = delta_ro / (mesh_width * mesh_height)

    rest = 0
    for i in range(mesh_height):
        for j in range(mesh_width):

            calculate_energy(surface, surface[i][j], mesh_height, mesh_width, False, 'von Neumann', None, None)

            if surface[i][j].crystalised:
                continue

            surface[i][j].dislocation += 0.3 * per_embryo
            rest += per_embryo - 0.3 * per_embryo

            check_crystalisation(surface[i][j], mesh_height, mesh_width, time)

    distribute_rest_of_disloations(surface, rest, mesh_width, mesh_height, time)
    pass


def distribute_rest_of_disloations(surface, ro_to_distribute, mesh_width, mesh_height, time):
    print("another")
    while ro_to_distribute >=0.01:
        czesc=(randint(1,9))/10

        losowa_paczka = czesc * ro_to_distribute
        ro_to_distribute -= losowa_paczka

        i = randint(0, mesh_height - 1)
        j = randint(0, mesh_width - 1)

        if surface[i][j].crystalised:
            continue

        if surface[i][j].energy != 0:
            if choices([True, False], [0.8, 0.2]):
                surface[i][j].dislocation += losowa_paczka
        else:
            if choices([True, False], [0.2, 0.8]):
                surface[i][j].dislocation += losowa_paczka

        check_crystalisation(surface[i][j], mesh_height, mesh_width, time)


def check_crystalisation(embryo, mesh_height, mesh_width, time):

    if embryo.dislocation.real > (4215840142323.42 / (mesh_height * mesh_width)) and embryo.energy != 0:
        print("crystalized True", embryo.x, embryo.y)
        embryo.crystalised = True
        embryo.crystalised_in_step = time
        embryo.dislocation = 0
        embryo.color = '%06X' % randint(0, 0xFF0000)


def algorithm(surface, mesh_width, mesh_height):
    previous_ro = 0

    for t in range(0, 200):

        time = t / 1000
        new_ro = ro(time)

        distribute_dislocations(surface, new_ro - previous_ro, mesh_width, mesh_height, time)

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
                    print("kiedykolwiek")
                    surface[i][j].crystalised = True
                    surface[i][j].dislocation = 0
                    surface[i][j].color = color
        previous_ro = new_ro
