from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MaxNLocator

FILE_PATH = Path(__file__).resolve().parent
PROJ_PATH = FILE_PATH.parent.parent
RESULTS_PATH = PROJ_PATH / "results"
RESULTS_FILE = RESULTS_PATH / "perf_tests_results.csv"
OUTPUT_PATH = Path(
    "/home/drifter/Public/latex_projects/drafts/fsm-python-hdl-framework/figures"
)

FIG_HEIGHT = 3.5
BINS = 30


metrics = [
    "transition_count",
    "parsing_execution_time",
    "parsing_peak_memory_usage",
    "generation_execution_time",
    "generation_peak_memory_usage",
]


# Read Data
df = pd.read_csv(RESULTS_FILE)

# Process Data
df["parsing_peak_memory_usage"] = df["parsing_peak_memory_usage"] / 1_000_000

df["generation_peak_memory_usage"] = (
    df["generation_peak_memory_usage"] / 1_000_000
)

df_mean = df.groupby("benchmark_name", as_index=False)[metrics].mean()
df_mean["transition_count"] = df_mean["transition_count"].astype(int)

df_sorted = df_mean.sort_values(by="transition_count", ascending=True)

# Initialize Matplotlib figure and primary axis
fig, ax1 = plt.subplots()

# Plot Runtime on Primary Axis
df_sorted.plot(
    x="transition_count",
    y="parsing_execution_time",
    kind="bar",
    ax=ax1,
    color="tab:blue",
    alpha=0.7,
    label="Runtime",
    legend=False,
)
ax1.set_ylabel("Execution Runtime (sec)", color="tab:blue")
ax1.tick_params(axis="y", labelcolor="tab:blue")
ax1.semilogy()

# Create Secondary Axis sharing the x-axis
ax2 = ax1.twinx()
df_sorted.plot(
    x="transition_count",
    y="parsing_peak_memory_usage",
    kind="bar",
    ax=ax2,
    color="tab:red",
    alpha=0.7,
    label="Memory",
    legend=False,
)
ax2.set_ylabel("Peak Memory Usage (MB)", color="tab:red")
ax2.tick_params(axis="y", labelcolor="tab:red")
ax2.semilogy()

# Reduce X-Axis Ticks
ax1.xaxis.set_major_locator(MaxNLocator(nbins=BINS))

# Finalize Labels and Layout
ax1.set_xlabel("Transitions")
plt.gcf().set_figheight(FIG_HEIGHT)
plt.tight_layout()
plt.savefig(OUTPUT_PATH / "parsing_info_chart.pdf")
plt.close()


# Initialize Matplotlib figure and primary axis
fig, ax1 = plt.subplots()

# Plot Runtime on Primary Axis
df_sorted.plot(
    x="transition_count",
    y="generation_execution_time",
    kind="bar",
    ax=ax1,
    color="tab:blue",
    alpha=0.7,
    label="Runtime",
    legend=False,
)
ax1.set_ylabel("Execution Runtime (sec)", color="tab:blue")
ax1.tick_params(axis="y", labelcolor="tab:blue")
ax1.semilogy()

# Create Secondary Axis sharing the x-axis
ax2 = ax1.twinx()
df_sorted.plot(
    x="transition_count",
    y="generation_peak_memory_usage",
    kind="bar",
    ax=ax2,
    color="tab:red",
    alpha=0.7,
    label="Memory",
    legend=False,
)
ax2.set_ylabel("Peak Memory Usage (MB)", color="tab:red")
ax2.tick_params(axis="y", labelcolor="tab:red")
ax2.semilogy()

# Reduce X-Axis Ticks
ax1.xaxis.set_major_locator(MaxNLocator(nbins=BINS))

# Finalize Labels and Layout
ax1.set_xlabel("Transitions")
plt.gcf().set_figheight(FIG_HEIGHT)
plt.tight_layout()
plt.savefig(OUTPUT_PATH / "generation_info_chart.pdf")
plt.close()
