import random

# A 2 3 4 5 6 7 8 9 T J Q K
# H D S C
# Card is suitvalue
card_values = {
    "A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 10, "Q": 10, "K": 10
}
def get_card_value(card: str)->int:
    return card_values[card[-1]]

def draw_cards(num_cards: int)-> list[str]:
    """Draw N cards from a complete deck"""
    full_deck = []
    for suit in ['H', 'D', 'S', 'C']:
        for number in card_values.keys():
            full_deck.append(suit+number)

    return random.sample(full_deck, num_cards)
