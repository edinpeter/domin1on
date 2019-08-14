from .Cards import ACTION_CARDS_LIST, TREASURE_CARDS_LIST, VICTORY_CARDS_LIST
import random
import logging


class Supply:
    def __init__(self):
        self.cards = {}
        self.logger = logging.getLogger("domin1on")

        self.init_victory_cards()
        self.init_treasure_cards()
        self.init_action_cards()

    def log(self, msg):
        self.logger.debug("Supply: %s" % msg)

    def get_card_counts(self):
        counts = {}
        card_sets = [ACTION_CARDS_LIST, TREASURE_CARDS_LIST, VICTORY_CARDS_LIST]
        for card_set in card_sets:
            for card in card_set:
                card_id = int(card["id"])
                if card_id in self.cards:
                    counts[card_id] = self.cards[card_id]["quantity"]
                else:
                    counts[card_id] = -1

        return counts

    def action_card_counts(self):
        active_cards = []
        for i in range(len(ACTION_CARDS_LIST)):
            active_cards.append(1 if i in self.cards else 0)
        return active_cards

    def get_active_treasure_cards(self):
        active_cards = []
        for i in range(len(TREASURE_CARDS_LIST)):
            active_cards.append(1 if i in self.cards else 0)
        return active_cards

    def get_active_victory_cards(self):
        active_cards = []
        for i in range(len(VICTORY_CARDS_LIST)):
            active_cards.append(1 if i in self.cards else 0)
        return active_cards

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
        self.log(
            "Query for cards of type: %s costing %s: %i " % (card_type, mode, threshold)
        )
        card_type_filters = {
            "action": lambda x: x < 100,
            "treasure": lambda x: 100 <= x < 200,
            "victory": lambda x: x >= 200,
            "any": lambda x: True,
        }
        card_price_filters = {
            "exact": lambda x, y=threshold: self.cards[x]["card"]["price"] == y,
            "min": lambda x, y=threshold: self.cards[x]["card"]["price"] >= y,
            "max": lambda x, y=threshold: self.cards[x]["card"]["price"] <= y,
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
        self.cards[card_id]["quantity"] -= amt
