"""
This is a Python-based tool that can generate synthesis-ready HDL code
from a high-level FSM specification.
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
    "code_gen",
    "common",
    "generate_verilog",
    "generate_vhdl",
    "load_fsm_json",
    "load_fsm_pickle",
    "mealy_to_moore_conversion",
    "parse_fsm_kiss2",
    "serialization",
    "serialize_fsm_kiss2",
    "simple_moore_to_mealy_conversion",
    "state_table",
    "store_fsm_json",
    "store_fsm_pickle",
]

from fsm2hdl import code_gen, common, serialization, state_table
from fsm2hdl.code_gen import (
    generate_verilog,
    generate_vhdl,
)
from fsm2hdl.common import (
    CodingStructure,
    CombinatorialSensitivityMode,
    CombinatorialStructure,
    Configuration,
    DefaultStateType,
    Fsm,
    FSMType,
    HDLType,
    Input,
    OutputHandlingMethod,
    ResetActiveLevel,
    ResetType,
    State,
    StateEncodingType,
    Transition,
    mealy_to_moore_conversion,
    simple_moore_to_mealy_conversion,
)
from fsm2hdl.serialization import (
    load_fsm_json,
    load_fsm_pickle,
    store_fsm_json,
    store_fsm_pickle,
)
from fsm2hdl.state_table import (
    parse_fsm_kiss2,
    serialize_fsm_kiss2,
)
