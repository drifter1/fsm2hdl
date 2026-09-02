"""
pytest tests for the function load_fsm_json().
"""

from typing import TYPE_CHECKING

from fsm2hdl import load_fsm_json

if TYPE_CHECKING:
    from fsm2hdl import Fsm

INPUT_PATH = "tests/benchmarks/json"


def test_load_fsm_json(file_name: str):
    """
    Perform tests for ``load_fsm_json()``:
    - check whether it returns an FSM object
    """
    fsm: Fsm = load_fsm_json(INPUT_PATH, file_name)
    assert fsm is not None
