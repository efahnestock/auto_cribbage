# Auto cribbage!

Cribbage

Goal 1: maxize expected points of a hand in counting given which card you discard

- Approach: calculate an expectation manually

Goal 2: create a good cribbage playing agent

Key types:

Key functions:
pick_discard(OrderedCardCollection in_hand) -> OrderedCardCollection out_hand
Given a hand of 5 or 6 cards, pick which card(s) to discard

- Optionally:
  - calculate the expected number of points that each point will come

counting_score(OrderedCardCollection hand) -> int num_points
pegging_score(OrderedCardCollection history) -> int num_points

State class:
current_round_played_cards: list[card] -> history of all previous cards played in pegging round
current_player: int
number_of_players: int
scores: score of each player
[OrderedCardCollection] hands: hands of each player

func get_actions(state)
func take_action(state, action) -> state
