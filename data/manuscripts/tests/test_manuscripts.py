import pytest
from unittest.mock import patch

import data.manuscripts.manuscripts as mnscrpt

TEMP_KEY = "TempManuscript"
NEW_KEY = "NewManuscript"
NEW_TITLE = "New Manuscript Title"
NEW_AUTHOR = "New Author"
NEW_AUTHOR_EMAIL = "author@example.com"
NEW_STATE = "Draft"
NEW_TEXT = "This is the manuscript text."
NEW_ABSTRACT = "This is the abstract."
NEW_EDITOR = "Editor Name"
NEW_REFEREE = {"referee1": "accepted"}
NEW_HISTORY = ["Created"]
NONE_EXISTENT_KEY = "NonExistentKey"


@pytest.fixture(scope='function')
def temp_manuscript():
    key = mnscrpt.create(
        TEMP_KEY,
        "Temp Manuscript Title",
        "Temp Author",
        "temp_author@example.com",
        "Submitted",
        "Temporary manuscript text.",
        "Temporary abstract.",
        "Temp Editor",
        {"referee1": "pending"},
        ["Submitted"]
    )
    yield key
    try:
        mnscrpt.delete(key)
    except Exception:
        print("Manuscript already deleted.")


def test_exists(temp_manuscript):
    assert mnscrpt.exists(temp_manuscript)


def test_doesnt_exist():
    assert not mnscrpt.exists(NONE_EXISTENT_KEY)


@patch('data.manuscripts.manuscripts.read', autospec=True, return_value={"RandManuscript": {"title": "RandTitle"}})
def test_read(mock_read):
    manuscripts = mnscrpt.read()
    assert isinstance(manuscripts, dict)
    for key in manuscripts:
        assert isinstance(key, str)


def test_read_one(temp_manuscript):
    assert mnscrpt.read_one(temp_manuscript) is not None


@patch('data.manuscripts.manuscripts.read_one', autospec=True, return_value={})
def test_read_one_not_found(mock_read):
    assert mnscrpt.read_one('Not a manuscript key!') == {}


def test_update(temp_manuscript):
    mnscrpt.update(
        temp_manuscript,
        NEW_TITLE,
        NEW_AUTHOR,
        NEW_AUTHOR_EMAIL,
        NEW_STATE,
        NEW_TEXT,
        NEW_ABSTRACT,
        NEW_EDITOR,
        NEW_REFEREE,
        NEW_HISTORY
    )
    updated_rec = mnscrpt.read_one(temp_manuscript)
    assert updated_rec[mnscrpt.TITLE] == NEW_TITLE
    assert updated_rec[mnscrpt.AUTHOR] == NEW_AUTHOR
    assert updated_rec[mnscrpt.AUTHOR_EMAIL] == NEW_AUTHOR_EMAIL
    assert updated_rec[mnscrpt.STATE] == NEW_STATE
    assert updated_rec[mnscrpt.TEXT] == NEW_TEXT
    assert updated_rec[mnscrpt.ABSTRACT] == NEW_ABSTRACT
    assert updated_rec[mnscrpt.EDITOR] == NEW_EDITOR
    assert updated_rec[mnscrpt.REFEREE] == NEW_REFEREE
    assert updated_rec[mnscrpt.HISTORY] == NEW_HISTORY


def test_update_none_existent():
    manuscripts = mnscrpt.read()
    assert NONE_EXISTENT_KEY not in manuscripts

    with pytest.raises(ValueError):
        mnscrpt.update(
            NONE_EXISTENT_KEY,
            "N/A",
            "N/A",
            "N/A",
            "N/A",
            "N/A",
            "N/A",
            "N/A",
            {},
            []
        )


def test_delete_manuscript(temp_manuscript):
    mnscrpt.delete(temp_manuscript)
    assert not mnscrpt.exists(temp_manuscript)


def test_create():
    mnscrpt.create(
        NEW_KEY,
        "Test Title",
        "Test Author",
        "test_author@example.com",
        "Draft",
        "Test manuscript text.",
        "Test abstract.",
        "Test Editor",
        {"referee1": "pending"},
        ["Created"]
    )
    assert mnscrpt.exists(NEW_KEY)
    mnscrpt.delete(NEW_KEY)


def test_create_duplicate(temp_manuscript):
    with pytest.raises(ValueError):
        mnscrpt.create(
            TEMP_KEY,
            "Duplicate Title",
            "Duplicate Author",
            "duplicate_author@example.com",
            "Draft",
            "Duplicate text.",
            "Duplicate abstract.",
            "Duplicate Editor",
            {"referee1": "rejected"},
            ["Submitted"]
        )
