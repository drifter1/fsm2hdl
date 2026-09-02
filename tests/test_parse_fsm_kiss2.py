"""
pytest tests for the function parse_fsm_kiss2().
"""

from typing import TYPE_CHECKING

from fsm2hdl import parse_fsm_kiss2

if TYPE_CHECKING:
    from fsm2hdl import Fsm

INPUT_PATH = "tests/benchmarks/kiss2"


def test_parse_fsm_kiss2(file_name: str):
    """
    Perform tests for ``parse_fsm_kiss2()``:
    - check whether it returns an FSM object
    """

    fsm: Fsm = parse_fsm_kiss2(INPUT_PATH, file_name)
    assert fsm is not None
