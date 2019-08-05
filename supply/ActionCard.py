import abc


class ActionCard(abc.ABC):
    @abc.property
    def price(self):
        pass

    @abc.abstractmethod
    def play(self):
        pass
