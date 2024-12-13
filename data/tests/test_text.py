import pytest
from unittest.mock import patch
from unittest import skip

import data.text as txt

TEMP_KEY = "Temptext"
NEW_KEY = "NEWTEXT"
NEW_TEXT = "NEW TEXT"
NEW_TITLE = "NEW TITLE"
NONE_EXISTENT_KEY = "NOT EXIST"


@pytest.fixture(scope='function')
def temp_text():
    key = txt.create(TEMP_KEY, 'Temp Text Title', "Temp Text Texts")
    yield key
    try:
        txt.delete(key)
    except Error:
        print('text already deleted.')


def test_exists(temp_text):
    assert txt.exists(temp_text)


def test_doesnt_exist():
    assert not txt.exists(NONE_EXISTENT_KEY)


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


def test_update(temp_text):
    txt.update(temp_text, NEW_TITLE, NEW_TEXT)
    updated_rec = txt.read_one(temp_text)
    assert updated_rec[txt.TITLE] == NEW_TITLE
    assert updated_rec[txt.TEXT] == NEW_TEXT


def test_update_none_existent():
    text = txt.read()
    assert NONE_EXISTENT_KEY not in text

    with pytest.raises(ValueError):
        txt.update(NONE_EXISTENT_KEY, "N/A", "N/A")


def test_delete_text(temp_text):
    txt.delete(temp_text)
    assert not txt.exists(temp_text)


def test_create():
    txt.create(NEW_KEY, "Title", "content")
    assert txt.exists(NEW_KEY)
    txt.delete(NEW_KEY)


def test_create_duplicate(temp_text):
    with pytest.raises(ValueError):
        txt.create(TEMP_KEY, "rand", "rand")

