import contextlib
import json
import multiprocessing as mp
import os
from pathlib import Path

from run_test import run_verilog_test, run_vhdl_test

PROJ_PATH = Path(__file__).resolve().parent.parent.parent
RTL_PATH = PROJ_PATH / "rtl"
RESULTS_PATH = PROJ_PATH / "results"

ACTIVE_HIGH = 2
ALL_IN_ONE = 4
MOORE = 1

NUM_PROCESSES = 32
CHUNK_SIZE = 1024


def get_simulation_settings(file_name_stem):
    # store generator parameters as list of integers
    generator_parameters = [
        int(char) for char in file_name_stem if char.isdigit()
    ][-10:]

    fsm_type = generator_parameters[1]
    reset_active_level = generator_parameters[5]
    coding_structure = generator_parameters[6]

    active_high = "1" if reset_active_level == ACTIVE_HIGH else "0"

    # CodingStructure is not ALL_IN_ONE
    if coding_structure != ALL_IN_ONE:
        # 1 when MOORE, 0 when MEALY
        delay = "1" if fsm_type == MOORE else "0"

    # CodingStructure is ALL_IN_ONE
    else:
        # 2 when MOORE, 1 when MEALY
        delay = "2" if fsm_type == MOORE else "1"

    return active_high, delay


def perform_verilog_simulation(file_path):
    file_name_stem: str = str(Path(file_path).stem)
    path_stem: str = str(Path(file_path).parent.stem)
    path_parent_stem: str = str(Path(file_path).parent.parent.stem)

    active_high, delay = get_simulation_settings(file_name_stem)

    return run_verilog_test(
        path_stem,
        path_parent_stem,
        file_name_stem,
        file_path.parent,
        active_high,
        delay,
    )


def perform_vhdl_simulation(file_path):
    file_name_stem: str = str(Path(file_path).stem)
    path_stem: str = str(Path(file_path).parent.stem)
    path_parent_stem: str = str(Path(file_path).parent.parent.stem)

    active_high, delay = get_simulation_settings(file_name_stem)

    return run_vhdl_test(
        path_stem,
        path_parent_stem,
        file_name_stem,
        file_path.parent,
        active_high,
        delay,
    )


def perform_simulation():
    with contextlib.suppress(FileExistsError):
        os.mkdir(RESULTS_PATH)

    results = {
        "total_success": 0,
        "total_failure": 0,
        "failure": [],
    }

    verilog_files: list[Path] = list(RTL_PATH.glob("**/*.v"))

    with mp.Pool(processes=NUM_PROCESSES) as pool:
        for result, file_name in zip(
            pool.imap_unordered(
                perform_verilog_simulation,
                verilog_files,
                chunksize=CHUNK_SIZE,
            ),
            verilog_files,
            strict=False,
        ):
            failed_count = result[1]
            if failed_count == 0:
                results["total_success"] = results["total_success"] + 1
            else:
                results["total_failure"] = results["total_failure"] + 1
                results["failure"].append(file_name)

            with open(RESULTS_PATH / "simulation_results.json", "w") as f:
                json.dump(results, f, indent=4)
                f.close()

    vhdl_files: list[Path] = list(RTL_PATH.glob("**/*.vhd"))

    with mp.Pool(processes=NUM_PROCESSES) as pool:
        for result, file_name in zip(
            pool.imap_unordered(
                perform_vhdl_simulation,
                vhdl_files,
                chunksize=CHUNK_SIZE,
            ),
            vhdl_files,
            strict=False,
        ):
            failed_count = result[1]
            if failed_count == 0:
                results["total_success"] = results["total_success"] + 1
            else:
                results["total_failure"] = results["total_failure"] + 1
                results["failure"].append(file_name)

            with open(RESULTS_PATH / "simulation_results.json", "w") as f:
                json.dump(results, f, indent=4)
                f.close()


if __name__ == "__main__":
    perform_simulation()
