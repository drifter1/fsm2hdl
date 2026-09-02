"""
This module specifies the Transition data-class.
"""

from dataclasses import dataclass

from .input import Input


@dataclass
class Transition:
    """
    A class used to represent a Transition.

    Attributes
    ----------
    transition_id : int
        The transition identifier.
    state_source : str
        The state source.
    state_target : str
        The state target.
    inputs : list[``Input``]
        The transition inputs.
    outputs : list[str]
        The transition outputs.
    """

    transition_id: int
    state_source: str
    state_target: str
    inputs: list[Input]
    outputs: list[str]
