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
HISTORY = 'history'
DISP_HISTORY = 'disp_hsitory'
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
TEST_FLD_HIS = HISTORY
TEST_FLD_DISP_HIS = 'History'
TEST_FLD_ED = EDITOR
TEST_FLD_DISP_ED = 'Editor'


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
    HISTORY: {
        DISP_HISTORY: TEST_FLD_DISP_HIS,
    },
    EDITOR: {
        DISP_EDITOR: TEST_FLD_DISP_ED,
    }
}


def get_flds() -> dict:
    return FIELDS


def get_fld_names() -> list:
    return list(FIELDS.keys())


def get_disp_name(fld_nm: str) -> dict:
    fld = FIELDS.get(fld_nm, '')
    return fld[DISP_NAME]  # should we use get() here?


def main():
    print(f'{get_flds()=}')


if __name__ == '__main__':
    main()
