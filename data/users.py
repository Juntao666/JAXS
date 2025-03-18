"""
This module interfaces to our user data.
"""

import data.db_connect as dbc
import hashlib
import secrets

LEVEL = 'level'
MIN_USER_NAME_LEN = 2
USERNAME = 'username'
PASSWORD = 'password'
USER_COLLECT = 'user'

client = dbc.connect_db()
print(f'{client=}')


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(stored_password: str, provided_password: str) -> bool:
    return secrets.compare_digest(stored_password, hash_password(provided_password))


def get_users() -> dict:
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on username (a str).
        - Each username must be the key for a dictionary.
        - That dictionary must at least include a LEVEL member that has an int
        value.
    """
    users = {
        "Callahan": {
            LEVEL: 0,
            PASSWORD: hash_password("123abc"),
        },
        "Reddy": {
            LEVEL: 1,
            PASSWORD: hash_password("123ABC"),
        },
    }
    return users


# users = get_users()
# for username, user in users.items():
#     password = user.get(PASSWORD)
#     level = user.get(LEVEL, 0)
#     usr = {USERNAME: username, PASSWORD: password, LEVEL: level}
#     dbc.create(USER_COLLECT, usr)


def read_one(username: str) -> dict:
    """
    Return a user record if username present in DB,
    else None.
    """
    user = dbc.read_one(USER_COLLECT, {USERNAME: username})
    return user


def read() -> dict:
    users = dbc.read_dict(USER_COLLECT, USERNAME)
    return users


def pass_is_valid(username: str, password: str) -> bool:
    user = read_one(username)
    if user and user.get(PASSWORD) == password:  # keep until cleanup db
        return True
    elif user and verify_password(user.get(PASSWORD, ''), password):
        return True
    return False


def create(username: str, password: str, level: int = 0) -> str:
    if read_one(username):
        raise ValueError(f"Username '{username}' already exists.")

    user = {USERNAME: username, PASSWORD: hash_password(password), LEVEL: level}

    dbc.create(USER_COLLECT, user)

    return username


def delete_user(username: str) -> bool:
    user = read_one(username)
    if user:
        dbc.delete(USER_COLLECT, {USERNAME: username})
        return True
    else:
        # User not found
        return False
