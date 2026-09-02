import contextlib
import json
import multiprocessing as mp
import os
import subprocess
from pathlib import Path

PROJ_PATH = Path(__file__).resolve().parent.parent.parent
RTL_PATH = PROJ_PATH / "rtl"
RESULTS_PATH = PROJ_PATH / "results"

NUM_PROCESSES = 32
CHUNK_SIZE = 1024


def check_verilog_file(file_path):
    return subprocess.run(
        ["iverilog", "-tnull", "-Wall", "-g2005", file_path],
        check=False,
    )


def check_vhdl_file(file_path):
    return subprocess.run(
        ["ghdl", "-s", "--std=08", file_path],
        check=False,
    )


def syntax_check():
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
                check_verilog_file,
                verilog_files,
                chunksize=CHUNK_SIZE,
            ),
            verilog_files,
            strict=False,
        ):
            if result.returncode == 0:
                results["total_success"] = results["total_success"] + 1
            else:
                results["total_failure"] = results["total_failure"] + 1
                results["failure"].append(file_name)

            with open(RESULTS_PATH / "syntax_check_results.json", "w") as f:
                json.dump(results, f, indent=4)
                f.close()

    vhdl_files: list[Path] = list(RTL_PATH.glob("**/*.vhd"))

    with mp.Pool(processes=NUM_PROCESSES) as pool:
        for result, file_name in zip(
            pool.imap_unordered(
                check_vhdl_file,
                vhdl_files,
                chunksize=CHUNK_SIZE,
            ),
            vhdl_files,
            strict=False,
        ):
            if result.returncode == 0:
                results["total_success"] = results["total_success"] + 1
            else:
                results["total_failure"] = results["total_failure"] + 1
                results["failure"].append(file_name)

            with open(RESULTS_PATH / "syntax_check_results.json", "w") as f:
                json.dump(results, f, indent=4)
                f.close()


if __name__ == "__main__":
    syntax_check()
