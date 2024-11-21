"""
This module interfaces to our user data.
"""
import re

import data.db_connect as dbc
import data.roles as rls

PEOPLE_COLLECT = 'people'

MIN_USER_NAME_LEN = 2
# fields
NAME = 'name'
ROLES = 'roles'
AFFILIATION = 'affiliation'
EMAIL = 'email'


client = dbc.connect_db()
print(f'{client=}')


LOCAL_PART = r'[a-zA-Z0-9._%+-]+'
DOMAIN_PART = r'(?=.{1,})(?!.*\.{2})[a-zA-Z0-9.-]+'
TOP_LEVEL_DOMAIN = r'[a-zA-Z]{2,3}'

EMAIL_PATTERN = fr'^{LOCAL_PART}@{DOMAIN_PART}\.{TOP_LEVEL_DOMAIN}$'


def is_valid_email(email: str) -> bool:
    """
    Checks if email is valid
    Arguments:
        - email: email as a string
    Returns a boolean of whether the email is valid
    """
    return re.match(EMAIL_PATTERN, email)


def read() -> dict:
    """
        PARAM: none
        RET: a dictionary of users emails as keys

        Note: each user email must be the key for another dictionary
    """
    people = dbc.read_dict(PEOPLE_COLLECT, EMAIL)
    print(f'{people=}')
    return people


def read_one(email: str) -> dict:
    """
    Return a person record if email present in DB,
    else None.
    """
    person = dbc.fetch_one(PEOPLE_COLLECT, {EMAIL: email})
    return person


def delete(email):
    """
        PARAM: _id (string)
        RET: returns _id (string) if successful, otherwise it returns None

        This function deletes a user from people_dict based on their email.
    """
    print(f'{EMAIL=}, {email=}')
    return dbc.delete(PEOPLE_COLLECT, {EMAIL: email})


def is_valid_person(name: str, affiliation: str, email: str,
                    role: str = None, roles: list = None) -> bool:
    """
    Checks if person is valid
    Arguments:
        - name: name of person
        - affiliation: affiliation of person
        - email: email of person
        - role: role of person
        - roles: all the roles of the person
    Returns a boolean of whether the person is valid
    """
    if not is_valid_email(email):
        raise ValueError(f'Invalid email: {email}')
    if role:
        if not rls.is_valid(role):
            raise ValueError(f'Invalid role: {role}')
    elif roles:
        for role in roles:
            if not rls.is_valid(role):
                raise ValueError(f'Invalid role: {role}')
    return True


def create(name: str, affiliation: str, email: str, role: str):
    """
        PARAM: name (string), affiliation (string), email (string),
               role (string)
            - information about the person to be added

        RET: a boolean indicating whether the creation was successful

        This function adds a user to people_dict.
    """
    people = dbc.read_dict(PEOPLE_COLLECT, EMAIL)
    if email in people:
        raise ValueError(f"Adding duplicate email {email}")
    if is_valid_person(name, affiliation, email, role):
        roles = []
        if role:
            roles.append(role)
        person = {NAME: name, AFFILIATION: affiliation,
                  EMAIL: email, ROLES: roles}
        print(person)
        dbc.create(PEOPLE_COLLECT, person)
    return email


def update_person(name: str, affiliation: str, email: str, roles: list):
    """
        PARAM: name (string), affiliation (string), email (string),
               roles (list)
            - information about the person to be updated

        RET: a boolean indicating whether the update was successful

        This function update a user's info to people_dict.
    """
    people = dbc.read_dict(PEOPLE_COLLECT, EMAIL)
    if email not in people:
        raise ValueError(f"User with email {email} does not exist")
    if is_valid_person(name, affiliation, email, roles=roles):
        update_dict = {NAME: name, AFFILIATION: affiliation,
                       EMAIL: email, ROLES: roles}
        dbc.update_doc(PEOPLE_COLLECT, {EMAIL: email}, update_dict)
        return True


def has_role(person: dict, role: str) -> bool:
    """
    Checks if a person has a role
    Arguments:
        - person: the person represented as a dictionary
        - role: the role to check for
    Returns a boolean of whether the person has the role
    """
    if role in person.get(ROLES):
        return True
    return False


MH_FIELDS = [NAME, AFFILIATION]


def get_mh_fields(journal_code=None) -> list:
    """
    gets all masthead fields
    Arguments:
        - journal_code: the journal code
    Returns all masthead fields as a list
    """
    return MH_FIELDS


def create_mh_rec(person: dict) -> dict:
    """
    create a masthead record
    Arguments:
        - person: person represented as a dict
    Returns the masthead record created
    """
    mh_rec = {}
    for field in get_mh_fields():
        mh_rec[field] = person.get(field, '')
    return mh_rec


def get_masthead() -> dict:
    """
    Returns the masthead
    Arguments:
        - None
    Returns the masthead dict
    """
    masthead = {}
    mh_roles = rls.get_masthead_roles()
    for mh_role, text in mh_roles.items():
        people_w_role = []
        people = read()
        for _id, person in people.items():
            if has_role(person, mh_role):
                rec = create_mh_rec(person)
                people_w_role.append(rec)
        masthead[text] = people_w_role
    return masthead


def create_person(name, affiliation, email, role_code):
    if '@' not in email:
        raise ValueError("Invalid email address")
    return {"name": name, "email": email, "role": role_code}


def main():
    print(get_masthead())


if __name__ == '__main__':
    main()
