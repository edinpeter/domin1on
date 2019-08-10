from .Cards import ACTION_CARDS_LIST, TREASURE_CARDS_LIST, VICTORY_CARDS_LIST
import random
from collections import namedtuple


class Supply:
    def __init__(self):
        self.cards = {}

        self.init_victory_cards()
        self.init_treasure_cards()
        self.init_action_cards()


    def init_victory_cards(self):
        for victory_card in VICTORY_CARDS_LIST:
            self.cards[victory_card["id"]] = {"quantity": 20, "card": victory_card}

    def init_treasure_cards(self):
        for treasure_card in TREASURE_CARDS_LIST:
            self.cards[treasure_card["id"]] = {"quantity": 20, "card": treasure_card}

    def init_action_cards(self):
        action_cards_idxs = set()

        while len(action_cards_idxs) != 10:
            random_index = random.randrange(0, len(ACTION_CARDS_LIST))
            action_cards_idxs.add(random_index)

        for idx in action_cards_idxs:
            self.cards[idx] = {"quantity": 20, "card": ACTION_CARDS_LIST[idx]}

    def get_card_info(self, card_id):
        return self.cards[card_id]["card"]

    def get_card_quantity(self, card_id):
        return self.cards[card_id]["quantity"]

    def get_active_cards(self):
        cards = self.cards.keys()
        cards = [card for card in cards if self.get_card_quantity(card) > 0]
        return cards

    def get_cards_costing(
        self, threshold, mode="exact", card_type="any", availability="available"
    ):
        card_type_filters = {
            "action": lambda x: x < 100,
            "treasure": lambda x: 100 <= x < 200,
            "victory": lambda x: x >= 200,
            "any": lambda x: True,
        }
        card_price_filters = {
            "exact": lambda x, y=threshold: x == y,
            "min": lambda x, y=threshold: x >= y,
            "max": lambda x, y=threshold: x <= y,
        }
        card_quantity_filters = {"available": lambda x: self.cards[x]["quantity"] > 0}
        assert mode in card_price_filters, "%s price filter not found" % mode
        assert card_type in card_type_filters, (
            "%s card_type filter not found" % card_type
        )

        matching_cards = filter(card_price_filters[mode], self.cards)
        matching_cards = filter(card_type_filters[card_type], matching_cards)
        matching_cards = filter(card_quantity_filters[availability], matching_cards)
        return list(matching_cards)

    def decrement_card(self, card_id, amt=1):
        self.cards[card_id]["quantitiy"] -= amt
