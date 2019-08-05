import abc


class VictoryCard(abc.ABC):
    @abc.property
    def price(self):
        pass

    @abc.property
    def victory_points(self):
        pass
