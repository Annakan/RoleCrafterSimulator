import msgspec.json
import pytest

from simulators.game_state import *


@pytest.fixture
def lane():
    lane = LaneStruct(cards=["C14", None, None, "C15"], slots_modifier=[-10, 30, 20, 0])
    return lane


@pytest.fixture
def reserve():
    reserve = LaneStruct(cards=["C34", None, None, "C45"], slots_modifier=[10, 0, -20, 10])
    return reserve


@pytest.fixture
def crafter_hand():
    ch = CrafterHandStruct(cards=["C12", "U34", "C45"])
    return ch


@pytest.fixture
def crafter_state():
    cs = CrafterState(endurance=20, skill=75)
    return cs


@pytest.fixture
def atelier(lane, reserve):
    atelier = AtelierStruct(lane, reserve, damage_resistance=0, complexity=100)
    return atelier


def test_visible_game_state_struct(crafter_state, crafter_hand, atelier):
    vgs = VisibleGameStateStruct(turn=0, crafter=crafter_state, turn_modifier=10,
                                 crafter_hand=crafter_hand, atelier=atelier)
    assert vgs.turn_modifier == 10
    assert vgs.crafter_hand.cards[0] == "C12"
    assert vgs.lane.cards[0] == "C14"
    assert vgs.lane.slots_modifier[0] == -10

