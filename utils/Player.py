import logging
import queue
import random

import keras
import numpy as np
from keras.layers import Dense
from keras.models import Sequential


class Player:
    def __init__(self, name, supply, random_inputs=False):
        self.in_play = []
        self.logger = logging.getLogger("domin1on")
        self.supply_ref = supply
        self.name = name
        self.deck = queue.SimpleQueue()
        self.discard_pile = [100] * 7 + [200] * 3
        self.hand = []
        self.shuffle_discard_to_deck()
        self.end_turn()
        self.treasure_balance = 0
        self.random_inputs = random_inputs
        self.log(
            "Initialized player: %s with starting hand: %s"
            % (self.name, str(self.hand))
        )
        self.card_counts = {100: 7, 200: 3}

    def get_card_counts(self):
        counts = {}
        supply_counts = self.supply_ref.get_card_counts()
        sorted_supply_counts = sorted(supply_counts.items(), key=lambda kv: kv[0])
        for kv in sorted_supply_counts:
            card_id, supply_count = kv[0], kv[1]
            if supply_count == -1:
                counts[card_id] = -1
            elif card_id in self.card_counts:
                counts[card_id] = self.card_counts[card_id]
            else:
                counts[card_id] = 0
        return counts

    def log(self, msg):
        self.logger.debug("Player %s: %s" % (self.name, msg))

    def shuffle_discard_to_deck(self):
        self.log(
            "Shuffling %i cards from discard pile into deck" % len(self.discard_pile)
        )
        random.shuffle(self.discard_pile)
        # map(self.deck.put, self.discard_pile)
        while self.discard_pile:
            self.deck.put(self.discard_pile.pop())
        self.log(
            "New length of discard pile: %i, new length of deck queue: %i"
            % (len(self.discard_pile), self.deck.qsize())
        )

    def discard(self, qty):
        self.log("Discarding %i cards" % qty)
        for i in range(qty):
            self.discard_pile.append(self.hand.pop())

    def discard_specific(self, card_id):
        self.log("Discarding card: %i" % card_id)
        self.hand.remove(card_id)
        self.discard_pile.append(card_id)

    def clear_in_play(self):
        while self.in_play:
            self.discard_pile.append(self.in_play.pop())

    def play_specific(self, card_id):
        self.log("Discarding card: %i" % card_id)
        self.hand.remove(card_id)
        self.in_play.append(card_id)

    def draw(self, qty):
        self.log("Drawing %i cards" % qty)
        for i in range(qty):
            if self.deck.empty():
                self.log("Deck is empty, shuffling discard pile into the deck")
                self.shuffle_discard_to_deck()
            if not self.deck.empty():
                self.hand.append(self.deck.get())

    def trash(self, card):
        self.log("Trashing card: %i" % card)
        self.hand.remove(card)
        self.card_counts[card] -= 1

    def trash_from_discard(self, card):
        self.discard_pile.remove(card)
        self.card_counts[card] -= 1

    def trash_from_in_play(self, card):
        self.in_play.remove(card)
        self.card_counts[card] -= 1

    def gain_from_supply(self, card):
        self.discard_pile.append(card)
        self.supply_ref.decrement_card(card)
        if card in self.card_counts:
            self.card_counts[card] += 1
        else:
            self.card_counts[card] = 1

    def end_turn(self):
        self.treasure_balance = 0
        self.discard(len(self.hand))
        self.clear_in_play()
        self.draw(5)
        self.log(
            "Turn ended, length of hand: %i, length of discard: %i, deck queue size: %i"
            % (len(self.hand), len(self.discard_pile), self.deck.qsize())
        )

    def calc_score(self):
        self.discard(len(self.hand))
        self.shuffle_discard_to_deck()
        score = 0
        while not self.deck.empty():
            card = self.deck.get()
            if card >= 200:
                score += self.supply_ref.get_card_info(card)["points"]
        return score

    def do_action(self):
        self.log("New action, current hand: %s" % str(self.hand))
        action_cards_in_hand = [card for card in self.hand if card < 100]
        action_cards_in_hand += [-1]
        action_card_choice = self.prompt_action_card(action_cards_in_hand)
        if action_card_choice != -1:
            self.play_specific(action_card_choice)
            return action_card_choice
        else:
            return None

    def end_action_phase(self):
        self.log("Ending action phase...")
        treasure_cards = [card for card in self.hand if 100 <= card < 200]
        self.log(
            "Treasure cards in hand: %s, starting treasure balance: %i"
            % (str(treasure_cards), self.treasure_balance)
        )
        for treasure_card in treasure_cards:
            self.treasure_balance += self.supply_ref.get_card_info(treasure_card)[
                "value"
            ]

        self.log("Available balance: %i" % self.treasure_balance)

    def do_buy(self):
        buyable_cards = self.supply_ref.get_cards_costing(
            self.treasure_balance, mode="max"
        ) + [-1]
        buy_choice = self.prompt_buy_card(buyable_cards)

        if buy_choice != -1:
            self.gain_from_supply(buy_choice)
            self.treasure_balance -= self.supply_ref.get_card_info(buy_choice)["price"]

    def increment_treasure_balance(self, amt):
        self.treasure_balance += amt

    def force_discard(self):
        choice = self.prompt_discard_card()
        self.discard_specific(choice)

    def discard_any_and_redraw(self):
        amt = self.prompt_discard_number()
        for i in range(amt):
            to_discard = self.prompt_discard_card()
            self.discard_specific(to_discard)
        self.draw(amt)

    def optional_trash(self):
        card_to_trash = self.prompt_trash_card(optional=True)
        if card_to_trash != -1:
            self.trash(card_to_trash)

    def force_trash(self):
        if self.hand:
            card_to_trash = self.prompt_trash_card(optional=False)
            self.trash(card_to_trash)
            return card_to_trash
        else:
            return -1

    def force_trash_treasure(self):
        choices = [card for card in self.hand if 100 <= card <= 200]
        if choices:
            card_to_trash = self.prompt_trash_card(choices=choices, optional=False)
            self.trash(card_to_trash)
            return card_to_trash

    def optional_draw_from_discard(self):
        card_to_draw = self.prompt_draw_from_discard()
        if card_to_draw != -1:
            self.discard_pile.remove(card_to_draw)
            self.hand.append(card_to_draw)

    def gain_card(self, price, mode="max", card_type="any"):
        choices = self.supply_ref.get_cards_costing(
            price, mode=mode, card_type=card_type
        )
        if choices:
            card_to_gain = self.prompt_gain_card(choices)
            self.gain_from_supply(card_to_gain)

    def can_trash(self, card_id):
        return card_id in self.hand


