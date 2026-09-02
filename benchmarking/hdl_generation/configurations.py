from fsm2hdl import (
    CodingStructure,
    CombinatorialSensitivityMode,
    CombinatorialStructure,
    Configuration,
    DefaultStateType,
    FSMType,
    HDLType,
    OutputHandlingMethod,
    ResetActiveLevel,
    ResetType,
    StateEncodingType,
)

VALID_CS_CSM_PAIRS = [
    (
        CodingStructure.SEPARATE_ALL,
        CombinatorialSensitivityMode.IMPLICIT,
    ),
    (
        CodingStructure.SEPARATE_ALL,
        CombinatorialSensitivityMode.EXPLICIT,
    ),
    (
        CodingStructure.SEPARATE_COMB_OUT,
        CombinatorialSensitivityMode.IMPLICIT,
    ),
    (
        CodingStructure.SEPARATE_COMB_OUT,
        CombinatorialSensitivityMode.EXPLICIT,
    ),
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
]


VALID_CONFIGURATIONS = [
    Configuration(
        hdl_type=hdl_type,
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
    for hdl_type in HDLType
    for fsm_type in [FSMType.MOORE, FSMType.MEALY]
    for encoding in StateEncodingType
    for default_state_type in DefaultStateType
    for reset_type in ResetType
    for reset_active_level in ResetActiveLevel
    for coding_structure, combinatorial_sensitivity_mode in VALID_CS_CSM_PAIRS
    for (combinatorial_structure) in CombinatorialStructure
    for (output_handling_method) in OutputHandlingMethod
]
