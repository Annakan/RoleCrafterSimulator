import pytest

from simulators.cards import CardTemplate, modulate, generate_variations
from simulators.card_templates import *


def test_card_from_tpl():
    card = materia_card_template_L1.generate_same()
    assert card.c == materia_card_template_L1.c
    assert card.d == materia_card_template_L1.d
    assert card.t == materia_card_template_L1.t

    card = product_card_template_L1.generate_same(cid="Base")
    assert card.c == product_card_template_L1.c
    assert card.d == product_card_template_L1.d
    assert card.t == product_card_template_L1.t
    assert card.cid.startswith("Base")


def test_fixed():
    card = tool_card_template.generate_same()
    assert card.is_fixed


def test_modulate():
    for i in range(100):
        x = modulate(50, 10)
        assert 40 <= x <= 60


def test_generate_variations1():
    # variations = generate_variations(materia_card_template_L1, 10)
    variations = materia_card_template_L1.generate_variations(count=10)
    assert len(variations) == 10
    for v in variations:
        assert v.t == materia_card_template_L1.t
        assert materia_card_template_L1.c - 10 <= v.c <= materia_card_template_L1.c + 10
        assert materia_card_template_L1.d - 10 <= v.d <= materia_card_template_L1.d + 10

