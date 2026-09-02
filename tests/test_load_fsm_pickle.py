"""
pytest tests for the function load_fsm_pickle().
"""

from typing import TYPE_CHECKING

from fsm2hdl.serialization import load_fsm_pickle

if TYPE_CHECKING:
    from fsm2hdl.common import Fsm

INPUT_PATH = "tests/benchmarks/pkl"


def test_load_fsm_pickle(file_name: str):
    """
    Perform tests for ``load_fsm_pickle()``:
    - check whether it returns an FSM object
    """
    fsm: Fsm = load_fsm_pickle(INPUT_PATH, file_name)
    assert fsm is not None
