import pytest

from simulators.cards import CardTemplate, modulate, generate_variations
from simulators.card_templates import *


@pytest.fixture
def card_mat_l1_tpl():
    return materia_card_template_L1


@pytest.fixture
def card_mat_l2_tpl():
    return materia_card_template_L2


@pytest.fixture
def card_default40_tpl():
    return CardTemplate(t="default40", c=40)


@pytest.fixture
def card_default50_tpl():
    return CardTemplate(t="default50", c=50)


@pytest.fixture
def card_craft50_tpl():
    return CardTemplate("craft50", c=50, d=-1)


def test_card_from_tpl(card_mat_l1_tpl):
    card = card_mat_l1_tpl.generate_same()
    assert card.c == card_mat_l1_tpl.c
    assert card.d == card_mat_l1_tpl.d
    assert card.t == card_mat_l1_tpl.t


def test_modulate():
    for i in range(100):
        x = modulate(50, 10)
        assert 40 <= x <= 60


def test_generate_variations1(card_mat_l2_tpl):
    # variations = generate_variations(card_mat_l2_tpl, 10)
    variations = card_mat_l2_tpl.generate_variations(count=10)
    assert len(variations) == 10
    for v in variations:
        assert v.t == card_mat_l2_tpl.t
        assert card_mat_l2_tpl.c - 10 <= v.c <= card_mat_l2_tpl.c + 10
        assert card_mat_l2_tpl.d - 10 <= v.d <= card_mat_l2_tpl.d + 10
