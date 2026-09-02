"""
pytest tests for the function serialize_fsm_kiss2().
"""

import os
from pathlib import Path
from typing import TYPE_CHECKING

from fsm2hdl import load_fsm_pickle, serialize_fsm_kiss2

if TYPE_CHECKING:
    from fsm2hdl import Fsm

INPUT_PATH = "tests/benchmarks/pkl"


def test_serialize_fsm_kiss2(file_name: str, tmp_path: Path):
    """
    Perform tests for ``serialize_fsm_kiss2()``:
    - check whether it yields output file
    """

    fsm: Fsm = load_fsm_pickle(INPUT_PATH, file_name)
    serialize_fsm_kiss2(fsm, tmp_path.as_posix())
    output_file_name = tmp_path.as_posix() + "/" + file_name + ".kiss2"
    assert os.path.isfile(output_file_name)
