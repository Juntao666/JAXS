"""
This module interfaces to our user data.
"""

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


def get_people():
    """
        PARAM: none
        RET: a dictionary of users emails as keys

        Note: each user email must be the key for another dictionary
    """
    people = people_dict
    return people


def delete_person(_id):
    """
        PARAM: _id (string)
        RET: returns _id (string) if successful, otherwise it returns None

        This function deletes a user from people_dict based on their email.
    """
    people = get_people()
    if _id in people:
        del people[_id]
        return _id
    else:
        return None


def create_person(name: str, affiliation: str, email: str):
    """
        PARAM: name (string), affiliation (string), email (string),
            - information about the person to be added

        RET: a boolean indicating whether the creation was successful

        This function adds a user to people_dict.
    """
    if email in people_dict:
        raise ValueError(f"Adding duplicate email {email}")
    people_dict[email] = {NAME: name, AFFILIATION: affiliation, EMAIL: email}
    return True
