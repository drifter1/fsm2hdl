"""
This package bundles everything that the FSM-to-HDL generator needs to run
and validate the finite-state-machines that it produces.

It includes:
- Core data-model classes - `fsm2hdl.common.models`
- Configuration parameters - `fsm2hdl.common.parameters`
- Useful utilities -`fsm2hdl.common.utils`
"""

__all__ = [
    "CodingStructure",
    "CombinatorialSensitivityMode",
    "CombinatorialStructure",
    "Configuration",
    "DefaultStateType",
    "FSMType",
    "Fsm",
    "HDLType",
    "Input",
    "OutputHandlingMethod",
    "ResetActiveLevel",
    "ResetType",
    "State",
    "StateEncodingType",
    "Transition",
    "configuration",
    "create_directory",
    "mealy_to_moore_conversion",
    "models",
    "open_file",
    "parameters",
    "simple_moore_to_mealy_conversion",
    "utils",
]

from . import configuration, models, parameters, utils
from .configuration import Configuration
from .models import Fsm, Input, State, Transition
from .parameters import (
    CodingStructure,
    CombinatorialSensitivityMode,
    CombinatorialStructure,
    DefaultStateType,
    FSMType,
    HDLType,
    OutputHandlingMethod,
    ResetActiveLevel,
    ResetType,
    StateEncodingType,
)
from .utils import (
    create_directory,
    mealy_to_moore_conversion,
    open_file,
    simple_moore_to_mealy_conversion,
)
