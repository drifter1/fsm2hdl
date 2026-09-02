"""
pytest tests for the function store_fsm_json().
"""

import os
from pathlib import Path
from typing import TYPE_CHECKING

from fsm2hdl.serialization import load_fsm_pickle, store_fsm_json

if TYPE_CHECKING:
    from fsm2hdl import Fsm

INPUT_PATH = "tests/benchmarks/pkl"


def test_store_fsm_json(file_name: str, tmp_path: Path):
    """
    Perform tests for ``store_fsm_json()``:
    - check whether it yields output file
    """

    fsm: Fsm = load_fsm_pickle(INPUT_PATH, file_name)
    store_fsm_json(fsm, tmp_path.as_posix())
    output_file_name = tmp_path.as_posix() + "/" + file_name + ".json"
    assert os.path.isfile(output_file_name)
