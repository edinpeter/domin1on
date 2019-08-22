import logging

from .Cards import Actions, BuyActions


class ActionHandler:
    def __init__(self, player, supply, global_action_handler):
        self.logger = logging.getLogger("domin1on")
        self.player = player
        self.supply = supply
        self.global_action_handler = global_action_handler

        self.action_stack = [Actions.PLUS_ACTION]
        self.buy_stack = [BuyActions.PLUS_BUY]
        self.global_action_stack = []

    def log(self, msg):
        self.logger.debug("Player %s ActionHandler: %s" % (self.player.name, msg))

    def log_err(self, msg):
        self.logger.error("Player %s ActionHandler: %s" % (self.player.name, msg))

    def process_action(self, action):
        if action == Actions.PLUS_ACTION:
            played_card = self.player.do_action()
            if played_card:
                for action in reversed(
                    self.supply.get_card_info(played_card)["actions"]
                ):
                    if action in Actions:
                        if action == Actions.TRASH_THIS:
                            self.player.trash_from_in_play(played_card)
                        else:
                            self.action_stack.append(action)
                    elif action in BuyActions:
                        self.buy_stack.append(action)

        elif action == Actions.PLUS_CARD:
            self.player.draw(1)
        elif action == Actions.DISCARD_ANY_AMOUNT_AND_REDRAW:
            self.player.discard_any_and_redraw()
        elif action == Actions.OPTIONAL_TRASH:
            self.player.optional_trash()
        elif action == Actions.OPTIONAL_PLUS_CARD_FROM_DISCARD:
            self.player.optional_draw_from_discard()
        elif action == Actions.GAIN_CARD_UP_TO_FOUR:
            self.player.gain_card(4)
        elif action == Actions.GAIN_CARD_UP_TO_FIVE:
            self.player.gain_card(5)
        elif action == Actions.OTHERS_DISCARD_TO_THREE:
            return Actions.OTHERS_DISCARD_TO_THREE
        elif action == Actions.PLUS_1_TREASURE:
            self.player.increment_treasure_balance(1)
        elif action == Actions.PLUS_2_TREASURE:
            self.player.increment_treasure_balance(2)
        elif action == Actions.OPTIONAL_TRASH_COPPER_FOR_THREE:
            if self.player.can_trash(100):
                self.player.trash(100)
                self.player.increment_treasure_balance(3)
        elif action == Actions.TRASH_FROM_HAND_FOR_VALUE_PLUS_TWO:
            trashed_card = self.player.force_trash()
            if trashed_card != -1:
                trashed_card = self.supply.get_card_info(trashed_card)
                value = trashed_card["price"] + 2
                self.player.gain_card(value)
        elif action == Actions.DOUBLE_PLAY_FROM_HAND:
            played_card = self.player.do_action()
            if played_card:
                for action in reversed(
                    self.supply.get_card_info(played_card)["actions"] * 2
                ):
                    if action in Actions:
                        if action == Actions.TRASH_THIS:
                            self.player.trash_from_in_play(played_card)
                        else:
                            self.action_stack.append(action)
                    elif action in BuyActions:
                        self.buy_stack.append(action)
        elif action == Actions.OTHERS_DRAW_ONE:
            return Actions.OTHERS_DRAW_ONE
        elif action == Actions.TRASH_TREASURE_FOR_VALUE_PLUS_THREE:
            trashed_card = self.player.force_trash_treasure()
            if trashed_card:
                trashed_card = self.supply.get_card_info(trashed_card)
                value = trashed_card["price"] + 3
                self.player.gain_card(value, mode="exact", card_type="treasure")
        elif action == Actions.OTHERS_GAIN_CURSE:
            return Actions.OTHERS_GAIN_CURSE
        else:
            raise NotImplementedError("action not implemented: ", action)

    def process_buy(self, buy_action):
        if buy_action == BuyActions.PLUS_BUY:
            self.player.do_buy()

    def process_actions(self):
        while self.action_stack:
            self.log("Current action stack: %s" % str(self.action_stack))
            """
            if len(self.action_stack) > 50:
                self.log_err(self.action_stack)
                self.log_err(self.player.get_card_counts())
                self.log_err(self.buy_stack)
                self.log_err(self.player.in_play)
                self.log_err(self.player.discard_pile)
                raise ValueError
            """
            action = self.action_stack.pop()
            global_action = self.process_action(action)
            if global_action:
                self.global_action_handler.process_global_action(global_action)
        self.player.end_action_phase()
        while self.buy_stack:
            self.log("Current buy stack: %s" % str(self.buy_stack))
            action = self.buy_stack.pop()
            global_action = self.process_buy(action)
            if global_action:
                self.global_action_handler.process_global_action(global_action)
