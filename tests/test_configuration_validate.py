"""
pytest tests for the Configuration __post_init__() method.
"""

from contextlib import nullcontext as does_not_raise

import pytest

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


@pytest.mark.parametrize("hdl_type", HDLType)
@pytest.mark.parametrize("fsm_type", FSMType)
@pytest.mark.parametrize("encoding", StateEncodingType)
@pytest.mark.parametrize("default_state_type", DefaultStateType)
@pytest.mark.parametrize("reset_type", ResetType)
@pytest.mark.parametrize("reset_active_level", ResetActiveLevel)
@pytest.mark.parametrize("coding_structure", CodingStructure)
@pytest.mark.parametrize(
    "combinatorial_sensitivity_mode", CombinatorialSensitivityMode
)
@pytest.mark.parametrize("output_handling_method", OutputHandlingMethod)
def test_configuration_validate(
    hdl_type: HDLType,
    fsm_type: FSMType,
    encoding: StateEncodingType,
    default_state_type: DefaultStateType,
    reset_type: ResetType,
    reset_active_level: ResetActiveLevel,
    coding_structure: CodingStructure,
    combinatorial_sensitivity_mode: CombinatorialSensitivityMode,
    output_handling_method: OutputHandlingMethod,
) -> None:
    """
    Perform tests for `` __post_init__()`` method:
    - check whether exception is raised when configuration is not valid.
    """

    if (
        coding_structure == CodingStructure.ALL_IN_ONE
        and combinatorial_sensitivity_mode
        != CombinatorialSensitivityMode.INAPPLICABLE
    ) or (
        coding_structure != CodingStructure.ALL_IN_ONE
        and combinatorial_sensitivity_mode
        == CombinatorialSensitivityMode.INAPPLICABLE
    ):
        with pytest.raises(ValueError, match="invalid choice"):
            Configuration(
                hdl_type=hdl_type,
                fsm_type=fsm_type,
                encoding=encoding,
                default_state_type=default_state_type,
                reset_type=reset_type,
                reset_active_level=reset_active_level,
                coding_structure=coding_structure,
                combinatorial_structure=CombinatorialStructure.CASE_WITH_NESTED_IF_ELSE,
                combinatorial_sensitivity_mode=combinatorial_sensitivity_mode,
                output_handling_method=output_handling_method,
            )
    else:
        with does_not_raise():
            Configuration(
                hdl_type=hdl_type,
                fsm_type=fsm_type,
                encoding=encoding,
                default_state_type=default_state_type,
                reset_type=reset_type,
                reset_active_level=reset_active_level,
                coding_structure=coding_structure,
                combinatorial_structure=CombinatorialStructure.CASE_WITH_NESTED_IF_ELSE,
                combinatorial_sensitivity_mode=combinatorial_sensitivity_mode,
                output_handling_method=output_handling_method,
            )
