"""
This module specifies functions related to states.
"""

import math

from fsm2hdl.common.parameters import (
    DefaultStateType,
    HDLType,
    StateEncodingType,
)


def calculate_encoding_bit_requirements(
    state_count: int,
    *,
    encoding: StateEncodingType,
    default_state_type: DefaultStateType,
) -> int:
    """
    Calculate the bit requirements for state encoding.

    Parameters
    ----------
    state_count : int
        The number of states.
    encoding : ``StateEncodingType``
        The encoding scheme used for FSM states.
    default_state_type : ``DefaultStateType``
        Specifies behavior upon encountering an undefined state.

    Returns
    -------
    int
        The bits required for the encoding.
    """
    state_bits: int

    # bits = ⌈log2(⌈state_count)⌉
    if encoding in [
        StateEncodingType.BINARY,
        StateEncodingType.GRAY,
    ]:
        if default_state_type == DefaultStateType.REGULAR:
            state_bits = math.ceil(math.log2(state_count))

        elif default_state_type == DefaultStateType.FALLBACK:
            state_bits = math.ceil(math.log2(state_count + 1))

    # bits = ⌈state_count
    elif encoding == StateEncodingType.ONEHOT:
        state_bits = state_count

    # bits = ⌈state_count/2⌉
    elif encoding == StateEncodingType.JOHNSON:
        if default_state_type == DefaultStateType.REGULAR:
            state_bits = math.ceil(state_count / 2)

        elif default_state_type == DefaultStateType.FALLBACK:
            state_bits = math.ceil((state_count + 1) / 2)

    return state_bits


def initial_state_value(
    *, encoding: StateEncodingType, default_state_type: DefaultStateType
) -> int:
    """
    Determine the initial state value.

    Parameters
    ----------
    encoding : ``StateEncodingType``
        The encoding scheme used for FSM states.
    default_state_type : ``DefaultStateType``
        Specifies behavior upon encountering an undefined state.

    Returns
    -------
    int
        The initial state value.
    """
    state_value: int

    if encoding in [
        StateEncodingType.BINARY,
        StateEncodingType.GRAY,
    ]:
        if default_state_type == DefaultStateType.REGULAR:
            state_value = 0

        elif default_state_type == DefaultStateType.FALLBACK:
            state_value = 1

    elif encoding == StateEncodingType.ONEHOT:
        state_value = 1

    # handled in precalculate_state_values instead
    elif encoding == StateEncodingType.JOHNSON:
        state_value = 0

    return state_value


def precalculate_state_values(
    state_bits,
    state_count,
    *,
    encoding: StateEncodingType,
    default_state_type: DefaultStateType,
) -> list[int]:
    """
    Precalculate the state values.

    Parameters
    ----------
    state_bits : int
        The bits required for the encoding.
    state_count : int
        The number of states.
    encoding : ``StateEncodingType``
        The encoding scheme used for FSM states.
    default_state_type : ``DefaultStateType``
        Specifies behavior upon encountering an undefined state.

    Returns
    -------
    list[int]
        The precalculated state values.
    """

    state_values: list[int] = []

    init_state_value: int = initial_state_value(
        encoding=encoding, default_state_type=default_state_type
    )

    if encoding == StateEncodingType.BINARY:
        state_values = [init_state_value + i for i in range(state_count)]

    elif encoding == StateEncodingType.ONEHOT:
        state_values = [init_state_value << i for i in range(state_count)]

    elif encoding == StateEncodingType.GRAY:
        state_values = [
            i ^ (i >> 1)
            for i in range(init_state_value, state_count + init_state_value)
        ]

    elif encoding == StateEncodingType.JOHNSON:
        state = tuple(format(init_state_value, "0" + str(state_bits) + "b"))

        if default_state_type == DefaultStateType.FALLBACK:
            state = [str(1 - int(state[-1])), *state[:-1]]

        sequence = [tuple(state)]
        for _ in range(state_count):
            state = [str(1 - int(state[-1])), *state[:-1]]
            sequence.append(tuple(state))
        sequence = ["".join(state_value) for state_value in sequence]

        state_values = [int(state_value, 2) for state_value in sequence]

    return state_values


def determine_default_state_value(
    start_state,
    state_bits,
    *,
    hdl_type: HDLType,
    default_state_type: DefaultStateType,
) -> str:
    """
    Determines the default state value.

    start_state : str
        The start state of the FSM.
    state_bits : int
        The bits required for the encoding.
    hdl_type : ``HDLType``
        The target HDL language for the generated code.
    default_state_type : ``DefaultStateType``
        Specifies behavior upon encountering an undefined state.

    Returns
    -------
    str
        The default state value.
    """

    if (
        default_state_type == DefaultStateType.FALLBACK
        and hdl_type == HDLType.VERILOG
    ):
        return "0"
    if (
        default_state_type == DefaultStateType.FALLBACK
        and hdl_type == HDLType.VHDL
    ):
        return '"' + format(0, "0" + str(state_bits) + "b") + '"'

    # DefaultStateType.REGULAR
    return start_state
