import pytest
from pprint import pprint
from simulators.refined_simulator import CraftGame, Atelier, Crafter


@pytest.fixture
def atelier():
    return Atelier(lane_size=5, reserve_size=3)


@pytest.fixture
def crafter():
    return Crafter(craft_skill=70, base_endurance=20, base_skill_modifier=0)


def test_simple_game(mid_craft_project, atelier, crafter):
    craft_game = CraftGame(
        project=mid_craft_project,
        crafter=crafter,
        atelier=atelier,
    )
    craft_game.start()
    craft_game.play_game()
    print()
    pprint(f"{craft_game.summary()}")
    # pprint(craft_game)
