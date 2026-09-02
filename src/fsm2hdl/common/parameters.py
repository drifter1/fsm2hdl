"""
This module bundles the configuration options that influence
the generation of the HDL code from an FSM description.
"""

from enum import Enum


class HDLType(Enum):
    """
    This enum is used to specify the target HDL language for the generated code.
    """

    VERILOG = 1
    VHDL = 2

    def __str__(self):
        return self.name


class FSMType(Enum):
    """
    This enum represents the behavioral (or type) model of the FSM.
    """

    INFERRED = 0
    MOORE = 1
    MEALY = 2

    def __str__(self):
        return self.name


class StateEncodingType(Enum):
    """
    This enum represents the encoding scheme used for FSM states.
    """

    ONEHOT = 1
    BINARY = 2
    GRAY = 3
    JOHNSON = 4

    def __str__(self):
        return self.name


class DefaultStateType(Enum):
    """
    This enum is used to specify behavior upon encountering an undefined state.
    """

    REGULAR = 1
    FALLBACK = 2

    def __str__(self):
        return self.name


class ResetType(Enum):
    """
    This enum represents how the reset signal is sampled.
    """

    SYNC = 1
    ASYNC = 2

    def __str__(self):
        return self.name


class ResetActiveLevel(Enum):
    """
    This enum represents the active level of the reset input.
    """

    ACTIVE_LOW = 1
    ACTIVE_HIGH = 2

    def __str__(self):
        return self.name


class CodingStructure(Enum):
    """
    This enum represents the overall organization of the generated HDL.
    """

    SEPARATE_ALL = 1
    SEPARATE_COMB_OUT = 2
    SEPARATE_COMB_AND_SEQ = 3
    ALL_IN_ONE = 4

    def __str__(self):
        return self.name


class CombinatorialStructure(Enum):
    """
    This enum represents the structural pattern that is used for implementing combinatorial logic.
    """

    CASE_WITH_NESTED_IF_ELSE = 1
    IF_ELSE_NESTED = 2

    def __str__(self):
        return self.name


class CombinatorialSensitivityMode(Enum):
    """
    This enum defines how the sensitivity list of a combinatorial block is specified.
    """

    INAPPLICABLE = 0
    IMPLICIT = 1
    EXPLICIT = 2

    def __str__(self):
        return self.name


class OutputHandlingMethod(Enum):
    """
    This enum specifies how the FSM outputs are initialized and updated relative to the state logic.
    """

    ALL_OUTPUTS_ZEROED_BEFORE_STATE_LOGIC = 1
    ALL_OUTPUTS_SET_FROM_STATE_LOGIC = 2

    def __str__(self):
        return self.name
