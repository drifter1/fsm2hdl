"""
This module specifies the Configuration data-class.
"""

from dataclasses import dataclass

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


@dataclass
class Configuration:
    """
    A class used to represent a generator configuration.

    Attributes
    ----------
    hdl_type : ``HDLType``
        The target HDL language for the generated code.
        Default is ``HDLType.VERILOG``
    fsm_type : ``FSMType``
        The behavioral model (or type) of the FSM.
        Default is ``FSMType.INFERRED``.
    encoding : ``StateEncodingType``
        The encoding scheme used for FSM states.
        Default is ``StateEncodingType.ONEHOT``.
    default_state_type : ``DefaultStateType``
        Specifies behavior upon encountering an undefined state.
        Default is ``DefaultStateType.REGULAR``.
    reset_type : ``ResetType``
        Specifies how the reset signal is sampled.
        Default is ``ResetType.SYNC``.
    reset_active_level : ``ResetActiveLevel``
        Specifies the active level of the reset input.
        Default is ``ResetActiveLevel.ACTIVE_LOW``.
    coding_structure : ``CodingStructure``
        Defines the overall organization of the generated HDL.
        Default is ``CodingStructure.SEPARATE_ALL``.
    combinatorial_structure : ``CombinatorialStructure``
        Defines the structural pattern that is used for implementing combinatorial logic.
        Default is ``CombinatorialStructure.CASE_WITH_NESTED_IF_ELSE``.
    combinatorial_sensitivity_mode : ``CombinatorialSensitivityMode``
        Defines how the sensitivity list of a combinatorial block is specified.
        Default is ``CombinatorialSensitivityMode.IMPLICIT``.
    output_handling_method : ``OutputHandlingMethod``
        Specifies how the FSM outputs are initialized and updated relative to the state logic.
        Default is ``OutputHandlingMethod.ALL_OUTPUTS_ZEROED_BEFORE_STATE_LOGIC``.

    Notes
    -----
    ``CodingStructure.ALL_IN_ONE`` pairs only with
    ``CombinatorialSensitivityMode.INAPPLICABLE``, and vise versa.
    """

    hdl_type: HDLType = HDLType.VERILOG
    fsm_type: FSMType = FSMType.INFERRED
    encoding: StateEncodingType = StateEncodingType.ONEHOT
    default_state_type: DefaultStateType = DefaultStateType.REGULAR
    reset_type: ResetType = ResetType.SYNC
    reset_active_level: ResetActiveLevel = ResetActiveLevel.ACTIVE_LOW
    coding_structure: CodingStructure = CodingStructure.SEPARATE_ALL
    combinatorial_structure: CombinatorialStructure = (
        CombinatorialStructure.CASE_WITH_NESTED_IF_ELSE
    )
    combinatorial_sensitivity_mode: CombinatorialSensitivityMode = (
        CombinatorialSensitivityMode.IMPLICIT
    )
    output_handling_method: OutputHandlingMethod = (
        OutputHandlingMethod.ALL_OUTPUTS_ZEROED_BEFORE_STATE_LOGIC
    )

    def __post_init__(self):
        """
        Executes after all fields have been populated and validates the configuration parameters.

        Raises
        ------
        TypeError
            When the fields received wrong type arguments.
        ValueError
            When CodingStructure.ALL_IN_ONE is not paired with
            CombinatorialSensitivityMode.INAPPLICABLE, and vise versa.
        """

        # check for invalid argument types
        for field_name, field_def in self.__dataclass_fields__.items():
            actual_value = getattr(self, field_name)
            expected_type = field_def.type

            if not isinstance(actual_value, expected_type):
                error_message = f"invalid type: {field_name} expected {expected_type.__name__}, got {type(actual_value).__name__}"

                raise TypeError(error_message)

        # CodingStructure.ALL_IN_ONE but not CombinatorialSensitivityMode.INAPPLICABLE
        if (
            self.coding_structure == CodingStructure.ALL_IN_ONE
            and self.combinatorial_sensitivity_mode
            != CombinatorialSensitivityMode.INAPPLICABLE
        ):
            raise ValueError(
                None,
                "invalid choice: CodingStructure.ALL_IN_ONE pairs only with CombinatorialSensitivityMode.INAPPLICABLE",
            )

        # CombinatorialSensitivityMode.INAPPLICABLE but not CodingStructure.ALL_IN_ONE
        if (
            self.combinatorial_sensitivity_mode
            == CombinatorialSensitivityMode.INAPPLICABLE
            and self.coding_structure != CodingStructure.ALL_IN_ONE
        ):
            raise ValueError(
                None,
                "invalid choice: CombinatorialSensitivityMode.INAPPLICABLE pairs only with CodingStructure.ALL_IN_ONE",
            )

    def __str__(self):
        return (
            str(self.hdl_type.value)
            + str(self.fsm_type.value)
            + str(self.encoding.value)
            + str(self.default_state_type.value)
            + str(self.reset_type.value)
            + str(self.reset_active_level.value)
            + str(self.coding_structure.value)
            + str(self.combinatorial_structure.value)
            + str(self.combinatorial_sensitivity_mode.value)
            + str(self.output_handling_method.value)
        )


DEFAULT_CONFIGURATION: Configuration = Configuration()
