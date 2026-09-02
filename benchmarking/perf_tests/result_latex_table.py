from pathlib import Path

import pandas as pd

FILE_PATH = Path(__file__).resolve().parent
PROJ_PATH = FILE_PATH.parent.parent
RESULTS_PATH = PROJ_PATH / "results"
RESULTS_FILE = RESULTS_PATH / "perf_tests_results.csv"

metrics_hdl = [
    "generation_execution_time",
    "generation_peak_memory_usage",
    "generation_utilization",
]

metrics_shared = [
    "input_count",
    "output_count",
    "transition_count",
    "state_count",
]

# Read Data
df = pd.read_csv(RESULTS_FILE)

# Filter
benchmarks = [
    "bbara",
    "bbtas",
    "dk14",
    "dk15",
    "dk16",
    "dk17",
    "dk27",
    "ex1",
    "ex5",
    "ex6",
    "lion",
    "planet",
    "planet1",
    "s1",
    "s1488",
    "s27",
    "s298",
    "s832",
    "tbk",
    "train11",
]

df = df[df["benchmark_name"].isin(benchmarks)].copy()

df["generation_peak_memory_usage"] = (
    df["generation_peak_memory_usage"] / 1_000_000
)
df["generation_utilization"] = df["generation_utilization"] / 1_000

# HDL-specific pivot
df_hdl = df.groupby(["benchmark_name", "hdl_type"], as_index=False)[
    metrics_hdl
].mean()

pivot = df_hdl.pivot(
    index="benchmark_name", columns="hdl_type", values=metrics_hdl
)
pivot.columns = [f"{m}_{hdl}" for m, hdl in pivot.columns]
pivot = pivot.reset_index()

# Shared metrics
df_shared = df.groupby("benchmark_name", as_index=False)[metrics_shared].mean()

# Combine
final = pivot.merge(df_shared, on="benchmark_name", how="left")

# Sort by utilization
final_sorted = final.sort_values(
    by="generation_utilization_VHDL", ascending=True
)

# Write LaTeX rows
with open("latex_table.txt", "w") as f:
    f.writelines(
        f"{row.benchmark_name} & "
        f"{row.input_count:.0f} & "
        f"{row.output_count:.0f} & "
        f"{row.transition_count:.0f} & "
        f"{row.state_count:.0f} & "
        f"{row.generation_execution_time_VERILOG:.4f} & "
        f"{row.generation_execution_time_VHDL:.4f} & "
        f"{row.generation_peak_memory_usage_VERILOG:.4f} & "
        f"{row.generation_peak_memory_usage_VHDL:.4f} & "
        f"{row.generation_utilization_VERILOG:.3f} & "
        f"{row.generation_utilization_VHDL:.3f}\n"
        f"\\\\\n"
        for row in final_sorted.itertuples(index=False)
    )
    f.close()
