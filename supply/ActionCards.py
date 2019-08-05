from .ActionCard import ActionCard
from enum import Enum, auto


class Actions(Enum):
    PLUS_ACTION = auto()
    PLUS_CARD = auto()
    PLUS_BUY = auto()
    DISCARD_ANY_AMOUNT_AND_REDRAW = auto()
    OPTIONAL_TRASH = auto()
    OPTIONAL_PLUS_CARD_FROM_DISCARD = auto()
    GAIN_CARD_UP_TO_FOUR = auto()
    GAIN_CARD_UP_TO_FIVE = auto()
    OTHERS_DISCARD_TO_THREE = auto()
    PLUS_1_TREASURE = auto()
    PLUS_2_TREASURE = auto()
    OPTIONAL_TRASH_COPPER_FOR_THREE = auto()
    TRASH_FROM_HAND_FOR_VALUE_PLUS_TWO = auto()
    DOUBLE_PLAY_FROM_HAND = auto()
    OTHERS_DRAW_ONE = auto()
    TRASH_TREASURE_FOR_VALUE_PLUS_THREE = auto()
    OTHERS_GAIN_CURSE = auto()
    TRASH_THIS = auto()


class Cellar(ActionCard):
    def __init__(self):
        self.price = 2

    def price(self):
        return self.price

    def play(self):
        return [Actions.PLUS_ACTION, Actions.DISCARD_ANY_AMOUNT_AND_REDRAW]


class Chapel(ActionCard):
    def __init__(self):
        self.price = 2

    def price(self):
        return self.price

    def play(self):
        return [Actions.OPTIONAL_TRASH] * 4


class Moat(ActionCard):
    def __init__(self):
        self.price = 2

    def price(self):
        return self.price

    def play(self):
        return [Actions.PLUS_CARD] * 2


class Harbinger(ActionCard):
    def __init__(self):
        self.price = 3

    def price(self):
        return self.price

    def play(self):
        return [
            Actions.PLUS_CARD,
            Actions.PLUS_ACTION,
            Actions.OPTIONAL_PLUS_CARD_FROM_DISCARD,
        ]


class Merchant(ActionCard):
    def __init__(self):
        self.price = 3

    def price(self):
        return self.price

    def play(self):
        return []


class Village(ActionCard):
    def __init__(self):
        self.price = 3

    def price(self):
        return self.price

    def play(self):
        return [Actions.PLUS_CARD] + [Actions.PLUS_ACTION] * 2


class Workshop(ActionCard):
    def __init__(self):
        self.price = 3

    def price(self):
        return self.price

    def play(self):
        return [Actions.GAIN_CARD_UP_TO_FOUR]


class Militia(ActionCard):
    def __init__(self):
        self.price = 4

    def price(self):
        return self.price

    def play(self):
        return [Actions.OTHERS_DISCARD_TO_THREE, Actions.PLUS_2_TREASURE]


class Moneylender(ActionCard):
    def __init__(self):
        self.price = 4

    def price(self):
        return self.price

    def play(self):
        return [Actions.OPTIONAL_TRASH_COPPER_FOR_THREE]


class Poacher(ActionCard):
    def __init__(self):
        self.price = 4

    def price(self):
        return self.price

    def play(self):
        return [Actions.PLUS_CARD, Actions.PLUS_ACTION, Actions.PLUS_1_TREASURE]


class Remodel(ActionCard):
    def __init__(self):
        self.price = 4

    def price(self):
        return self.price

    def play(self):
        return [Actions.TRASH_FROM_HAND_FOR_VALUE_PLUS_TWO]


class Smithy(ActionCard):
    def __init__(self):
        self.price = 4

    def price(self):
        return self.price

    def play(self):
        return [Actions.PLUS_CARD] * 3


class ThroneRoom(ActionCard):
    def __init__(self):
        self.price = 4

    def price(self):
        return self.price

    def play(self):
        return [Actions.DOUBLE_PLAY_FROM_HAND]


class CouncilRoom(ActionCard):
    def __init__(self):
        self.price = 5

    def price(self):
        return self.price

    def play(self):
        return [Actions.PLUS_CARD] * 4 + [Actions.PLUS_BUY] + [Actions.OTHERS_DRAW_ONE]


class Festival(ActionCard):
    def __init__(self):
        self.price = 5

    def price(self):
        return self.price

    def play(self):
        return (
            [Actions.PLUS_ACTION] * 2 + [Actions.PLUS_BUY] + [Actions.PLUS_2_TREASURE]
        )


class Laboratory(ActionCard):
    def __init__(self):
        self.price = 5

    def price(self):
        return self.price

    def play(self):
        return [Actions.PLUS_CARD] * 2 + [Actions.PLUS_ACTION]


class Market(ActionCard):
    def __init__(self):
        self.price = 5

    def price(self):
        return self.price

    def play(self):
        return [
            Actions.PLUS_CARD,
            Actions.PLUS_ACTION,
            Actions.PLUS_BUY,
            Actions.PLUS_1_TREASURE,
        ]


class Mine(ActionCard):
    def __init__(self):
        self.price = 5

    def price(self):
        return self.price

    def play(self):
        return [Actions.TRASH_TREASURE_FOR_VALUE_PLUS_THREE]


class Witch(ActionCard):
    def __init__(self):
        self.price = 5

    def price(self):
        return self.price

    def play(self):
        return [Actions.PLUS_CARD] * 2 + [Actions.OTHERS_GAIN_CURSE]


class Woodcutter(ActionCard):
    def __init__(self):
        self.price = 3

    def price(self):
        return self.price

    def play(self):
        return [Actions.PLUS_BUY, Actions.PLUS_2_TREASURE]


class Feast(ActionCard):
    def __init__(self):
        self.price = 3

    def price(self):
        return self.price

    def play(self):
        return [Actions.TRASH_THIS, Actions.GAIN_CARD_UP_TO_FIVE]


CARD_LIST = [Cellar, Chapel, Moat, Harbinger, Merchant, Village, Workshop, Militia, Moneylender, Poacher, Remodel, Smithy, ThroneRoom, CouncilRoom, Festival, Laboratory, Market, Mine, Witch, Woodcutter, Feast]
