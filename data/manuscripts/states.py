"""
This module is attempt for state changes.
"""

# state fields
SUBMITTED = 'submitted'
REFEREE_REVIEW = 'referee_review'
AUTHOR_REVISIONS = 'author_revisions'
EDITOR_REVIEW = 'editor_review'
COPY_EDIT = 'copy_edit'
AUTHOR_REVIEW = 'author_review'
FORMATTING = 'formatting'
PUBLISHED = 'published'
REJECTED = 'rejected'
WITHDRAWN = 'withdrawn'

# testing purposes
TEST_CURR_STATE = SUBMITTED
TEST_NEXT_STATE = REFEREE_REVIEW

# possible state changes (not sure if best way to implement)
STATE_CHANGES = {
    SUBMITTED: [REFEREE_REVIEW, REJECTED, WITHDRAWN],
    REFEREE_REVIEW: [AUTHOR_REVISIONS, COPY_EDIT, REJECTED, WITHDRAWN, SUBMITTED],
    AUTHOR_REVISIONS: [EDITOR_REVIEW, WITHDRAWN],
    EDITOR_REVIEW: [COPY_EDIT, WITHDRAWN],
    COPY_EDIT: [AUTHOR_REVIEW, WITHDRAWN],
    AUTHOR_REVIEW: [FORMATTING, WITHDRAWN],
    FORMATTING: [PUBLISHED, WITHDRAWN],
    PUBLISHED: [],
    REJECTED: [],
    WITHDRAWN: [],
}


def get_next_state(curr_state: str) -> list:
    if curr_state not in STATE_CHANGES:
        raise ValueError(f"Invalid state: {curr_state}")
    return STATE_CHANGES[curr_state]


def is_valid_state_change(curr_state: str, next_state: str) -> bool:
    return next_state in get_next_state(curr_state)