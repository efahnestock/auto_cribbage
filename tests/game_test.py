import pytest
from auto_cribbage.game_state import GameState, get_pegging_actions, score_pegging_action, take_pegging_action

def make_game():
    state = GameState(2, 42)
    state.current_player = 0
    state.current_round_played_cards = ['CJ', 'H7', 'C7'] # 24 points
    state.hands[0] = ['S7', 'SK', 'S2']
    state.hands[1] = ['SA']
    state.last_to_play = 1
    return state
def test_game_creation():
    state = GameState(2, 42)
    assert state.num_players == 2
    state = GameState(3, 43)
    assert state.num_players == 3
    state = GameState(4, 44)
    assert state.num_players == 4

    with pytest.raises(ValueError):
        state = GameState(1, 42)
    with pytest.raises(ValueError):
        state = GameState(5, 43)


def test_game_reset():
    state = GameState(2, 43)
    state.hands = []
    state.scores = [100,100]
    state.reset()
    assert len(state.hands) > 0
    assert state.scores[0] == 0


def test_get_pegging_actions():
    state = GameState(2, 42)
    actions = get_pegging_actions(state)
    assert(actions == state.hands[state.current_player])
    state = make_game()
    actions = get_pegging_actions(state)
    assert(actions == ['S7', 'S2'])

def test_score_pegging_action():
    state = make_game()
    assert(score_pegging_action(state, 'S7') == 8)
    assert(score_pegging_action(state, 'S2') == 0)
    with pytest.raises(Exception):
        score_pegging_action(state, None)

def test_take_pegging_action():
    state = make_game()

    # pass actions
    take_pegging_action(state, None)
    assert(state.current_player == 1)
    assert(state.last_to_play == 1)
    take_pegging_action(state, None)
    assert(state.current_player == 0)
    assert(state.last_to_play == 1)

    # invalid action
    # card not in hand
    state = make_game()
    with pytest.raises(Exception):
        take_pegging_action(state, 'C5')

    # NOTE: can enter invalid game state if unallowed card is played

    # valid action
    state = make_game()
    take_pegging_action(state, 'S7')
    assert(state.scores[0] == 8)
    assert(state.current_player == 1)
    assert(state.last_to_play == 0)
    assert(len(state.hands[0])==2)
