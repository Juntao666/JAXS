import data.manuscripts.states as msts


def test_get_next_state():
    assert isinstance(msts.get_next_state(msts.TEST_CURR_STATE), list)


def test_is_valid_state_change():
    assert isinstance(msts.is_valid_state_change(msts.TEST_CURR_STATE, msts.TEST_NEXT_STATE), bool)