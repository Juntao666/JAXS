# fields

TITLE = 'title'
DISP_NAME = 'disp_name'
AUTHOR = 'author'
REFEREES = 'referees'
DISP_AUTHOR = 'disp_author'
AUTHOR_EMAIL = 'author@domain.com'
DISP_AUTHOR_EMAIL = 'disp_author_email'
STATE = 'state'  # STR
DISP_STATE = 'disp_state'
VAL_STATE = 'val_state'
DISP_VAL_STATE = 'disp_val_state'
TEXT = 'text'
DISP_TEXT = 'disp_text'
ABSTRACT = 'abstract'
DISP_ABSTRACT = 'disp_abstract'
EDITOR = 'editor'
DISP_EDITOR = 'disp_editor'


TEST_FLD_NM = TITLE
TEST_FLD_DISP_NM = 'Title'
TEST_FLD_AU = AUTHOR
TEST_FLD_DISP_AU = 'Author'
TEST_FLD_AU_EM = AUTHOR_EMAIL
TEST_FLD_DISP_AU_EM = 'AuthorEmail@domain.com'
TEST_FLD_ST = STATE
TEST_FLD_DISP_ST = 'State'
TEST_FLD_VAL_ST = VAL_STATE
TEST_FLD_TXT = TEXT
TEST_FLD_DISP_TXT = 'Text'
TEST_FLD_ABS = ABSTRACT
TEST_FLD_DISP_ABS = 'Abstract'
TEST_FLD_ED = EDITOR
TEST_FLD_DISP_ED = 'Editor'


REFEREE = 'referee'
DISP_REF = 'disp_referee'
REFEREE_ID = 'referee@domain.com'
REPORT = 'report'
VERDICT = 'verdict'  # 'ACCEPT', 'ACCEPT_W_REV', or 'REJECT'
referee_dict = {
    REFEREE_ID: {
        REPORT,
        VERDICT,
    },
}

TEST_FLD_REF = REFEREE
TEST_FLD_DISP_REF = referee_dict


HISTORY = 'history'
DISP_HIS = 'disp_history'
history_list = [STATE,]

TEST_FLD_HIS = HISTORY
TEST_FLD_DISP_HIS = history_list

FIELDS = {
    TITLE: {
        DISP_NAME: TEST_FLD_DISP_NM,
    },
    AUTHOR: {
        DISP_AUTHOR: TEST_FLD_DISP_AU,
    },
    AUTHOR_EMAIL: {
        DISP_AUTHOR_EMAIL: TEST_FLD_DISP_AU_EM,
    },
    STATE: {
        DISP_STATE: TEST_FLD_DISP_ST,
        DISP_VAL_STATE: TEST_FLD_VAL_ST,
    },
    TEXT: {
        DISP_TEXT: TEST_FLD_DISP_TXT,
    },
    ABSTRACT: {
        DISP_ABSTRACT: TEST_FLD_DISP_ABS,
    },
    EDITOR: {
        DISP_EDITOR: TEST_FLD_DISP_ED,
    },
    REFEREE: {
        DISP_REF: TEST_FLD_DISP_REF,
    },
    HISTORY: {
        DISP_HIS: TEST_FLD_DISP_HIS,
    },
}


def get_flds() -> dict:
    return FIELDS


def get_fld_names() -> list:
    return list(FIELDS.keys())


def get_disp_name(fld_nm: str) -> dict:
    fld = FIELDS.get(fld_nm, '')
    return fld[DISP_NAME]  # should we use get() here?


def get_history() -> list:
    return history_list


def get_referees() -> dict:
    return referee_dict


def is_valid_state(state: str) -> bool:
    import data.manuscripts.query as qry

    valid_states = qry.VALID_STATES
    if state in valid_states:
        return True
    else:
        return False


def is_valid_verdict(verdict: str) -> bool:
    import data.manuscripts.query as qry

    valid_verdicts = qry.REF_VERDICT
    if verdict in valid_verdicts:
        return True
    else:
        return False


def get_disp_name(fld_nm: str) -> str:
    fld = FIELDS.get(fld_nm)
    if fld is None:
        import logging
        logging.warning(f"Field name {fld_nm} does not exist in FIELDS.")
        return None
    return fld.get(DISP_NAME, "Unknown")


def main():
    print(f'{get_flds()=}')
    missing_fields = validate_field_names()
    if missing_fields:
        print(f"Missing DISP_NAME fields: {missing_fields}")
    else:
        print("All fields are valid.")


if __name__ == '__main__':
    main()
