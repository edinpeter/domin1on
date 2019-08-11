from utils.Supply import Supply
from utils.Player import Player, HumanPlayer, MachinePlayer
from utils.ActionHandler import ActionHandler
from utils.GlobalActionHandler import GlobalActionHandler
import logging
from multiprocessing import Pool

logging.basicConfig(level = logging.DEBUG)
class Game:
    def __init__(self):
        self.supply = Supply()
        self.players = []
        self.game_status = "pregame"
        self.turn_limit = 500
        self.turn_counter = 0
        self.logger = logging.getLogger("domin1on")

    def log(self, msg):
        self.logger.debug("Game Controller: %s" % msg)

    def add_player(self, name, random_inputs=False):
        new_player = MachinePlayer(name, self.supply, random_inputs)
        self.players.append(new_player)

    def process_turn(self, player):
        other_players = [op for op in self.players if op is not player]
        global_handler = GlobalActionHandler(other_players)
        action_handler = ActionHandler(player, self.supply, global_handler)
        action_handler.process_actions()
        player.end_turn()

    def win_conditions_met(self):
        victory_cards_depleted = (
            len(self.supply.get_cards_costing(0, mode="min", card_type="victory")) != 4
        )
        turn_limit_hit = self.turn_counter >= self.turn_limit
        self.log(
            "Victory conditions: victory card depletion: %s, turn limit hit: %s"
            % (victory_cards_depleted, turn_limit_hit)
        )
        return victory_cards_depleted or turn_limit_hit

    def game_loop(self):
        while not self.win_conditions_met():
            for player in self.players:
                self.turn_counter += 1
                self.log("Incremented turn counter: %i" % self.turn_counter)
                if not self.win_conditions_met():
                    self.process_turn(player)
        for player in self.players:
            self.log(
                "Final score for player %s: %i" % (player.name, player.calc_score())
            )

def play_games(i):
    for i in range(10000):
        g = Game()
        g.add_player("pete", random_inputs=True)
        g.add_player("pete2", random_inputs=True)
        g.game_loop()
    print("done")
    return i

if __name__ == "__main__":
   # with Pool(16) as p:
    #    p.map(play_games, range(16))

    g = Game()
    g.add_player("pete", random_inputs=True)
    g.add_player("pete2", random_inputs=True)
    g.game_loop()


