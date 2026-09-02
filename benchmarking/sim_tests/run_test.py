import shutil
from pathlib import Path

from cocotb_tools.runner import get_results, get_runner

VERILOG_SIM = "icarus"
VHDL_SIM = "ghdl"

GHDL_BUILD_ARGS = ["--std=08"]

FILE_PATH = Path(__file__).resolve().parent
BUILD_DIR = FILE_PATH / "sim_build"


def run_verilog_test(
    benchmark, benchmark_format, design, rtl_path, active_high, delay
):
    file_name = design + ".v"
    sources = [rtl_path / file_name]
    build_dir = BUILD_DIR / design

    runner = get_runner(VERILOG_SIM)

    runner.build(
        sources=sources,
        hdl_toplevel=design,
        build_dir=build_dir,
        always=True,
        waves=True,
    )

    runner.test(
        hdl_toplevel=design,
        test_module="fsm_test",
        waves=True,
        extra_env={
            "ACTIVE_HIGH": active_high,
            "DELAY": delay,
            "BENCHMARK": benchmark,
            "BENCHMARK_FORMAT": benchmark_format,
        },
    )

    results = get_results(build_dir / "results.xml")

    shutil.rmtree(build_dir)

    return results


def run_vhdl_test(
    benchmark, benchmark_format, design, rtl_path, active_high, delay
):
    file_name = design + ".vhd"
    sources = [rtl_path / file_name]
    build_dir = BUILD_DIR / design

    runner = get_runner(VHDL_SIM)

    runner.build(
        sources=sources,
        hdl_toplevel=design,
        build_dir=build_dir,
        always=True,
        waves=True,
        build_args=GHDL_BUILD_ARGS,
    )

    runner.test(
        hdl_toplevel=design,
        test_module="fsm_test",
        waves=True,
        extra_env={
            "ACTIVE_HIGH": active_high,
            "DELAY": delay,
            "BENCHMARK": benchmark,
            "BENCHMARK_FORMAT": benchmark_format,
        },
    )

    results = get_results(build_dir / "results.xml")

    shutil.rmtree(build_dir)

    return results
