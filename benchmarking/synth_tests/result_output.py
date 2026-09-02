import csv
from operator import itemgetter
from pathlib import Path

from fsm2hdl.common import (
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

FILE_PATH = Path(__file__).resolve().parent
PROJ_PATH = FILE_PATH.parent.parent
RESULTS_PATH = PROJ_PATH / "results"


def convert_to_list_of_dict(results):
    data = []
    for benchmarks in results.values():
        for benchmark_results in benchmarks.values():
            entry = {
                "Benchmark Format": benchmark_results.benchmark_format,
                "Benchmark Name": benchmark_results.benchmark_name,
                "HDL File": benchmark_results.hdl_file,
                "Synth LUT (Vivado)": benchmark_results.vivado_results.synth_results.lut,
                "Synth FF (Vivado)": benchmark_results.vivado_results.synth_results.ff,
                "Synth Fmax (Vivado)": benchmark_results.vivado_results.synth_results.fmax,
                "Synth Power (Vivado)": benchmark_results.vivado_results.synth_results.power,
                "Synth Time (Vivado)": benchmark_results.vivado_results.synth_results.time,
                "Synth Memory (Vivado)": benchmark_results.vivado_results.synth_results.memory,
                "Impl LUT (Vivado)": benchmark_results.vivado_results.impl_results.lut,
                "Impl FF (Vivado)": benchmark_results.vivado_results.impl_results.ff,
                "Impl Fmax (Vivado)": benchmark_results.vivado_results.impl_results.fmax,
                "Impl Power (Vivado)": benchmark_results.vivado_results.impl_results.power,
                "Impl Time (Vivado)": benchmark_results.vivado_results.impl_results.time,
                "Impl Memory (Vivado)": benchmark_results.vivado_results.impl_results.memory,
                "Synth LUT (Yosys)": benchmark_results.yosys_results.synth_results.lut,
                "Synth FF (Yosys)": benchmark_results.yosys_results.synth_results.ff,
                "Synth Fmax (Yosys)": benchmark_results.yosys_results.synth_results.fmax,
                "Synth Power (Yosys)": benchmark_results.yosys_results.synth_results.power,
                "Synth Time (Yosys)": benchmark_results.yosys_results.synth_results.time,
                "Synth Memory (Yosys)": benchmark_results.yosys_results.synth_results.memory,
                "Impl LUT (Yosys)": benchmark_results.yosys_results.impl_results.lut,
                "Impl FF (Yosys)": benchmark_results.yosys_results.impl_results.ff,
                "Impl Fmax (Yosys)": benchmark_results.yosys_results.impl_results.fmax,
                "Impl Power (Yosys)": benchmark_results.yosys_results.impl_results.power,
                "Impl Time (Yosys)": benchmark_results.yosys_results.impl_results.time,
                "Impl Memory (Yosys)": benchmark_results.yosys_results.impl_results.memory,
            }

            entry["HDL Type"] = HDLType(benchmark_results.parameters[0]).name
            entry["FSM Type"] = FSMType(benchmark_results.parameters[1]).name
            entry["State Encoding Type"] = StateEncodingType(
                benchmark_results.parameters[2]
            ).name
            entry["Default State Type"] = DefaultStateType(
                benchmark_results.parameters[3]
            ).name
            entry["Reset Type"] = ResetType(
                benchmark_results.parameters[4]
            ).name
            entry["Reset Active Level"] = ResetActiveLevel(
                benchmark_results.parameters[5]
            ).name
            entry["Coding Structure"] = CodingStructure(
                benchmark_results.parameters[6]
            ).name
            entry["Combinatorial Structure"] = CombinatorialStructure(
                benchmark_results.parameters[7]
            ).name
            entry["Combinatorial Sensitivity Mode"] = (
                CombinatorialSensitivityMode(
                    benchmark_results.parameters[8]
                ).name
            )
            entry["Output Handling Method"] = OutputHandlingMethod(
                benchmark_results.parameters[9]
            ).name
            entry["Configuration"] = "".join(
                map(str, benchmark_results.parameters)
            )
            data.append(entry)

    data.sort(key=itemgetter("Benchmark Format", "Benchmark Name", "HDL File"))

    return data


def output_results(results):
    data = convert_to_list_of_dict(results)

    with open(RESULTS_PATH / "synth_reports.csv", "w") as f:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
