from .VictoryCard import VictoryCard


class Province(VictoryCard):
    def __init__(self):
        self.price = 8
        self.victory_points = 6

    def price(self):
        return self.price

    def victory_points(self):
        return self.victory_points


class Duchy(VictoryCard):
    def __init__(self):
        self.price = 5
        self.victory_points = 3

    def price(self):
        return self.price

    def victory_points(self):
        return self.victory_points


class Estate(VictoryCard):
    def __init__(self):
        self.price = 2
        self.victory_points = 1

    def price(self):
        return self.price

    def victory_points(self):
        return self.victory_points
