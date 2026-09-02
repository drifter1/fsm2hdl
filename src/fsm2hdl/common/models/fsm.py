"""
This module specifies the Fsm data-class.
"""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from fsm2hdl.common.parameters import FSMType

from .fsm_helpers import (
    add_missing_source_states,
    check_state_transition_outputs_same,
    determine_missing_source_state,
    identify_unique_io,
    set_fsm_outputs_moore,
)
from .state import State

if TYPE_CHECKING:
    from .transition import Transition


@dataclass
class Fsm:
    """
    A class used to represent an FSM.

    Attributes
    ----------
    name : str
        The FSM name.
    states : dict[str, ``State``]
        The FSM states.
    inputs : list[str]
        The FSM inputs.
    outputs : list[str]
        The FSM outputs.
    start_state : str
        The start state of the FSM.
    fsm_type : ``FSMType``
        The behavioral model (or type) of the FSM.
    """

    name: str
    states: dict[str, State]
    inputs: list[str] = field(init=False)
    outputs: list[str] = field(init=False)
    start_state: str = field(init=False)
    fsm_type: FSMType = field(init=False)

    def __post_init__(self) -> None:
        """
        Executes after the name and states fields have been populated and
        computes derived attributes that depend on the state dictionary.
        """

        if determine_missing_source_state(self.states) is not None:
            add_missing_source_states(self.states)

        self.inputs, self.outputs = identify_unique_io(self.states)

        # self.start_state: str = sorted(self.states.keys())[0]
        self.start_state: str = sorted(
            self.states.keys(), key=lambda x: int(x[1 : len(x.split("_")[0])])
        )[0]

        self.fsm_type = self.identify_fsm_type()

        # if Moore then set outputs for each state object
        if self.fsm_type == FSMType.MOORE:
            set_fsm_outputs_moore(self.states)

    def identify_fsm_type(self) -> FSMType:
        """
        Identifies the behavioral model (or type) of the FSM.

        Returns
        -------
        ``FSMType``
            The behavioral model (or type) of the FSM.
        """

        # loop through all state names
        state_name: str
        for state_name in self.states:
            # keep first transition
            first_transition_outputs: list[str]
            is_first_transition: bool = True

            # loop through all states
            state: State
            for state in self.states.values():
                # loop through all transitions
                transition: Transition
                for transition in state.transitions:
                    # target is the current state which is being checked
                    if transition.state_target == state_name:
                        # store first transition outputs
                        if is_first_transition:
                            first_transition_outputs = transition.outputs
                            is_first_transition = False
                            continue
                        # check if the transition outputs are the same
                        if not check_state_transition_outputs_same(
                            transition.outputs, first_transition_outputs
                        ):
                            return FSMType.MEALY

        # if all checks pass the FSM is of type Moore
        return FSMType.MOORE
