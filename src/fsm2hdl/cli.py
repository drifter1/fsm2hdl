"""
This module specifies the ``fsm2hdl`` command-line tool.
"""

import argparse
import sys
from collections.abc import Callable
from enum import Enum
from importlib.metadata import version
from pathlib import Path

from fsm2hdl.code_gen import generate_verilog, generate_vhdl
from fsm2hdl.common.configuration import Configuration
from fsm2hdl.common.models import Fsm
from fsm2hdl.common.parameters import (
    CodingStructure,
    CombinatorialSensitivityMode,
    CombinatorialStructure,
    DefaultStateType,
    FSMType,
    HDLType,
    OutputHandlingMethod,
    ResetActiveLevel,
    ResetType,
    StateEncodingType,
)
from fsm2hdl.serialization import (
    load_fsm_json,
    load_fsm_pickle,
)
from fsm2hdl.state_table import parse_fsm_kiss2


def enum_choice(enum_cls: type) -> Callable[[str], Enum]:
    """
    Creates an ``argparse`` type callable that validates a value against members of an enum.

    Parameters
    ----------
    enum_cls : type
        A subclass of the class Enum.

    Returns
    -------
    Callable[[str], Enum]
        A function suitable to be passed as ``argparse`` type argument.
    """

    def _convert(val: str):
        """
        Convert a command-line string into an enum member.


        Parameters
        ----------
        val : str
            The raw string value supplied by the user on the command-line.

        Raises
        ------
        argparse.ArgumentError
            Raised when the supplied string ``val`` does not match any enum member.


        Returns
        -------
        enum_cls : type
            The enum member whose name matches ``val``.

        -------
        """

        # try matching with name (case-insensitive)
        try:
            return enum_cls[val.upper()]
        except KeyError:
            pass

        # try matching with value
        try:
            return enum_cls(int(val, 0))
        except (ValueError, TypeError):
            pass

        # prepare valid choices
        valid_choices: list[str] = [f"{m.name}/{m.value}" for m in enum_cls]

        # argparse expects an ArgumentError to be raised
        # from the type callable when the value is invalid.
        raise argparse.ArgumentError(
            None,
            f"invalid choice: {val!r} (choose from {valid_choices})",
        )

    return _convert


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """
    Parse command-line arguments.

    Parameters
    ----------
    argv : list[str] | None, optional
        The argument list to parse.

    Returns
    -------
    argparse.Namespace
        A namespace object containing the parsed arguments as attributes.
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("input", type=str, help="Input path")
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=Path.cwd().as_posix(),
        help="output path (default : script invocation path)",
    )
    parser.add_argument(
        "-t",
        "--hdl-type",
        choices=list(HDLType),
        type=enum_choice(HDLType),
        default=HDLType.VERILOG,
        help="HDL to generate default : Verilog)",
    )
    parser.add_argument(
        "-f",
        "--fsm-type",
        choices=list(FSMType),
        type=enum_choice(FSMType),
        default=FSMType.INFERRED,
        help="behavioral model (default : inferred type)",
    )
    parser.add_argument(
        "-e",
        "--state-encoding-type",
        choices=list(StateEncodingType),
        type=enum_choice(StateEncodingType),
        default=StateEncodingType.ONEHOT,
        help="encoding scheme (default : one-hot encoding)",
    )
    parser.add_argument(
        "-d",
        "--default-state-type",
        choices=list(DefaultStateType),
        type=enum_choice(DefaultStateType),
        default=DefaultStateType.REGULAR,
        help="behavior on undefined state encounter (default : regular initialization state)",
    )
    parser.add_argument(
        "-r",
        "--reset-type",
        choices=list(ResetType),
        type=enum_choice(ResetType),
        default=ResetType.SYNC,
        help="reset signal sampling (default : synchronous)",
    )
    parser.add_argument(
        "-a",
        "--reset-active-level",
        choices=list(ResetActiveLevel),
        type=enum_choice(ResetActiveLevel),
        default=ResetActiveLevel.ACTIVE_LOW,
        help="reset active level (default : active low)",
    )
    parser.add_argument(
        "-s",
        "--coding-structure",
        choices=list(CodingStructure),
        type=enum_choice(CodingStructure),
        default=CodingStructure.SEPARATE_ALL,
        help="overall HDL organization (default : three separate always blocks)",
    )
    parser.add_argument(
        "-c",
        "--combinatorial-structure",
        choices=list(CombinatorialStructure),
        type=enum_choice(CombinatorialStructure),
        default=CombinatorialStructure.CASE_WITH_NESTED_IF_ELSE,
        help="structural pattern of combinatorial logic (default : case with nested if-else)",
    )
    parser.add_argument(
        "-l",
        "--combinatorial-sensitivity-mode",
        choices=list(CombinatorialSensitivityMode),
        type=enum_choice(CombinatorialSensitivityMode),
        default=CombinatorialSensitivityMode.IMPLICIT,
        help="sensitivity list of combinatorial blocks (default : implicit sensitivity list)",
    )
    parser.add_argument(
        "-m",
        "--output-handling-method",
        choices=list(OutputHandlingMethod),
        type=enum_choice(OutputHandlingMethod),
        default=OutputHandlingMethod.ALL_OUTPUTS_ZEROED_BEFORE_STATE_LOGIC,
        help="output initialization and assignment method \
        (default : outputs zeroed before state logic)",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s v{version('fsm2hdl')}",
    )

    return parser.parse_args(argv)


def parse_fsm(args: argparse.Namespace) -> Fsm:
    """
    Parse command-line arguments.

    Parameters
    ----------
    argparse.Namespace
        A namespace object containing the parsed arguments as attributes.

    Returns
    -------
    ``Fsm``
        An Fsm instance.
    """
    input_path = Path(args.input)

    directory_name = input_path.parent.as_posix()
    file_name = str(input_path.stem)
    extension = str(input_path.suffix)

    # parse according to extension
    fsm: Fsm
    match extension:
        case ".kiss2":
            fsm = parse_fsm_kiss2(directory_name, file_name)
        case ".json":
            fsm = load_fsm_json(directory_name, file_name)
        case ".pkl":
            fsm = load_fsm_pickle(directory_name, file_name)
        case _:
            raise argparse.ArgumentError(
                None,
                f"invalid file extension: {extension} (provide .kiss2, .json or .pkl)",
            )

    return fsm


def main(argv: list[str] | None = None) -> int:
    """
    Entry point for the ``fsm2hdl`` command-line tool.

    Parameters
    ----------
    argv : list[str] | None, optional
        Command-line arguments to parse.

    Returns
    -------
    argparse.Namespace
        A namespace object containing the parsed arguments as attributes.
    """

    args: argparse.Namespace = parse_args(argv)

    cfg: Configuration = Configuration(
        hdl_type=args.hdl_type,
        fsm_type=args.fsm_type,
        encoding=args.state_encoding_type,
        default_state_type=args.default_state_type,
        reset_type=args.reset_type,
        reset_active_level=args.reset_active_level,
        coding_structure=args.coding_structure,
        combinatorial_structure=args.combinatorial_structure,
        combinatorial_sensitivity_mode=args.combinatorial_sensitivity_mode,
        output_handling_method=args.output_handling_method,
    )

    fsm: Fsm = parse_fsm(args)

    generate = (
        generate_verilog if args.hdl_type == HDLType.VERILOG else generate_vhdl
    )

    output_path: str = Path(args.output).as_posix()

    generate(fsm, output_path, cfg)

    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
