
def test_deck_building(mid_craft_project):
    deck = mid_craft_project.generate_deck()
    assert len(deck) > 0
    # TODO
