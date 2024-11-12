import pytest
from unittest.mock import patch

import data.text as txt


@pytest.fixture(scope='function')
def temp_text():
    _key = txt.create('TempText', 'Temp Text Title', "Temp Text Texts")
    yield _key
    txt.delete(_key)


@patch('data.text.read', autospec=True,
       return_value={"RandPage": {"title": "RandTitle"}})
def test_read(mock_read):
    texts = txt.read()
    assert isinstance(texts, dict)
    for key in texts:
        assert isinstance(key, str)


def test_read_one(temp_text):
    assert txt.read_one(temp_text) is not None


@patch('data.text.read_one', autospec=True,
       return_value={})
def test_read_one_not_found(mock_read):
    assert txt.read_one('Not a page key!') == {}


TITLE = 'title'
TEXT = 'text'
TEST_KEY_DATA = {
    TITLE: 'Home Page',
    TEXT: 'This is a journal about building API servers.',
}
NEW_TEXT = "NEW TEXT"
NEW_TITLE = "NEW TITLE"


def test_update():
    assert txt.read_one(txt.TEST_KEY) == TEST_KEY_DATA
    response = txt.update(txt.TEST_KEY, NEW_TITLE, NEW_TEXT)
    assert response
    assert txt.read_one(txt.TEST_KEY) != TEST_KEY_DATA


NONE_EXISTENT_KEY = "NOT EXIST"


def test_update_none_existent():
    response = txt.update(NONE_EXISTENT_KEY, "N/A", "N/A")
    assert response
    assert txt.read_one(NONE_EXISTENT_KEY) == {}


def test_delete_text():
    text = txt.read()
    old_len = len(text)
    txt.delete(txt.DEL_KEY)
    text = txt.read()
    assert len(text) < old_len
    assert txt.DEL_KEY not in text


NEW_KEY = "NEW TEXT"


def test_create():
    text = txt.read()
    assert NEW_KEY not in text
    txt.create(NEW_KEY, "Title", "content")
    text = txt.read()
    assert NEW_KEY in text
