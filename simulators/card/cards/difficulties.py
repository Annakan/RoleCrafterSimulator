from ..core import Card
from ...refined_simulator import VisibleGameState


class BlanckDifficulty(Card):
    _CardID = "D:701:01"  # @TODO remove last : when present the number after is the card variation (illustration change for instance)

    def can_play(self, state: VisibleGameState) -> bool:
        return True


