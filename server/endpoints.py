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
import data.text as txt
import data.manuscripts as manu
import data.users as usr
import data.roles as rls

import subprocess

import security.security as sec

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
ROLES_EP = '/roles'
RETURN = 'return'
PROJECT_NAME_EP = '/project_name'
PROJECT_NAME_RESP = 'Project Name'
PROJECT_NAME = 'JAXS'
MASTHEAD = 'Masthead'
TITLE = 'The Journal of API Technology'
TITLE_EP = '/title'
TITLE_RESP = 'Title'
TEXT_EP = '/texts'
MANUSCRIPT_EP = '/manus'
MANU_EP = '/manu'
LOGIN_EP = '/login'
USER_EP = '/user'
DEV_EP = '/dev/logs'
ELOG_LOC = '/var/log/jaxs-proj-annatx.pythonanywhere.com.error.log'
ELOG_KEY = 'error logs'
ALOG_LOC = '/var/log/jaxs-proj-annatx.pythonanywhere.com.access.log'
ALOG_KEY = 'access logs'
SLOG_LOC = '/var/log/jaxs-proj-annatx.pythonanywhere.com.server.log'
SLOG_KEY = 'server logs'


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


@api.route(ROLES_EP)
class Roles(Resource):
    """
    This class handles reading person roles.
    """
    def get(self):
        """
        Retrieve the journal person roles.
        """
        return rls.read()


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


EDITOR = 'editor'


@api.route(f'{PEOPLE_EP}/<email>/<user_id>')
class Person(Resource):
    @api.response(HTTPStatus.OK, 'Success.')
    @api.response(HTTPStatus.NOT_FOUND, 'No such person.')
    def get(self, email, user_id):
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
    def delete(self, email, user_id):
        kwargs = {sec.LOGIN_KEY: 'any key for now'}
        if not sec.is_permitted(sec.PEOPLE, sec.DELETE, user_id,
                                **kwargs):
            raise wz.Forbidden('This user does not have '
                               + 'authorization for this action.')
        person = ppl.read_one(email)
        ret = ppl.delete(email)
        if ret is not None:
            if person:
                usr.delete_user(person.get('name'))
            return {'Deleted': ret}, HTTPStatus.OK
        else:
            raise wz.NotFound(f'No such person: {email}')
        # return {'Message': ret}


# @api.route(f'{PEOPLE_EP}/<email>')
# class PersonDelete(Resource):
#     """
#     Delete a journal person without requiring a user_id.
#     """
#     @api.response(HTTPStatus.OK, 'Success.')
#     @api.response(HTTPStatus.NOT_FOUND, 'No such person.')
#     def get(self, email):
#         person = ppl.read_one(email)
#         if person:
#             return person, HTTPStatus.OK
#         else:
#             raise wz.NotFound(f'No such record: {email}')
#
#     @api.response(HTTPStatus.OK, 'Success.')
#     @api.response(HTTPStatus.NOT_FOUND, 'No such person.')
#     def delete(self, email):
#         """
#         Delete a journal person by email.
#         """
#         ret = ppl.delete(email)
#         if ret is not None:
#             return {'Deleted': ret}, HTTPStatus.OK
#         else:
#             raise wz.NotFound(f'No such person: {email}')


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
    ppl.ROLES: fields.List(fields.String),
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
            roles = request.json.get(ppl.ROLES)
            ret = ppl.update_person(name, affiliation, email, roles)
        except Exception as err:
            raise wz.NotAcceptable(f'Could not update person: '
                                   f'{err=}')
        return {
            MESSAGE: 'Person updated!',
            RETURN: ret,
        }


TEXT_CREATE_FLDS = api.model('AddNewTextEntry', {
    txt.KEY: fields.String,
    txt.TITLE: fields.String,
    txt.TEXT: fields.String,
})

TEXT_UPDATE_FLDS = api.model('UpdateTextEntry', {
    txt.TITLE: fields.String,
    txt.TEXT: fields.String,
})


