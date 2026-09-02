import contextlib
import csv
import os
from dataclasses import asdict, fields
from pathlib import Path

from configurations import VALID_CONFIGURATIONS
from disk import disk_space_utilization
from memory import MemoryTracker
from result import (
    BenchmarkResult,
)
from runtime import Timer

from fsm2hdl import (
    Fsm,
    HDLType,
    generate_verilog,
    generate_vhdl,
    parse_fsm_kiss2,
)

FILE_PATH = Path(__file__).resolve().parent
PROJ_PATH = FILE_PATH.parent.parent
BENCHMARK_PATH = PROJ_PATH / "benchmarks"
RESULTS_PATH = PROJ_PATH / "results"
OUTPUT_PATH = FILE_PATH / "rtl"


def perform_perf_tests():
    with contextlib.suppress(FileExistsError):
        os.mkdir(RESULTS_PATH)

    benchmark_results: list[dict] = []

    for path, _dirs, files in os.walk(BENCHMARK_PATH):
        for file_name in sorted(files):
            file_name_stem: str = str(Path(file_name).stem)
            path_stem: str = str(Path(path).stem)
            current_output_path: str = (
                Path(OUTPUT_PATH) / path_stem
            ).as_posix()

            for cfg in VALID_CONFIGURATIONS:
                generate = (
                    generate_verilog
                    if cfg.hdl_type == HDLType.VERILOG
                    else generate_vhdl
                )

                timer: Timer = Timer()
                memory_tracker: MemoryTracker = MemoryTracker()

                timer.start()
                memory_tracker.start()

                fsm: Fsm = parse_fsm_kiss2(path, file_name_stem)

                timer.end()
                parsing_time: float = timer.calc_diff()
                parsing_peak: int = memory_tracker.get()
                memory_tracker.stop()
                memory_tracker.reset()

                timer.start()
                memory_tracker.start()
                generate(fsm, current_output_path, cfg)
                timer.end()
                generation_time: float = timer.calc_diff()
                generation_peak: int = memory_tracker.get()
                memory_tracker.stop()
                memory_tracker.reset()

                current_output_file: str = current_output_path + "/" + fsm.name
                if cfg.hdl_type == HDLType.VERILOG:
                    current_output_file += ".v"
                else:
                    current_output_file += ".vhd"

                generation_utilization: int = disk_space_utilization(
                    current_output_file
                )

                benchmark_result: BenchmarkResult = BenchmarkResult(
                    path_stem,
                    fsm.name,
                    str(cfg),
                    cfg.hdl_type.name,
                    len(fsm.states),
                    sum(
                        len(state.transitions) for state in fsm.states.values()
                    ),
                    len(fsm.inputs),
                    len(fsm.outputs),
                    parsing_time,
                    parsing_peak,
                    generation_time,
                    generation_peak,
                    generation_utilization,
                )

                benchmark_results.append(asdict(benchmark_result))

                with open(RESULTS_PATH / "perf_tests_results.csv", "w") as f:
                    field_names = [
                        field.name for field in fields(BenchmarkResult)
                    ]
                    writer = csv.DictWriter(f, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerows(benchmark_results)


if __name__ == "__main__":
    perform_perf_tests()
