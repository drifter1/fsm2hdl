"""
This module specifies the VHDL generator.
"""

from datetime import datetime
from importlib.metadata import metadata, version
from typing import TYPE_CHECKING
from zoneinfo import ZoneInfo

from fsm2hdl.code_gen.utils import (
    calculate_encoding_bit_requirements,
    determine_default_state_value,
    precalculate_state_values,
    prepare_jinja2_environment,
)
from fsm2hdl.common.configuration import DEFAULT_CONFIGURATION, Configuration
from fsm2hdl.common.models import Fsm
from fsm2hdl.common.parameters import (
    FSMType,
    HDLType,
)
from fsm2hdl.common.utils import (
    mealy_to_moore_conversion,
    open_file,
    simple_moore_to_mealy_conversion,
)

from .state_constants import prepare_state_constant_pair

if TYPE_CHECKING:
    from jinja2 import Environment


def generate_vhdl(
    fsm: Fsm,
    directory_name: str = "",
    cfg: Configuration = DEFAULT_CONFIGURATION,
) -> None:
    """
    Generates VHDL code for a given Fsm instance.

    Parameters
    ----------
    fsm : ``Fsm``
        The FSM to generate HDL code for.
    directory_name : str, default=""
        Path of the directory that will contain the file with .v extension.
        If an empty string, the current working directory is used.
    cfg: ``Configuration``, default=DEFAULT_CONFIGURATION
        The generator configuration.
    """

    # make sure HDL type in configuration is VHDL
    cfg.hdl_type = HDLType.VHDL

    # convert FSM if generator configuration specifies so
    if cfg.fsm_type == FSMType.MOORE:
        fsm: Fsm = mealy_to_moore_conversion(fsm)

    elif cfg.fsm_type == FSMType.MEALY:
        fsm: Fsm = simple_moore_to_mealy_conversion(fsm)

    env: Environment = prepare_jinja2_environment(cfg.hdl_type)

    template = env.get_template("fsm_top_vhdl.j2")

    state_bits: int = calculate_encoding_bit_requirements(
        len(fsm.states),
        encoding=cfg.encoding,
        default_state_type=cfg.default_state_type,
    )

    state_values: list[int] = precalculate_state_values(
        state_bits,
        len(fsm.states),
        encoding=cfg.encoding,
        default_state_type=cfg.default_state_type,
    )

    output = template.render(
        version=version("fsm2hdl"),
        timestamp=datetime.now(tz=ZoneInfo("UTC")).strftime(
            "%Y-%m-%d %H:%M %Z"
        ),
        gen_conf_vector=str(cfg),
        summary=metadata("fsm2hdl")["summary"],
        repository=metadata("fsm2hdl")["Project-URL"].split(",")[1],
        fsm=fsm,
        state_bits=state_bits,
        state_constant_pair=prepare_state_constant_pair(
            state_bits, state_values, fsm.states.values()
        ),
        default_state=determine_default_state_value(
            fsm.start_state,
            state_bits,
            hdl_type=cfg.hdl_type,
            default_state_type=cfg.default_state_type,
        ),
        coding_structure=cfg.coding_structure.name,
        reset_type=cfg.reset_type.name,
        reset_active_level=cfg.reset_active_level.name,
        combinatorial_structure=cfg.combinatorial_structure.name,
        combinatorial_sensitivity_mode=cfg.combinatorial_sensitivity_mode.name,
        output_handling_method=cfg.output_handling_method.name,
    )

    with open_file(directory_name, fsm.name, ".vhd", "w") as f:
        f.write(output)
        f.close()
