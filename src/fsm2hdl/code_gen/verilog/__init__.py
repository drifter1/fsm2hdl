"""
This package specifies the Verilog generator.
"""

__all__ = [
    "format_state_parameters",
    "generate_verilog",
    "prepare_state_parameter_pair",
    "state_parameters",
]

from . import state_parameters
from .generator import generate_verilog
from .state_parameters import (
    format_state_parameters,
    prepare_state_parameter_pair,
)
