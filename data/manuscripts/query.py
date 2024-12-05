# states:
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


def handle_action(curr_state, action, goal_state=ED_MOVING) -> str:
    if not is_valid_state(curr_state):
        raise ValueError(f'Invalid state: {curr_state}')
    if not is_valid_state(goal_state):
        raise ValueError(f'Invalid state: {goal_state}')
    if not is_valid_action(action):
        raise ValueError(f'Invalid action: {action}')

    new_state = curr_state

    if action == EDITOR_MOVE:
        new_state = goal_state
        return new_state

    if curr_state == SUBMITTED:
        if action == ASSIGN_REF:
            new_state = IN_REF_REV
        elif action == REJECT:
            new_state = REJECTED
        elif action == WITHDRAW:
            new_state = WITHDRAWN
    elif curr_state == IN_REF_REV:
        if action == ACCEPT:
            new_state = COPY_EDIT
        elif action == REJECT:
            new_state = REJECTED
        elif action == ACCEPT_W_REV:
            new_state = AU_REVISIONS
        elif action == WITHDRAW:
            new_state = WITHDRAWN
    elif curr_state == AU_REVISIONS:
        if action == DONE:
            new_state = ED_REV
        elif action == WITHDRAW:
            new_state = WITHDRAWN
    elif curr_state == ED_REV:
        if action == ACCEPT:
            new_state = COPY_EDIT
        elif action == WITHDRAW:
            new_state = WITHDRAWN
    elif curr_state == COPY_EDIT:
        if action == DONE:
            new_state = AU_REVIEW
        elif action == WITHDRAW:
            new_state = WITHDRAWN
    elif curr_state == AU_REVIEW:
        if action == DONE:
            new_state = FORMATTING
        elif action == WITHDRAW:
            new_state = WITHDRAWN
    elif curr_state == FORMATTING:
        if action == DONE:
            new_state = PUBLISHED
        elif action == WITHDRAW:
            new_state = WITHDRAWN
    return new_state
