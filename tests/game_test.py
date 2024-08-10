import pytest
from auto_cribbage.game_state import GameState, get_pegging_actions

def test_game_creation():
    state = GameState(2)
    assert state.num_players == 2
    state = GameState(3)
    assert state.num_players == 3
    state = GameState(4)
    assert state.num_players == 4

    with pytest.raises(ValueError):
        state = GameState(1)
    with pytest.raises(ValueError):
        state = GameState(5)


def test_game_reset():
    state = GameState(2)
    state.hands = []
    state.scores = [100,100]
    state.reset()
    assert len(state.hands) > 0
    assert state.scores[0] == 0


def test_get_pegging_actions():
    state = GameState(2)
    actions = get_pegging_actions(state)
    assert(actions == state.hands[state.current_player])
