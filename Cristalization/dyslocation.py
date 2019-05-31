import copy
from cmath import exp
from random import random, choices, randint


def calculate_delta_ro(previous_ro, time_step):
    A = 86710969050178.5
    B = 9.41268203527779

    new_ro = A / B + (1 - A / B) * exp(-B * time_step)
    return new_ro - previous_ro


def distribute_dislocations(surface, delta_ro, mesh_width, mesh_height, time):
    per_embryo = delta_ro / (mesh_width * mesh_height)

    rest = 0
    for i in range(mesh_height):
        for j in range(mesh_width):

            if surface[i][j].crystalised:
                continue

            surface[i][j].dislocation += 0.7 * per_embryo
            rest += per_embryo - 0.7 * per_embryo

            check_crystalisation(surface[i][j], time)

    distribute_rest_of_disloations(surface, rest, mesh_width, mesh_height, time)
    pass


def distribute_rest_of_disloations(surface, ro_to_distribute, mesh_width, mesh_height, time):
    while ro_to_distribute != 0:
        losowa_paczka = random() * ro_to_distribute
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

        check_crystalisation(surface[i][j], time)


def check_crystalisation(embryo, time):

    if embryo.dislocation > 0 and embryo.energy != 0:
        embryo.crystalised = True
        embryo.crystalised_in_step = time
        embryo.dislocation = 0



def algorithm(surface, mesh_width, mesh_height):
    previous_ro = 0
    for t in range(0, 7000):

        time = t / 1000
        delta_ro = calculate_delta_ro(previous_ro, time)

        distribute_dislocations(surface, delta_ro, mesh_width, mesh_height)

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

                        if surface[k][l].crystalised == True and surface[k][l].crystalised_in_time == time - 0.001:
                            nbr = True

                        if surface[k][l].dislocation < surface[i][j].dislocation:
                            lower = True
                        else:
                            lower = False

                if nbr and lower:
                    surface[i][j].crystalised = True
