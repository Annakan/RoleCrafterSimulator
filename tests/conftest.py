import pytest

from simulators.refined_simulator import CraftProject
from simulators.card_templates import *


@pytest.fixture
def mid_craft_project():
    return CraftProject(products_tpls=[(product_card_template_L1, 6), ],
                        materias_tpls=[(materia_card_template_L2, 5), ],
                        defaults_tpls=[(default_card_template_L2, 8), (default_card_template_L3, 3)],
                        tools_tpls=[])
