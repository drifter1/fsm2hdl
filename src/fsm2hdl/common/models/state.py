"""
This module specifies the State data-class.
"""

from dataclasses import dataclass, field

from .transition import Transition


@dataclass
class State:
    """
    A class used to represent a State.

    Attributes
    ----------
    name : str
        The state name.
    transitions : list[``Transition``]
        The state transitions.
    outputs : list[str]
        The state outputs (not used when ``FSMType.MEALY``).
    """

    name: str
    transitions: list[Transition] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
