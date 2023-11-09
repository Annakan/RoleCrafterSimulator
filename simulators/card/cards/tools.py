from ..core import Card, ToolCard
from ...refined_simulator import VisibleGameState


class ToolCardTemplate(ToolCard):
    _card_id = "D:302:01"
    name = "Fluidifiant Actif"
    category = "Permanent"
    properties = ["Placé 4 | Immobile"]
    effect = "Gagne un point d'endurance"
    complexity = 70
    difficulty_value = 90
    rarity = "R"

    """
    1	O	Permanent	D:302:01	normal	Fluidifiant Actif	"Placé 4 | Immobile"	Gagne un point d'endurance	70	90	Les outils s'activent sur un test d'artisanat simple			R				Les outils s'activent sur un test d'artisanat simple

    """
    pass
