"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

from flask import Flask, request
from flask_restx import Resource, Api, fields  # Namespace
from flask_cors import CORS

import werkzeug.exceptions as wz

import data.people as ppl

app = Flask(__name__)
CORS(app)
api = Api(app)

DATE = '2024-10-17'
DATE_RESP = 'Date'
EDITOR = 'jl13036@nyu.edu'
EDITOR_RESP = 'Editor'
ENDPOINT_EP = '/endpoints'
ENDPOINT_RESP = 'Available endpoints'
HELLO_EP = '/hello'
HELLO_RESP = 'hello'
MESSAGE = 'Message'
PEOPLE_EP = '/people'
PUBLISHER = 'Palgave'
PUBLISHER_RESP = 'Publisher'
RETURN = 'return'
PROJECT_NAME_EP = '/project_name'
PROJECT_NAME_RESP = 'Project Name'
PROJECT_NAME = 'JAXS'
MASTHEAD = 'Masthead'
TITLE = 'The Journal of API Technology'
TITLE_EP = '/title'
TITLE_RESP = 'Title'


@api.route(HELLO_EP)
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {HELLO_RESP: 'world'}


@api.route(ENDPOINT_EP)
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    def get(self):
        """
        The `get()` method will return a list of available endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}


@api.route(PROJECT_NAME_EP)
class ProjectName(Resource):
    """
    This class is used to handle the creating, retrieving,
    deleting, editing of the journal name
    """
    def get(self):
        """
        The `get()` method will retrieve the project name.
        """
        project_name = {
            PROJECT_NAME_RESP: PROJECT_NAME,
            EDITOR_RESP: EDITOR,
            DATE_RESP: DATE,
            PUBLISHER_RESP: PUBLISHER,
        }
        if project_name:
            return project_name, HTTPStatus.OK
        else:
            raise wz.NotFound('Project name not found.')


@api.route(TITLE_EP)
class JournalTitle(Resource):
    """
    This class handles creating, reading, updating
    and deleting the journal title.
    """
    def get(self):
        """
        Retrieve the journal title.
        """
        return {
            TITLE_RESP: TITLE,
            EDITOR_RESP: EDITOR,
            DATE_RESP: DATE,
            PUBLISHER_RESP: PUBLISHER,
        }


@api.route(PEOPLE_EP)
class People(Resource):
    """
    This class handles creating, reading, updating
    and deleting people in journal
    """
    def get(self):
        """
        Retrieve the people in journal
        """
        return ppl.read()


@api.route(f'{PEOPLE_EP}/<email>')
class Person(Resource):
    @api.response(HTTPStatus.OK, 'Success.')
    @api.response(HTTPStatus.NOT_FOUND, 'No such person.')
    def get(self, email):
        """
        Retrieve a journal person.
        """
        person = ppl.read_one(email)
        if person:
            return person, HTTPStatus.OK
        else:
            raise wz.NotFound(f'No such record: {email}')

    @api.response(HTTPStatus.OK, 'Success.')
    @api.response(HTTPStatus.NOT_FOUND, 'No such person.')
    def delete(self, email):
        ret = ppl.delete(email)
        if ret is not None:
            return {'Deleted': ret}
        else:
            raise wz.NotFound(f'No such person: {email}')
        # return {'Message': ret}


PEOPLE_CREATE_FLDS = api.model('AddNewPeopleEntry', {
    ppl.NAME: fields.String,
    ppl.EMAIL: fields.String,
    ppl.AFFILIATION: fields.String,
    ppl.ROLES: fields.String,
})


@api.route(f'{PEOPLE_EP}/create')
class PeopleCreate(Resource):
    """
    Add a person to the journal db.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(PEOPLE_CREATE_FLDS)
    def put(self):
        """
        Add a person.
        """
        try:
            name = request.json.get(ppl.NAME)
            affiliation = request.json.get(ppl.AFFILIATION)
            email = request.json.get(ppl.EMAIL)
            role = request.json.get(ppl.ROLES)
            ret = ppl.create(name, affiliation, email, role)
        except Exception as err:
            raise wz.NotAcceptable(f'Could not add person: '
                                   f'{err=}')
        return {
            MESSAGE: 'Person added!',
            RETURN: ret,
        }


PEOPLE_UPDATE_FLDS = api.model('UpdatePeopleEntry', {
    ppl.NAME: fields.String,
    ppl.EMAIL: fields.String,
    ppl.AFFILIATION: fields.String,
    ppl.ROLES: fields.String,
})


@api.route(f'{PEOPLE_EP}/update')
class PeopleUpdate(Resource):
    """
    Update a person in the journal db.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(PEOPLE_UPDATE_FLDS)
    def post(self):
        """ updates a person """
        try:
            name = request.json.get(ppl.NAME)
            affiliation = request.json.get(ppl.AFFILIATION)
            email = request.json.get(ppl.EMAIL)
            role = request.json.get(ppl.ROLES)
            ret = ppl.update_person(name, affiliation, email, role)
        except Exception as err:
            raise wz.NotAcceptable(f'Could not update person: '
                                   f'{err=}')
        return {
            MESSAGE: 'Person updated!',
            RETURN: ret,
        }


@api.route(f'{PEOPLE_EP}/masthead')
class Masthead(Resource):
    """
    Get a journal's masthead.
    """
    def get(self):
        return {MASTHEAD: ppl.get_masthead()}
