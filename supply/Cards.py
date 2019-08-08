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


ACTION_CARDS_LIST = [
    {
        "id": 0,
        "name": "Cellar",
        "price": 2,
        "actions": [Actions.PLUS_ACTION, Actions.DISCARD_ANY_AMOUNT_AND_REDRAW],
    },
    {"id": 1, "name": "Chapel", "price": 2, "actions": [Actions.OPTIONAL_TRASH] * 4},
    {"id": 2, "name": "Moat", "price": 2, "actions": [Actions.PLUS_CARD] * 2},
    {
        "id": 3,
        "name": "Harbinger",
        "price": 3,
        "actions": [
            Actions.PLUS_CARD,
            Actions.PLUS_ACTION,
            Actions.OPTIONAL_PLUS_CARD_FROM_DISCARD,
        ],
    },
    {"id": 4, "name": "Merchant", "price": 3, "actions": []},
    {
        "id": 5,
        "name": "Village",
        "price": 3,
        "actions": [Actions.PLUS_CARD] + [Actions.PLUS_ACTION] * 2,
    },
    {
        "id": 6,
        "name": "Workshop",
        "price": 3,
        "actions": [Actions.GAIN_CARD_UP_TO_FOUR],
    },
    {
        "id": 7,
        "name": "Militia",
        "price": 4,
        "actions": [Actions.OTHERS_DISCARD_TO_THREE, Actions.PLUS_2_TREASURE],
    },
    {
        "id": 8,
        "name": "Moneylender",
        "price": 4,
        "actions": [Actions.OPTIONAL_TRASH_COPPER_FOR_THREE],
    },
    {
        "id": 9,
        "name": "Poacher",
        "price": 4,
        "actions": ([Actions.PLUS_CARD, Actions.PLUS_ACTION, Actions.PLUS_1_TREASURE]),
    },
    {
        "id": 10,
        "name": "Remodel",
        "price": 4,
        "actions": [Actions.TRASH_FROM_HAND_FOR_VALUE_PLUS_TWO],
    },
    {"id": 11, "name": "Smithy", "price": 4, "actions": ([Actions.PLUS_CARD] * 3)},
    {
        "id": 12,
        "name": "ThroneRoom",
        "price": 4,
        "actions": [Actions.DOUBLE_PLAY_FROM_HAND],
    },
    {
        "id": 13,
        "name": "CouncilRoom",
        "price": 5,
        "actions": (
            [Actions.PLUS_CARD] * 4 + [Actions.PLUS_BUY] + [Actions.OTHERS_DRAW_ONE]
        ),
    },
    {
        "id": 14,
        "name": "Festival",
        "price": 5,
        "actions": (
            [Actions.PLUS_ACTION] * 2 + [Actions.PLUS_BUY] + [Actions.PLUS_2_TREASURE]
        ),
    },
    {
        "id": 15,
        "name": "Laboratory",
        "price": 5,
        "actions": ([Actions.PLUS_CARD] * 2 + [Actions.PLUS_ACTION]),
    },
    {
        "id": 16,
        "name": "Market",
        "price": 5,
        "actions": (
            [
                Actions.PLUS_CARD,
                Actions.PLUS_ACTION,
                Actions.PLUS_BUY,
                Actions.PLUS_1_TREASURE,
            ]
        ),
    },
    {
        "id": 17,
        "name": "Mine",
        "price": 5,
        "actions": [Actions.TRASH_TREASURE_FOR_VALUE_PLUS_THREE],
    },
    {
        "id": 18,
        "name": "Witch",
        "price": 5,
        "actions": [Actions.PLUS_CARD] * 2 + [Actions.OTHERS_GAIN_CURSE],
    },
    {
        "id": 19,
        "name": "Woodcutter",
        "price": 3,
        "actions": [Actions.PLUS_BUY, Actions.PLUS_2_TREASURE],
    },
    {
        "id": 20,
        "name": "Feast",
        "price": 3,
        "actions": [Actions.TRASH_THIS, Actions.GAIN_CARD_UP_TO_FIVE],
    },
]

TREASURE_CARDS_LIST = [
    {"id": 100, "name": "Copper", "price": 0, "value": 1},
    {"id": 101, "name": "Silver", "price": 3, "value": 2},
    {"id": 102, "name": "Gold", "price": 6, "value": 3},
]


VICTORY_CARDS_LIST = [
    {"id": 200, "name": "Estate", "price": 2, "points": 1},
    {"id": 201, "name": "Duchy", "price": 5, "points": 3},
    {"id": 202, "name": "Province", "price": 8, "points": 6},
]
