"""
This module specifies helper functions for the kiss2 serializer.
"""

from fsm2hdl.common.models import Input, State, Transition


def format_inputs(
    transition_inputs: list[Input], fsm_inputs: list[str]
) -> str:
    """ """

    if len(transition_inputs) == 1 and transition_inputs[0].name == "1":
        return "-" * len(fsm_inputs)

    transition_inputs_string: str = ""

    fsm_input: str
    is_dont_care: bool
    for fsm_input in fsm_inputs:
        is_dont_care = True

        for transition_input in transition_inputs:
            if fsm_input == transition_input.name:
                is_dont_care = False
                if transition_input.inverted:
                    transition_inputs_string += "0"
                else:
                    transition_inputs_string += "1"

        if is_dont_care:
            transition_inputs_string += "-"

    return transition_inputs_string


def format_outputs(
    transition_outputs: list[str], fsm_outputs: list[str]
) -> str:
    """ """

    if len(transition_outputs) == 0:
        return "0" * len(fsm_outputs)

    transition_outputs_string: str = ""

    for fsm_output in fsm_outputs:
        if fsm_output in transition_outputs:
            transition_outputs_string += "1"
        else:
            transition_outputs_string += "0"

    return transition_outputs_string


def find_max_state_name_length(states: dict[str, State]) -> int:
    """ """

    state_name_len_max: int = 0

    # loop through all states
    state: State
    for state in states.values():
        state_name_len_max = max(state_name_len_max, len(state.name))

    return state_name_len_max


def whitespace_string(length: int, max_length: int, spacing: int):
    """ """

    return " " * (max_length - length + spacing)


def prepare_output_line(
    transition: Transition,
    fsm_inputs: list[str],
    fsm_outputs: list[str],
    max_state_name_length: int,
    spacing: int,
) -> str:
    """ """

    formatted_inputs: str = format_inputs(transition.inputs, fsm_inputs)
    formatted_outputs: str = format_outputs(transition.outputs, fsm_outputs)

    whitespace = " " * spacing

    return (
        formatted_inputs
        + whitespace
        + transition.state_source
        + whitespace_string(
            len(transition.state_source), max_state_name_length, spacing
        )
        + transition.state_target
        + whitespace_string(
            len(transition.state_target), max_state_name_length, spacing
        )
        + formatted_outputs
        + "\n"
    )
