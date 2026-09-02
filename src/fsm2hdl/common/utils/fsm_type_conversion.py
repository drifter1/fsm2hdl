"""
This module specifies FSM type conversion functions.
"""

from copy import deepcopy

from fsm2hdl.common.models import Fsm, State, Transition
from fsm2hdl.common.parameters import FSMType


def __moore_state_name(transition: Transition) -> str:
    """
    Build the Moore-state name that corresponds to a given Mealy transition.

    Parameters
    ----------
    transition : Transition
        The Mealy transition for which the Moore state name should be generated.

    Returns
    -------
    str
        The generated state name.
    """

    state_name: str = transition.state_target

    # if there are transition outputs
    if len(transition.outputs) > 0:
        output_str: str = ""
        output: str
        for output in transition.outputs:
            output_str += output

        state_name += "_" + output_str

    return state_name


def __moore_required_states(states: dict[str, State]) -> list[str]:
    """
    Enumerate all required Moore states for a given Mealy FSM.

    Parameters
    ----------
    states : dict[str, State]
        Mapping from state names to ``State`` objects representing the original Mealy machine.

    Returns
    -------
    list[str]
        A sorted list of unique Moore-state names.
    """

    required_states: list[str] = []

    # identify required states by looping through original FSM
    state: State
    for state in states.values():
        # loop through all transitions
        transition: Transition
        for transition in state.transitions:
            state_name = __moore_state_name(transition)

            # if state is new state create a dictionary entry
            if state_name not in required_states:
                required_states.append(state_name)

    # add states which are not in state targets
    original_state_names = [
        state_name.split("_")[0] for state_name in required_states
    ]
    required_states.extend(
        state.name
        for state in states.values()
        if state.name not in original_state_names
    )

    # sort state list twice
    required_states = sorted(required_states)
    return sorted(
        required_states, key=lambda x: int(x[1 : len(x.split("_")[0])])
    )


def mealy_to_moore_conversion(fsm: Fsm) -> Fsm:
    """
    Convert a Mealy finite-state machine to an equivalent Moore machine.

    Parameters
    ----------
    fsm : Fsm
        The Mealy FSM to convert.

    Returns
    -------
    Fsm
        A new Fsm instance representing the equivalent Moore machine.
    """

    # check if already Moore then simply return the FSM
    if fsm.identify_fsm_type() == FSMType.MOORE:
        return deepcopy(fsm)

    # identify required states
    required_states: list[str] = __moore_required_states(fsm.states)

    # states dictionary
    moore_states: dict[str, State] = {}

    # create dictionary entries for each required states
    state_name: str
    for state_name in required_states:
        moore_states[state_name] = State(state_name)

    # fill dictionary by looping through original FSM again
    state: State
    transition_id: int = 1
    for state in fsm.states.values():
        # loop through all transitions
        transition: Transition
        for transition in state.transitions:
            state_source = transition.state_source
            state_target = __moore_state_name(transition)

            transition_inputs = deepcopy(transition.inputs)
            transition_outputs = deepcopy(transition.outputs)

            # for each state
            state_name: str
            for state_name in required_states:
                if state_source == state_name.split("_")[0]:
                    # create transition
                    new_transition: Transition = Transition(
                        transition_id,
                        state_name,
                        state_target,
                        transition_inputs,
                        transition_outputs,
                    )

                    # add transition to state
                    moore_states[state_name].transitions.append(new_transition)

                    # increment transition ID
                    transition_id += 1

    # create and return FSM

    return Fsm(fsm.name, moore_states)


def simple_moore_to_mealy_conversion(fsm: Fsm) -> Fsm:
    """
    Convert a Moore FSM to a Mealy FSM in a lightweight manner.

    Parameters
    ----------
    fsm : Fsm
        The Moore FSM to convert.

    Returns
    -------
    Fsm
        A deep-copy of the input Fsm with its ``type`` attribute set to ``FSMType.MEALY``
    """
    # check if already Mealy then simply return the FSM
    if fsm.identify_fsm_type() == FSMType.MEALY:
        return deepcopy(fsm)

    # make a deep copy of the original FSM
    mealy_fsm = deepcopy(fsm)

    # since every transition already has the outputs only the type variable needs to be changed
    mealy_fsm.fsm_type = FSMType.MEALY

    return mealy_fsm
