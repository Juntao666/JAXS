import pytest

import data.people as ppl


def test_get_people():
    people = ppl.get_people()
    assert isinstance(people, dict)
    assert len(people) > 0
    # check for string IDs:
    for _id, person in people.items():
        assert isinstance(_id, str)
        assert ppl.NAME in person


def test_delete_person():
    # Check that the person is initially in the dictionary
    people = ppl.get_people()
    email_to_delete = ppl.DEL_EMAIL
    assert email_to_delete in people

    # Delete the person
    deletion_success = ppl.delete_person(email_to_delete)
    assert deletion_success is True

    # Verify the person is no longer in the dictionary
    people = ppl.get_people()
    assert email_to_delete not in people

    # Also try deleting a non-existing person
    deletion_failure = ppl.delete_person('non_existing@nyu.edu')
    assert deletion_failure is False


NEW_EMAIL = "joe@nyu.edu"


def test_create_person():
    people = ppl.get_people()
    assert NEW_EMAIL not in people
    ppl.create_person("Joe Smith", "NYU", NEW_EMAIL)
    people = ppl.get_people()
    assert NEW_EMAIL in people


def test_duplicate_person():
    with pytest.raises(ValueError):
        ppl.create_person("Do Not Care", "Do Not Care", ppl.TEST_EMAIL)
    people = ppl.get_people()
    assert NEW_EMAIL in people
