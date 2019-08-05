from .TreasureCards import Copper, Silver, Gold
from .VictoryCards import Estate, Duchy, Province


class Supply:
    def __init__(self):
        self.cards = dict()

    def init_victory_cards(self):
        self.cards["Estate"] = 20
        self.cards["Duchy"] = 20
        self.cards["Province"] = 20

    def init_treasure_cards(self):
        self.cards["Copper"] = 20
        self.cards["Silver"] = 20
        self.cards["Gold"] = 20
