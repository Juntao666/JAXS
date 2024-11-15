import data.manuscripts.fields as mflds

from unittest.mock import patch


def test_get_flds():
    assert isinstance(mflds.get_flds(), dict)


def test_get_fld_names():
    assert isinstance(mflds.get_fld_names(), list)


def test_get_referees():
    assert isinstance(mflds.get_referees(), dict)


def test_get_history():
    assert isinstance(mflds.get_history(), list)


@patch('data.manuscripts.fields.get_disp_name', autospec=True,
       return_value="Display_name")
def test_get_disp_name(mock_read):
    result = mflds.get_disp_name("title")
    assert isinstance(result, str)


@patch('data.manuscripts.fields.get_disp_name', autospec=True,
       return_value=None)
def test_get_disp_name_not_exist(mock_read):
    result = mflds.get_disp_name("none_existant")
    assert result is None
