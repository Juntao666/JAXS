import random

import pytest
from unittest.mock import patch

import data.manuscripts as mqry


def gen_random_not_valid_str() -> str:
    """
    That huge number is only important in being huge:
        any big number would do.
    """
    BIG_NUM = 10_000_000_000
    big_int = random.randint(0, BIG_NUM)
    big_int += BIG_NUM
    bad_str = str(big_int)


def test_is_valid_state():
    for state in mqry.get_states():
        assert mqry.is_valid_state(state)


def test_is_not_valid_state():
    # run this test "a few" times
    for i in range(10):
        assert not mqry.is_valid_state(gen_random_not_valid_str())


def test_is_valid_action():
    for action in mqry.get_actions():
        assert mqry.is_valid_action(action)


def test_is_not_valid_action():
    # run this test "a few" times
    for i in range(10):
        assert not mqry.is_valid_action(gen_random_not_valid_str())


def test_handle_action_bad_state():
    with pytest.raises(ValueError):
        mqry.handle_action(mqry.TEST_ID,
                           gen_random_not_valid_str(),
                           mqry.TEST_ACTION,
                           manu=mqry.SAMPLE_MANU)


def test_handle_action_bad_action():
    with pytest.raises(ValueError):
        mqry.handle_action(mqry.TEST_ID,
                           mqry.TEST_STATE,
                           gen_random_not_valid_str(),
                           manu=mqry.SAMPLE_MANU)


def test_handle_action_valid_return():
    for state in mqry.get_states():
        for action in mqry.get_valid_actions_by_state(state):
            print(f'{action=}')
            if action == mqry.EDITOR_MOVE:
                new_state = mqry.handle_action(
                    mqry.TEST_ID,
                    state,
                    action,
                    manu=mqry.SAMPLE_MANU,
                    referee='Some ref',
                    target_state=mqry.SUBMITTED
                )
            else:
                new_state = mqry.handle_action(mqry.TEST_ID,
                                               state,
                                               action,
                                               manu=mqry.SAMPLE_MANU,
                                               referee='Some ref')
            print(f'{new_state=}')
            assert mqry.is_valid_state(new_state)


TEMP_KEY = "tempManuscript1"
NEW_KEY = "newManuscript1"
NEW_TITLE = "New Manuscript Title"
NEW_AUTHOR = "New Author"
NEW_AUTHOR_EMAIL = "author@example.com"
NEW_STATE = "Draft"
NEW_TEXT = "This is the manuscript text."
NEW_ABSTRACT = "This is the abstract."
NEW_EDITOR = ["Editor1"]
NEW_REFEREE = ["referee1"]
NEW_HISTORY = ["Created"]
NONE_EXISTENT_KEY = "NonExistentKey"


@pytest.fixture(scope='function')
def temp_manuscript():
    key = mqry.create(
        TEMP_KEY,
        "Temp Manuscript Title",
        "Temp Author",
        "temp_author@example.com",
        "SUB",
        "Temporary manuscript text.",
        "Temporary abstract.",
        ["Temp Editor"],
        ["Temp referee"],
        ["SUB"]
    )
    yield key
    try:
        mqry.delete(key)
    except Exception:
        print("Manuscript already deleted.")


def test_exists(temp_manuscript):
    assert mqry.exists(temp_manuscript)


def test_doesnt_exist():
    assert not mqry.exists(NONE_EXISTENT_KEY)


def test_read_one(temp_manuscript):
    assert mqry.read_one(temp_manuscript) is not None


@patch('data.manuscripts.read_one', autospec=True, return_value={})
def test_read_one_not_found(mock_read):
    assert mqry.read_one('Not a manuscript key!') == {}


def test_delete_manuscript(temp_manuscript):
    mqry.delete(temp_manuscript)
    assert not mqry.exists(temp_manuscript)


def test_create():
    mqry.create(
        NEW_KEY,
        "Test Title",
        "Test Author",
        "test_author@example.com",
        "SUB",
        "Test manuscript text.",
        "Test abstract.",
        ["Test Editor"],
        ["Temp referee"],
        ["SUB"]
    )
    assert mqry.exists(NEW_KEY)
    mqry.delete(NEW_KEY)


def test_update_action(temp_manuscript):
    mqry.update_action(TEMP_KEY, action='REJ')
    updated_manu = mqry.read_one(TEMP_KEY)
    assert updated_manu[mqry.STATE] == 'REJ'
