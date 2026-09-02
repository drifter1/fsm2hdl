from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

FILE_PATH = Path(__file__).resolve().parent
PROJ_PATH = FILE_PATH.parent.parent
RESULTS_PATH = PROJ_PATH / "results"
REPORTS_FILE = RESULTS_PATH / "synth_reports.csv"
OUTPUT_PATH = Path(
    "/home/drifter/Public/latex_projects/drafts/fsm-python-hdl-framework/figures"
)
BENCHMARK = "tbk"
FIG_HEIGHT = 4
PIE_CHART_WIDTH = 4
PCT_DIST = 1.2

CLOCK_FREQ = 100
THRESHOLD = 2

# Read Data
df = pd.read_csv(REPORTS_FILE)

# DESIGN & TOOL METRICS

df_benchmark = df[df["Benchmark Name"] == BENCHMARK]
df_benchmark = df_benchmark[df_benchmark["Impl Time (Vivado)"] > 0]
df_benchmark = df_benchmark[df_benchmark["Synth Fmax (Yosys)"] > CLOCK_FREQ]
df_benchmark = df_benchmark[df_benchmark["Impl Fmax (Yosys)"] > CLOCK_FREQ]
df_benchmark = df_benchmark[df_benchmark["Synth Fmax (Vivado)"] > CLOCK_FREQ]
df_benchmark = df_benchmark[df_benchmark["Impl Fmax (Vivado)"] > CLOCK_FREQ]

# Min and Max Values
min_lut = min(
    df_benchmark["Synth LUT (Yosys)"].min(),
    df_benchmark["Impl LUT (Yosys)"].min(),
    df_benchmark["Synth LUT (Vivado)"].min(),
    df_benchmark["Impl LUT (Vivado)"].min(),
)
max_lut = max(
    df_benchmark["Synth LUT (Yosys)"].max(),
    df_benchmark["Impl LUT (Yosys)"].max(),
    df_benchmark["Synth LUT (Vivado)"].max(),
    df_benchmark["Impl LUT (Vivado)"].max(),
)

min_ff = min(
    df_benchmark["Synth FF (Yosys)"].min(),
    df_benchmark["Impl FF (Yosys)"].min(),
    df_benchmark["Synth FF (Vivado)"].min(),
    df_benchmark["Impl FF (Vivado)"].min(),
)
max_ff = max(
    df_benchmark["Synth FF (Yosys)"].max(),
    df_benchmark["Impl FF (Yosys)"].max(),
    df_benchmark["Synth FF (Vivado)"].max(),
    df_benchmark["Impl FF (Vivado)"].max(),
)

min_fmax = min(
    df_benchmark["Synth Fmax (Yosys)"].min(),
    df_benchmark["Impl Fmax (Yosys)"].min(),
    df_benchmark["Synth Fmax (Vivado)"].min(),
    df_benchmark["Impl Fmax (Vivado)"].min(),
)
max_fmax = max(
    df_benchmark["Synth Fmax (Yosys)"].max(),
    df_benchmark["Impl Fmax (Yosys)"].max(),
    df_benchmark["Synth Fmax (Vivado)"].max(),
    df_benchmark["Impl Fmax (Vivado)"].max(),
)

min_power = min(
    df_benchmark["Synth Power (Yosys)"].min(),
    df_benchmark["Impl Power (Yosys)"].min(),
    df_benchmark["Synth Power (Vivado)"].min(),
    df_benchmark["Impl Power (Vivado)"].min(),
)
max_power = max(
    df_benchmark["Synth Power (Yosys)"].max(),
    df_benchmark["Impl Power (Yosys)"].max(),
    df_benchmark["Synth Power (Vivado)"].max(),
    df_benchmark["Impl Power (Vivado)"].max(),
)

