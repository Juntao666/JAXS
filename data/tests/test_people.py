import pytest

import data.people as ppl


def test_read():
    people = ppl.read()
    assert isinstance(people, dict)
    assert len(people) > 0
    # check for string IDs:
    for _id, person in people.items():
        assert isinstance(_id, str)
        assert ppl.NAME in person


def test_del_person():
    people = ppl.read()
    old_len = len(people)
    ppl.delete(ppl.DEL_EMAIL)
    people = ppl.read()
    assert len(people) < old_len
    assert ppl.DEL_EMAIL not in people


NEW_EMAIL = "joe@nyu.edu"

def test_create():
    people = ppl.read()
    assert NEW_EMAIL not in people
    ppl.create("Joe Smith", "NYU", NEW_EMAIL)
    people = ppl.read()
    assert NEW_EMAIL in people


def test_duplicate_person():
    with pytest.raises(ValueError):
        ppl.create("Do Not Care", "Do Not Care", ppl.TEST_EMAIL)
    people = ppl.read()
    assert NEW_EMAIL in people


TEST_EMAIL = 'netID@nyu.edu'
NAME = 'name'
ROLES = 'roles'
AFFILIATION = 'affiliation'
EMAIL = 'email'
TEST_EMAIL_DATA = {
        NAME: 'Person Created',
        ROLES: [],
        AFFILIATION: 'NYU',
        EMAIL: TEST_EMAIL,
    }

def test_update_person():
    people = ppl.read()
    assert people[TEST_EMAIL] == TEST_EMAIL_DATA
    response = ppl.update_person("new", "new", TEST_EMAIL)
    people = ppl.read()
    assert response
    assert people[TEST_EMAIL] != TEST_EMAIL_DATA


NONEXISTENT_EMAIL = "not-real@email.com"
def test_update_nonexistent_person():
    with pytest.raises(ValueError):
        ppl.update_person("Do Not Care", "Do Not Care", NONEXISTENT_EMAIL)
    people = ppl.read()
    assert NONEXISTENT_EMAIL not in people

