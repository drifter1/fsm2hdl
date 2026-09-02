"""
This module provides helpers that format the state parameters.
"""

from collections.abc import Iterator


def format_state_parameters(
    state_bits: int, state_values: list[int]
) -> list[str]:
    """
    Formats the state values as Verilog parameters.

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

    state_parameters: list[str] = [
        format(state_value, "0" + str(state_bits) + "b")
        for state_value in state_values
    ]

    return state_parameters


def prepare_state_parameter_pair(
    state_bits: int, state_values: list[int], state_names
) -> Iterator[tuple[str, str]]:
    """
    Prepare state parameter pair for use in jinja2 template.

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

    state_parameters: list[str] = format_state_parameters(
        state_bits, state_values
    )

    return zip(state_names, state_parameters, strict=False)
