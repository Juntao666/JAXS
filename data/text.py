"""
This module interfaces to our user data.
"""

import data.db_connect as dbc

TEXTS_COLLECT = 'texts'
# fields
KEY = 'key'
TITLE = 'title'
TEXT = 'text'


def create(key: str, title: str, text: str) -> str:
    """
    Adds a new page entry to the text_dict if the key does not already exist.
    Arguments:
        - key: The key for the new page
        - title: The title of the page
        - text: The body text for the page
    Returns a success message or already exists message
    """
    if exists(key):
        raise ValueError(f"Adding duplicate text {key}")
    dbc.create(TEXTS_COLLECT, {KEY: key, TITLE: title, TEXT: text})
    return key


def delete(key: str) -> str:
    """
    Removes a page entry from the text_dict if the key exists.
    Arguments:
        - key: The key of the page to delete
    Returns a success message or a does not exist message
    """
    if not exists(key):
        return f"'{key}' does not exist."
    dbc.delete(TEXTS_COLLECT, {KEY: key})
    return f"'{key}' deleted successfully."


def update(key: str, title: str, text: str) -> str:
    """
    Updates a page entry to the text_dict if the key already exist.
    Arguments:
        - key: The key for the page
        - title: The new title of the page
        - text: The new body text for the page
    Returns a success message or does not exists message
    """
    if not exists(key):
        return f"'{key}' does not exists."
    dbc.update(TEXTS_COLLECT, {KEY: key}, {KEY: key, TITLE: title, TEXT: text})
    return f"'{title}' updated successfully."


def read() -> dict:
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user email.
        - Each user email must be the key for another dictionary.
    """
    text = dbc.read_dict(TEXTS_COLLECT, KEY)
    return text


def read_one(key: str) -> dict:
    """
    Retrieves the page dictionary for a key.
    Arguments:
        - key: The key for the page
    Returns the page dictionary or None if key not found.
    """
    result = dbc.read_one(TEXTS_COLLECT, {KEY: key})
    return result


def exists(key: str) -> bool:
    return read_one(key) is not None


def main():
    print(read())


if __name__ == '__main__':
    main()
