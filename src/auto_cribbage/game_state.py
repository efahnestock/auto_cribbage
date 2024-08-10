#!/usr/bin/env python
import random
import math
from auto_cribbage.cards import draw_cards, get_card_value

class GameState:
    num_players: int
    current_player: int
    last_to_play: int # can not be the one before current player as players can pass
    scores: list[int]
    hands: list[list[str]]
    current_round_played_cards: list[str]

    def __init__(
        self: "GameState",
        num_players: int,
    ) -> None:
        if type(num_players) != int or num_players < 2 or num_players > 4:
            raise ValueError("Only 2-4 players are allowed")
        self.num_players = num_players # max 4
        self.reset()

    def reset(self) -> None:
        """Reset the game to the beginning"""
        self.current_player = random.randint(0, self.num_players)
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
            self.hands.append(all_cards[start_idx:end_idx])

        self.cut_card = all_cards[-1]

    @property
    def current_round_running_total(self)->int:
        running_total = 0
        for card in self.current_round_played_cards:
            running_total += get_card_value(card)
        return running_total

    def __repr__(self) -> str:
        repr = "#################\n\n" + str(self.num_players) + " Player Cribbage Game\n"
        for p_idx in range(self.num_players):
            repr += "\n\t- Player " + str(p_idx) + " has scored: " + str(self.scores[p_idx]) + " pts"
            repr += "\n\t\t with current hand: " + str(self.hands[p_idx])
        return repr




def score_pegging_action(state: GameState, action: str) -> int:
    """
    Count the number of points scored through taking the given action
    """
    num_points = 0
    running_total = state.current_round_running_total
    card_value = get_card_value(action)
    # n of a kind (e.g. pair)
    n_of_a_kind = 0
    for card in reversed(state.current_round_played_cards):
        if action[-1] == card[-1]:
            n_of_a_kind += 1
        else:
            break
    if n_of_a_kind > 0:
        num_points += math.factorial(n_of_a_kind+1)
    # run
    #TODO: add points for getting a run (e.g. 4,5,3,6 is 4 points)
    # 15
    if running_total + card_value == 15:
        num_points += 2
    # 31
    elif running_total + card_value == 31:
        num_points += 2

    return num_points


def take_pegging_action(state: GameState, action: str | None) -> None:
    """
    Take an action on the current game state
    """
    # add points
    # remove card from hand
    # update history of played cards
    # update current player
    if (action):
        state.scores[state.current_player] += score_pegging_action(state, action)
        state.hands[state.current_player].remove(action)
        state.current_round_played_cards.append(action)
    state.current_player = state.current_player + 1 if (state.current_player+1) < state.num_players else 0


def get_pegging_actions(state: GameState)-> list[str]:
    """
    A function that returns the action options avalible to the current player.
    If no action is avalible, an empty list is returned.
    """

    current_pegging_score = sum([get_card_value(card) for card in state.current_round_played_cards])
    playable_card_value = 31 - current_pegging_score
    return list(filter(lambda card: (get_card_value(card) <= playable_card_value), state.hands[state.current_player]))
