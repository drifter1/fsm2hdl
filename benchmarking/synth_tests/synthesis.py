import os
import subprocess
from pathlib import Path

FILE_PATH = Path(__file__).resolve().parent

VERILOG_TCL_SCRIPT = (FILE_PATH / "verilog.tcl").as_posix()
VHDL_TCL_SCRIPT = (FILE_PATH / "vhdl.tcl").as_posix()
EDIF_TCL_SCRIPT = (FILE_PATH / "edif.tcl").as_posix()

PART_NAME = "xc7a100tcsg324-1"
CONSTRAINTS_FILE = (FILE_PATH / "constraints.xdc").as_posix()


def perform_yosys_synthesis(
    cur_report_dir, file_name_stem, file_extension, file_path
):
    synth_log_file: str = (Path(cur_report_dir) / "synth.log").as_posix()

    edif_file: str = Path(cur_report_dir) / f"{file_name_stem}.edif"

    if file_extension == ".v":
        subprocess.run(
            [
                "yosys",
                "-l",
                synth_log_file,
                "-p",
                f"synth_xilinx; write_edif {edif_file}",
                file_path,
            ],
            check=False,
        )

    # ".vhd"
    else:
        subprocess.run(
            [
                "yosys",
                "-l",
                synth_log_file,
                "-m",
                "ghdl",
                "-p"
                f"ghdl --std=08 {file_path} -e {file_name_stem}; synth_xilinx; write_edif {edif_file}",
            ],
            check=False,
        )

    impl_log_file = Path(cur_report_dir) / "impl.log"
    impl_jou_file = Path(cur_report_dir) / "impl.jou"

    subprocess.run(
        [
            "vivado",
            "-mode",
            "batch",
            "-notrace",
            "-log",
            impl_log_file,
            "-journal",
            impl_jou_file,
            "-source",
            EDIF_TCL_SCRIPT,
            "-tclargs",
            file_name_stem,
            edif_file,
            CONSTRAINTS_FILE,
            PART_NAME,
            cur_report_dir,
        ],
        check=False,
    )

    if impl_jou_file.exists():
        os.remove(impl_jou_file)


def perform_vivado_synthesis(
    cur_report_dir, cur_proj_dir, file_name_stem, file_extension, file_path
):
    if file_extension == ".v":
        tcl_script = VERILOG_TCL_SCRIPT

    # ".vhd"
    else:
        tcl_script = VHDL_TCL_SCRIPT

    vivado_log_file = Path(cur_report_dir) / "vivado.log"
    vivado_jou_file = Path(cur_report_dir) / "vivado.jou"

    subprocess.run(
        [
            "vivado",
            "-mode",
            "batch",
            "-notrace",
            "-log",
            vivado_log_file,
            "-journal",
            vivado_jou_file,
            "-source",
            tcl_script,
            "-tclargs",
            file_name_stem,
            file_path,
            CONSTRAINTS_FILE,
            PART_NAME,
            cur_report_dir,
            cur_proj_dir,
        ],
        check=False,
    )

    if vivado_log_file.exists():
        os.remove(vivado_log_file)

    if vivado_jou_file.exists():
        os.remove(vivado_jou_file)
