# from http.client import (
#     BAD_REQUEST,
#     FORBIDDEN,
#     NOT_ACCEPTABLE,
#     NOT_FOUND,
#     OK,
#     SERVICE_UNAVAILABLE,
# )
#
# from unittest.mock import patch
#
# import pytest

from data.people import NAME

import server.endpoints as ep

TEST_CLIENT = ep.app.test_client()


def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    resp_json = resp.get_json()
    assert ep.HELLO_RESP in resp_json


def test_project_name():
    resp = TEST_CLIENT.get(ep.PROJECT_NAME_EP)
    resp_json = resp.get_json()
    assert ep.PROJECT_NAME_RESP in resp_json
    assert isinstance(resp_json[ep.PROJECT_NAME_RESP], str)
    assert len(resp_json[ep.PROJECT_NAME_RESP]) > 0


def test_get_people():
    resp = TEST_CLIENT.get(ep.PEOPLE_EP)
    resp_json = resp.get_json()
    for _id, person in resp_json.items():
        assert isinstance(_id, str)
        assert len(_id) > 0
        assert NAME in person


def test_add_person():
    NEW_EMAIL = "test@nyu.edu"
    resp = TEST_CLIENT.post(f"{ep.PEOPLE_EP}/{NEW_EMAIL}/Random/Random/RE")
    assert resp.status_code == 200

    people = TEST_CLIENT.get(ep.PEOPLE_EP)
    resp_json = people.get_json()
    assert NEW_EMAIL in resp_json


def test_update_person():
    TEST_EMAIL = 'netID@nyu.edu'
    resp = TEST_CLIENT.put(f"{ep.PEOPLE_EP}/{TEST_EMAIL}/new/new/ED")
    assert resp.status_code == 200

    people = TEST_CLIENT.get(ep.PEOPLE_EP)
    resp_json = people.get_json()
    assert TEST_EMAIL in resp_json
    assert resp_json[TEST_EMAIL]["name"] == "new"
    assert resp_json[TEST_EMAIL]["affiliation"] == "new"


# def test_delete_person():
#     email = ""
#     resp = TEST_CLIENT.delete(f'{ep.PEOPLE_EP}/{email}')
#     assert resp.status_code == 200

#     # Check if the person is actually deleted
#     resp = TEST_CLIENT.get(ep.PEOPLE_EP)
#     resp_json = resp.get_json()
#     assert email not in resp_json
