import queue
import random


class Player:
    def __init__(self, name):
        self.name = name
        self.deck = queue.Queue()
        self.discard = [100] * 7 + [200] * 3
        self.hand = []
        self.shuffle_discard_to_deck()
        self.draw_end_of_turn()
        self.action_stack = []

    def shuffle_discard_to_deck(self):
        random.shuffle(self.discard)
        map(self.deck.put, self.discard)

    def discard(self, qty):
        for i in range(qty):
            self.discard.append(self.hand.pop())

    def draw(self, qty):
        for i in range(qty):
            if not self.deck:
                self.shuffle_discard_to_deck()
            if self.deck:
                self.hand.append(self.deck.get())

    def end_turn(self):
        self.discard(len(self.hand))
        self.shuffle_discard_to_deck()
        self.draw(5)

    def do_action(self):
        pass

    def do_buy(self):
        pass
