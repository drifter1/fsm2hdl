"""
This module specifies IO-related functions.
"""

import os
from pathlib import Path


def create_directory(directory_name: str) -> None:
    """
    Creates a new directory if it does not already exist.

    Parameters
    ----------
    directory_name : str
        The path of the directory to create.The path may be absolute or relative.
    """

    Path(directory_name).mkdir(parents=True, exist_ok=True)


def open_file(directory_name: str, file_name: str, extension: str, mode: str):
    """
    Opens a file, creating its directory if necessary.

    Parameters
    ----------
    directory_name : str
        Path of the directory that will contain the file.
        If an empty string, the current working directory is used.
    file_name : str
        Base name of the file (without extension).
    extension : str
        File extension, including the leading period.
    mode : str
        Mode in which the file should be opened.

    Returns
    -------
    file
        The file object returned by `open`.
    """
    file_path: str

    if directory_name != "":
        create_directory(directory_name)
        file_path = os.path.join(directory_name, file_name + extension)
    else:
        file_path = file_name + extension

    if mode in ["rb", "wb"]:
        return open(file_path, mode)
    return open(file_path, mode, encoding="utf-8")
