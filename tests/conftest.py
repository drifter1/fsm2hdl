"""
Special pytest configuration file that provides dynamic fixture for file_name
"""

import glob
from pathlib import Path

INPUT_PATH = "tests/benchmarks/kiss2"


def pytest_generate_tests(metafunc):
    """
    Dynamic file_name parametrization during collection phase.
    """
    file_list: list[str] = glob.glob(INPUT_PATH + "/*.kiss2")
    file_names: list[str] = [
        str(Path(file_name).stem) for file_name in file_list
    ]
    # check if the test function requires the fixture "file_name"
    if "file_name" in metafunc.fixturenames:
        metafunc.parametrize("file_name", sorted(file_names))