@api.route(TEXT_EP)
class Texts(Resource):
    """
    This class handles retrieving all text entries
    or creating new text entries.
    """
    def get(self):
        """
        Retrieve all text entries.
        """
        return txt.read(), HTTPStatus.OK

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(TEXT_CREATE_FLDS)
    def post(self):
        """
        Add a new text entry.
        """
        try:
            key = request.json.get(txt.KEY)
            title = request.json.get(txt.TITLE)
            text = request.json.get(txt.TEXT)
            ret = txt.create(key, title, text)
        except ValueError as err:
            raise wz.NotAcceptable(f'Could not add text: {err}')
        return {
            MESSAGE: 'Text added!',
            RETURN: ret,
        }, HTTPStatus.OK


@api.route(f'{TEXT_EP}/<key>')
class Text(Resource):
    """
    This class handles retrieving, updating,
    or deleting a specific text entry by its key.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Text not found')
    def get(self, key):
        """
        Retrieve a specific text entry by key.
        """
        text = txt.read_one(key)
        if text:
            return text, HTTPStatus.OK
        else:
            raise wz.NotFound(f'Text with key \'{key}\' not found.')

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Text not found')
    def delete(self, key):
        """
        Delete a specific text entry by key.
        """
        ret = txt.delete(key)
        if "does not exist" in ret:
            raise wz.NotFound(ret)
        return {
            MESSAGE: ret,
        }, HTTPStatus.OK

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(TEXT_UPDATE_FLDS)
    def put(self, key):
        """
        Update a specific text entry by key.
        """
        try:
            title = request.json.get(txt.TITLE)
            text = request.json.get(txt.TEXT)
            ret = txt.update(key, title, text)
        except ValueError as err:
            raise wz.NotAcceptable(f'Could not update text: {err}')
        return {
            MESSAGE: 'Text updated!',
            RETURN: ret,
        }, HTTPStatus.OK


MANUSCRIPTS_CREATE_FLDS = api.model('AddNewManuscriptEntry', {
    'key': fields.String,
    'title': fields.String,
    'author': fields.String,
    'author_email': fields.String,
    'state': fields.String,
    'text': fields.String,
    'abstract': fields.String,
    'editors': fields.List(fields.String),
    'referees': fields.List(fields.String),
    'history': fields.List(fields.String),
})

MANUSCRIPTS_UPDATE_FLDS = api.model('UpdateManuscriptEntry', {
    'title': fields.String,
    'author': fields.String,
    'author_email': fields.String,
    'state': fields.String,
    'text': fields.String,
    'abstract': fields.String,
    'editor': fields.String,
    'referee': fields.Raw,
    'history': fields.List(fields.String),
})


@api.route(f'{PEOPLE_EP}/masthead')
class Masthead(Resource):
    """
    Get a journal's masthead.
    """
    def get(self):
        return {MASTHEAD: ppl.get_masthead()}


MANU_ACTION_FLDS = api.model('ManuscriptActionReceived', {
    manu.MANU_ID: fields.String,
    manu.CURR_STATE: fields.String,
    manu.ACTION: fields.String,
    manu.REFEREE: fields.String,
    manu.TARGET_STATE: fields.String,
})

MANU_UPDATE_ACTION_FLDS = api.model('ManuscriptUpdateAction', {
    manu.MANU_ID: fields.String,
    manu.ACTION: fields.String,
    manu.REFEREE: fields.String,
    manu.TARGET_STATE: fields.String,
})


# Testing fsm only
@api.route(f'{MANU_EP}/receive_action')
class ReceiveAction(Resource):
    """
    Receive an action for a manuscript.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(MANU_ACTION_FLDS)
    def put(self):
        """
        Receive an action for a manuscript.
        """
        try:
            manu_id = request.json.get(manu.MANU_ID)
            curr_state = request.json.get(manu.CURR_STATE)
            action = request.json.get(manu.ACTION)
            try:
                target_state = request.json.get(manu.TARGET_STATE)
            except Exception:
                target_state = None
            kwargs = {}
            kwargs[manu.REFEREE] = request.json.get(manu.REFEREE)

            ret = manu.handle_action(manu_id, curr_state,
                                     action, target_state, **kwargs)
        except Exception as err:
            raise wz.NotAcceptable(f'Bad action: ' f'{err=}')
        return {
            MESSAGE: 'Action received!',
            RETURN: ret,
        }


