"""
pytest tests for the function load_fsm_pickle().
"""

import pytest

from fsm2hdl.serialization import load_fsm_pickle

INPUT_PATH = ""
FILE_NAME = "invalid"


def test_load_fsm_pickle_invalid():
    """
    Perform tests for ``load_fsm_pickle()``:
    - check whether exception is raised when file doesn't exist.
    """

    with pytest.raises(FileNotFoundError):
        load_fsm_pickle(INPUT_PATH, FILE_NAME)
