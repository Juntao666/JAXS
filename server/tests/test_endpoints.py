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
import data.manuscripts as manu
import data.users as usr

TEST_CLIENT = ep.app.test_client()

PEOPLE_LOC = 'data.people.'

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


@patch(PEOPLE_LOC + 'read', autospec=True,
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


@patch(PEOPLE_LOC + 'read_one', autospec=True,
       return_value={NAME: 'Joe Schmoe'})
def test_read_one(mock_read):
    resp = TEST_CLIENT.get(f'{ep.PEOPLE_EP}/mock_id/fake_id')
    assert resp.status_code == OK


@patch(PEOPLE_LOC + 'read_one', autospec=True, return_value=None)
def test_read_one_not_found(mock_read):
    resp = TEST_CLIENT.get(f'{ep.PEOPLE_EP}/mock_id/fake_id')
    assert resp.status_code == NOT_FOUND

    
@patch('data.manuscripts.handle_action', autospec=True,
       return_value='SOME STRING')
def test_handle_action(mock_read):
    resp = TEST_CLIENT.put(f'{ep.MANU_EP}/receive_action',
                           json={
                               manu.MANU_ID: 'some id',
                               manu.CURR_STATE: 'some state',
                               manu.ACTION: 'some action',
                           })
    assert resp.status_code == OK


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
@skip("minor bug")
def add_person():
    NEW_EMAIL = "sdsdad@nyu.edu"
    data = {
        "name": "Test",
        "email": NEW_EMAIL,
        "affiliation": "Rand",
        "roles": "ED"
    }
    resp = TEST_CLIENT.put(f'{ep.PEOPLE_EP}/create', json=data)
    assert resp.status_code == HTTPStatus.OK

    yield NEW_EMAIL

    delete_resp = TEST_CLIENT.delete(f"{ep.PEOPLE_EP}/{NEW_EMAIL}")
    assert delete_resp.status_code == HTTPStatus.OK


@skip("minor bug")
def test_add_person(add_person):
    NEW_EMAIL = add_person

    people = TEST_CLIENT.get(ep.PEOPLE_EP)
    resp_json = people.get_json()
    assert NEW_EMAIL in resp_json


@skip("minor bug")
def test_update_person():
    UPDATE_EMAIL = "sdsdad@nyu.edu"
    data = {
        "name": "original",
        "email": UPDATE_EMAIL,
        "affiliation": "Rand",
        "roles": "ED"
    }

    resp = TEST_CLIENT.put(f"{ep.PEOPLE_EP}/create", json=data)
    assert resp.status_code == HTTPStatus.OK

    updated_data = {
        "name": "updated",
        "email": UPDATE_EMAIL,
        "affiliation": "updated",
        "roles": ["ED"]
    }

    resp = TEST_CLIENT.post(f"{ep.PEOPLE_EP}/update", json=updated_data)
    assert resp.status_code == HTTPStatus.OK


    people = TEST_CLIENT.get(ep.PEOPLE_EP)
    resp_json = people.get_json()
    assert UPDATE_EMAIL in resp_json
    assert resp_json[UPDATE_EMAIL]["name"] == "updated"
    assert resp_json[UPDATE_EMAIL]["affiliation"] == "updated"

    delete_resp = TEST_CLIENT.delete(f"{ep.PEOPLE_EP}/{UPDATE_EMAIL}")
    assert delete_resp.status_code == HTTPStatus.OK


@skip("minor bug")
def test_delete_person():
    DELETE_EMAIL = "sdsdad@nyu.edu"
    data = {
        "name": "delete",
        "email": DELETE_EMAIL,
        "affiliation": "Rand",
        "roles": "ED"
    }

    resp = TEST_CLIENT.put(f"{ep.PEOPLE_EP}/create", json=data)
    assert resp.status_code == HTTPStatus.OK

    resp = TEST_CLIENT.delete(f'{ep.PEOPLE_EP}/{DELETE_EMAIL}')
    assert resp.status_code == HTTPStatus.OK

    # Check if the person is actually deleted
    resp = TEST_CLIENT.get(ep.PEOPLE_EP)
    resp_json = resp.get_json()
    assert DELETE_EMAIL not in resp_json


@patch('data.text.read', autospec=True, return_value={
    'mock_key_1': {'title': 'Test 1', 'text': 'Sample text 1'},
    'mock_key_2': {'title': 'Test 2', 'text': 'Sample text 2'}
})
def test_read_text(mock_read):
    resp = TEST_CLIENT.get(ep.TEXT_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    for _key, entry in resp_json.items():
        assert isinstance(_key, str)
        assert len(_key) > 0
        assert 'title' in entry
        assert 'text' in entry


@patch('data.text.read_one', autospec=True, return_value={'title': 'Sample Title', 'text': 'Sample Text'})
def test_read_one_text(mock_read_one):
    resp = TEST_CLIENT.get(f'{ep.TEXT_EP}/mock_key')
    assert resp.status_code == OK


@patch('data.text.read_one', autospec=True, return_value=None)
def test_read_one_text_not_found(mock_read_one):
    resp = TEST_CLIENT.get(f'{ep.TEXT_EP}/mock_key')
    assert resp.status_code == NOT_FOUND


@pytest.fixture(scope="function")
def add_text():
    NEW_KEY = "testKey"
    data = {
        "key": NEW_KEY,
        "title": "Test Title",
        "text": "This is a test text"
    }
    resp = TEST_CLIENT.post(ep.TEXT_EP, json=data)
    assert resp.status_code == HTTPStatus.OK

    yield NEW_KEY

    delete_resp = TEST_CLIENT.delete(f"{ep.TEXT_EP}/{NEW_KEY}")
    assert delete_resp.status_code == HTTPStatus.OK


def test_add_text(add_text):
    NEW_KEY = add_text
    resp = TEST_CLIENT.get(ep.TEXT_EP)
    resp_json = resp.get_json()
    assert NEW_KEY in resp_json


def test_update_text():
    UPDATE_KEY = "updateKey"
    data = {
        "key": UPDATE_KEY,
        "title": "Original Title",
        "text": "Original text"
    }
    resp = TEST_CLIENT.post(ep.TEXT_EP, json=data)
    assert resp.status_code == HTTPStatus.OK

    updated_data = {
        "title": "Updated Title",
        "text": "Updated text"
    }
    resp = TEST_CLIENT.put(f"{ep.TEXT_EP}/{UPDATE_KEY}", json=updated_data)
    assert resp.status_code == HTTPStatus.OK

    resp = TEST_CLIENT.get(f"{ep.TEXT_EP}/{UPDATE_KEY}")
    resp_json = resp.get_json()
    assert resp_json['title'] == "Updated Title"
    assert resp_json['text'] == "Updated text"

    delete_resp = TEST_CLIENT.delete(f"{ep.TEXT_EP}/{UPDATE_KEY}")
    assert delete_resp.status_code == HTTPStatus.OK


def test_delete_text():
    DELETE_KEY = "deleteKey"
    data = {
        "key": DELETE_KEY,
        "title": "To Delete",
        "text": "This text will be deleted"
    }

    resp = TEST_CLIENT.post(ep.TEXT_EP, json=data)
    assert resp.status_code == HTTPStatus.OK

    resp = TEST_CLIENT.delete(f'{ep.TEXT_EP}/{DELETE_KEY}')
    assert resp.status_code == HTTPStatus.OK

    resp = TEST_CLIENT.get(ep.TEXT_EP)
    resp_json = resp.get_json()
    assert DELETE_KEY not in resp_json


@patch('data.users.read', autospec=True, return_value=[{'username': 'Callahan', 'password': '123abc', 'level': 0}])
def test_read_user(mock_get_users):
    resp = TEST_CLIENT.get(ep.USER_EP)
    resp_json = resp.get_json()
    assert len(resp_json) > 0
    assert any(user['username'] == 'Callahan' for user in resp_json)


@patch.object(usr, 'delete_user')
def test_delete_user_success(mock_delete):
    # Arrange
    mock_delete.return_value = True
    username = "alice"

    # Act
    resp = TEST_CLIENT.delete(f"{ep.USER_EP}/{username}")

    # Assert
    assert resp.status_code == HTTPStatus.OK
    assert resp.get_json() == {"message": f"User '{username}' deleted."}
    mock_delete.assert_called_once_with(username)


@patch.object(usr, 'delete_user')
def test_delete_user_not_found(mock_delete):
    # Arrange
    mock_delete.return_value = False
    username = "bob"

    # Act
    resp = TEST_CLIENT.delete(f"{ep.USER_EP}/{username}")

    # Assert
    assert resp.status_code == HTTPStatus.NOT_FOUND
    assert resp.get_json() == {"message": f"User '{username}' not found."}
    mock_delete.assert_called_once_with(username)


@pytest.fixture(scope="function")
@skip("work in progress")
def add_manuscript():
    NEW_KEY = "testManuscript"
    data = {
        "key": NEW_KEY,
        "title": "Test Manuscript Title",
        "author": "Test Author",
        "author_email": "email@nyu.edu",
        "state": "SUB",
        "text": "blah blah blah",
        "abstract": "Test Abstract",
        "editors": ["editor1"],
        "referees": ["ref1"],
        "history": ["SUB"]
    }
    resp = TEST_CLIENT.post(ep.MANUSCRIPT_EP, json=data)
    assert resp.status_code == HTTPStatus.OK

    yield NEW_KEY

    delete_resp = TEST_CLIENT.delete(f"{ep.MANUSCRIPT_EP}/{NEW_KEY}")
    assert delete_resp.status_code == HTTPStatus.OK


@skip("work in progress")
def test_add_manuscript(add_manuscript):
    NEW_KEY = add_manuscript
    resp = TEST_CLIENT.get(ep.MANUSCRIPT_EP)
    resp_json = resp.get_json()
    assert NEW_KEY in resp_json


def test_delete_manuscript():
    DELETE_KEY = "deleteManuscript"
    data = {
        "key": DELETE_KEY,
        "title": "To Delete",
        "author": "Author To Delete",
        "state": "SUB",
        "abstract": "Abstract to delete"
    }
    resp = TEST_CLIENT.post(ep.MANUSCRIPT_EP, json=data)
    assert resp.status_code == HTTPStatus.OK

    resp = TEST_CLIENT.delete(f'{ep.MANUSCRIPT_EP}/{DELETE_KEY}')
    assert resp.status_code == HTTPStatus.OK

    resp = TEST_CLIENT.get(ep.MANUSCRIPT_EP)
    resp_json = resp.get_json()
    assert DELETE_KEY not in resp_json


def test_valid_actions_for_valid_state():
    response = TEST_CLIENT.get(ep.MANU_EP + '/valid_actions/SUB')
    assert response.status_code == 200
    data = response.get_json()
    assert data['state'] == 'SUB'
    assert isinstance(data['valid_actions'], list)
    assert all(isinstance(action, str) for action in data['valid_actions'])


def test_valid_actions_for_invalid_state():
    response = TEST_CLIENT.get(ep.MANU_EP + '/valid_actions/INVALID_STATE')
    assert response.status_code == 400
    data = response.get_json()
    assert 'Invalid state' in data['message']
