import data.db_connect as dbc
import data.manus.fields as flds
MANUSCRIPTS_COLLECT = 'manuscripts'

ACTION = 'action'
AUTHOR = 'author'
CURR_STATE = 'curr_state'
DISP_NAME = 'disp_name'
MANU_ID = '_id'
TARGET_STATE = 'target_state'
REFEREE = 'referee'
REFEREES = 'referees'
TITLE = 'title'
EDITORS = 'editors'

TEST_ID = 'fake_id'
TEST_FLD_NM = TITLE
TEST_FLD_DISP_NM = 'Title'


FIELDS = {
    TITLE: {
        DISP_NAME: TEST_FLD_DISP_NM,
    },
}

# states:
AUTHOR_REV = 'AUR'
COPY_EDIT = 'CED'
IN_REF_REV = 'REV'
REJECTED = 'REJ'
SUBMITTED = 'SUB'
WITHDRAWN = 'WIT'
EDITOR_REV = 'ERV'
FORMATTING = 'FOR'
PUBLISHED = 'PUB'
AUTHOR_REVISIONS = "ARN"

TEST_STATE = SUBMITTED

VALID_STATES = [
    AUTHOR_REV,  # author review
    COPY_EDIT,  # copy edit
    IN_REF_REV,  # referee review
    REJECTED,  # rejected
    SUBMITTED,  # submitted
    WITHDRAWN,  # withdrawn
    EDITOR_REV,  # editor review
    AUTHOR_REVISIONS,  # author revision
    PUBLISHED,  # published
    FORMATTING,  # formatting
]


SAMPLE_MANU = {
    TITLE: 'Short module import names in Python',
    AUTHOR: 'Eugene Callahan',
    REFEREES: [],
    EDITORS: [],
}


def get_states() -> list:
    return VALID_STATES


def is_valid_state(state: str) -> bool:
    return state in VALID_STATES


# ed actions:
ACCEPT = 'ACC'
ASSIGN_REF = 'ARF'
DELETE_REF = 'DRF'
REJECT = 'REJ'
ACCEPT_W_REV = 'AWR'
EDITOR_MOVE = "EDM"

# au action
DONE = 'DON'
WITHDRAW = 'WIT'

# ref action
SUBMIT_REV = 'SRV'
# for testing:
TEST_ACTION = ACCEPT

VALID_ACTIONS = [
    ACCEPT,
    ASSIGN_REF,
    DELETE_REF,
    REJECT,
    DONE,
    ACCEPT_W_REV,
    WITHDRAW,
    EDITOR_MOVE,
    SUBMIT_REV
]

# for data fields
REF_VERDICT = [
    ACCEPT,
    ACCEPT_W_REV,
    REJECT
]


def get_actions() -> list:
    return VALID_ACTIONS


def is_valid_action(action: str) -> bool:
    return action in VALID_ACTIONS


def assign_ref(manu: dict, referee: str, **kwargs) -> str:
    if REFEREES not in manu:
        manu[REFEREES] = []
    if referee and referee not in manu[REFEREES]:
        manu[REFEREES].append(referee)

    manu[STATE] = IN_REF_REV

    dbc.update(
      MANUSCRIPTS_COLLECT,
      {KEY: manu[KEY]},
      {
        REFEREES: manu[REFEREES],
        STATE:    IN_REF_REV
      }
    )

    return IN_REF_REV


def delete_ref(manu: dict, referee: str) -> str:
    if REFEREES not in manu:
        manu[REFEREES] = []

    if referee in manu[REFEREES]:
        manu[REFEREES].remove(referee)
        dbc.update(MANUSCRIPTS_COLLECT, {KEY: manu[KEY]},
                   {REFEREES: manu[REFEREES]})

    return IN_REF_REV if manu[REFEREES] else SUBMITTED


def read_one(_id: str) -> dict:
    manu = dbc.read_one(MANUSCRIPTS_COLLECT, {KEY: _id})
    return manu


def handle_editor_move(manu: dict, target_state: str) -> str:
    if target_state not in VALID_STATES:
        raise ValueError(f"Invalid target state: {target_state}")
    return target_state


FUNC = 'f'

COMMON_ACTIONS = {
    WITHDRAW: {
        FUNC: lambda **kwargs: WITHDRAWN,
    },
}

STATE_TABLE = {
    SUBMITTED: {
        ASSIGN_REF: {
            FUNC: assign_ref,
        },
        REJECT: {
            FUNC: lambda **kwargs: REJECTED,
        },
        EDITOR_MOVE: {
            FUNC: handle_editor_move,
        },
        **COMMON_ACTIONS,
    },
    IN_REF_REV: {
        ASSIGN_REF: {
            FUNC: assign_ref,
        },
        DELETE_REF: {
            FUNC: delete_ref,
        },
        ACCEPT: {
            FUNC: lambda **kwargs: COPY_EDIT,
        },
        ACCEPT_W_REV: {
            FUNC: lambda **kwargs: AUTHOR_REVISIONS,
        },
        REJECT: {
            FUNC: lambda **kwargs: REJECTED,
        },
        EDITOR_MOVE: {
            FUNC: handle_editor_move,
        },
        **COMMON_ACTIONS,
    },
    COPY_EDIT: {
        DONE: {
            FUNC: lambda **kwargs: AUTHOR_REV,
        },
        EDITOR_MOVE: {
            FUNC: handle_editor_move,
        },
        **COMMON_ACTIONS,
    },
    AUTHOR_REV: {
        DONE: {
            FUNC: lambda **kwargs: FORMATTING,
        },
        EDITOR_MOVE: {
            FUNC: handle_editor_move,
        },
        **COMMON_ACTIONS,
    },
    REJECTED: {
        EDITOR_MOVE: {
            FUNC: handle_editor_move,
        },
        **COMMON_ACTIONS,
    },
    WITHDRAWN: {
        EDITOR_MOVE: {
            FUNC: handle_editor_move,
        },
        **COMMON_ACTIONS,
    },
    AUTHOR_REVISIONS: {
        DONE: {
            FUNC: lambda **kwargs: EDITOR_REV,
        },
        EDITOR_MOVE: {
            FUNC: handle_editor_move,
        },
        **COMMON_ACTIONS,
    },
    EDITOR_REV: {
        ACCEPT: {
            FUNC: lambda **kwargs: COPY_EDIT,
        },
        EDITOR_MOVE: {
            FUNC: handle_editor_move,
        },
        **COMMON_ACTIONS,
    },
    FORMATTING: {
        DONE: {
            FUNC: lambda **kwargs: PUBLISHED,
        },
        EDITOR_MOVE: {
            FUNC: handle_editor_move,
        },
        **COMMON_ACTIONS,
    },
    PUBLISHED: {
        EDITOR_MOVE: {
            FUNC: handle_editor_move,
        },
        # End
    },
}


