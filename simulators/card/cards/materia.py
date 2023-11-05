from ..core import Card, MaterialCard
from ...refined_simulator import VisibleGameState


class MateriaInstanceCard(MaterialCard):
    _CardID = "M:701:01"  # @TODO remove last : when present the number after is the card variation (illustration
    # change for instance)

    def can_play(self, state: VisibleGameState) -> bool:
        return True
