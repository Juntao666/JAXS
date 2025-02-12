ACTION = 'action'
AUTHOR = 'author'
CURR_STATE = 'curr_state'
DISP_NAME = 'disp_name'
MANU_ID = '_id'
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
REMOVE_REF = 'RRF'
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
    DONE,
    REJECT,
    WITHDRAW,
    REMOVE_REF
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


def assign_ref(manu: dict, referee: str, extra=None) -> str:
    manu[REFEREES].append(referee)
    return IN_REF_REV


def delete_ref(manu: dict, referee: str) -> str:
    if len(manu[REFEREES]) > 0:
        manu[REFEREES].remove(referee)
    if len(manu[REFEREES]) > 0:
        return IN_REF_REV
    else:
        return SUBMITTED


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
        REMOVE_REF: {
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


def handle_action(manu_id, curr_state, action, **kwargs) -> str:
    kwargs['manu'] = SAMPLE_MANU
    if curr_state not in STATE_TABLE:
        raise ValueError(f'Bad state: {curr_state}')
    if action not in STATE_TABLE[curr_state]:
        raise ValueError(f'{action} not available in {curr_state}')

    # Handle editor move
    if action == EDITOR_MOVE:
        target_state = kwargs.get('target_state')
        if target_state is None:
            raise ValueError("target_state is required for EDITOR_MOVE")
        return STATE_TABLE[curr_state][action][FUNC](manu=kwargs['manu'],
                                                     target_state=target_state)

    # Handle everything else
    return STATE_TABLE[curr_state][action][FUNC](**kwargs)


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
