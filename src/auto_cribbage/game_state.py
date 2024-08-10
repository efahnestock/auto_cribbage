#!/usr/bin/env python
from auto_cribbage.cards import draw_cards
class GameState:
    num_players: int
    current_player: int
    scores: list[int]
    hands: list[list[str]]
    current_round_played_cards: list[str]

    def __init__(
        self: "GameState",
        num_players: int,
    ) -> None:
        self.num_players = num_players # max 4
        self.reset()

    def reset(self) -> None:
        """Reset the game to the beginning"""
        self.current_player = 0
        self.current_round_played_cards = []
        self.scores = [0] * self.num_players

        # cribbage hands per player count
        #  2 -> 6 cards per player
        #  3 -> 5
        #  4 -> 5
        num_cards_per_player = 6 if self.num_players <= 2 else 5

        all_cards = draw_cards(num_cards_per_player * self.num_players + 1)
        self.hands = []
        for player_index in range(self.num_players):
            start_idx = player_index * num_cards_per_player
            end_idx = start_idx + num_cards_per_player
            self.hands[player_index] = all_cards[start_idx:end_idx]

        self.cut_card = all_cards[-1]
