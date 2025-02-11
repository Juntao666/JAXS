import data.manus.fields as mflds

from unittest.mock import patch


def test_get_flds():
    assert isinstance(mflds.get_flds(), dict)


def test_get_fld_names():
    assert isinstance(mflds.get_fld_names(), list)


def test_get_referees():
    assert isinstance(mflds.get_referees(), dict)


def test_get_history():
    assert isinstance(mflds.get_history(), list)


@patch('data.manus.fields.get_history', autospec=True, return_value=['SUB', 'REJ'])
def test_is_valid_history(mock_get_history):
    history = mock_get_history()
    for state in history:
        assert mflds.is_valid_state(state), f"Invalid state {state} in history."


@patch('data.manus.fields.get_history', autospec=True, return_value=['INVALID_STATE'])
def test_is_invalid_history(mock_get_history):
    history = mock_get_history()
    for state in history:
        assert not mflds.is_valid_state(state), f"Valid state {state} in history."


@patch('data.manus.fields.get_referees', autospec=True, return_value={
    'referee1': ['ACC'],
    'referee2': ['AWR'],
    'referee3': ['REJ'],
})
def test_is_valid_referee_verdicts(mock_get_referees):
    referees = mock_get_referees()
    for referee_id, verdicts in referees.items():
        for verdict in verdicts:
            assert mflds.is_valid_verdict(verdict), f"Invalid verdict {verdict} for referee {referee_id}."


@patch('data.manus.fields.get_referees', autospec=True, return_value={
    'referee4': ['INVALID_VERDICT'],
})
def test_is_invalid_referee_verdicts(mock_get_referees):
    referees = mock_get_referees()
    for referee_id, verdicts in referees.items():
        for verdict in verdicts:
            assert not mflds.is_valid_verdict(verdict), f"Valid verdict {verdict} for referee {referee_id}."


@patch('data.manus.fields.get_disp_name', autospec=True,
       return_value="Display_name")
def test_get_disp_name(mock_read):
    result = mflds.get_disp_name("title")
    assert isinstance(result, str)


@patch('data.manus.fields.get_disp_name', autospec=True, return_value=None)
def test_get_disp_name_not_exist(mock_read):
    result = mflds.get_disp_name("non_existent")
    assert result is None, "Expected None for non-existent field name."

