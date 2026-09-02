"""
This module specifies the kiss2 serializer.
"""

from fsm2hdl.common.models import Fsm, State, Transition
from fsm2hdl.common.utils import (
    open_file,
    simple_moore_to_mealy_conversion,
)

from .helpers import (
    find_max_state_name_length,
    prepare_output_line,
)


def serialize_fsm_kiss2(fsm: Fsm, directory_name: str, spacing: int = 1):
    """
    Serializes an FSM into a file formatted in kiss2 truth table format.

    Parameters
    ----------
    fsm : ``Fsm``
        The FSM to serialize into kiss2 format.
    directory_name : str
        Path of the directory that will contain the file.
        If an empty string, the current working directory is used.
    spacing: int, default=1
        The spacing between each distinct part of an output line.
    """

    file = open_file(directory_name, fsm.name, ".kiss2", "w")

    # convert FSM to Mealy
    fsm: Fsm = simple_moore_to_mealy_conversion(fsm)

    file.write(f"\n.i {len(fsm.inputs)}\n")
    file.write(f".o {len(fsm.outputs)}\n")
    file.write(
        f".p {sum(len(state.transitions) for state in fsm.states.values())}\n"
    )
    file.write(f".s {len(fsm.states)}\n")
    file.write(f".r {fsm.start_state}\n")

    max_state_name_length: int = find_max_state_name_length(fsm.states)

    # loop through all states
    state: State
    for state in fsm.states.values():
        # loop through all transitions
        transition: Transition
        for transition in state.transitions:
            line = prepare_output_line(
                transition,
                fsm.inputs,
                fsm.outputs,
                max_state_name_length,
                spacing,
            )

            file.write(line)

    file.write(".e\n")

    # close file
    file.close()
