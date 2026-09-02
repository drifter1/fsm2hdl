"""
This module specifies the kiss2 parser.
"""

from typing import TYPE_CHECKING

from fsm2hdl.common.models import Fsm, State, Transition
from fsm2hdl.common.utils import open_file

from .helpers import (
    extract_line_info,
    process_raw_transition_inputs,
    process_raw_transition_outputs,
    set_transition_identifiers,
)

if TYPE_CHECKING:
    from fsm2hdl.common.models import Input

TRANSITION_PARTS: int = 4
STATE_NAME_START = "a"
TRANSITION_ID_TEMP: int = 0


def parse_fsm_kiss2(directory_name: str, file_name: str) -> Fsm:
    """
    Parses an FSM from a file formatted in kiss2 truth table format.

    Parameters
    ----------
    directory_name : str
        Path of the directory that contains the file with .kiss2 extension.
        If an empty string, the current working directory is used.
    file_name : str
        Base name of the file (without extension).

    Returns
    -------
    Fsm
        A new Fsm instance constructred from the parsed truth table.
    """

    file = open_file(directory_name, file_name, ".kiss2", "r")

    # states dictionary
    states: dict[str, State] = {}

    # state names list
    state_names: list[str] = []

    for line in file:
        # split line
        parts: list[str] = line.split()

        # whitespace or header information
        if len(parts) < TRANSITION_PARTS:
            continue

        # extract line info
        # state_source state_target inputs outputs
        line_info: tuple[str, str, list[str], list[str]]
        line_info = extract_line_info(parts)

        # keep track of original state names
        if line_info[0] not in state_names:
            state_names.append(line_info[0])  # state_source

        if line_info[1] not in state_names:
            state_names.append(line_info[1])  # state_target

        # prepare new state names
        state_source: str = STATE_NAME_START + str(
            state_names.index(line_info[0]) + 1  # state_source
        )
        state_target: str = STATE_NAME_START + str(
            state_names.index(line_info[1]) + 1  # state_target
        )

        # if source is new state create a dictionary entry
        if state_source not in states:
            states[state_source] = State(state_source)

        # process raw transition inputs
        transition_inputs: list[Input]
        transition_inputs = process_raw_transition_inputs(
            line_info[2],  # raw_inputs
        )

        # process raw transition outputs
        transition_outputs: list[str]
        transition_outputs = process_raw_transition_outputs(
            line_info[3],  # raw_outputs
        )

        # create new transition
        transition: Transition = Transition(
            TRANSITION_ID_TEMP,
            state_source,
            state_target,
            transition_inputs,
            transition_outputs,
        )

        # add transition to state
        states[state_source].transitions.append(transition)

    # sort dictionary
    states = dict(sorted(states.items(), key=lambda x: int(x[0][1:])))

    set_transition_identifiers(states)

    # close file
    file.close()

    # specify FSM name
    name = file_name

    # create FSM object
    fsm: Fsm = Fsm(name, states)

    return fsm
