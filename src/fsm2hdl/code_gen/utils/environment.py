"""
This module provides a function that prepares the Jinja environment.
"""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from fsm2hdl.common.parameters import HDLType

TEMPLATES_PATH = str(Path(__file__).parent.parent / "templates")
MACROS_PATH = TEMPLATES_PATH + "/macros"


def prepare_jinja2_environment(hdl_type: HDLType) -> Environment:
    """
    Prepares the jinja2 environment.

    Returns
    -------
    jinja2.Environment
        The jinja2 environment.
    """

    if hdl_type == HDLType.VERILOG:
        includes_path = str(
            Path(__file__).parent.parent / "templates/includes/verilog"
        )
    else:  # HDLType.VHDL
        includes_path = str(
            Path(__file__).parent.parent / "templates/includes/vhdl"
        )

    return Environment(
        loader=FileSystemLoader([TEMPLATES_PATH, MACROS_PATH, includes_path]),
        autoescape=False,  # noqa: S701
    )
