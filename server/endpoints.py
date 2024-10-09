"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
# from http import HTTPStatus

from flask import Flask  # , request
from flask_restx import Resource, Api  # Namespace, fields
from flask_cors import CORS

# import werkzeug.exceptions as wz

import data.people as ppl

app = Flask(__name__)
CORS(app)
api = Api(app)

ENDPOINT_EP = '/endpoints'
ENDPOINT_RESP = 'Available endpoints'
HELLO_EP = '/hello'
HELLO_RESP = 'hello'
PEOPLE_EP = '/people'
PROJECT_NAME_EP = '/project_name'
PROJECT_NAME_RESP = 'Project Name'
PROJECT_NAME = 'JAXS'


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


@api.route('/endpoints')
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
        return {PROJECT_NAME_RESP: PROJECT_NAME}


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
        return ppl.get_people()

    def delete(self, email):
        """
        Delete a person from the journal.
        """
        success = ppl.delete_person(email)
        if success:
            return {"message": f"User with email '{email}' was deleted."}, 200
        else:
            return {"error": "Person not found."}, 404


@api.route(f"{PEOPLE_EP}/<_id>/<name>/<affiliation>")
class Person(Resource):
    def post(self, name: str, affiliation: str, _id: str):
        """
        Add a person to the journal.
        """
        success = ppl.create_person(name, affiliation, _id)
        if success:
            return {"message": f"User with email '{_id}' was added."}, 200
        else:
            return {"error": "Person cannot be added."}, 404
