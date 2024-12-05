from http.client import (
    BAD_REQUEST,
    FORBIDDEN,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE,
)

from http import HTTPStatus

from unittest.mock import patch
from unittest import skip

import pytest

from data.people import NAME

import server.endpoints as ep

TEST_CLIENT = ep.app.test_client()


@skip("hello world")
def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    resp_json = resp.get_json()
    assert ep.HELLO_RESP in resp_json


def test_title():
    resp = TEST_CLIENT.get(ep.TITLE_EP)
    print(f'{ep.TITLE_EP=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.TITLE_RESP in resp_json
    assert isinstance(resp_json[ep.TITLE_RESP], str)
    assert len(resp_json[ep.TITLE_RESP]) > 0


@patch('data.people.read', autospec=True,
       return_value={'id': {NAME: 'Joe Schmoe'}})
def test_read(mock_read):
    resp = TEST_CLIENT.get(ep.PEOPLE_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    for _id, person in resp_json.items():
        assert isinstance(_id, str)
        assert len(_id) > 0
        assert NAME in person
        assert person[NAME] == 'Joe Schmoe'


@patch('data.people.read_one', autospec=True,
       return_value={NAME: 'Joe Schmoe'})
def test_read_one(mock_read):
    resp = TEST_CLIENT.get(f'{ep.PEOPLE_EP}/mock_id')
    assert resp.status_code == OK


@patch('data.people.read_one', autospec=True, return_value=None)
def test_read_one_not_found(mock_read):
    resp = TEST_CLIENT.get(f'{ep.PEOPLE_EP}/mock_id')
    assert resp.status_code == NOT_FOUND


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



@pytest.fixture(scope="function")
@skip("Work in progress")
def add_person():
    data = {
        "name": "Test",
        "email": "test@nyu.edu",
        "affiliation": "Rand",
        "roles": "ED"
    }
    resp = TEST_CLIENT.put(f'{ep.PEOPLE_EP}/create', json=data)
    assert resp.status_code == HTTPStatus.OK
    
    yield NEW_EMAIL
    
    delete_resp = TEST_CLIENT.delete(f"{ep.PEOPLE_EP}/{NEW_EMAIL}")
    assert delete_resp.status_code == 200

    
def test_add_person(add_person):
    NEW_EMAIL = add_person

    people = TEST_CLIENT.get(ep.PEOPLE_EP)
    resp_json = people.get_json()
    assert NEW_EMAIL in resp_json


@skip("Work in progress")
def test_update_person():
    data = {
        "name": "original",
        "email": "update@nyu.edu",
        "affiliation": "Rand",
        "roles": "ED"
    }

    resp = TEST_CLIENT.put(f"{ep.PEOPLE_EP}/create", json=data)
    assert resp.status_code == HTTPStatus.OK

    updated_data = {
        "name": "updated",
        "email": "update@nyu.edu",
        "affiliation": "updated",
        "roles": "ED"
    }

    resp = TEST_CLIENT.post(f"{ep.PEOPLE_EP}/update", json=updated_data)
    assert resp.status_code == HTTPStatus.OK


    people = TEST_CLIENT.get(ep.PEOPLE_EP)
    resp_json = people.get_json()
    assert TEST_EMAIL in resp_json
    assert resp_json[TEST_EMAIL]["name"] == "updated"
    assert resp_json[TEST_EMAIL]["affiliation"] == "updated"


@skip("Delete functionality test not done")
def test_delete_person():
    email = ""
    resp = TEST_CLIENT.delete(f'{ep.PEOPLE_EP}/{email}')
    assert resp.status_code == 200

    # Check if the person is actually deleted
    resp = TEST_CLIENT.get(ep.PEOPLE_EP)
    resp_json = resp.get_json()
    assert email not in resp_json