min_time = min(
    df_benchmark["Synth Time (Yosys)"].min(),
    df_benchmark["Impl Time (Yosys)"].min(),
    df_benchmark["Synth Time (Vivado)"].min(),
    df_benchmark["Impl Time (Vivado)"].min(),
)
max_time = max(
    df_benchmark["Synth Time (Yosys)"].max(),
    df_benchmark["Impl Time (Yosys)"].max(),
    df_benchmark["Synth Time (Vivado)"].max(),
    df_benchmark["Impl Time (Vivado)"].max(),
)

min_mem = min(
    df_benchmark["Synth Memory (Yosys)"].min(),
    df_benchmark["Impl Memory (Yosys)"].min(),
    df_benchmark["Synth Memory (Vivado)"].min(),
    df_benchmark["Impl Memory (Vivado)"].min(),
)
max_mem = max(
    df_benchmark["Synth Memory (Yosys)"].max(),
    df_benchmark["Impl Memory (Yosys)"].max(),
    df_benchmark["Synth Memory (Vivado)"].max(),
    df_benchmark["Impl Memory (Vivado)"].max(),
)


with open("benchmark_results.txt", "w") as f:
    f.write(
        f"LUT Range: ({min_lut}, {max_lut})\n"
        f"FF Range: ({min_ff}, {max_ff})\n"
        f"Fmax Range: ({min_fmax}, {max_fmax})\n"
        f"Power Range: ({min_power}, {max_power})\n"
        f"Time Range: ({min_time}, {max_time})\n"
        f"Memory Range: ({min_mem}, {max_mem})\n"
    )
    f.close()

# SYNTHESIS & IMPLEMENTATION PASS & FAIL

df = df[df["Impl Time (Vivado)"] > 0]

group_cols = ["Benchmark Format", "Benchmark Name", "FSM Type"]
structure_group_key = df["Coding Structure"].apply(
    lambda x: "ALL_IN_ONE" if x == "ALL_IN_ONE" else "NOT ALL_IN_ONE"
)
encoding_group_key = df["State Encoding Type"].apply(
    lambda x: "ONEHOT"
    if x == "ONEHOT"
    else "JOHNSON"
    if x == "JOHNSON"
    else "BINARY_OR_GRAY"
)
groups = [*group_cols, structure_group_key, encoding_group_key]

# YOSYS

# Calculate Z-scores
target_cols = [
    "Synth LUT (Yosys)",
    "Synth FF (Yosys)",
    "Impl LUT (Yosys)",
    "Impl FF (Yosys)",
]
output_cols = [
    "Synth LUT Z Score",
    "Synth FF Z Score",
    "Impl LUT Z Score",
    "Impl FF Z Score",
]

for target, output in zip(target_cols, output_cols, strict=False):
    group_mean = df.groupby(groups)[target].transform("mean")
    group_std = df.groupby(groups)[target].transform("std")

    df[output] = (df[target] - group_mean) / group_std
    df[output] = df[output].replace([np.inf, -np.inf], 0).fillna(0)

# Conditions

failed_synthesis = (
    (df["Synth Fmax (Yosys)"] == 0)
    | (df["Synth Fmax (Yosys)"] < CLOCK_FREQ)
    | (df["Synth LUT Z Score"].abs() > THRESHOLD)
    | (df["Synth FF Z Score"].abs() > THRESHOLD)
)

failed_implementation = (
    (df["Impl Fmax (Yosys)"] == 0)
    | (df["Impl Fmax (Yosys)"] < CLOCK_FREQ)
    | (df["Impl LUT Z Score"].abs() > THRESHOLD)
    | (df["Impl FF Z Score"].abs() > THRESHOLD)
)

# Statuses

conditions = [
    ~failed_synthesis & ~failed_implementation,
    ~failed_synthesis & failed_implementation,
    failed_synthesis & failed_implementation,
]

choices = [
    "Successful Synthesis and Implementation",
    "Passed Synthesis But Failed Implementation",
    "Failed Synthesis",
]

df["Status (Yosys)"] = np.select(
    conditions, choices, default="Successful Synthesis and Implementation"
)