# testing update action with manuscript
@api.route(f'{MANU_EP}/update_action')
class UpdateAction(Resource):
    """
    Receive an action for a manuscript.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(MANU_UPDATE_ACTION_FLDS)
    def put(self):
        """
        Receive an action for a manuscript.
        """
        try:
            manu_id = request.json.get(manu.MANU_ID)
            action = request.json.get(manu.ACTION)
            try:
                target_state = request.json.get(manu.TARGET_STATE)
            except Exception:
                target_state = None
            kwargs = {}
            kwargs[manu.REFEREE] = request.json.get(manu.REFEREE)
            ret = manu.update_action(manu_id, action, target_state, **kwargs)

        except Exception as err:
            raise wz.NotAcceptable(f'Bad action: ' f'{err=}')
        return {
            MESSAGE: 'Action received!',
            RETURN: ret,
        }


AssignRefModel = api.model('AssignRefModel', {
    manu.KEY:      fields.String(required=True, description='Manuscript key'),
    manu.REFEREE:  fields.String(required=True,
                                 description='Email of the referee'),
})


@api.route(f'{MANU_EP}/assign_referee')
class AssignReferee(Resource):
    @api.expect(AssignRefModel)
    @api.response(HTTPStatus.OK,   'Referee assigned and role updated')
    @api.response(HTTPStatus.NOT_FOUND, 'Missing manuscript or person')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Bad request')
    def post(self):
        payload = request.get_json() or {}
        manu_id = payload.get(manu.KEY, '').strip()
        referee = payload.get(manu.REFEREE, '').strip()

        if not manu_id or not referee:
            raise wz.NotAcceptable('Both manuscript key'
                                   'and referee email are required.')

        manuscript = manu.read_one(manu_id)
        if not manuscript:
            raise wz.NotFound(f'No manuscript with key {manu_id}')

        person = ppl.read_one(referee)
        if not person:
            raise wz.NotFound(f'No person with email {referee}')

        new_state = manu.assign_ref(manuscript, referee)

        roles = set(person.get(ppl.ROLES, []))
        if 'REF' not in roles:
            roles.add('REF')
            ppl.update_person(
                name=person[ppl.NAME],
                affiliation=person[ppl.AFFILIATION],
                email=referee,
                roles=list(roles)
            )

        return {
            'message': 'Referee assigned and REF role granted',
            'new_state':  new_state,
        }, HTTPStatus.OK


@api.route(MANUSCRIPT_EP)
class Manuscripts(Resource):
    """
    This class handles retrieving all manuscript entries
    or creating new manuscript entries.
    """
    def get(self):
        """
        Retrieve all manuscript entries.
        """
        return manu.read(), HTTPStatus.OK

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(MANUSCRIPTS_CREATE_FLDS)
    def post(self):
        """
        Add a new manuscript entry.
        """
        try:
            key = request.json.get('key')
            title = request.json.get('title')
            author = request.json.get('author')
            author_email = request.json.get('author_email')
            state = request.json.get('state')
            text = request.json.get('text')
            abstract = request.json.get('abstract')
            editors = request.json.get('editors')
            referees = request.json.get('referees')
            history = request.json.get('history')
            ret = manu.create(key, title, author, author_email, state,
                              text, abstract, editors, referees, history)
        except ValueError as err:
            raise wz.NotAcceptable(f'Could not add manuscript: {err}')
        return {
            'message': 'Manuscript added!',
            'return': ret,
        }, HTTPStatus.OK


@api.route(f'{MANUSCRIPT_EP}/<key>')
class Manuscript(Resource):
    """
    This class handles retrieving, updating,
    or deleting a specific manuscript entry by its key.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Manuscript not found')
    def get(self, key):
        """
        Retrieve a specific manuscript entry by key.
        """
        manuscript = manu.read_one(key)
        if manuscript:
            return manuscript, HTTPStatus.OK
        else:
            raise wz.NotFound(f'Manuscript with key \'{key}\' not found.')

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Manuscript not found')
    def delete(self, key):
        """
        Delete a specific manuscript entry by key.
        """
        ret = manu.delete(key)
        if "does not exist" in ret:
            raise wz.NotFound(ret)
        return {
            'message': ret,
        }, HTTPStatus.OK


