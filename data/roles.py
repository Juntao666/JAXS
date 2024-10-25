"""
This module manages person roles for a journal.
"""
AUTHOR_CODE = 'AU'
TEST_CODE = AUTHOR_CODE

ROLES = {
    AUTHOR_CODE: 'Author',
    'ED': 'Editor',
    'RE': 'Referee',
}


def get_roles() -> dict:
    return ROLES

def get_masthead_roles() -> dict:
    mh_roles = get_roles()
    del_mh_roles = []
    for role in mh_roles:
        if role not in MH_ROLES:
            del_mh_roles.append(role)
    for del_role in del_mh_roles:
        del mh_roles[del_role]
    return mh_roles

def get_role_codes() -> list:
    return list(ROLES.keys())

def is_valid(code: str) -> bool:
    return code in ROLES


def main():
    print(get_roles())
    print(get_masthead_roles())


if __name__ == '__main__':
    main()
