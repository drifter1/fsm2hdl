"""
This module specifies the Input data-class.
"""

from dataclasses import dataclass


@dataclass
class Input:
    """
    A class used to represent an Input.

    Attributes
    ----------
    name : str
        The input name.
    inverted : bool
        Whether input is inverted or not.
    """

    name: str
    inverted: bool
