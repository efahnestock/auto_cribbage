#!/usr/bin/env python
import random
import math
from auto_cribbage.cards import draw_cards, get_card_value

class GameState:
    num_players: int
    current_player: int
    last_to_play: int # -1 if no one has played
    scores: list[int]
    hands: list[list[str]]
    current_round_played_cards: list[str]

    def __init__(
        self: "GameState",
        num_players: int,
        seed = None
    ) -> None:
        if type(num_players) != int or num_players < 2 or num_players > 4:
            raise ValueError("Only 2-4 players are allowed")
        self.num_players = num_players # max 4
        self.reset(random.Random(seed))

    def reset(self, random_state: random.Random = random.Random()) -> None:
        """Reset the game to the beginning"""
        self.current_player = random_state.randint(0, self.num_players - 1)
        self.last_to_play = -1
        self.current_round_played_cards = []
        self.scores = [0] * self.num_players

        # cribbage hands per player count
        #  2 -> 6 cards per player
        #  3 -> 5
        #  4 -> 5
        num_cards_per_player = 6 if self.num_players <= 2 else 5

        all_cards = draw_cards(num_cards_per_player * self.num_players + 1, random_state)
        self.hands = []
        for player_index in range(self.num_players):
            start_idx = player_index * num_cards_per_player
            end_idx = start_idx + num_cards_per_player
            self.hands.append(all_cards[start_idx:end_idx])

        self.cut_card = all_cards[-1]
    @property
    def is_game_over(self)->bool:
        for hand in self.hands:
            if len(hand) > 0:
                return False
        return True
    @property
    def current_round_running_total(self)->int:
        running_total = 0
        for card in self.current_round_played_cards:
            running_total += get_card_value(card)
        return running_total

    def __repr__(self) -> str:
        repr = "#################\n\n" + str(self.num_players) + " Player Cribbage Game\n"
        repr += f"Current player: {self.current_player}. Last to play: {self.last_to_play}\n"
        repr += f"Current run of cards: {self.current_round_played_cards}\n"
        for p_idx in range(self.num_players):
            repr += "\n\t- Player " + str(p_idx) + " has scored: " + str(self.scores[p_idx]) + " pts"
            repr += "\n\t\t with current hand: " + str(self.hands[p_idx])
        return repr




def score_pegging_action(state: GameState, action: str) -> int:
    """
    Count the number of points scored through taking the given action
    """
    assert action is not None
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
    Take an action on the current game state.
    If action is empty understood as a pass
    """
    if (action):
        # add points
        state.scores[state.current_player] += score_pegging_action(state, action)
        # remove card from hand
        state.hands[state.current_player].remove(action)
        # update history of played cards
        state.current_round_played_cards.append(action)
        # update last player to move
        state.last_to_play = state.current_player
    # update current player
    state.current_player = state.current_player + 1 if (state.current_player+1) < state.num_players else 0


def get_pegging_actions(state: GameState)-> list[str]:
    """
    A function that returns the action options avalible to the current player.
    If no action is avalible, an empty list is returned.
    """
    print(state)
    current_pegging_score = sum([get_card_value(card) for card in state.current_round_played_cards])
    playable_card_value = 31 - current_pegging_score
    print(state.current_player)
    print(state.hands[state.current_player])
    playable_cards = [card for card in state.hands[state.current_player] if get_card_value(card) <= playable_card_value]
    return list(filter(lambda card: (get_card_value(card) <= playable_card_value), state.hands[state.current_player]))