class HumanPlayer(Player):
    def prompt_gain_card(self, choices):
        if self.random_inputs:
            return random.choice(choices)
        choice = input("Choose a card to gain: %s" % str(choices))
        while not (self.is_int(choice) and int(choice) in choices):
            choice = input("Invalid Card: Choose a card to gain: %s" % str(choices))
        return int(choice)

    def prompt_draw_from_discard(self):
        choices = self.discard_pile + [-1]
        if self.random_inputs:
            return random.choice(choices)
        choice = input("Choose a card to draw from discard: %s" % choices)
        while not (self.is_int(choice) and int(choice) in choices):
            choice = input(
                "Invalid Card: Choose a card to draw from discard: %s" % str(self.hand)
            )
        return int(choice)

    def prompt_trash_card(self, choices=None, optional=True):
        if not choices:
            choices = self.hand + ([-1] if optional else [])
        if self.random_inputs:
            return random.choice(choices)
        choice = input("Choose a card to trash: %s" % choices)
        while not (self.is_int(choice) and int(choice) in choices):
            choice = input("Invalid Card: Choose a card to trash: %s" % str(self.hand))
        return int(choice)

    def prompt_action_card(self, choices):
        if self.random_inputs:
            return random.choice(choices)
        choice = input("Choose a card to play: %s" % str(choices))
        while not (self.is_int(choice) and int(choice) in choices):
            choice = input("Invalid Card: Choose a card to play: %s" % str(choices))
        return int(choice)

    def prompt_buy_card(self, choices):
        if self.random_inputs:
            return random.choice(choices)
        choice = input(
            "Player %s: Choose a card to buy: %s" % (self.name, str(choices))
        )
        while not (self.is_int(choice) and int(choice) in choices):
            choice = input("Invalid Card: Choose a card to buy: %s" % str(choices))
        return int(choice)

    def prompt_discard_card(self):
        choices = self.hand
        if self.random_inputs:
            return random.choice(choices)
        choice = input("Choose a card to discard: %s" % str(choices))
        while not (self.is_int(choice) and int(choice) in choices):
            choice = input("Invalid Card: Choose a card to buy: %s" % str(choices))
        return int(choice)

    def prompt_discard_number(self):
        choices = list(range(0, len(self.hand)))
        if self.random_inputs:
            return random.choice(choices)
        choice = input("Choose a card to discard: %s" % choices)
        while not (self.is_int(choice) and int(choice) in choices):
            choice = input(
                "Invalid Amount: Choose a an amount to discard: %s" % str(self.hand)
            )
        return int(choice)

    @staticmethod
    def is_int(input):
        try:
            num = int(input)
        except ValueError:
            return False
        return True


