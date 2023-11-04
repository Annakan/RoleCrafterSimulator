import pytest
from pprint import pprint
from simulators.refined_simulator import CraftGame, Atelier, Crafter, RPGPlayerCharacter


@pytest.fixture
def atelier():
    return Atelier(lane_size=5, reserve_size=3)


@pytest.fixture
def character():
    return RPGPlayerCharacter(name="Test Character", craft_skill=100, base_endurance=100)


@pytest.fixture
def crafter(character):
    return Crafter(character=character, base_skill_modifier=0)


def test_simple_game(mid_craft_project, atelier, crafter):
    craft_game = CraftGame(
        project=mid_craft_project,
        crafter=crafter,
        atelier=atelier,
    )
    craft_game.start()
    craft_game.play_full_game()
    print()
    pprint(f"{craft_game.summary}")
    # pprint(craft_game)
