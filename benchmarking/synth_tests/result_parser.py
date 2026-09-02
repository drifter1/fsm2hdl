import contextlib
import os
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from result import BenchmarkResults

FILE_PATH = Path(__file__).resolve().parent
PROJ_PATH = FILE_PATH.parent.parent
RESULTS_PATH = PROJ_PATH / "results"
REPORTS_PATH = PROJ_PATH / "reports"

UTILIZATION_LINE_PARTS = 14
TIMING_LINE_PARTS = 9
POWER_LINE_PARTS = 8
VIVADO_LOG_PARTS_TIME = 10
VIVADO_LOG_PARTS_MEM = 18
YOSYS_LOG_PARTS = 15

CLOCK_PERIOD = 10

TIME_ZONE = ZoneInfo("Europe/Athens")


def parse_reports():
    with contextlib.suppress(FileExistsError):
        os.mkdir(RESULTS_PATH)

    results: dict[str, dict] = {"kiss2": {}}
    results["kiss2"]: dict[str, BenchmarkResults] = {}

    for path, _dirs, files in os.walk(REPORTS_PATH):
        for file_name in sorted(files):
            tool: str = str(Path(path).stem)
            hdl: str = str(Path(path).parent.stem)
            benchmark_name: str = str(Path(path).parent.parent.stem)
            benchmark_format: str = str(Path(path).parent.parent.parent.stem)

            generator_parameters = [
                int(char) for char in hdl if char.isdigit()
            ][-10:]

            if hdl not in results[benchmark_format]:
                results[benchmark_format][hdl] = BenchmarkResults(
                    benchmark_format, benchmark_name, hdl, generator_parameters
                )

            with open(Path(path) / file_name) as f:
                match file_name:
                    case "synth_utilization.rpt":
                        for line in f:
                            parts = line.split()

                            # whitespace or too little information
                            if len(parts) < UTILIZATION_LINE_PARTS:
                                continue

                            # extract LUT information
                            if parts[1] == "Slice" and parts[2] == "LUTs*":
                                lut = int(parts[4])
                                match tool:
                                    case "Vivado":
                                        results[benchmark_format][
                                            hdl
                                        ].vivado_results.synth_results.lut = (
                                            lut
                                        )
                                    case "Yosys":
                                        results[benchmark_format][
                                            hdl
                                        ].yosys_results.synth_results.lut = lut

                            # extract FF information
                            if parts[1] == "Slice" and parts[2] == "Registers":
                                ff = int(parts[4])
                                match tool:
                                    case "Vivado":
                                        results[benchmark_format][
                                            hdl
                                        ].vivado_results.synth_results.ff = ff
                                    case "Yosys":
                                        results[benchmark_format][
                                            hdl
                                        ].yosys_results.synth_results.ff = ff

                                break
                    case "impl_utilization.rpt":
                        for line in f:
                            parts = line.split()

                            # whitespace or too little information
                            if len(parts) < UTILIZATION_LINE_PARTS:
                                continue

                            # extract LUT information
                            if parts[1] == "Slice" and parts[2] == "LUTs":
                                lut = int(parts[4])
                                match tool:
                                    case "Vivado":
                                        results[benchmark_format][
                                            hdl
                                        ].vivado_results.impl_results.lut = lut
                                    case "Yosys":
                                        results[benchmark_format][
                                            hdl
                                        ].yosys_results.impl_results.lut = lut

                            # extract FF information
                            if parts[1] == "Slice" and parts[2] == "Registers":
                                ff = int(parts[4])
                                match tool:
                                    case "Vivado":
                                        results[benchmark_format][
                                            hdl
                                        ].vivado_results.impl_results.ff = ff
                                    case "Yosys":
                                        results[benchmark_format][
                                            hdl
                                        ].yosys_results.impl_results.ff = ff
                                break
                    case "synth_timing.rpt":
                        for line in f:
                            parts = line.split()

                            # whitespace or too little information
                            if len(parts) < TIMING_LINE_PARTS:
                                continue

                            # extract timing information
                            if parts[0] == "Slack":
                                slack = float(parts[3][: len(parts[3]) - 2])
                                fmax = round(1000 / (CLOCK_PERIOD - slack), 3)

                                match tool:
                                    case "Vivado":
                                        results[benchmark_format][
                                            hdl
                                        ].vivado_results.synth_results.fmax = (
                                            fmax
                                        )
                                    case "Yosys":
                                        results[benchmark_format][
                                            hdl
                                        ].yosys_results.synth_results.fmax = (
                                            fmax
                                        )
                                break
                    case "impl_timing.rpt":
                        for line in f:
                            parts = line.split()

                            # whitespace or too little information
                            if len(parts) < TIMING_LINE_PARTS:
                                continue

                            # extract timing information
                            if parts[0] == "Slack":
                                slack = float(parts[3][: len(parts[3]) - 2])
                                fmax = round(1000 / (CLOCK_PERIOD - slack), 3)

                                match tool:
                                    case "Vivado":
                                        results[benchmark_format][
                                            hdl
                                        ].vivado_results.impl_results.fmax = (
                                            fmax
                                        )
                                    case "Yosys":
                                        results[benchmark_format][
                                            hdl
                                        ].yosys_results.impl_results.fmax = (
                                            fmax
                                        )
                                break
                    case "synth_power.rpt":
                        for line in f:
                            parts = line.split()

                            # whitespace or too little information
                            if len(parts) < POWER_LINE_PARTS:
                                continue

                            # extract power information
                            if parts[1] == "Total" and parts[2] == "|":
                                power = float(parts[3]) * 1000
                                match tool:
                                    case "Vivado":
                                        results[benchmark_format][
                                            hdl
                                        ].vivado_results.synth_results.power = power
                                    case "Yosys":
                                        results[benchmark_format][
                                            hdl
                                        ].yosys_results.synth_results.power = (
                                            power
                                        )
                                break
                    case "impl_power.rpt":
                        for line in f:
                            parts = line.split()

                            # whitespace or too little information
                            if len(parts) < POWER_LINE_PARTS:
                                continue

                            # extract power information
                            if parts[1] == "Total" and parts[2] == "|":
                                power = float(parts[3]) * 1000
                                match tool:
                                    case "Vivado":
                                        results[benchmark_format][
                                            hdl
                                        ].vivado_results.impl_results.power = (
                                            power
                                        )
                                    case "Yosys":
                                        results[benchmark_format][
                                            hdl
                                        ].yosys_results.impl_results.power = (
                                            power
                                        )
                                break
                    case "synth.log":
                        match tool:
                            case "Vivado":
                                session_start: datetime
                                session_end: datetime

                                for line in f:
                                    parts = line.split()

                                    # whitespace or too little information
                                    if len(parts) < VIVADO_LOG_PARTS_TIME:
                                        continue

                                    # extract session start information
                                    if (
                                        parts[0] == "****"
                                        and parts[1] == "Start"
                                    ):
                                        month = parts[6]
                                        day = parts[7]
                                        time = parts[8]
                                        year = parts[9]

                                        date_str = (
                                            month
                                            + " "
                                            + day
                                            + " "
                                            + time
                                            + " "
                                            + year
                                        )

                                        session_start = datetime.strptime(
                                            date_str, "%b %d %H:%M:%S %Y"
                                        ).replace(tzinfo=TIME_ZONE)

                                    # extract session end information
                                    if (
                                        parts[0] == "INFO:"
                                        and parts[3] == "Exiting"
                                    ):
                                        month = parts[7]
                                        day = parts[8]
                                        time = parts[9]
                                        year = re.sub(r"\.{3,}", "", parts[10])

                                        date_str = (
                                            month
                                            + " "
                                            + day
                                            + " "
                                            + time
                                            + " "
                                            + year
                                        )

                                        session_end = datetime.strptime(
                                            date_str, "%b %d %H:%M:%S %Y"
                                        ).replace(tzinfo=TIME_ZONE)

                                    # whitespace or too little information
                                    if len(parts) < VIVADO_LOG_PARTS_MEM:
                                        continue

                                    # extract memory usage information
                                    if parts[15] == "peak":
                                        memory = round(float(parts[17]))

                                        results[benchmark_format][
                                            hdl
                                        ].vivado_results.synth_results.memory = memory

                                session_time = int(
                                    (
                                        session_end - session_start
                                    ).total_seconds()
                                )

                                results[benchmark_format][
                                    hdl
                                ].vivado_results.synth_results.time = (
                                    session_time
                                )

                            case "Yosys":
                                for line in f:
                                    parts = line.split()

                                    # whitespace or too little information
                                    if len(parts) < YOSYS_LOG_PARTS:
                                        continue

                                    if (
                                        parts[0] == "End"
                                        and parts[1] == "of"
                                        and parts[2] == "script."
                                    ):
                                        time = round(
                                            float(parts[8][:-2])
                                            + float(parts[10][:-2])
                                        )
                                        memory = round(float(parts[12]))

                                        results[benchmark_format][
                                            hdl
                                        ].yosys_results.synth_results.time = (
                                            time
                                        )
                                        results[benchmark_format][
                                            hdl
                                        ].yosys_results.synth_results.memory = memory

                                        break

                    case "impl.log":
                        session_start: datetime
                        session_end: datetime

                        for line in f:
                            parts = line.split()

                            # whitespace or too little information
                            if len(parts) < VIVADO_LOG_PARTS_TIME:
                                continue

                            # extract session start information
                            if (
                                parts[0] in ["#", "****"]
                                and parts[1] == "Start"
                            ):
                                month = parts[6]
                                day = parts[7]
                                time = parts[8]
                                year = parts[9]

                                date_str = (
                                    month + " " + day + " " + time + " " + year
                                )

                                session_start = datetime.strptime(
                                    date_str, "%b %d %H:%M:%S %Y"
                                ).replace(tzinfo=TIME_ZONE)

                            # extract session end information
                            if parts[0] == "INFO:" and parts[3] == "Exiting":
                                month = parts[7]
                                day = parts[8]
                                time = parts[9]
                                year = re.sub(r"\.{3,}", "", parts[10])

                                date_str = (
                                    month + " " + day + " " + time + " " + year
                                )

                                session_end = datetime.strptime(
                                    date_str, "%b %d %H:%M:%S %Y"
                                ).replace(tzinfo=TIME_ZONE)

                            # whitespace or too little information
                            if len(parts) < VIVADO_LOG_PARTS_MEM:
                                continue

                            # extract memory usage information
                            if parts[15] == "peak":
                                memory = round(float(parts[17]))

                                match tool:
                                    case "Vivado":
                                        results[benchmark_format][
                                            hdl
                                        ].vivado_results.impl_results.memory = memory
                                    case "Yosys":
                                        results[benchmark_format][
                                            hdl
                                        ].yosys_results.impl_results.memory = (
                                            memory
                                        )

                        session_time = int(
                            (session_end - session_start).total_seconds()
                        )

                        match tool:
                            case "Vivado":
                                results[benchmark_format][
                                    hdl
                                ].vivado_results.impl_results.time = (
                                    session_time
                                )
                            case "Yosys":
                                results[benchmark_format][
                                    hdl
                                ].yosys_results.impl_results.time = (
                                    session_time
                                )

                f.close()

    return results
