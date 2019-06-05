import copy
import csv
from math import exp
from random import random, choices, randint

from Neighbourhoods.Hex import Hex
from Neighbourhoods.Pentagonal import Pentagonal
from Neighbourhoods.WithRadius import WithRadius
from Neighbourhoods.Moore import Moore
from Neighbourhoods.vonNeuman import vonNeuman
from Smoothing.algorithm import calculate_energy


def ro(time_step):
    A = 86710969050178.5
    B = 9.41268203527779

    new_ro = (A / B) + (1 - (A / B)) * exp(-B * time_step)
    print(time_step, new_ro)
    return new_ro


def distribute_dislocations(surface, delta_ro, mesh_width, mesh_height, time):
    # print("new distribution")
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
    # print("another")
    while ro_to_distribute >= 0.01:
        czesc = (randint(1, 9)) / 10

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

    save_dislocations_to_csv(surface, mesh_width, mesh_height)


def check_crystalisation(embryo, mesh_height, mesh_width, time):
    if embryo.dislocation.real > (4215840142323.42 / (mesh_height * mesh_width)) and embryo.energy != 0:
        # print("crystalized True", embryo.x, embryo.y)
        embryo.crystalised = True
        embryo.crystalised_in_step = time
        embryo.dislocation = 0
        embryo.color = '%06X' % randint(0, 0xFF0000)


def algorithm(surface, mesh_width, mesh_height, neighbourhood_type, border_condition, hex_type, with_radius):
    previous_ro = 0

    with open('C:/Users/Katarzyna/PycharmProjects/RekrystalizacjaDynamiczna/Utility/results.csv', 'w',
              newline='') as file:
        file.truncate(0)

    for t in range(0, 200):

        time = t / 1000
        new_ro = ro(time)

        distribute_dislocations(surface, new_ro - previous_ro, mesh_width, mesh_height, time)

        if neighbourhood_type == 'Moore':
            Moore.przejscie_krystalizacja_Moore(surface, mesh_height, mesh_width, border_condition, time)
        elif neighbourhood_type == 'hexagonal':
            if hex_type is None:
                return False
            Hex.przejscie_krystalizacja_hex(surface, mesh_height, mesh_width, border_condition, time, hex_type)
        elif neighbourhood_type == 'pentagonal':
            Pentagonal.przejscie_krystalizacja_pentagonal(surface, mesh_height, mesh_width, border_condition, time)
        elif neighbourhood_type == 'radius':
            if with_radius is None:
                return False
            return
        elif neighbourhood_type == 'von Neumann':
            vonNeuman.przejscie_krystalizacja_vonNeumann(surface, mesh_height, mesh_width, border_condition, time)
        else:
            return False


        previous_ro = new_ro


def save_dislocations_to_csv(surface, mesh_width, mesh_height):
    sum_dislocation = 0
    for i in range(mesh_height):
        for j in range(mesh_width):
            sum_dislocation += surface[i][j].dislocation

    with open('C:/Users/Katarzyna/PycharmProjects/RekrystalizacjaDynamiczna/Utility/results.csv', 'a+',
              newline='') as file:
        writer = csv.writer(file)
        writer.writerow([sum_dislocation])

    pass
