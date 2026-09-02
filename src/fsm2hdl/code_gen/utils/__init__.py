"""
This package bundles useful utilities used in HDL generation.
"""

__all__ = [
    "calculate_encoding_bit_requirements",
    "determine_default_state_value",
    "initial_state_value",
    "precalculate_state_values",
    "prepare_jinja2_environment",
]

from .environment import prepare_jinja2_environment
from .states import (
    calculate_encoding_bit_requirements,
    determine_default_state_value,
    initial_state_value,
    precalculate_state_values,
)
