import data.manuscripts.fields as flds

# states:
AUTHOR_REV = 'AUR'
COPY_EDIT = 'CED'
IN_REF_REV = 'REV'
REJECTED = 'REJ'
SUBMITTED = 'SUB'
AU_REVIEW = 'ARV'
AU_REVISIONS = 'ARN'
ED_REV = 'ERV'
FORMATTING = 'FOR'
PUBLISHED = 'PUB'
WITHDRAWN = 'WDN'
ED_MOVING = 'MOV'  # extra state to implement editor move
TEST_STATE = SUBMITTED

VALID_STATES = [
    AUTHOR_REV,
    COPY_EDIT,
    IN_REF_REV,
    REJECTED,
    SUBMITTED,
    AU_REVIEW,
    AU_REVISIONS,
    ED_REV,
    FORMATTING,
    PUBLISHED,
    WITHDRAWN,
    ED_MOVING,  # extra state to implement editor move
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
REJECT = 'REJ'
ACCEPT_W_REV = 'AWR'
REMOVE_REF = 'RRF'
EDITOR_MOVE = "EDM"

# au action
DONE = 'DON'
WITHDRAW = 'WDW'

# ref action
SUBMIT_REV = 'SRV'

# for testing:
TEST_ACTION = ACCEPT

VALID_ACTIONS = [
    ACCEPT,
    ASSIGN_REF,
    DONE,
    REJECT,
    ACCEPT_W_REV,
    WITHDRAW,
    REMOVE_REF,  # not sure how this works
    SUBMIT_REV,
    EDITOR_MOVE,
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


def sub_assign_ref(manu: dict) -> str:
    return IN_REF_REV


FUNC = 'f'
STATE_TABLE = {
    SUBMITTED: {
        ASSIGN_REF: {
            # These next lines are alternatives that work the same.
            # FUNC: sub_assign_ref,
            FUNC: lambda m: IN_REF_REV,
        },
        REJECT: {
            FUNC: lambda m: REJECTED,
        },
    },
    IN_REF_REV: {
    },
    COPY_EDIT: {
        DONE: {
            FUNC: lambda m: AUTHOR_REV,
        },
    },
    AUTHOR_REV: {
    },
    REJECTED: {
    },
}


def get_valid_actions_by_state(state: str):
    valid_actions = STATE_TABLE[state].keys()
    print(f'{valid_actions=}')
    return valid_actions


def handle_action(curr_state, action, manuscript) -> str:
    if curr_state not in STATE_TABLE:
        raise ValueError(f'Bad state: {curr_state}')
    if action not in STATE_TABLE[curr_state]:
        raise ValueError(f'{action} not available in {curr_state}')
    return STATE_TABLE[curr_state][action][FUNC](manuscript)


def main():
    print(handle_action(SUBMITTED, ASSIGN_REF, SAMPLE_MANU))
    print(handle_action(SUBMITTED, REJECT, SAMPLE_MANU))


if __name__ == '__main__':
    main()
