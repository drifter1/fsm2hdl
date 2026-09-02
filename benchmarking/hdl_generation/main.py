import multiprocessing as mp
from itertools import product
from pathlib import Path
from typing import TYPE_CHECKING

from configurations import VALID_CONFIGURATIONS
from helpers import ret_convert, ret_generate, ret_output_file_name

from fsm2hdl import Configuration, Fsm, parse_fsm_kiss2

if TYPE_CHECKING:
    from collections.abc import Callable

PROJ_PATH = Path(__file__).resolve().parent.parent.parent
BENCHMARK_PATH = PROJ_PATH / "benchmarks"
RTL_PATH = PROJ_PATH / "rtl"

NUM_PROCESSES = 32
CHUNK_SIZE = 1024


def process_pair(pair: tuple[Path, Configuration]):
    filepath: Path
    cfg: Configuration
    filepath, cfg = pair

    path: Path = filepath.parent
    path_stem: str = Path(filepath).parent.stem
    file_name_stem: str = filepath.stem

    current_output_path: str = (
        Path(RTL_PATH) / path_stem / file_name_stem
    ).as_posix()

    convert: Callable = ret_convert(cfg.fsm_type)
    generate: Callable = ret_generate(cfg.hdl_type)

    fsm: Fsm
    fsm = parse_fsm_kiss2(path, file_name_stem)
    fsm = convert(fsm)

    fsm.name = ret_output_file_name(file_name_stem, cfg)

    generate(
        fsm,
        current_output_path,
        cfg,
    )


def hdl_generation():
    files: list[Path] = list(BENCHMARK_PATH.glob("**/*.kiss2"))

    with mp.Pool(processes=NUM_PROCESSES) as pool:
        for _ in pool.imap_unordered(
            process_pair,
            product(files, VALID_CONFIGURATIONS),
            chunksize=CHUNK_SIZE,
        ):
            pass


if __name__ == "__main__":
    hdl_generation()
