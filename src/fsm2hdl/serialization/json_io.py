"""
This module provides routines for serializing and deserializing an FSM in ``json`` format.
"""

import json

from fsm2hdl.common import Fsm, open_file

from .dict_helpers import fsm_from_dict, fsm_to_dict


def load_fsm_json(directory_name: str, file_name: str) -> Fsm:
    """
    Parses an FSM from a JSON representation.

    Parameters
    ----------
    directory_name : str
        Path of the directory that contains the file with .json extension.
        If an empty string, the current working directory is used.
    file_name : str
        Base name of the file (without extension)

    Returns
    -------
    ``Fsm``
        A new Fsm instance constructed from the parsed JSON representation.
    """

    with open_file(directory_name, file_name, ".json", "r") as f:
        fsm_json = json.load(f)
        f.close()

    return fsm_from_dict(fsm_json)


def store_fsm_json(fsm: Fsm, directory_name: str, indent: int = 4) -> None:
    """
    Stores an FSM in JSON format.

    Parameters
    ----------
    fsm : ``Fsm``
        The FSM to store in JSON format.
    directory_name : str
        Path of the directory that will contain the file.
        If an empty string, the current working directory is used.
    indent: int, default=4
        The indentation level.
    """

    fsm_dict = fsm_to_dict(fsm)
    with open_file(directory_name, fsm.name, ".json", "w") as f:
        json.dump(fsm_dict, f, indent=indent)
        f.close()
