"""
This module interfaces to our user data.
"""

# fields
KEY = 'key'
TITLE = 'title'
TEXT = 'text'
EMAIL = 'email'

TEST_KEY = 'HomePage'
SUBM_KEY = 'SubmissionsPage'
DEL_KEY = 'DeletePage'

text_dict = {
    TEST_KEY: {
        TITLE: 'Home Page',
        TEXT: 'This is a journal about building API servers.',
    },
    SUBM_KEY: {
        TITLE: 'Submissions Page',
        TEXT: 'All submissions must be original work in Word format.',
    },
    DEL_KEY: {
        TITLE: 'Delete Page',
        TEXT: 'This is a text to delete.',
    },
}


def create(key: str, title: str, text: str):
    """
    Adds a new page entry to the text_dict if the key does not already exist.
    Arguments:
        - key: The key for the new page
        - title: The title of the page
        - text: The body text for the page
    Returns a success message or already exists message
    """
    if key in text_dict:
        return f"'{key}' already exists."
    text_dict[key] = {TITLE: title, TEXT: text}
    return f"'{title}' created successfully."


def delete(key: str):
    """
    Removes a page entry from the text_dict if the key exists.
    Arguments:
        - key: The key of the page to delete
    Returns a success message or a does not exist message
    """
    if key not in text_dict:
        return f"'{key}' does not exist."
    del text_dict[key]
    return f"'{key}' deleted successfully."


def update(key: str, title: str, text: str):
    """
    Updates a page entry to the text_dict if the key already exist.
    Arguments:
        - key: The key for the page
        - title: The new title of the page
        - text: The new body text for the page
    Returns a success message or does not exists message
    """
    if key not in text_dict:
        return f"'{key}' does not exists."
    text_dict[key] = {TITLE: title, TEXT: text}
    return f"'{title}' updated successfully."


def read():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user email.
        - Each user email must be the key for another dictionary.
    """
    text = text_dict
    return text


def read_one(key: str) -> dict:
    # This should take a key and return the page dictionary
    # for that key. Return an empty dictionary of key not found.
    result = {}
    if key in text_dict:
        result = text_dict[key]
    return result


def main():
    print(read())


if __name__ == '__main__':
    main()
