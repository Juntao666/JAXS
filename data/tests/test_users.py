import data.users as usrs


def test_get_users():
    users = usrs.get_users()
    assert isinstance(users, dict)
    assert len(users) > 0  # at least one user :)
    for key in users:
        assert isinstance(key, str)
        assert len(key) >= usrs.MIN_USER_NAME_LEN
        user = users[key]
        assert isinstance(user, dict)
        assert usrs.LEVEL in user
        assert isinstance(user[usrs.LEVEL], int)


def test_read_one():
    existing_user = "Callahan"
    user = usrs.read_one(existing_user)
    assert isinstance(user, dict)
    assert usrs.USERNAME in user
    assert user[usrs.USERNAME] == existing_user
    assert usrs.LEVEL in user
    assert isinstance(user[usrs.LEVEL], int)
    assert usrs.PASSWORD in user


def test_pass_is_valid():
    valid_user = "Callahan"
    valid_password = "123abc"
    assert usrs.pass_is_valid(valid_user, valid_password) is True


def test_create():
    new_user = "TestUser"
    new_password = "test_password"
    new_level = 1

    existing_user = usrs.read_one(new_user)
    if existing_user:
        usrs.delete_user(new_user)  # Delete the user if it exists

    created_user = usrs.create(new_user, new_password, new_level)
    assert created_user == new_user

    user = usrs.read_one(new_user)
    assert user is not None
    assert user[usrs.USERNAME] == new_user
    assert user[usrs.LEVEL] == new_level


def test_delete_user():
    user_to_delete = "TestUser"

    existing_user = usrs.read_one(user_to_delete)
    if existing_user:
        assert usrs.delete_user(user_to_delete) is True
        deleted_user = usrs.read_one(user_to_delete)
        assert deleted_user is None
    else:
        assert usrs.delete_user(user_to_delete) is False
