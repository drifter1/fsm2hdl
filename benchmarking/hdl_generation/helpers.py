from collections.abc import Callable

from fsm2hdl import (
    Configuration,
    FSMType,
    HDLType,
    generate_verilog,
    generate_vhdl,
    mealy_to_moore_conversion,
    simple_moore_to_mealy_conversion,
)


def ret_convert(fsm_type: FSMType) -> Callable:
    if fsm_type == FSMType.MOORE:
        return mealy_to_moore_conversion
    # FSMType.MEALY
    return simple_moore_to_mealy_conversion


def ret_generate(hdl_type: HDLType) -> Callable:
    if hdl_type == HDLType.VERILOG:
        return generate_verilog
    # HDLType.VHDL
    return generate_vhdl


def ret_output_file_name(file_name_stem: str, cfg: Configuration):
    output_file_name: str = file_name_stem
    if output_file_name[-1].isdigit():
        output_file_name += "_"
    output_file_name += str(cfg)

    return output_file_name
