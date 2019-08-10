from .Cards import Actions, BuyActions


class GlobalActionHandler:
    def __init__(self, other_players):
        self.other_players = other_players

    def process_global_action(self, action):
        if action == Actions.OTHERS_GAIN_CURSE:
            for op in self.other_players:
                op.gain_from_supply(203)
        elif action == Actions.OTHERS_DRAW_ONE:
            for op in self.other_players:
                op.draw(1)
        elif action == Actions.OTHERS_DISCARD_TO_THREE:
            for op in self.other_players:
                for i in range(len(op.hand) - 3):
                    op.force_discard()
