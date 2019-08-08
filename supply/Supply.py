from .Cards import ACTION_CARDS_LIST, TREASURE_CARDS_LIST, VICTORY_CARDS_LIST
import random


class Supply:
    def __init__(self):
        self.victory_cards = {}
        self.treasure_cards = {}
        self.action_cards = {}

        self.init_victory_cards()
        self.init_treasure_cards()
        self.init_action_cards()

    def init_victory_cards(self):
        for victory_card in VICTORY_CARDS_LIST:
            self.victory_cards[victory_card["id"]] = {
                "quantity": 20,
                "card": victory_card,
            }

    def init_treasure_cards(self):
        for treasure_card in TREASURE_CARDS_LIST:
            self.treasure_cards[treasure_card["id"]] = {
                "quantity": 20,
                "card": treasure_card,
            }

    def init_action_cards(self):
        action_cards_idxs = set()

        while len(action_cards_idxs) != 10:
            random_index = random.randrange(0, len(ACTION_CARDS_LIST))
            action_cards_idxs.add(random_index)

        for idx in action_cards_idxs:
            self.action_cards[idx] = ACTION_CARDS_LIST[idx]
