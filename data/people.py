"""
This module interfaces to our user data.
"""
import re

import data.roles as rls

MIN_USER_NAME_LEN = 2
# fields
NAME = 'name'
ROLES = 'roles'
AFFILIATION = 'affiliation'
EMAIL = 'email'

TEST_EMAIL = 'netID@nyu.edu'
DEL_EMAIL = 'delete@nyu.edu'

people_dict = {
    TEST_EMAIL: {
        NAME: 'Person Created',
        ROLES: [],
        AFFILIATION: 'NYU',
        EMAIL: TEST_EMAIL,
    },
    DEL_EMAIL: {
        NAME: 'Person Deleted',
        ROLES: [],
        AFFILIATION: 'NYU',
        EMAIL: DEL_EMAIL,
    },
}


CHAR_OR_DIGIT = '[A-Za-z0-9]'


def is_valid_email(email: str) -> bool:
    return re.match(f"{CHAR_OR_DIGIT}.*@{CHAR_OR_DIGIT}.*", email)


def read():
    """
        PARAM: none
        RET: a dictionary of users emails as keys

        Note: each user email must be the key for another dictionary
    """
    people = people_dict
    return people


def delete(_id):
    """
        PARAM: _id (string)
        RET: returns _id (string) if successful, otherwise it returns None

        This function deletes a user from people_dict based on their email.
    """
    people = read()
    if _id in people:
        del people[_id]
        return _id
    else:
        return None


def is_valid_person(name: str, affiliation: str, email: str,
                    role: str) -> bool:
    if email in people_dict:
        raise ValueError(f'Adding duplicate {email=}')
    if not is_valid_email(email):
        raise ValueError(f'Invalid email: {email}')
    if not rls.is_valid(role):
        raise ValueError(f'Invalid role: {role}')
    return True


def create(name: str, affiliation: str, email: str, role: str):
    """
        PARAM: name (string), affiliation (string), email (string),
            - information about the person to be added

        RET: a boolean indicating whether the creation was successful

        This function adds a user to people_dict.
    """
    if email in people_dict:
        raise ValueError(f"Adding duplicate email {email}")
    if is_valid_person(name, affiliation, email, role):
        people_dict[email] = {NAME: name, AFFILIATION: affiliation,
                              EMAIL: email, ROLES: role}
    return email


def update_person(name: str, affiliation: str, email: str, role: str):
    """
        PARAM: name (string), affiliation (string), email (string),
            - information about the person to be updated

        RET: a boolean indicating whether the update was successful

        This function update a user's info to people_dict.
    """
    if email not in people_dict:
        raise ValueError(f"User with email {email} does not exist")
    else:
        people_dict[email] = {NAME: name, AFFILIATION: affiliation,
                              EMAIL: email, ROLES: role}
        return True


def main():
    print(read())


if __name__ == '__main__':
    main()