status_counts = df["Status (Yosys)"].value_counts()

start_angle = 0
if "Failed Synthesis" in status_counts:
    start_angle += (100 * status_counts["Failed Synthesis"]) / (
        len(df["Status (Yosys)"] * 360)
    )
if "Passed Synthesis But Failed Implementation" in status_counts:
    start_angle += (
        100 * status_counts["Passed Synthesis But Failed Implementation"]
    ) / (len(df["Status (Yosys)"] * 360))
start_angle *= 2

# Plotting

plt.pie(
    status_counts,
    autopct="%1.1f%%",
    pctdistance=PCT_DIST,
    colors=["green", "red", "orange"],
    startangle=start_angle,
)

plt.axis("equal")
plt.legend(status_counts.index, loc="lower center")
plt.gcf().set_figheight(FIG_HEIGHT)
plt.gcf().set_figwidth(PIE_CHART_WIDTH)
plt.tight_layout()
plt.savefig(OUTPUT_PATH / "yosys_pie_chart.pdf")
plt.close()

# VIVADO

# Calculate Z-scores
target_cols = [
    "Synth LUT (Vivado)",
    "Synth FF (Vivado)",
    "Impl LUT (Vivado)",
    "Impl FF (Vivado)",
]
output_cols = [
    "Synth LUT Z Score",
    "Synth FF Z Score",
    "Impl LUT Z Score",
    "Impl FF Z Score",
]

for target, output in zip(target_cols, output_cols, strict=False):
    group_mean = df.groupby(groups)[target].transform("mean")
    group_std = df.groupby(groups)[target].transform("std")

    df[output] = (df[target] - group_mean) / group_std
    df[output] = df[output].replace([np.inf, -np.inf], 0).fillna(0)

# Conditions

failed_synthesis = (
    (df["Synth Fmax (Vivado)"] == 0)
    | (df["Synth Fmax (Vivado)"] < CLOCK_FREQ)
    | (df["Synth LUT Z Score"].abs() > THRESHOLD)
    | (df["Synth FF Z Score"].abs() > THRESHOLD)
)

failed_implementation = (
    (df["Impl Fmax (Vivado)"] == 0)
    | (df["Impl Fmax (Vivado)"] < CLOCK_FREQ)
    | (df["Impl LUT Z Score"].abs() > THRESHOLD)
    | (df["Impl FF Z Score"].abs() > THRESHOLD)
)

# Statuses

conditions = [
    ~failed_synthesis & ~failed_implementation,
    ~failed_synthesis & failed_implementation,
    failed_synthesis & failed_implementation,
]

choices = [
    "Successful Synthesis and Implementation",
    "Passed Synthesis But Failed Implementation",
    "Failed Synthesis",
]

df["Status (Vivado)"] = np.select(
    conditions, choices, default="Successful Synthesis and Implementation"
)

status_counts = df["Status (Vivado)"].value_counts()

start_angle = 0
if "Failed Synthesis" in status_counts:
    start_angle += (100 * status_counts["Failed Synthesis"]) / (
        len(df["Status (Vivado)"] * 360)
    )
if "Passed Synthesis But Failed Implementation" in status_counts:
    start_angle += (
        100 * status_counts["Passed Synthesis But Failed Implementation"]
    ) / (len(df["Status (Vivado)"] * 360))
start_angle *= 2

# Plotting

plt.pie(
    status_counts,
    autopct="%1.1f%%",
    pctdistance=PCT_DIST,
    colors=["green", "red", "orange"],
    startangle=start_angle,
)
plt.axis("equal")
plt.legend(status_counts.index, loc="lower center")
plt.gcf().set_figheight(FIG_HEIGHT)
plt.gcf().set_figwidth(PIE_CHART_WIDTH)
plt.tight_layout()
plt.savefig(OUTPUT_PATH / "vivado_pie_chart.pdf")
plt.close()
