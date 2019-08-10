import queue
import random
import logging
logging.basicConfig(level=logging.DEBUG)

class Player:
    def __init__(self, name, supply):
        self.supply_ref = supply
        self.name = name
        self.deck = queue.Queue()
        self.discard_pile = [100] * 7 + [200] * 3
        self.hand = []
        self.shuffle_discard_to_deck()
        self.end_turn()
        self.treasure_balance = 0
        logging.debug("Initialized player: %s with starting hand: %s" % (self.name, str(self.hand)))

    def shuffle_discard_to_deck(self):
        random.shuffle(self.discard_pile)
        map(self.deck.put, self.discard_pile)

    def discard(self, qty):
        for i in range(qty):
            self.discard_pile.append(self.hand.pop())

    def discard_specific(self, card_id):
        self.hand.remove(card_id)
        self.discard_pile.append(card_id)

    def draw(self, qty):
        for i in range(qty):
            if self.deck.empty():
                self.shuffle_discard_to_deck()
            if not self.deck.empty():
                self.hand.append(self.deck.get())

    def trash(self, card):
        self.hand.remove(card)

    def trash_from_discard(self, card):
        self.discard_pile.remove(card)

    def gain_from_supply(self, card):
        self.discard_pile.append(card)
        self.supply_ref.decrement_card(card)

    def end_turn(self):
        self.treasure_balance = 0
        self.discard(len(self.hand))
        self.shuffle_discard_to_deck()
        self.draw(5)

    def do_action(self):
        action_cards_in_hand = [card for card in self.hand if card < 100]
        action_cards_in_hand += [-1]
        action_card_choice = self.prompt_action_card(action_cards_in_hand)
        if action_cards_in_hand != -1:
            self.discard_specific(action_card_choice)
        return action_card_choice

    def do_buy(self):
        treasure_cards = [card for card in self.hand if 100 <= card <= 200]
        for treasure_card in treasure_cards:
            self.treasure_balance += self.supply_ref.get_card_info(treasure_card).value

        buyable_cards = self.supply_ref.get_cards_costing(
            self.treasure_balance, mode="max"
        )
        buy_choice = self.prompt_buy_card(buyable_cards)

        self.gain_from_supply(buy_choice)
        self.treasure_balance -= self.supply_ref.get_card_info(buy_choice).value

    def increment_treasure_balance(self, amt):
        self.treasure_balance += amt

    def prompt_action_card(self, choices):
        choice = input("Choose a card to play: %s" % str(choices))
        while not (self.is_int(choice) and choice in choices):
            choice = input("Invalid Card: Choose a card to play: %s" % str(choices))
        return int(choice)

    def prompt_buy_card(self, choices):
        choice = input("Choose a card to buy: %s" % str(choices))
        while not (self.is_int(choice) and choice in choices):
            choice = input("Invalid Card: Choose a card to buy: %s" % str(choices))
        return int(choice)

    def prompt_discard_card(self):
        choices = self.hand
        choice = input("Choose a card to discard: %s" % str(choices))
        while not (self.is_int(choice) and choice in choices):
            choice = input("Invalid Card: Choose a card to buy: %s" % str(choices))
        return int(choice)

    def force_discard(self):
        choice = self.prompt_discard_card()
        self.discard_specific(choice)

    def prompt_discard_number(self):
        choices = list(range(0, len(self.hand)))
        choice = input("Choose a card to discard: %s" % choices)
        while not (self.is_int(choice) and choice in choices):
            choice = input(
                "Invalid Amount: Choose a an amount to discard: %s" % str(self.hand)
            )
        return int(choice)

    def discard_any_and_redraw(self):
        amt = self.prompt_discard_number()
        for i in range(amt):
            to_discard = self.prompt_discard_card()
            self.discard_specific(to_discard)
        self.draw(amt)

    def prompt_trash_card(self, choices=None, optional=True):
        if not choices:
            choices = self.hand + [-1] if optional else []
        choice = input("Choose a card to trash: %s" % choices)
        while not (self.is_int(choice) and choice in choices):
            choice = input("Invalid Card: Choose a card to trash: %s" % str(self.hand))
        return int(choice)

    def optional_trash(self):
        card_to_trash = self.prompt_trash_card(optional=True)
        if card_to_trash != -1:
            self.trash(card_to_trash)

    def force_trash(self):
        card_to_trash = self.prompt_trash_card(optional=False)
        self.trash(card_to_trash)
        return card_to_trash

    def force_trash_treasure(self):
        choices = [card for card in self.hand if 100 <= card <= 200]
        if choices:
            card_to_trash = self.prompt_trash_card(choices=choices, optional=False)
            self.trash(card_to_trash)
            return card_to_trash

    def prompt_draw_from_discard(self):
        choices = self.discard_pile + [-1]
        choice = input("Choose a card to draw from discard: %s" % choices)
        while not (self.is_int(choice) and choice in choices):
            choice = input(
                "Invalid Card: Choose a card to draw from discard: %s" % str(self.hand)
            )
        return int(choice)

    def optional_draw_from_discard(self):
        card_to_draw = self.prompt_draw_from_discard()
        if card_to_draw != -1:
            self.discard_pile.remove(card_to_draw)
            self.hand.append(card_to_draw)

    def prompt_gain_card(self, choices):
        choice = input("Choose a card to gain: %s" % str(choices))
        while not (self.is_int(choice) and choice in choices):
            choice = input("Invalid Card: Choose a card to gain: %s" % str(choices))
        return int(choice)

    def gain_card(self, price, mode="max", card_type="any"):
        choices = self.supply_ref.get_cards_costing(
            price, mode=mode, card_type=card_type
        )
        if choices:
            card_to_gain = self.prompt_gain_card(choices)
            self.gain_from_supply(card_to_gain)

    def can_trash(self, card_id):
        return card_id in self.hand

    @staticmethod
    def is_int(input):
        try:
            num = int(input)
        except ValueError:
            return False
        return True
