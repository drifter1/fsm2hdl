"""
pytest tests for the function generate_verilog().
"""

from typing import TYPE_CHECKING

from fsm2hdl.common.parameters import FSMType
from fsm2hdl.common.utils import (
    mealy_to_moore_conversion,
    simple_moore_to_mealy_conversion,
)
from fsm2hdl.serialization import load_fsm_pickle

if TYPE_CHECKING:
    from fsm2hdl.common.models import Fsm

INPUT_PATH = "tests/benchmarks/pkl"


def test_mealy_moore_conversion(file_name):
    """
    Perform tests for the following functions:
    - ``mealy_to_moore_conversion()``
    - ``simple_moore_to_mealy_conversion()``
    Check whether they returns an FSM object.
    """

    fsm: Fsm = load_fsm_pickle(INPUT_PATH, file_name)

    fsm_moore: Fsm = mealy_to_moore_conversion(fsm)
    fsm_mealy: Fsm = simple_moore_to_mealy_conversion(fsm)

    assert fsm_moore.fsm_type == FSMType.MOORE
    assert fsm_mealy.fsm_type == FSMType.MEALY
