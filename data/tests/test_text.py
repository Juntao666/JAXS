import data.text as txt


def test_read():
    texts = txt.read()
    assert isinstance(texts, dict)
    for key in texts:
        assert isinstance(key, str)


def test_read_one():
    assert len(txt.read_one(txt.TEST_KEY)) > 0


def test_read_one_not_found():
    assert txt.read_one('Not a page key!') == {}


TITLE = 'title'
TEXT = 'text'
TEST_KEY_DATA = {
        TITLE: 'Home Page',
        TEXT: 'This is a journal about building API servers.',
    }
NEW_TEXT = "NEW TEXT"
NEW_TITLE = "NEW TITLE"

def test_update():
    assert txt.read_one(txt.TEST_KEY) == TEST_KEY_DATA
    response = txt.update(txt.TEST_KEY, NEW_TITLE, NEW_TEXT)
    assert response
    assert txt.read_one(txt.TEST_KEY) != TEST_KEY_DATA


NONE_EXISTENT_KEY = "NOT EXIST"

def test_update_none_existent():
    response = txt.update(NONE_EXISTENT_KEY, "N/A", "N/A")
    assert response
    assert txt.read_one(NONE_EXISTENT_KEY) == {}
