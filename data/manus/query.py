import data.manus.fields as flds

MANU_ID = "_id"
CURR_STATE = "curr_state"
ACTION = "action"
REFEREE = "referee"


# states:
AUTHOR_REV = 'AUR'
COPY_EDIT = 'CED'
IN_REF_REV = 'REV'
REJECTED = 'REJ'
SUBMITTED = 'SUB'
WITHDRAWN = 'WIT'
AUTHOR_REVISIONS = 'ARN'
ED_REV = 'ERV'
FORMATTING = 'FOR'
PUBLISHED = 'PUB'
ED_MOVING = 'MOV'  # extra state to implement editor move
TEST_STATE = SUBMITTED

VALID_STATES = [
    AUTHOR_REV,
    COPY_EDIT,
    IN_REF_REV,
    REJECTED,
    SUBMITTED,
    # AUTHOR_REVISIONS,
    # ED_REV,
    # FORMATTING,
    # PUBLISHED,
    WITHDRAWN,
]


SAMPLE_MANU = {
    flds.TITLE: 'Short module import names in Python',
    flds.AUTHOR: 'Sunny Li',
    flds.REFEREES: [],
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


def assign_ref(manu: dict, ref: str, extra=None) -> str:
    print(extra)
    manu[flds.REFEREES].append(ref)
    return IN_REF_REV


def handle_editor_move(manu: dict, target_state: str) -> str:
    if target_state not in VALID_STATES:
        raise ValueError(f"Invalid target state: {target_state}")
    return target_state


def delete_ref(manu: dict, ref: str) -> str:
    if len(manu[flds.REFEREES]) > 0:
        manu[flds.REFEREES].remove(ref)
    if len(manu[flds.REFEREES]) > 0:
        return IN_REF_REV
    else:
        return SUBMITTED


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
        **COMMON_ACTIONS,
    },
    IN_REF_REV: {
        ASSIGN_REF: {
            FUNC: assign_ref,
        },
        DELETE_REF: {
            FUNC: delete_ref,
        },
        **COMMON_ACTIONS,
    },
    COPY_EDIT: {
        DONE: {
            FUNC: lambda **kwargs: AUTHOR_REV,
        },
        **COMMON_ACTIONS,
    },
    AUTHOR_REV: {
        **COMMON_ACTIONS,
    },
    REJECTED: {
        **COMMON_ACTIONS,
    },
    WITHDRAWN: {
        **COMMON_ACTIONS,
    },
}


def get_valid_actions_by_state(state: str):
    valid_actions = STATE_TABLE[state].keys()
    print(f'{valid_actions=}')
    return valid_actions


def handle_action(curr_state, action, **kwargs) -> str:
    if curr_state not in STATE_TABLE:
        raise ValueError(f'Bad state: {curr_state}')
    if action not in STATE_TABLE[curr_state]:
        raise ValueError(f'{action} not available in {curr_state}')
    return STATE_TABLE[curr_state][action][FUNC](**kwargs)
    

def main():
    print(handle_action(SUBMITTED, ASSIGN_REF,
                        manu=SAMPLE_MANU, ref='Jack'))
    print(handle_action(IN_REF_REV, ASSIGN_REF, manu=SAMPLE_MANU,
                        ref='Jill', extra='Extra!'))
    print(handle_action(IN_REF_REV, DELETE_REF, manu=SAMPLE_MANU,
                        ref='Jill'))
    print(handle_action(IN_REF_REV, DELETE_REF, manu=SAMPLE_MANU,
                        ref='Jack'))
    print(handle_action(SUBMITTED, WITHDRAW, manu=SAMPLE_MANU))
    print(handle_action(SUBMITTED, REJECT, manu=SAMPLE_MANU))


if __name__ == '__main__':
    main()
