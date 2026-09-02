"""
This module specifies dictionary helpers for serialization and deserialization.
"""

from dataclasses import asdict

from fsm2hdl.common.models import Fsm, Input, State, Transition
from fsm2hdl.common.parameters import FSMType
from fsm2hdl.common.utils import (
    mealy_to_moore_conversion,
    simple_moore_to_mealy_conversion,
)


def fsm_to_dict(fsm: Fsm) -> dict:
    """
    Serialize an `Fsm` object to its dict representation.FSM

    Parameters
    ----------
    fsm : ``Fsm``
        The Fsm instance to serialize.

    Returns
    -------
    dict
        ``Fsm`` in dict format.
    """

    fsm_dict: dict = asdict(fsm)

    # change FSMType Enum into string
    fsm_dict["fsm_type"] = fsm.fsm_type.name

    return fsm_dict


def fsm_from_dict(fsm_dict: dict) -> Fsm:
    """
    Parse an ``Fsm`` object from its dict representation.

    Parameters
    ----------
    fsm_dict : dict
        ``Fsm`` in dict format.

    Returns
    -------
    ``Fsm``
        A new ``Fsm`` instance constructed from the parsed dict representation.
    """
    name = fsm_dict["name"]

    states: dict[str, State] = {}

    for state in fsm_dict["states"].values():
        states[state["name"]] = state_from_dict(state)

    fsm: Fsm = Fsm(name, states)

    fsm_type = FSMType[fsm_dict["fsm_type"]]

    if fsm_type == FSMType.MOORE:
        fsm = mealy_to_moore_conversion(fsm)

    elif fsm_type == FSMType.MEALY:
        fsm = simple_moore_to_mealy_conversion(fsm)

    return fsm


def state_from_dict(state_dict: dict) -> State:
    """
    Parse an ``State`` object from its dict representation.

    Parameters
    ----------
    state_dict : dict
        ``State`` in dict format.

    Returns
    -------
    ``State``
        A new ``State`` instance constructed from the parsed dict representation.
    """
    state: State

    name = state_dict["name"]

    transitions: list[Transition] = [
        transition_from_dict(transition)
        for transition in state_dict["transitions"]
    ]
    outputs: list[str] = state_dict["outputs"]

    state = State(name)
    state.transitions = transitions
    state.outputs = outputs

    return state


def transition_from_dict(transition_dict: dict) -> Transition:
    """
    Parse an ``Transition`` object from its dict representation.

    Parameters
    ----------
    transition_dict : dict
        ``Transition`` in dict format.

    Returns
    -------
    ``Transition``
        A new ``Transition`` instance constructed from the parsed dict representation.
    """
    transition: Transition

    transition_id = int(transition_dict["transition_id"])
    state_source = transition_dict["state_source"]
    state_target = transition_dict["state_target"]
    inputs: list[Input] = [
        input_from_dict(transition_input)
        for transition_input in transition_dict["inputs"]
    ]
    outputs: list[str] = transition_dict["outputs"]

    transition = Transition(
        transition_id, state_source, state_target, inputs, outputs
    )

    return transition


def input_from_dict(input_dict: dict) -> Input:
    """
    Parse an ``Input`` object from its dict representation.

    Parameters
    ----------
    input_dict : dict
        ``Input`` in dict format.

    Returns
    -------
    ``Input``
        A new ``Input`` instance constructed from the parsed dict representation.
    """

    return Input(**input_dict)
