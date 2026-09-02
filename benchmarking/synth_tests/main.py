import contextlib
import multiprocessing as mp
import os
from pathlib import Path

from synthesis import perform_vivado_synthesis, perform_yosys_synthesis

FILE_PATH = Path(__file__).resolve().parent
PROJ_PATH = FILE_PATH.parent.parent
RTL_PATH = PROJ_PATH / "rtl"
REPORTS_PATH = PROJ_PATH / "reports"
PROJECTS_PATH = PROJ_PATH / "projects"

LARGE_BENCHMARKS = ("s1488", "s1494", "s298", "s820", "s832", "tbk")

NUM_PROCESSES_LARGE = 2
NUM_PROCESSES_SMALL = 8


def process_file(file_path):
    file_name_stem: str = str(Path(file_path).stem)
    file_extension: str = str(Path(file_path).suffix)
    path_stem: str = str(Path(file_path).parent.stem)
    path_parent_stem: str = str(Path(file_path).parent.parent.stem)

    # prepare report path
    cur_report_dir: str = str(
        Path(REPORTS_PATH) / path_parent_stem / path_stem / file_name_stem
    )

    # prepare project path
    cur_proj_dir: str = str(
        Path(PROJECTS_PATH) / path_parent_stem / path_stem / file_name_stem
    )

    if os.path.isdir(cur_report_dir):
        return

    os.makedirs(cur_report_dir, exist_ok=True)

    # prepare Yosys and Vivado reports paths
    cur_yosys_report_dir: str = str(Path(cur_report_dir) / "Yosys")
    os.makedirs(cur_yosys_report_dir, exist_ok=True)

    cur_vivado_report_dir: str = str(Path(cur_report_dir) / "Vivado")
    os.makedirs(cur_vivado_report_dir, exist_ok=True)

    # prepare project paths
    os.makedirs(cur_proj_dir, exist_ok=True)

    # perform Yosys synthesis
    perform_yosys_synthesis(
        cur_yosys_report_dir, file_name_stem, file_extension, file_path
    )

    # perform Vivado synthesis
    perform_vivado_synthesis(
        cur_vivado_report_dir,
        cur_proj_dir,
        file_name_stem,
        file_extension,
        file_path,
    )


def perform_synthesis():
    with contextlib.suppress(FileExistsError):
        os.mkdir(PROJECTS_PATH)

    files = [f for f in RTL_PATH.rglob("*") if f.suffix in [".v", ".vhd"]]

    large_files = [
        file for file in files if file.stem.startswith(LARGE_BENCHMARKS)
    ]
    small_files = [
        file for file in files if not file.stem.startswith(LARGE_BENCHMARKS)
    ]

    # process smaller benchmarks in parallel (more processes)
    with mp.Pool(processes=NUM_PROCESSES_SMALL) as pool:
        for _ in pool.imap_unordered(process_file, small_files):
            pass

    # process larger benchmarks in parallel (less processes)
    with mp.Pool(processes=NUM_PROCESSES_LARGE) as pool:
        for _ in pool.imap_unordered(process_file, large_files):
            pass


if __name__ == "__main__":
    perform_synthesis()
