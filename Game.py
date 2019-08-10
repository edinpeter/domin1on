from utils.Supply import Supply
from utils.Player import Player
from utils.ActionHandler import ActionHandler
from utils.GlobalActionHandler import GlobalActionHandler


class Game:
    def __init__(self):
        self.supply = Supply()
        self.players = []
        self.game_status = "pregame"
        self.turn_limit = 1000
        self.turn_counter = 0

    def add_player(self, name):
        new_player = Player(name, self.supply)
        self.players.append(new_player)

    def process_turn(self, player):
        other_players = [op for op in self.players if op is not player]
        global_handler = GlobalActionHandler(other_players)
        action_handler = ActionHandler(player, self.supply, global_handler)
        action_handler.process_actions()

    def win_conditions_not_met(self):
        return (
            len(self.supply.get_cards_costing(0, mode="min", card_type="victory")) == 4
            and self.turn_counter < self.turn_limit
        )

    def game_loop(self):
        for player in self.players:
            self.turn_counter += 1
            if self.win_conditions_not_met:
                self.process_turn(player)


if __name__ == "__main__":
    g = Game()
    g.add_player("pete")
    g.add_player("pete2")
    g.game_loop()