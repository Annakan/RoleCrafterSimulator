import pytest
from pprint import pprint
from simulators.refined_simulator import CraftGame, Atelier


@pytest.fixture
def atelier():
    return Atelier(lane_size=5, reserve_size=3)


def test_simple_game(mid_craft_project, atelier):
    craft_game = CraftGame(project=mid_craft_project,
                           craft_skill=90,
                           craft_endurance=20,
                           atelier=atelier,
                           )
    craft_game.start()
    craft_game.play_game()
    print()
    pprint(f"{craft_game.summary()}")
    pprint(craft_game)

