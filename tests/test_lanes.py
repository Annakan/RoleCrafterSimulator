
from simulators.refined_simulator import Lane
from simulators.card.card_templates import *


def test_lane():

    lane_size = 6
    lane = Lane(_size=lane_size)
    assert all(l is None for l in lane)
    assert lane.free_count() == lane_size

    reject = lane.add_card(default_card_template_40.generate_same())
    assert len(reject) == 0
    assert lane.free_lane_space() == lane_size - 1
    assert lane.first_free_slot() == 1
    assert len(lane) == lane_size

    reject = lane.add_card(tool_card_template.generate_same(cid="tool_fixed"))
    assert len(reject) == 0

    card0 = default_card_template_50.generate_same(cid="card0")
    reject = lane.add_card(card0)
    assert len(reject) == 0
    assert lane.first_free_slot() == 3
    assert lane.free_lane_space() == lane_size - 3
    assert len(lane) == lane_size

    card1 = default_card_template_70.generate_same(cid="card1")
    reject = lane.add_card(card1, at_pos=4)
    assert lane.at_pos(4) == card1
    assert len(reject) == 0
    assert lane.first_free_slot() == 3  # we still have a free slot at index 3 even if we filled index 4
    assert lane.free_lane_space() == lane_size - 4
    assert len(lane) == lane_size

    card2 = default_card_template_50.generate_same(cid="card2")
    reject = lane.add_card(card2)
    assert len(reject) == 0
    assert lane.at_pos(3) == card2
    assert lane.first_free_slot() == 5  # we have filled index 3 and 4 was occupied
    assert lane.free_lane_space() == lane_size - 5
    assert len(lane) == lane_size

    card3 = default_card_template_90.generate_same(cid="card3")
    reject = lane.add_card(card3, at_pos=4)
    assert lane.at_pos(4) == card3
    assert lane.at_pos(5) == card1
    card4 = default_card_template_90.generate_same(cid="card4")
    reject = lane.add_card(card4, at_pos=3)
    assert(lane.at_pos(3) == card4)
    assert len(reject) == 1
    assert reject[0] == card1

    # but we have a fixed card in position 2 (index 1)
    fixed_card_at1 = lane.at_pos(1)
    assert fixed_card_at1.is_fixed
    card5 = default_card_template_100.generate_same(cid="card4")
    reject = lane.add_card(card5, at_pos=1)
    assert lane.at_pos(1) == fixed_card_at1
    assert lane.at_pos(2) == card5
    assert len(reject) == 1
    assert reject[0] == card3

    # let's add_card other fixed cards in position 3 and 6 (index 2 and 5)
    fixed_card_at2 = tool_card_template.generate_same(cid="fixed_card_at2")
    reject = lane.add_card(fixed_card_at2, at_pos=2)
    assert reject[0] == card2
    assert lane.at_pos(5) == card4
    fixed_card_at5 = tool_card_template.generate_same(cid="fixed_card_at5")
    reject = lane.add_card(fixed_card_at5, at_pos=5)
    assert reject[0] == card4

    card6 = product_card_template_40.generate_same()
    assert (lane.at_pos(4) == card0)  # This card will be pushed out
    reject = lane.add_card(card6, at_pos=1)
    assert lane.at_pos(1) == fixed_card_at1
    assert lane.at_pos(2) == fixed_card_at2
    assert lane.at_pos(5) == fixed_card_at5
    assert lane.at_pos(4) == card5
    assert len(reject) == 1
    assert reject[0] == card0




