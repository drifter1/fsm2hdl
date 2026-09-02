import json
import os
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

FILE_PATH = Path(__file__).resolve().parent
TESTS_DIR = FILE_PATH / "tests"


async def reset_dut(dut, *, active_high=True):
    dut.rst.value = 1 if active_high else 0
    await RisingEdge(dut.clk)
    dut.rst.value = 0 if active_high else 1


def add_delay(test_vectors, delay):
    for _ in range(delay):
        test_vectors.append({"inputs": None, "outputs": None})

    for _ in range(delay):
        for i in range(len(test_vectors) - 1, 0, -1):
            test_vectors[i]["outputs"] = test_vectors[i - 1]["outputs"]

    for i in range(delay):
        test_vectors[i]["outputs"] = None


async def drive_inputs(dut, inputs):
    for name, value in inputs.items():
        getattr(dut, name).value = value


def compare_outputs(dut, outputs):
    return all(
        getattr(dut, name).value == value for name, value in outputs.items()
    )


async def test_dut(dut, test_vectors):
    for vec in test_vectors:
        if vec["inputs"] is not None:
            await drive_inputs(dut, vec["inputs"])

        await RisingEdge(dut.clk)

        if vec["outputs"] is not None:
            assert compare_outputs(dut, vec["outputs"]), "Output mismatch"  # noqa: S101


@cocotb.test()
async def test_operation(dut):
    active_high = os.environ.get("ACTIVE_HIGH") == "1"
    delay = int(os.environ.get("DELAY"))
    benchmark = os.environ.get("BENCHMARK")
    benchmark_format = os.environ.get("BENCHMARK_FORMAT")

    clock = Clock(dut.clk, 1, unit="ns")
    cocotb.start_soon(clock.start(start_high=False))

    json_file_path = TESTS_DIR / benchmark_format / benchmark

    for _path, _dirs, files in os.walk(json_file_path):
        for file_name in sorted(files):
            with open(json_file_path / file_name, encoding="utf-8") as f:  # noqa: ASYNC230
                test_vectors = json.load(f)
                f.close()

            add_delay(test_vectors, delay)

            await reset_dut(dut, active_high=active_high)
            await test_dut(dut, test_vectors)
