"""
This module provides helpers that format the state constants.
"""

from collections.abc import Iterator


def format_state_constants(
    state_bits: int, state_values: list[int]
) -> list[str]:
    """
    Formats the state values as VHDL constants.

    Parameters
    ----------
    state_bits : int
        The bits required for the encoding.
    state_values :list[int]
        The state values.

    Returns
    -------
    list[str]
        The Verilog-formatted state parameters.
    """

    state_constants: list[str] = [
        format(state_value, "0" + str(state_bits) + "b")
        for state_value in state_values
    ]

    return state_constants


def prepare_state_constant_pair(
    state_bits: int, state_values: list[int], state_names
) -> Iterator[tuple[str, str]]:
    """
    Prepare state constant pair for use in jinja2 template.

    Parameters
    ----------
    state_bits : int
        The bits required for the encoding.
    state_values :list[int]
        The state values.
    state_names : list[str]
        The state names.

    Returns
    -------
    Iterator[tuple[list[str], list[str]]]
        An Iterator for use in jinja2 template.
    """

    state_constants: list[str] = format_state_constants(
        state_bits, state_values
    )

    return zip(state_names, state_constants, strict=False)