class MachinePlayer(Player):
    def __init__(self, name, supply, networks_config):
        super().__init__(name, supply)
        self.networks = self.get_netset(networks_config)

    def get_netset(self, networks_config):
        # Iterate over dictionary with kv = {"net_name" : (model_config, model_weights)}
        # Return netset for each network {"net_name" : predict-able_network }
        networks = {}
        for network_name in networks_config:
            network_config = networks_config[network_name]
            networks[network_name] = self.import_model(network_config)
        return networks

    def import_model(self, model_info):
        config, weights = model_info[0], model_info[1]
        model = Sequential.from_config(config)
        model.set_weights(weights)
        model._make_predict_function()
        return model

    def get_supply_input_vector(self):
        counts = self.supply_ref.get_card_counts()
        sorted_supply_counts = sorted(counts.items(), key=lambda kv: kv[0])
        supply_counts = map(lambda x: x[1], sorted_supply_counts)
        return list(supply_counts)

    def get_deck_input_vector(self):
        counts = self.get_card_counts()
        sorted_deck_counts = sorted(counts.items(), key=lambda kv: kv[0])
        deck_counts = map(lambda x: x[1], sorted_deck_counts)
        return list(deck_counts)

    def get_input_vectors(self, supply_input_vector, deck_input_vector, choices):
        input_vector = supply_input_vector + deck_input_vector
        input_vectors = []
        for choice in choices:
            input_vectors.append(input_vector + [choice])
        return input_vectors

    def get_network_choice(self, network_name, choices):
        supply_input_vector = self.get_supply_input_vector()
        deck_input_vector = self.get_deck_input_vector()

        input_vectors = self.get_input_vectors(
            supply_input_vector, deck_input_vector, choices
        )
        input_vectors = np.array(input_vectors)
        predictions = self.networks[network_name].predict(input_vectors)
        return choices[np.argmax(predictions)]

    def prompt_gain_card(self, choices):
        choice = self.get_network_choice("gain", choices)
        return choice

    def prompt_draw_from_discard(self):
        choices = self.discard_pile + [-1]
        choice = self.get_network_choice("draw_discard", choices)
        return choice

    def prompt_trash_card(self, choices=None, optional=True):
        if not choices:
            choices = self.hand + ([-1] if optional else [])
        choice = self.get_network_choice("trash", choices)
        return choice

    def prompt_action_card(self, choices):
        choice = self.get_network_choice("action", choices)
        return choice

    def prompt_buy_card(self, choices):
        choice = self.get_network_choice("buy", choices)
        return choice

    def prompt_discard_card(self):
        choices = self.hand
        choice = self.get_network_choice("discard", choices)
        return choice

    def prompt_discard_number(self):
        choices = list(range(0, len(self.hand)))
        choice = self.get_network_choice("discard_number", choices)
        return choice
