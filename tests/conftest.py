import pytest

from simulators.refined_simulator import CraftProject
from simulators.card_templates import *  # noqa: F403


@pytest.fixture
def mid_craft_project():
    return CraftProject(
        products_tpls=[
            (product_card_template_40, 6),
        ],
        materias_tpls=[
            (materia_card_template_50, 5),
        ],
        defaults_tpls=[(default_card_template_70, 10), (default_card_template_90, 4)],
        tools_tpls=[],
    )