def get_valid_actions_by_state(state: str):
    valid_actions = STATE_TABLE[state].keys()
    print(f'{valid_actions=}')
    return valid_actions


def handle_action(manu_id, curr_state, action,
                  target_state=None, **kwargs) -> str:
    kwargs['manu'] = read_one(manu_id)
    if curr_state not in STATE_TABLE:
        raise ValueError(f'Bad state: {curr_state}')
    if action not in STATE_TABLE[curr_state]:
        raise ValueError(f'{action} not available in {curr_state}')

    # Handle editor move
    if action == EDITOR_MOVE:
        if target_state is None:
            raise ValueError("target_state is required for EDITOR_MOVE")
        return STATE_TABLE[curr_state][action][FUNC](manu=kwargs['manu'],
                                                     target_state=target_state)

    # Handle everything else
    return STATE_TABLE[curr_state][action][FUNC](**kwargs)

# implementation of manuscript in the database ----------------


# Fields
KEY = 'key'
TITLE = 'title'
AUTHOR = 'author'
AUTHOR_EMAIL = 'author_email'
STATE = 'state'
TEXT = 'text'
ABSTRACT = 'abstract'
HISTORY = 'history'


def exists(key: str) -> bool:
    """
    Checks if a manuscript with the given key exists.
    Arguments:
        - key: The key for the manuscript
    Returns True if the manuscript exists, False otherwise.
    """
    return read_one(key) is not None


def read() -> dict:
    """
    Retrieves all manuscripts as a dictionary keyed on manuscript keys.
    Returns a dictionary of manuscripts.
    """
    manuscripts = dbc.read_dict(MANUSCRIPTS_COLLECT, KEY)
    return manuscripts


def create(key: str, title: str, author: str, author_email: str,
           state: str, text: str, abstract: str, editors: list,
           referees: list, history: list) -> str:
    """
    Adds a new manuscript entry if the key does not already exist.
    Arguments:
        - key: The unique ID for the manuscript
        - title: The title of the manuscript
        - author: The author of the manuscript
        - author_email: The email address of the author
        - state: The current state of the manuscript
        - text: The body text of the manuscript
        - abstract: The abstract of the manuscript
        - editors: The assigned editors for the manuscript
        - referees: A list of referees
        - history: A list of historical states for the manuscript
    Returns a success message or raises an error if the key already exists.
    """
    if exists(key):
        raise ValueError(f"Adding duplicate manuscript {key}")
    dbc.create(MANUSCRIPTS_COLLECT, {
        KEY: key,
        TITLE: title,
        AUTHOR: author,
        AUTHOR_EMAIL: author_email,
        STATE: state,
        TEXT: text,
        ABSTRACT: abstract,
        EDITORS: editors,
        REFEREES: referees,
        HISTORY: history,
    })
    return key


def delete(key: str) -> str:
    """
    Removes a manuscript entry if the key exists.
    Arguments:
        - key: The key of the manuscript to delete
    Returns a success message or a does not exist message.
    """
    if not exists(key):
        return f"'{key}' does not exist."
    dbc.delete(MANUSCRIPTS_COLLECT, {KEY: key})
    return f"'{key}' deleted successfully."


def update_action(_id: str, action: str, target_state=None, **kwargs):
    manuscript = read_one(_id)
    if not exists(_id):
        raise ValueError(f"Manuscript {_id} does not exist")
    if action not in VALID_ACTIONS:
        raise ValueError(f"Invalid action: {action}")
    new_state = handle_action(_id, manuscript[STATE], action,
                              target_state, **kwargs)
    update_dict = {
        flds.STATE: new_state,
        flds.HISTORY: manuscript[flds.HISTORY] + [new_state],
    }
    dbc.update(MANUSCRIPTS_COLLECT, {KEY: _id}, update_dict)
    return new_state


def main():
    print(handle_action(TEST_ID, SUBMITTED, ASSIGN_REF, ref='Jack'))
    print(handle_action(TEST_ID, IN_REF_REV, ASSIGN_REF,
                        ref='Jill', extra='Extra!'))
    print(handle_action(TEST_ID, IN_REF_REV, DELETE_REF,
                        ref='Jill'))
    print(handle_action(TEST_ID, IN_REF_REV, DELETE_REF,
                        ref='Jack'))
    print(handle_action(TEST_ID, SUBMITTED, WITHDRAW))
    print(handle_action(TEST_ID, SUBMITTED, REJECT))


if __name__ == '__main__':
    main()
