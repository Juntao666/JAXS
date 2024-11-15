# fields

TITLE = 'title'
DISP_NAME = 'disp_name'
AUTHOR = 'author'
DISP_AUTHOR = 'disp_author'
AUTHOR_EMAIL = 'author@domain.com'
DISP_AUTHOR_EMAIL = 'disp_author_email'
STATE = 'state'  # (INT or STR)
DISP_STATE = 'disp_state'
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
        DISP_REF: TEST_FLD_DISP_REF
    },
    HISTORY: {
        DISP_HIS: TEST_FLD_DISP_HIS
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


def main():
    print(f'{get_flds()=}')


if __name__ == '__main__':
    main()
