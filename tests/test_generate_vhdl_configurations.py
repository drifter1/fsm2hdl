"""
pytest tests for the function generate_vhdl().
"""

import os
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from fsm2hdl.code_gen import generate_vhdl
from fsm2hdl.common import Configuration
from fsm2hdl.common.parameters import (
    CodingStructure,
    CombinatorialSensitivityMode,
    CombinatorialStructure,
    DefaultStateType,
    FSMType,
    HDLType,
    OutputHandlingMethod,
    ResetActiveLevel,
    ResetType,
    StateEncodingType,
)
from fsm2hdl.serialization import load_fsm_pickle

if TYPE_CHECKING:
    from fsm2hdl.common.models import Fsm

INPUT_PATH = "tests/benchmarks/pkl"


@pytest.mark.parametrize("fsm_type", [FSMType.MOORE, FSMType.MEALY])
@pytest.mark.parametrize("encoding", StateEncodingType)
@pytest.mark.parametrize("default_state_type", DefaultStateType)
@pytest.mark.parametrize("reset_type", ResetType)
@pytest.mark.parametrize("reset_active_level", ResetActiveLevel)
@pytest.mark.parametrize(
    ("coding_structure", "combinatorial_sensitivity_mode"),
    [
        (CodingStructure.SEPARATE_ALL, CombinatorialSensitivityMode.IMPLICIT),
        (CodingStructure.SEPARATE_ALL, CombinatorialSensitivityMode.EXPLICIT),
        (
            CodingStructure.SEPARATE_COMB_AND_SEQ,
            CombinatorialSensitivityMode.IMPLICIT,
        ),
        (
            CodingStructure.SEPARATE_COMB_AND_SEQ,
            CombinatorialSensitivityMode.EXPLICIT,
        ),
        (
            CodingStructure.ALL_IN_ONE,
            CombinatorialSensitivityMode.INAPPLICABLE,
        ),
    ],
)
@pytest.mark.parametrize("combinatorial_structure", CombinatorialStructure)
@pytest.mark.parametrize("output_handling_method", OutputHandlingMethod)
def test_generate_vhdl_configurations(
    file_name: str,
    tmp_path: Path,
    fsm_type: FSMType,
    encoding: StateEncodingType,
    default_state_type: DefaultStateType,
    reset_type: ResetType,
    reset_active_level: ResetActiveLevel,
    coding_structure: CodingStructure,
    combinatorial_structure: CombinatorialStructure,
    combinatorial_sensitivity_mode: CombinatorialSensitivityMode,
    output_handling_method: OutputHandlingMethod,
) -> None:
    """
    Test whether all possible configurations for ``generate_vhdl()`` yield output file.
    """
    fsm: Fsm = load_fsm_pickle(INPUT_PATH, file_name)

    cfg: Configuration = Configuration(
        hdl_type=HDLType.VHDL,
        fsm_type=fsm_type,
        encoding=encoding,
        default_state_type=default_state_type,
        reset_type=reset_type,
        reset_active_level=reset_active_level,
        coding_structure=coding_structure,
        combinatorial_structure=combinatorial_structure,
        combinatorial_sensitivity_mode=combinatorial_sensitivity_mode,
        output_handling_method=output_handling_method,
    )

    output_file_name: str = fsm.name

    if output_file_name[-1].isdigit():
        output_file_name += "_"

    output_file_name += str(cfg)

    fsm.name = output_file_name

    generate_vhdl(fsm, tmp_path.as_posix(), cfg)

    assert os.path.isfile(
        tmp_path.as_posix() + "/" + output_file_name + ".vhd"
    )
