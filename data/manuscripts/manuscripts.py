"""
This module interfaces with manuscript data.
"""

import data.db_connect as dbc

MANUSCRIPTS_COLLECT = 'manuscripts'

# Fields
KEY = 'key'
TITLE = 'title'
AUTHOR = 'author'
AUTHOR_EMAIL = 'author_email'
STATE = 'state'
TEXT = 'text'
ABSTRACT = 'abstract'
EDITOR = 'editor'
REFEREE = 'referee'
HISTORY = 'history'


def create(key: str, title: str, author: str, author_email: str, state: str, text: str, abstract: str, editor: str, referee: dict, history: list) -> str:
    """
    Adds a new manuscript entry if the key does not already exist.
    Arguments:
        - key: The unique key for the manuscript
        - title: The title of the manuscript
        - author: The author of the manuscript
        - author_email: The email address of the author
        - state: The current state of the manuscript
        - text: The body text of the manuscript
        - abstract: The abstract of the manuscript
        - editor: The assigned editor for the manuscript
        - referee: A dictionary containing referee reports and verdicts
        - history: A list of historical states for the manuscript
    Returns a success message or raises an error if the key already exists.
    """
    if exists(key):
        raise ValueError(f"Adding duplicate manuscript {key}")
    dbc.create(MANUSCRIPTS_COLLECT, {
        KEY: key,
        TITLE: title,
        AUTHOR: author,
        AUTHOR_EMAIL: author_email,
        STATE: state,
        TEXT: text,
        ABSTRACT: abstract,
        EDITOR: editor,
        REFEREE: referee,
        HISTORY: history,
    })
    return key


def delete(key: str) -> str:
    """
    Removes a manuscript entry if the key exists.
    Arguments:
        - key: The key of the manuscript to delete
    Returns a success message or a does not exist message.
    """
    if not exists(key):
        return f"'{key}' does not exist."
    dbc.delete(MANUSCRIPTS_COLLECT, {KEY: key})
    return f"'{key}' deleted successfully."


def update(key: str, title: str, author: str, author_email: str, state: str, text: str, abstract: str, editor: str, referee: dict, history: list) -> str:
    """
    Updates a manuscript entry if the key exists.
    Arguments:
        - key: The unique key for the manuscript
        - title: The new title of the manuscript
        - author: The new author of the manuscript
        - author_email: The new email address of the author
        - state: The new state of the manuscript
        - text: The new body text of the manuscript
        - abstract: The new abstract of the manuscript
        - editor: The new assigned editor
        - referee: The updated referee dictionary
        - history: The updated list of historical states
    Returns a success message or raises an error if the key does not exist.
    """
    if not exists(key):
        raise ValueError(f"Manuscript {key} does not exist")
    dbc.update(MANUSCRIPTS_COLLECT, {KEY: key}, {
        KEY: key,
        TITLE: title,
        AUTHOR: author,
        AUTHOR_EMAIL: author_email,
        STATE: state,
        TEXT: text,
        ABSTRACT: abstract,
        EDITOR: editor,
        REFEREE: referee,
        HISTORY: history,
    })
    return f"Manuscript '{title}' updated successfully."


def read() -> dict:
    """
    Retrieves all manuscripts as a dictionary keyed on manuscript keys.
    Returns a dictionary of manuscripts.
    """
    manuscripts = dbc.read_dict(MANUSCRIPTS_COLLECT, KEY)
    return manuscripts


def read_one(key: str) -> dict:
    """
    Retrieves the manuscript dictionary for a specific key.
    Arguments:
        - key: The key for the manuscript
    Returns the manuscript dictionary or None if key not found.
    """
    result = dbc.read_one(MANUSCRIPTS_COLLECT, {KEY: key})
    return result


def exists(key: str) -> bool:
    """
    Checks if a manuscript with the given key exists.
    Arguments:
        - key: The key for the manuscript
    Returns True if the manuscript exists, False otherwise.
    """
    return read_one(key) is not None


def main():
    print(read())


if __name__ == '__main__':
    main()
