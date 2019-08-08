from .supply import Supply
from .supply import Player


class Game:
    def __init__(self):
        self.supply = Supply.Suppy()
        self.players = []
        self.game_status = "pregame"
        self.turn_limit = 1000

    def add_player(self, name):
        new_player = Player(name)
        self.players.append(new_player)

    def process_turn(self, player):
        action_stack = [Actions.PLUS_ACTION]


    def get_supply_piles(self):
        supply = dict()

    def game_loop(self):
        pass