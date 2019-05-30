import random


class Embryo:

    def __init__(self, x, y, id_num, color):
        self.x = x
        self.y = y
        self.id = id_num
        self.center_point_x = random.choice([1, 2, 3])
        self.center_point_y = random.choice([1, 2, 3])
        self.color = color
        self.drawn = False
        self.energy = 0
        self.nbr_ids = set([])
