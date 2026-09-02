"""
This module specifies helper functions for the kiss2 parser.
"""

from typing import TYPE_CHECKING

from fsm2hdl.common.models import Input, State

if TYPE_CHECKING:
    from fsm2hdl.common.models import Transition

INPUT_ID_START = "x"
OUTPUT_ID_START = "y"


def extract_line_info(
    parts: list[str],
) -> tuple[str, str, list[str], list[str]]:
    """
    Extracts the information of a single parsed input line into a tuple.

    Parameters
    ----------
    parts : list[str]
        A list created by splitting the parsed input line in string format.

    Returns
    -------
    state_source : str
        The state source.
    state_target : str
        The state target.
    raw_inputs : list[str]
        The transition inputs (raw format).
    outputs : list[str]
        The transition outputs (raw format)..
    """

    # line format: inputs state_source state_target outputs
    raw_inputs: list[str] = list(parts[0])
    state_source: str = parts[1]
    state_target: str = parts[2]
    raw_outputs: list[str] = list(parts[3])

    return state_source, state_target, raw_inputs, raw_outputs


def process_raw_transition_inputs(
    raw_inputs: list[str],
) -> list[Input]:
    """ """

    transition_inputs: list[Input] = []

    for index, transition_input in enumerate(raw_inputs):
        input_name = INPUT_ID_START + str(index + 1)

        # input is inverted
        if transition_input == "0":
            transition_inputs.append(Input(input_name, inverted=True))

        # input is not inverted
        elif transition_input == "1":
            transition_inputs.append(Input(input_name, inverted=False))

        # don't care input (-, x or X) is ignored

    if len(transition_inputs) == 0:
        transition_inputs.append(Input("1", inverted=False))

    return transition_inputs


def process_raw_transition_outputs(raw_outputs: list[str]) -> list[str]:
    """ """

    transition_outputs: list[str] = []

    for index, transition_output in enumerate(raw_outputs):
        output_name = OUTPUT_ID_START + str(index + 1)

        # add only active outputs
        if transition_output == "1":
            transition_outputs.append(output_name)

    return transition_outputs


def set_transition_identifiers(states: dict[str, State]):
    """ """

    transition_id: int = 1
    state: State
    for state in states.values():
        transition: Transition
        for transition in state.transitions:
            transition.transition_id = transition_id
            transition_id += 1
