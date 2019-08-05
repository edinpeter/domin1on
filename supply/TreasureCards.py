from .TreasureCard import TreasureCard


class Gold(TreasureCard):
    def __init__(self):
        self.price = 6
        self.value = 3

    def price(self):
        return self.price

    def value(self):
        return self.value


class Silver(TreasureCard):
    def __init__(self):
        self.price = 3
        self.value = 2

    def price(self):
        return self.price

    def value(self):
        return self.value


class Copper(TreasureCard):
    def __init__(self):
        self.price = 0
        self.value = 1

    def price(self):
        return self.price

    def value(self):
        return self.value
