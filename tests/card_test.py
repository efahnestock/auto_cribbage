import random
from auto_cribbage.cards import get_card_value, draw_cards


def test_draw_cards():
    drawn_cards = draw_cards(5, random.Random(42))
    assert len(drawn_cards) == 5 # we should have 5 cards
    assert len(drawn_cards) == len(set(drawn_cards)) # they should all be unique
