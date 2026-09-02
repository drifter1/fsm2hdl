"""
This module provides routines for serializing and deserializing an FSM in ``pickle`` format.
"""

import pickle

from fsm2hdl.common import Fsm, open_file


def load_fsm_pickle(directory_name: str, file_name: str) -> Fsm:
    """
    Parses an FSM from pickle representation.

    Parameters
    ----------
    directory_name : str
        Path of the directory that contains the file with .pickle extension.
        If an empty string, the current working directory is used.
    file_name : str
        Base name of the file (without extension)

    Returns
    -------
    ``Fsm``
        A new Fsm instance constructed from the deserialized pickle representation.
    """

    with open_file(directory_name, file_name, ".pkl", "rb") as f:
        fsm = pickle.load(f)  # noqa: S301
        f.close()

    return fsm


def store_fsm_pickle(fsm: Fsm, directory_name: str) -> None:
    """
    Stores an FSM as a pickle.

    Parameters
    ----------
    fsm : ``Fsm``
        The FSM to store as a pickle.
    directory_name : str
        Path of the directory that will contain the file.
        If an empty string, the current working directory is used.
    """

    with open_file(directory_name, fsm.name, ".pkl", "wb") as f:
        pickle.dump(fsm, f, protocol=pickle.HIGHEST_PROTOCOL)
        f.close()
