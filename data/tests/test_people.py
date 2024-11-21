import pytest
from unittest.mock import patch

import data.people as ppl
import data.roles as rls

from data.roles import TEST_CODE as TEST_ROLE_CODE

NAME = 'name'
ROLES = 'roles'
AFFILIATION = 'affiliation'
EMAIL = 'email'

NO_AT="userexample.com"
NO_NAME="@example.com"
NO_DOMAIN="user@"
NO_SUB_DOMAIN = 'kajshd@com'
DOMAIN_TOO_SHORT = 'kajshd@nyu.e'
DOMAIN_TOO_LONG = 'kajshd@nyu.eedduu'

NONEXISTENT_EMAIL = "not-real@email.com"
TEMP_EMAIL = 'temp_person@temp.org'
NEW_EMAIL = "joe@nyu.edu"
TEST_EMAIL = 'netID@nyu.edu'
DEL_EMAIL = 'delete@nyu.edu'

VALID_ROLES = ['ED', 'AU']


@pytest.fixture(scope='function')
def temp_person():
    _id = ppl.create('Joe Smith', 'NYU', TEMP_EMAIL, TEST_ROLE_CODE)
    yield _id
    ppl.delete(_id)


def test_get_mh_fields():
    flds = ppl.get_mh_fields()
    assert isinstance(flds, list)
    assert len(flds) > 0


def test_create_mh_rec(temp_person):
    person_rec = ppl.read_one(temp_person)
    mh_rec = ppl.create_mh_rec(person_rec)
    assert isinstance(mh_rec, dict)
    for field in ppl.MH_FIELDS:
        assert field in mh_rec


def test_has_role(temp_person):
    person_rec = ppl.read_one(temp_person)
    assert ppl.has_role(person_rec, TEST_ROLE_CODE)


def test_doesnt_have_role(temp_person):
    person_rec = ppl.read_one(temp_person)
    assert not ppl.has_role(person_rec, 'Not a good role!')


def test_is_valid_email_no_at():
    assert not ppl.is_valid_email(NO_AT)


def test_is_valid_email_no_name():
    assert not ppl.is_valid_email(NO_NAME)


def test_is_valid_email_no_domain():
    assert not ppl.is_valid_email(NO_DOMAIN)


def test_is_valid_no_sub_domain():
    assert not ppl.is_valid_email(NO_SUB_DOMAIN)


def test_is_valid_email_domain_too_short():
    assert not ppl.is_valid_email(DOMAIN_TOO_SHORT)


def test_is_valid_email_domain_too_long():
    assert not ppl.is_valid_email(DOMAIN_TOO_LONG)


def test_is_valid_email():
    assert ppl.is_valid_email('sl9052@nyu.edu')


def test_create_bad_email():
    with pytest.raises(ValueError):
        ppl.create('Do not care about name',
                   'Or affiliation', 'bademail', TEST_ROLE_CODE)


@patch('data.people.read', autospec=True,
       return_value={'id': {NAME: 'Joe Schmoe'}})
def test_read(mock_read):
    people = ppl.read()
    assert isinstance(people, dict)
    assert len(people) > 0
    # check for string IDs:
    for _id, person in people.items():
        assert isinstance(_id, str)
        assert ppl.NAME in person


def test_read_one(temp_person):
    assert ppl.read_one(temp_person) is not None


@patch('data.people.read_one', autospec=True,
       return_value=None)
def test_read_one_not_there(mock_read):
    assert ppl.read_one('Not an existing email!') is None


def test_delete():
    _id = ppl.create('someone', 'NYU', DEL_EMAIL, TEST_ROLE_CODE)
    people = ppl.read()
    old_len = len(people)

    ppl.delete(_id)
    
    people = ppl.read()
    assert len(people) < old_len
    assert DEL_EMAIL not in people


def test_create(temp_person):
    people = ppl.read()
    assert TEMP_EMAIL in people


def test_create_duplicate(temp_person):
    with pytest.raises(ValueError):
        ppl.create('Joe Smith', 'NYU', TEMP_EMAIL, TEST_ROLE_CODE)


@pytest.fixture(scope='function')
def revert_update():
    person_rec = ppl.read_one(TEST_EMAIL)

    yield person_rec

    response = ppl.update_person(
        person_rec[NAME], 
        person_rec[AFFILIATION], 
        TEST_EMAIL, 
        person_rec[ROLES]
    )

    
def test_update_person(revert_update):
    response = ppl.update_person("new", "new", TEST_EMAIL, VALID_ROLES)
    assert response
    
    people = ppl.read_one(TEST_EMAIL)
    assert people != revert_update


def test_update_nonexistent_person():
    with pytest.raises(ValueError):
        ppl.update_person("Do Not Care", "Do Not Care", NONEXISTENT_EMAIL, ["ED"])
    people = ppl.read()
    assert NONEXISTENT_EMAIL not in people


def test_get_masthead():
    mh = ppl.get_masthead()
    assert isinstance(mh, dict)


@pytest.mark.skip('Skipping cause not done.')
def test_update(temp_person):
    ppl.update('Buffalo Bill', 'UBuffalo', temp_person, VALID_ROLES)


def test_create_person_bad_email():
    with pytest.raises(ValueError, match="Invalid email address"):
        ppl.create_person('Do not care about name', 'Or affiliation', 'bademail', 'TEST_ROLE_CODE')
