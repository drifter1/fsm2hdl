"""
This module specifies helper functions for the FSM data-class.
"""

from .input import Input
from .state import State
from .transition import Transition


def determine_missing_source_state(states: dict[str, State]) -> str | None:
    """
    Determines missing source state by checking the transition targets.

    Parameters
    ----------
    states: dict[str, State]
        The FSM states

    Returns
    -------
    str or None
        The missing source state, or None if no state is missing.
    """

    # loop through all states
    state: State
    for state in states.values():
        # loop through all transitions
        transition: Transition
        for transition in state.transitions:
            # check if state target is not included in the states dictionary
            if transition.state_target not in states:
                return transition.state_target

    # no missing state identified
    return None


def add_missing_source_states(states: dict[str, State]):
    """
    Iteratively adds missing source states.

    Parameters
    ----------
    states: dict[str, State]
        The FSM states
    """

    # calculate transition count
    transition_count: int = sum(
        len(state.transitions) for state in states.values()
    )

    # last transition identifier equals the transition count
    transition_id: int = transition_count

    # infinite loop that terminates when no state is missing
    while True:
        # identifiy missing state
        missing_state: str | None = determine_missing_source_state(states)

        # no state is missing, therefore terminate loop
        if missing_state is None:
            break

        # add missing state to states dictionary
        states[missing_state] = State(missing_state)

        # increment transition identifier
        transition_id += 1

        # create new don't care input
        transition_input: Input = Input("1", inverted=False)

        # create new transition from/to missing state
        transition: Transition = Transition(
            transition_id,
            missing_state,
            missing_state,
            [transition_input],  # don't care input
            [],  # no outputs
        )

        # add transition to state
        states[missing_state].transitions.append(transition)


def identify_unique_io(
    states: dict[str, State],
) -> tuple[list[str], list[str]]:
    """
    Identifies the unique FSM inputs and outputs.

    Parameters
    ----------
    states: dict[str, State]
        The FSM states

    Returns
    -------
    inputs : list[str]
        The unique inputs.
    outputs : list[str]
        The unique outputs.
    """

    inputs: list[str] = []
    outputs: list[str] = []

    # loop through all states to find unique inputs and outputs
    state: State
    for state in states.values():
        transition: Transition
        for transition in state.transitions:
            transition_input: Input
            for transition_input in transition.inputs:
                # check if transition regardless input case
                if transition_input.name == "1":
                    break

                if transition_input.name not in inputs:
                    inputs.append(transition_input.name)

            output: str
            for output in transition.outputs:
                if output not in outputs:
                    outputs.append(output)

    # sort input and output lists using lambda function
    inputs = sorted(inputs, key=lambda x: int(x[1:]))
    outputs = sorted(outputs, key=lambda x: int(x[1:]))

    return inputs, outputs


def check_state_transition_outputs_same(
    current_transition_outputs: list[str], first_transition_outputs: list[str]
) -> bool:
    """
    Checks whether state transition outputs are the same.

    Parameters
    ----------
    current_transition_outputs : list[str]
        The transition outputs of the current transition that is being checked.
    first_transition_outputs : list[str]
        The transition outputs of the first transition going to a state.

    Returns
    -------
    bool
        Whether state transition outputs are the same or not.
    """

    # different lengths therefore different
    if len(current_transition_outputs) != len(first_transition_outputs):
        return False

    # check outputs one by one
    i: int
    output1: str
    for i, output1 in enumerate(current_transition_outputs):
        output2: str = first_transition_outputs[i]

        # different output therefore different
        if output1 != output2:
            return False

    return True


def set_fsm_outputs_moore(states: dict[str, State]) -> None:
    """
    Sets the FSM state outputs when the FSM is of type MOORE.

    Parameters
    ----------
    states: dict[str, State]
        The FSM states
    """

    # loop through all state names
    state_1: State
    for state_1 in states.values():
        # loop through all states
        state_2: State
        is_output_set: bool = False
        for state_2 in states.values():
            if is_output_set:
                break

            # loop through all transitions
            transition: Transition
            for transition in state_2.transitions:
                # target is the current state which is being checked
                if transition.state_target == state_1.name:
                    # store transition outputs
                    state_1.outputs = transition.outputs
                    is_output_set = True

                    break