@api.route(f'{MANU_EP}/valid_actions/<state>')
class ValidActions(Resource):
    """
    Return valid actions for a given manuscript state.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.BAD_REQUEST, 'Invalid state')
    def get(self, state):
        try:
            valid_actions = manu.get_valid_actions_by_state(state)
            return {'state': state,
                    'valid_actions': list(valid_actions)}, HTTPStatus.OK
        except KeyError as e:
            raise wz.BadRequest(f"Invalid state '{state}': {e}")


USER_LOGIN_FIELDS = api.model('UserLogin', {
    usr.USERNAME: fields.String,
    usr.PASSWORD: fields.String,
})


@api.route(USER_EP)
class Users(Resource):
    def get(self):
        """
        Retrieve all login credentials.
        """
        return usr.read(), HTTPStatus.OK

    @api.route(f"{USER_EP}/<username>")
    @api.param('username', 'The username to delete')
    class User(Resource):
        @api.response(HTTPStatus.OK, 'User deleted')
        @api.response(HTTPStatus.NOT_FOUND, 'User not found')
        def delete(self, username):
            """
            Delete a user by username.
            """
            if usr.delete_user(username):
                return ({"message": f"User '{username}' deleted."},
                        HTTPStatus.OK)
            return ({"message": f"User '{username}' not found."},
                    HTTPStatus.NOT_FOUND)


@api.route(LOGIN_EP)
class UserLogin(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.UNAUTHORIZED, 'Not authorized')
    @api.expect(USER_LOGIN_FIELDS)
    def post(self):
        try:
            username = request.json.get(usr.USERNAME)
            password = request.json.get(usr.PASSWORD)

            if not username or not password:
                raise ValueError("Missing username or password")

            # Check if user exists in MongoDB
            user = usr.read_one(username)
            if user and usr.pass_is_valid(username, password):
                return {"message": "Login successful",
                        "email": user["email"]}, HTTPStatus.OK

            raise ValueError("Invalid username or password")

        except Exception as err:
            return ({"message": f"Authentication failed: {err}"},
                    HTTPStatus.UNAUTHORIZED)


USER_REGISTER_FIELDS = api.model('UserRegister', {
    usr.USERNAME: fields.String,
    usr.PASSWORD: fields.String,
})


@api.route(f'{LOGIN_EP}/create')
class UserRegister(Resource):
    @api.response(HTTPStatus.CREATED, 'Success')
    @api.response(HTTPStatus.BAD_REQUEST, 'Bad Request')
    @api.response(HTTPStatus.CONFLICT, 'Conflict')
    @api.expect(USER_REGISTER_FIELDS)
    def post(self):
        """
        Create a new user with username, email and password.
        """
        try:
            username = request.json.get(usr.USERNAME)
            password = request.json.get(usr.PASSWORD)
            email = request.json.get(usr.EMAIL)

            if not username or not password or not email:
                return ({"message": "Missing username, password, or email"},
                        HTTPStatus.BAD_REQUEST)

            if usr.read_one(username):
                return ({"message": "Username already exists"},
                        HTTPStatus.CONFLICT)

            try:
                usr.validate_password(password)
            except ValueError as err:
                return {"message": str(err)}, HTTPStatus.BAD_REQUEST

            usr.create(username, password, email)
            return ({"message": "User created successfully!"},
                    HTTPStatus.CREATED)

        except Exception as err:
            return ({"message": f"User creation failed: {err}"},
                    HTTPStatus.INTERNAL_SERVER_ERROR)


def format_output(result):
    return result.stdout.decode("utf-8")


@api.route(f'{DEV_EP}/error')
class ErrorLog(Resource):
    def get(self):
        """
        Retrieves last 10 error logs.
        """
        result = subprocess.run(f"tail {ELOG_LOC}",
                                shell=True, stdout=subprocess.PIPE)
        return {ELOG_KEY: format_output(result)}


@api.route(f'{DEV_EP}/access')
class AccessLog(Resource):
    def get(self):
        """
        Retrieves last 10 access logs.
        """
        result = subprocess.run(f"tail {ALOG_LOC}",
                                shell=True, stdout=subprocess.PIPE)
        return {ALOG_KEY: format_output(result)}


@api.route(f'{DEV_EP}/server')
class ServerLog(Resource):
    def get(self):
        """
        Retrieves last 10 server logs.
        """
        result = subprocess.run(f"tail {SLOG_LOC}",
                                shell=True, stdout=subprocess.PIPE)
        return {SLOG_KEY: format_output(result)}
